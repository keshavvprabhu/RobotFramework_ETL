*** Test Cases ***
Test1
    Log    Hello. I am in ${TEST NAME}
    Skip if    1==1
    Log    This should not be printed as the test is skipped

Test2
    Log    Hello. I am in ${TEST NAME}
    Skip
    Log    This should not be executed

Test3
    Log    Hello. I am in ${TEST NAME}
