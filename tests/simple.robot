*** Settings ***
Library     DotNetLibraryBase    DotNetDemoLibrary    DotNetDemoLibrary.DemoKeywords    1234    AS    DotNetDemoLibrary
Library     DotNetLibraryBase    ${None}    System.String    1234    AS    Str


*** Test Cases ***
first
    Do Something
    DotNetDemoLibrary.Do Something
    Do Something With An String    a value
    ${aa}    Str.Get Length
