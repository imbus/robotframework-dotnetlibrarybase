// SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
//
// SPDX-License-Identifier: Apache-2.0

namespace DotNetDemoLibrary;

public class DemoKeywords
{
    public const string ROBOT_LIBRARY_SCOPE = "GLOBAL";
    public const string ROBOT_LIBRARY_VERSION = "1.0";

    public string? AProperty { get; set; }

    public DemoKeywords()
    {
        Console.WriteLine("<empty>");
    }

    public DemoKeywords(string a)
    {
        Console.WriteLine("string?");
        this.AProperty = a;
    }

    // public DemoKeywords(string[] b)
    // {
    //     Console.WriteLine("string[]");
    //     if (b.Length > 0)
    //         this.a = b[0];
    // }


    public void DoSomething()
    {
        Console.WriteLine($"Done Something {this.AProperty}");
    }

    public void DoSomethingWithAnString(string value)
    {
        Console.WriteLine($"Done Something with str {value}");
    }

    public void DoSomethingWithAnInt(int value)
    {
        Console.WriteLine($"Done Something with int {value}");
    }
}
