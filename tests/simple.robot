*** Settings ***
Library     DotNetLibraryBase    DotNetDemoLibrary    DotNetDemoLibrary.DemoKeywords    1234    AS    DotNetDemoLibrary
Library     DotNetLibraryBase    ${None}    System.String    1234    AS    Str


*** Test Cases ***
first
    Do Something
    DotNetDemoLibrary.Do Something
    ${aa}    Str.Get Length
