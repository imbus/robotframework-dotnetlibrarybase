*** Settings ***
Library     DotNetLibraryBase
...             DotNetDemoLibrary.DemoKeywords, DotNetDemoLibrary, Version\=1.0.0.0, Culture\=de, PublicKeyToken\=null
...             1234
...         AS    DotNetDemoLibrary
Library     DotNetLibraryBase    {'type_name': 'System.String', 'options': 'asd'}    1234    AS    Str
Library     DotNetLibraryBase    System.Console    ${EMPTY}    AS    Console
# Library    DotNetLibraryBase    System.String    1234    AS    Str


*** Test Cases ***
first
    Do Something
    DotNetDemoLibrary.Do Something
    Do Something With An String    a value
    ${aa}    Str.Get Length
    Console.WriteLine    Hallo Welt from Console
    Console.Set ForegroundColor    Green
    Console.WriteLine    Hallo Welt from Console in Green

second
    Do Something With An String    another value

third
    Console.Write Line    buffer=Hallo Welt from Console
