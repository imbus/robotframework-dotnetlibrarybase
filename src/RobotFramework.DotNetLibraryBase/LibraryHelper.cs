// SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>
//
// SPDX-License-Identifier: Apache-2.0

namespace RobotFramework.DotNetLibraryBase;

class LibraryInfo
{
    public static string GetLibraryName()
    {
        return "DotNetDemoLibrary";
    }

    public static string GetLibraryVersion()
    {
        return "1.0.0";
    }

    public static string GetLibraryType()
    {
        return "DotNet";
    }
}

class LibraryHelper
{
    public static string GetLibraryInfo()
    {
        return $"{LibraryInfo.GetLibraryName()} {LibraryInfo.GetLibraryVersion()} ({LibraryInfo.GetLibraryType()})";
    }
}
