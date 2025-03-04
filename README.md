# robotframework-DotNetLibraryBase

[![PyPI - Version](https://img.shields.io/pypi/v/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)
[![License](https://img.shields.io/github/license/imbus/robotframework-dotnetlibrarybase.svg)](https://github.com/imbus/robotframework-dotnetlibrarybase/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)


# Introduction
Welcome to the documentation for `robotframework-DotNetLibraryBase`. This library allows you to integrate .NET functionalities into Robot Framework test suites.

### Features

- Seamless integration with .NET libraries.
- Easy to use and configure.
- Supports various .NET functionalities out-of-the-box.

### To get started, We need:

<details>
  <summary> .NET 8.0</summary>

  1. Go to [official .NET download page](https://dotnet.microsoft.com/download).
  2. Download the installer for your operating system.
  3. Run the installer and follow the instructions.
  4. Run `dotnet --version`
</details>

<details>
  <summary> Python</summary>

  1. Go to [official Python page](https://www.python.org/).
  2. Download the installer for your operating system.
  3. Run the installer and follow the instructions.
  4. Run `python --version`

</details>

<details>
  <summary> Visual Studio Code (VS Code)</summary>

  1. Go to [official Visual Studio Code](https://code.visualstudio.com/download).
</details>

<details>
  <summary> RobotCode Extension</summary>

  1. Go to [official RobotCode](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode).
</details>

<details>
  <summary> C# Extension (optional)</summary>

  1. Go to [official Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp).
</details>

<details>
  <summary> C# Dev Kit Extension (optional)</summary>

  1. Go to [official Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit).
</details>
<br>

# Installation

Create a new virtual environment and activate it (recommended)

### Install dotnetlibrarybase

```console
pip install robotframework-dotnetlibrarybase
```


<br>
<span style="color: #3794FF; font-weight: bold; display: block; text-align: center; font-size: 2em;">.NET PART</span>



## Create a Solution

```sh
dotnet new sln -o . -n libraryname
```
`Output:`
<span style="font-family: 'Courier New', monospace;">The template "Solution File" was created successfully.</span>


## Create .NET Project:
Create a new folder called `src` and navigate into it:

```sh
mkdir src
cd src
dotnet new classlib -n libraryname.example
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Build succeeded in 0.5s
Restore succeeded.</span>


## Add Projects to solution:
`cd..` Back, to add new project to the solution.

```sh
 dotnet sln add .\src\libraryname.example\
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Project 'src\libraryname.example\libraryname.example.csproj' added to the solution.</span>


## Create C# function:
In `src` we have now `library.name`. lets add this function to `Class1.cs`.

```c#
namespace libraryname.example;

public class Class1
{
    public void HelloFromCS()
    {
        System.Console.WriteLine("Hello Mom, from C#");
    }
}
```

## Build .NET:
And to do that we need first `cd` `.\src\libraryname.example\` and run:

```sh
dotnet build
```

`Output:`
<span style="font-family: 'Courier New', monospace;">Build succeeded in 2.9s</span>


## Create robot.toml:
Create a new toml file `robot.toml`.
```toml
extend-python-path = ["src/libraryname.example/bin/Debug/net8.0"]

[env]
PYTHONNET_RUNTIME = "coreclr"
```

## Import dotnet to test.robot
Create a new `test.robot` file

```Robotframework
*** Settings ***
Library    DotNetLibraryBase    libraryname.example.Class1, libraryname.example
#####      DotNetLibraryBase    [namespace].[classname], [Assemblyname]

*** Test Cases ***

New test
    Hello From CS
```

`Output:`
<span style="font-family: 'Courier New', monospace;">Hello Mom, from C#</span>

## Reporting Issues

If you encounter any bugs, have questions, or want to suggest improvements, please don't hesitate to open an [Issues](https://github.com/imbus/robotframework-dotnetlibrarybase/issues). Your feedback is valuable and helps make this project better for everyone.

We appreciate your contribution to improving this project!
