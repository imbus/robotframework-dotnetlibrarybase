// SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
//
// SPDX-License-Identifier: Apache-2.0

namespace RobotFramework.DotNetLibraryBase;

using System.Text;

public class ConsoleRedirectorWriter : TextWriter
{
    public ConsoleRedirectorWriter(string? encoding)
    {
        if (encoding != null)
            Encoding = Encoding.GetEncoding(encoding);
        else
            Encoding = Encoding.Default;
    }

    public override Encoding Encoding { get; }

    public override void Write(char value)
    {
        WriteChar(value);
    }

    protected virtual void WriteChar(char value) { }
}
