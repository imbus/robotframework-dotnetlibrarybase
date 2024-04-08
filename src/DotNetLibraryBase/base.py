import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, TextIO

from robot.api.interfaces import DynamicLibrary


def _is_file(s: str) -> bool:
    return s.lower().endswith(".dll") or "\\" in s or "/" in s


@dataclass
class KeywordInfo:
    name: str


class DotNetLibraryBase(DynamicLibrary):

    __dotnet_initialized = False
    __stdout_writer: Any = None
    __stderr_writer: Any = None

    @staticmethod
    def _init_dotnet() -> None:
        if not DotNetLibraryBase.__dotnet_initialized:
            import clr
            import System  #  pyright: ignore[reportMissingImports]

            base_path = (Path(__file__).parent / "runtime").absolute()

            clr.AddReference(str(base_path / "RobotFramework.DotNetLibraryBase.dll"))

            from RobotFramework.DotNetLibraryBase import (  #  pyright: ignore[reportMissingImports]
                ConsoleRedirectorWriter,
            )

            class MyConsoleRedirectorWriter(ConsoleRedirectorWriter):
                __namespace__ = "RobotFramework.DotNetLibraryBase.Internal"

                def __init__(self, encoding: str, is_stderr: bool) -> None:
                    super().__init__(encoding)
                    self.is_stderr = is_stderr

                @clr.clrmethod(None, [System.Char])
                def WriteChar(self, value: str) -> None:  # noqa: N802
                    print(
                        value, end="", file=sys.stderr if self.is_stderr else sys.stdout
                    )

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

    def __init__(
        self, reference: Optional[str], class_name: str, *args: Any, **kwargs: Any
    ) -> None:
        import clr
        import System  #  pyright: ignore[reportMissingImports]

        self._init_dotnet()

        self._reference_name = reference

        if self._reference_name:
            self._reference = clr.AddReference(
                str(Path(self._reference_name).absolute())
                if _is_file(self._reference_name)
                else self._reference_name
            )
        self._namespace, self._class_name = class_name.rsplit(".", 1)

        self._instance = getattr(__import__(self._namespace), self._class_name)(
            *args, *kwargs
        )

        self._keyword_infos: Optional[List[KeywordInfo]] = None

    @property
    def keyword_infos(self) -> List[KeywordInfo]:
        if self._keyword_infos is None:
            self._keyword_infos = []

            for method in self._instance.GetType().GetMethods():
                self._keyword_infos.append(KeywordInfo(method.Name))
        return self._keyword_infos

    def get_keyword_names(self) -> Sequence[str]:
        return [i.name for i in self.keyword_infos]

    def run_keyword(
        self, name: str, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> Any:
        method = getattr(self._instance, name)
        return method(*args, **kwargs)
