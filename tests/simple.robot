*** Settings ***
Library     DotNetLibraryBase
...         DotNetDemoLibrary.DemoKeywords, DotNetDemoLibrary, Version\=2.0.1.1, Culture\=de, PublicKeyToken\=null
...         1234
...         AS    DotNetDemoLibrary
Library     DotNetLibraryBase    System.String    1234    AS    Str


*** Test Cases ***
first
    Do Something
    DotNetDemoLibrary.Do Something
    Do Something With An String    a value
    ${aa}    Str.Get Length
