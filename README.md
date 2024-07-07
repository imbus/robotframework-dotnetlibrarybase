<!--
SPDX-FileCopyrightText: 2024 Daniel Biehl <daniel.biehl@imbus.de>

SPDX-License-Identifier: Apache-2.0
-->

# robotframework-DotNetLibraryBase

[![PyPI - Version](https://img.shields.io/pypi/v/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)
[![License](https://img.shields.io/github/license/imbus/robotframework-dotnetlibrarybase.svg)](https://github.com/imbus/robotframework-dotnetlibrarybase/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/robotframework-dotnetlibrarybase.svg)](https://pypi.org/project/robotframework-dotnetlibrarybase)


## Introduction
Welcome to the documentation for `robotframework-DotNetLibraryBase`. This library allows you to integrate .NET functionalities into your Robot Framework test suites.

### Features

- Seamless integration with .NET libraries.
- Easy to use and configure.
- Supports various .NET functionalities out-of-the-box.


### To get started, you will need:

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
  <summary> Hatch (a modern Python project manager)</summary>
  <br>

  ```sh
  pipx install hatch==1.12.0
  ```
  Run `hatch --version`
</details>

<details>
  <summary> Visual Studio Code (VS Code)</summary>

  1. Go to [official Visual Studio Code](https://code.visualstudio.com/download).
</details>

<details>
  <summary> RobotCode - (VS Code Extension)</summary>

  1. Go to [official RobotCode](https://marketplace.visualstudio.com/items?itemName=d-biehl.robotcode).
</details>

<details>
  <summary> Terminal (optional)</summary>

  1. Go to [official Terminal](https://learn.microsoft.com/de-de/windows/terminal/install).
</details>

<details>
  <summary> C# Extension (optional)</summary>

  1. Go to [official Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp).
</details>

<details>
  <summary> C# Dev Kit Extension (optional)</summary>

  1. Go to [official Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit).
</details>


## Create a New Project:
Use Hatch to create a new project:
  ```sh
  hatch new libraryname .
  ```
  The *libraryname* is your new dotnet library that you want to use in Robot test. and the dot at the end is where you wnat to create your project. (which is in the same folder where you are at)

### Edit pyproject.toml
Edit `pyproject.toml` file to add libraries in `dependencies` list and add the folowing:

```toml
# Edit dependencies
dependencies = ["robotframework>=6.0.0","robotframework-dotnetlibrarybase"]

# Add more dependencies
[tool.hatch.envs.default]
dependencies = [
  "coverage[toml]>=6.5.0",
  "pytest",
  "ruff",
  "mypy",
  "black",
]

[tool.hatch.build]
dev-mode.dirs = ["src"]
```

### Build Hatch
  ```sh
  hatch build
  ```
  ```sh
  hatch env create
  ```
## Create New Robot-Test:
Inside our `tests` directory add a new robot test for example `test.robot`.
and at this point VSCode might ask you to choose python Interpreter. chose the environment that we already created with <span style="color: #3794FF;">Hatch</span>  at the end.

## Create Python keyword:
Inside `src` we need to create a simple python function in `__init__.py` to use it in our robot test file.

```python
def hello_from_python():
    print("Hello Mom, from Python!")
```
### Run Hatch pip list
  ```sh
  hatch run pip list
  ```

## Robot Test Case:

```Robotframework
*** Settings ***
Library    libraryname

*** Test Cases ***
new test
    Hello From Python
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Hello Mom, from Python</span>

<h1 style="color: #3794FF; font-weight: bold; text-align: center;">.NET PART</h1>

## Create a Solution

```sh
dotnet new sln -o . -n libraryname
```
`Output:`
<span style="font-family: 'Courier New', monospace;">The template "Solution File" was created successfully.</span>


## Create .NET Project:
`cd` to `src` and write this:

```sh
dotnet new classlib -n libraryname.example
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Build succeeded in 0.5s
Restore succeeded.</span>

## Create Playground Console (Optional):
```sh
dotnet new console -n libraryname.playground
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Build succeeded in 0.5s
Restore succeeded.</span>

## Add Projects to solution:
`cd..` Back, to add our new project/s to the solution.

```sh
 dotnet sln add .\src\libraryname.example\
 dotnet sln add .\src\libraryname.playground\
```
`Output:`
<span style="font-family: 'Courier New', monospace;">Project 'src\libraryname.example\libraryname.example.csproj' added to the solution.</span>

## Create C# function:
In `src` you'll see `library.name` folder. and we already have `Class1.cs`. we want to do the same thing as we did in python.
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
We can not use this class directly in our `test.robot` like we used to do with python. first we need to build dotnet. And to do that we need first `cd .\src\libraryname.example\` and write:

```sh
dotnet build
```

`Output:`
<span style="font-family: 'Courier New', monospace;">Build succeeded in 2.9s</span>


## Create robot.toml:
create a new toml file `robot.toml`.
```toml
extend-python-path = ["src/libraryname.example/bin/Debug/net8.0"]

[env]
PYTHONNET_RUNTIME = "coreclr"
```

## Import dotnet to test.robot

```Robotframework
*** Settings ***
Library    libraryname
# INFO     DotNetLibraryBase    [namespace].[classname], [Assemblyname]
Library    DotNetLibraryBase    libraryname.example.Class1, libraryname.example

*** Test Cases ***
new test
    Hello From Python

another new test
    Hello From CS
```

`Output:`
<span style="font-family: 'Courier New', monospace;">Hello Mom, from C#</span>

## Reporting Issues

If you encounter any bugs, have questions, or want to suggest improvements, please don't hesitate to open an [Issues](https://github.com/imbus/robotframework-dotnetlibrarybase/issues). Your feedback is valuable and helps make this project better for everyone.

We appreciate your contribution to improving this project!
