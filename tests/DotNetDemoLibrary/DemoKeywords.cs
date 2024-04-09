// SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
//
// SPDX-License-Identifier: Apache-2.0

﻿namespace DotNetDemoLibrary;

public class DemoKeywords
{
    public string? a { get; private set; }

    // public DemoKeywords()
    // {
    //     Console.WriteLine("<empty>");
    // }


    public DemoKeywords(string? a)
    {
        Console.WriteLine("string?");
        this.a = a;
    }

    // public DemoKeywords(string[] b)
    // {
    //     Console.WriteLine("string[]");
    //     if (b.Length > 0)
    //         this.a = b[0];
    // }


    public void DoSomething()
    {
        Console.WriteLine($"Done Something {this.a}");
    }

    public void DoSomethingWithAnString(string value)
    {
        Console.WriteLine($"Done Something with {value}");
    }
}
