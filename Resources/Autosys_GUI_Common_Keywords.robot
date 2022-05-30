*** Settings ***
Library           SeleniumLibrary    implicit_wait=2 hours
Library           OperatingSystem
Library           Screenshot
Library           ../Scripts/python/FileConverters.py
Library           ../Scripts/python/FileCompare.py

*** Keywords ***
Login to Autosys
    [Arguments]    ${ENVIRONMENT}
    Open and Maximize Browser Headless    Chrome
    Set Selenium Speed    0.1s
    Set Selenium Implicit Wait    5m
    Set Selenium Timeout    1h
    Set Log Level    NONE
    ${autosys_url}    ${autosys_user_name}    ${autosys_password}    Choose Autosys Environment Setup    ${ENVIRONMENT}
    Set Log Level    INFO
    Go to    ${autosys_url}
    Wait Until Element is Visible    ${autosys_username_textbox}
