# SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
#
# SPDX-License-Identifier: Apache-2.0


import functools
import importlib
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple, Type, TypedDict, Union

from robot.api.interfaces import DynamicLibrary
from robot.utils import find_file

# pyright: reportMissingImports=false, reportUnusedVariable=warning


def _is_file(s: str) -> bool:
    return s.lower().endswith(".dll") or "\\" in s or "/" in s


class TypeNameWithOptions(TypedDict):
    type_name: str
    options: Any


class TypeName(str):
    @staticmethod
    def from_string(value: str) -> "TypeName":
        return TypeName(value)


class classproperty(object):  # noqa: N801
    def __init__(self, f: Callable[..., Any]) -> None:
        self.f = f

    def __get__(self, _obj: Any, owner: Any) -> Any:
        return self.f(owner)


class KeywordInfo(Protocol):
    @property
    def Name(self) -> str: ...  # noqa: N802


class LibraryInfo(Protocol):
    @property
    def Version(self) -> str: ...  # noqa: N802

    @property
    def Scope(self) -> str: ...  # noqa: N802

    @property
    def DocFormat(self) -> str: ...  # noqa: N802

    @property
    # TODO: implement DictEncoders/Decoders
    # def Keywords(self) -> Dict[str, KeywordInfo]: ...
    def Keywords(self) -> Any: ...  # noqa: N802


class DotNetLibraryBase(DynamicLibrary):
    ROBOT_LIBRARY_CONVERTERS: Dict[Any, Any] = {TypeName: TypeName.from_string}

    __dotnet_initialized = False
    __stdout_writer: Any = None
    __stderr_writer: Any = None

    @staticmethod
    def _ensure_dotnet_initialized() -> None:
        if not DotNetLibraryBase.__dotnet_initialized:
            import clr
            import System

            base_path = (Path(__file__).parent / "runtime").absolute()

            clr.AddReference(str(base_path / "RobotFramework.DotNetLibraryBase"))

            from RobotFramework.DotNetLibraryBase import ConsoleRedirectorWriter

            class MyConsoleRedirectorWriter(ConsoleRedirectorWriter):
                __namespace__ = "RobotFramework.DotNetLibraryBase.Internal"

                def __init__(self, encoding: str, is_stderr: bool) -> None:
                    super().__init__(encoding)
                    self.is_stderr = is_stderr

                @clr.clrmethod(None, [System.Char])
                def WriteChar(self, value: str) -> None:  # noqa: N802
                    print(value, end="", file=sys.stderr if self.is_stderr else sys.stdout)

                @clr.clrmethod(None, [])
                def Flush(self) -> None:  # noqa: N802
                    (sys.stderr if self.is_stderr else sys.stdout).flush()

            DotNetLibraryBase.__dotnet_initialized = True

            DotNetLibraryBase.__stdout_writer = MyConsoleRedirectorWriter(
                sys.stdout.encoding or sys.getdefaultencoding(), False
            )

            System.Console.SetOut(DotNetLibraryBase.__stdout_writer)

            DotNetLibraryBase.__stderr_writer = MyConsoleRedirectorWriter(
                sys.stdout.encoding or sys.getdefaultencoding(), True
            )

            System.Console.SetError(DotNetLibraryBase.__stderr_writer)

    def __init__(self, type_name: Union[TypeNameWithOptions, TypeName], *args: Any, **kwargs: Any) -> None:
        self._keyword_infos: Optional[List[KeywordInfo]] = None
        self._class_name: Optional[str] = None
        self._namespace: Optional[str] = None
        self._type: Optional[Any] = None
        self._instance: Optional[Any] = None
        self._is_static_class = False
        self._clr_type: Optional[Any] = None
        self._library_info: Optional[LibraryInfo] = None
        self._enum_types: List[Type[Any]] = []

        if not isinstance(type_name, dict):
            type_name = {"type_name": type_name, "options": None}

        splitted = type_name["type_name"].split(",", 1)
        class_name: Optional[str]
        reference_name: Optional[str]

        class_name, reference_name = splitted if len(splitted) == 2 else (splitted[0], None)

        if class_name:
            class_name = class_name.strip()

        if reference_name:
            reference_name = reference_name.strip()

        self._reference_name = reference_name

        if class_name:
            self._namespace, self._class_name = class_name.rsplit(".", 1)

        self._ensure_dotnet_initialized()

        self._init_instance(*args, **kwargs)

    def _init_instance(self, *args: Any, **kwargs: Any) -> None:
        import clr
        from RobotFramework.DotNetLibraryBase import LibraryInfo

        if self._reference_name:
            self._reference = clr.AddReference(
                str(Path(find_file(self._reference_name))) if _is_file(self._reference_name) else self._reference_name
            )

        if self._class_name and self._namespace:
            try:
                module = importlib.import_module(self._namespace)
                self._type = getattr(module, self._class_name)
                self._clr_type = clr.GetClrType(self._type)

                if self._clr_type.IsAbstract and self._clr_type.IsSealed:
                    self._is_static_class = True
                    self._instance = self._type
                else:
                    self._instance = self._type(*args, *kwargs)
            except (AttributeError, ImportError) as e:
                raise TypeError(f"Could not load .NET class '{self._namespace}.{self._class_name}'.") from e

        self._library_info = LibraryInfo(self._clr_type)

    @classproperty
    def ROBOT_LIBRARY_SCOPE(cls) -> str:  # noqa: N802
        # TODO: helper = cls._get_library_helper()
        return "GLOBAL"

    def get_keyword_names(self) -> Sequence[str]:
        if self._library_info is None:
            return []
        return [i for i in self._library_info.Keywords.Keys]

    def get_keyword_arguments(self, name: str) -> Optional[Sequence[Union[str, Tuple[str], Tuple[str, Any]]]]:
        if self._library_info is None:
            return None

        keyword_info = self._library_info.Keywords[name]

        return [((i.Name, None) if i.IsOptional else i.Name) for i in keyword_info.Arguments]

    @functools.cached_property
    def _simple_types_mapping(self) -> Dict[Tuple[Any, ...], "Type[Any]"]:
        import clr
        import System

        def get_types(*args: Any) -> Tuple[Any, ...]:
            return tuple(clr.GetClrType(t) for t in args)

        return {
            get_types(System.String): str,
            get_types(
                System.Int16,
                System.Int32,
                System.Int64,
                System.UInt16,
                System.UInt32,
                System.UInt64,
                System.Byte,
                System.SByte,
            ): int,
            get_types(
                System.Single,
                System.Double,
                System.Single,
                System.Decimal,
            ): float,
            get_types(
                System.Boolean,
                System.Double,
                System.Single,
                System.Decimal,
            ): bool,
            # TODO: Char
            # TODO: System.Object
            # TODO "System.DateTime": str,
        }

    def _convert_type(self, type_: Any) -> Any:
        import System

        is_nullable = False
        nullable_type = System.Nullable.GetUnderlyingType(type_)
        if nullable_type is not None:
            type_ = nullable_type
            is_nullable = True

        for dotnet_types, python_type in self._simple_types_mapping.items():
            if type_ in dotnet_types:
                return Union[python_type, None] if is_nullable else python_type

        if type_.IsEnum:
            return_type = Enum(  # type: ignore
                str(type_.Name),
                [(type_.GetEnumName(i), i) for i in type_.GetEnumValues()],
                module=self.__module__,
            )
            self._enum_types.append(return_type)
            return return_type

        type_converters = getattr(self, "DOTNET_TYPE_CONVERTER", None)
        if type_converters is None:
            return type_

        type_name = str(type_)
        if type_name in type_converters:
            return type_converters[type_name]

        return type_converters.get(str(type), type_)

    def get_keyword_types(self, name: str) -> Optional[Mapping[str, Any]]:
        if self._library_info is None:
            return None

        keyword_info = self._library_info.Keywords[name]

        return {i.Name: [self._convert_type(t) for t in i.Types] for i in keyword_info.Arguments}

    def run_keyword(self, name: str, args: Sequence[Any], kwargs: Mapping[str, Any]) -> Any:
        method = getattr(self._instance, name)
        real_args = list(args)
        real_kwargs = dict(kwargs)
        for i, v in enumerate(real_args):
            if type(v) in self._enum_types:
                real_args[i] = v.value

        for v in real_kwargs:
            if type(real_kwargs[v]) in self._enum_types:
                real_kwargs[v] = real_kwargs[v].value

        return method(*real_args, **kwargs)
