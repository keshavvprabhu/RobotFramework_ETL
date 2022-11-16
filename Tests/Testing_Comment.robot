*** Settings ***
Resource          ../Resources/Common_Keywords.robot

*** Test Cases ***
Testing Comment 1
    ${Arg1}    Convert to Integer    1
    ${Arg2}    Convert to String    This is a value
    ${Arg3}    Convert To Number    0.456
    ${return1}    ${return2}    ${return3}    Sample Keyword with Multiple Arguments    ${Arg1}    ${Arg2}    ${Arg3}
    #Before Pressing Ctrl+3 (Comment)
    ${return1}    ${return2}    ${return3}    Sample Keyword with Multiple Arguments    ${Arg1}    ${Arg2}    ${Arg3}
    #After Pressing Ctrl+3 \ (Comment) \ - This works as expected
    Comment    ${return1}    ${return2}    ${return3}    Sample Keyword with Multiple Arguments    ${Arg1}    ${Arg2}    ${Arg3}
    #After Pressing Ctrl+3 (Comment) and Ctrl+z (Undo) \ - Did not work as expected and the Keyword went to the rightmost cell
    ${return1}    ${return2}    ${return3}    ${Arg1}    ${Arg2}    ${Arg3}    Sample Keyword with Multiple Arguments
    #After Pressing Ctrl+3 Comment and Ctrl+4 (Uncomment) and the Keyword went to the rightmost cell
    ${return1}    ${return2}    ${return3}    ${Arg1}    ${Arg2}    ${Arg3}    Sample Keyword with Multiple Arguments

Test Templates
    [Template]    Calculate
    3    +    8
    8    -    4
    8    /    4
    4    *    2
