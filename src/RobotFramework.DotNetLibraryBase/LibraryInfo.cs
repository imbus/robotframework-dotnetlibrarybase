// SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
//
// SPDX-License-Identifier: Apache-2.0

namespace RobotFramework.DotNetLibraryBase;

using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;

internal enum RobotLibraryConstants
{
    ROBOT_LIBRARY_SCOPE,
    ROBOT_LIBRARY_VERSION,
    ROBOT_LIBRARY_CONVERTERS,
    ROBOT_LIBRARY_DOC_FORMAT,
    ROBOT_LIBRARY_LISTENER
}

public class ArgumentInfo
{
    public ArgumentInfo(string? name, int index)
    {
        Name = name;
        Index = index;
    }

    public string? Name { get; internal set; }
    public int Index { get; }
    public bool IsOptional { get; internal set; }

    public IList<Type> Types { get; } = new List<Type>();

    public bool HasDefaultValue => DefaultValue != DBNull.Value;
    public object? DefaultValue { get; internal set; } = DBNull.Value;
}

public class KeywordInfo
{
    public KeywordInfo(IEnumerable<MethodInfo> methods)
    {
        Methods = methods.ToArray();
        if (Methods.Length == 0)
            throw new ArgumentException("At least one method is required", nameof(methods));

        _documentation = new Lazy<string?>(() => null); // TODO: Get doc from attribute
        _tags = new Lazy<string[]>(() => Array.Empty<string>()); // TODO: Get tags from attribute
        _arguments = new Lazy<ArgumentInfo[]>(CollectArguments);
    }

    public MethodInfo[] Methods { get; }

    public string Name => Methods[0].Name;

    private readonly Lazy<string[]> _tags;
    public string[] Tags => _tags.Value;

    private readonly Lazy<string?> _documentation;
    public string? Documentation => _documentation.Value;

    private readonly Lazy<ArgumentInfo[]> _arguments;
    public ArgumentInfo[] Arguments => _arguments.Value;

    private ArgumentInfo[] CollectArguments()
    {
        var arguments = new List<ArgumentInfo>();
        foreach (var methodEntry in Methods.Select((method, index) => new { method, index }))
        {
            foreach (
                var parameterEntry in methodEntry
                    .method.GetParameters()
                    .Select((parameter, index) => new { parameter, index })
            )
            {
                var newly = false;
                var argument = arguments.FirstOrDefault(a => a.Name == parameterEntry.parameter.Name);
                if (argument == null)
                {
                    argument = new ArgumentInfo(parameterEntry.parameter.Name, parameterEntry.index);
                    arguments.Add(argument);
                    newly = true;
                }

                if (!argument.IsOptional && parameterEntry.parameter.IsOptional)
                    argument.IsOptional = true;

                if (parameterEntry.parameter.HasDefaultValue && !argument.HasDefaultValue)
                    argument.DefaultValue = parameterEntry.parameter.DefaultValue;

                if (!argument.Types.Contains(parameterEntry.parameter.ParameterType))
                    argument.Types.Add(parameterEntry.parameter.ParameterType);

                if (Nullable.GetUnderlyingType(parameterEntry.parameter.ParameterType) != null)
                    argument.IsOptional = true;

                if (methodEntry.index > 0)
                {
                    if (argument.Index != parameterEntry.index || newly)
                    {
                        argument.IsOptional = true;
                    }
                }
            }
        }

        var opt = false;
        foreach (var arg in arguments)
        {
            if (arg.IsOptional)
                opt = true;

            if (opt && !arg.IsOptional) {
                arg.IsOptional = true;
            }
        }
        return arguments.ToArray();
    }
}

/// <summary>
/// This is the LibraryInfo class
/// </summary>
public class LibraryInfo
{
    public LibraryInfo(Type type)
    {
        Type = type;

        _version = new Lazy<string?>(
            () => GetRobotLibraryConstant(nameof(RobotLibraryConstants.ROBOT_LIBRARY_VERSION))
        );
        _scope = new Lazy<string?>(() => GetRobotLibraryConstant(nameof(RobotLibraryConstants.ROBOT_LIBRARY_SCOPE)));
        _docFormat = new Lazy<string?>(
            () => GetRobotLibraryConstant(nameof(RobotLibraryConstants.ROBOT_LIBRARY_DOC_FORMAT))
        );
        _keywords = new Lazy<IDictionary<string, KeywordInfo>>(CollectKeywords);
    }

    public Type Type { get; }

    private string? GetRobotLibraryConstant(string name)
    {
        return Type.GetField(name, BindingFlags.Static | BindingFlags.Public)?.GetValue(null) as string;
    }

    private readonly Lazy<string?> _version;
    public string? Version => _version.Value;

    private readonly Lazy<string?> _scope;
    public string? Scope => _scope.Value;

    private readonly Lazy<string?> _docFormat;
    public string? DocFormat => _docFormat.Value;

    private readonly Lazy<IDictionary<string, KeywordInfo>> _keywords;
    public IDictionary<string, KeywordInfo> Keywords => _keywords.Value;

    private Dictionary<string, KeywordInfo> CollectKeywords()
    {
        return Type.GetMethods(
                BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static | BindingFlags.OptionalParamBinding
            )
            .Where(m => m.DeclaringType != typeof(object))
            .GroupBy(k => k.Name)
            .Select(m => new KeywordInfo(m))
            .ToDictionary(m => m.Name, m => m);
    }
}
