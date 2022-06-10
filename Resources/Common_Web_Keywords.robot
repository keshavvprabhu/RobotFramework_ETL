*** Settings ***
Library           DateTime
Library           SeleniumLibrary

*** Keywords ***
Open and Maximize Browser
    [Arguments]    ${browser}=chrome
    [Documentation]    Open and Maximize Browser
    ...
    ...    Provide a parameter: ${browser}
    ...
    ...    Possible parameters values are chrome, ff, ie (depending on the drivers available)
    ${options}    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --start-maximized
    Call Method    ${options}    add_experimental_option    useAutomationExtension    ${False}
    Create WebDriver    ${browser}    chrome_options=${options}

Close Browser After Test
    [Documentation]    Closes the browser
    Close Browser

Capture a Screenshot
    ${current_timestamp}    Get Current Date    result_format=%Y%m%%d_%H%M%S_%f
    Sleep    2s
    Capture Page Screenshot    Screenshot_${current_timestamp}.png

Open and Maximize Browser Headless
    [Arguments]    ${browser}
    [Documentation]    Opens a Browser in headless mode
    ${options}    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    headless
    Call Method    ${options}    add_argument    disable-gpu
    Call Method    ${options}    add_experimental_option    useAutomationExtension    ${False}
    Log    ${options}
    Create WebDriver    ${browser}    chrome_options=${options}
