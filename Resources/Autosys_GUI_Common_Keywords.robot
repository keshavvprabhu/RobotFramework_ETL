*** Settings ***
Library           SeleniumLibrary    implicit_wait=2 hours
Library           OperatingSystem
Library           Screenshot
Library           ../Scripts/python/FileConverters.py
Library           ../Scripts/python/FileCompare.py
Resource          Autosys_GUI_Locators.robot
Library           Collections
Resource          Common_Web_Keywords.robot

*** Keywords ***
Login to Autosys
    [Arguments]    ${ENVIRONMENT}
    [Documentation]    Login to Autosys Web Portal
    Open and Maximize Browser Headless    chrome
    Set Selenium Speed    0.1s
    Set Selenium Implicit Wait    2h
    Set Selenium Timeout    2h
    Set Log Level    NONE
    ${autosys_url}    ${autosys_username}    ${autosys_password}    Choose Autosys Environment Setup    ${ENVIRONMENT}
    Set Log Level    INFO
    Go to    ${autosys_url}
    Wait Until Element is Visible    ${autosys_username_textbox}
    Input Text    ${autosys_username_textbox}    ${autosys_username}
    Wait Until Element is Visible    ${autosys_password_textbox}
    Input Password    ${autosys_password_textbox}    ${autosys_password}
    Sleep    3s
    Wait until Element is Visible    ${autosys_login_button}
    SeleniumLibrary.Click Button    ${autosys_login_button}
    Wait until element is not Visible    ${autosys_loader}    5m    Autosys is Still Loading
    Wait until Element is Visible    ${autosys_logout}

Navidate to Enterprise Command Line Screen
    [Documentation]    Navigate to Enterprise Command Line Tabl in Autosys GUI
    Page Should Contain    ${autosys_logout}
    Unselect Frame
    Wait until Element is Visible    ${autosys_ecli_tab}
    Click Element    ${autosys_ecli_tab}
    Page Should Contain Element    ${ecli_frame}
    Select Frame    ${ecli_frame}

Logout from Autosys
    [Documentation]    Logout from Autosys
    Unselect Frame
    Click Element    ${autosys_logout}
    Wait Until Element is not Visible    ${autosys_loader}    1m    Autosys is Still Loading
    Wait Until Element is Visible    ${autosys_username_txtbox}    1m
    Sleep    1m

Get Job Status Extract
    [Arguments]    ${job_name}
    [Documentation]    Get Job Status in Autosys
    ${autosys_server_name}    Convert to String    CSA
    ${command}    Convert to String    autorep -j ${job_name} -l2
    SeleniumLibrary.Set Focus to Element    ${autosys_ecli_server_txtbox}
    Input Text    ${autosys_ecli_server_txtbox}    ${autosys_server_name}
    SeleniumLibrary.Set Focus to Element    ${autosys_ecli_cmdline_txtbos}
    Input Text    ${autosys_ecli_cmdline_txtbos}    ${command}
    Click Element    ${autosys_ecli_execute_btn}
    Wait until Element is not visible    ${autosys_loader}    5m    Autosys Still Loading
    ${result}    Get Text    ${autosys_ecli_cmdline_output_textarea}
    Should not be empty    ${result}
    [Return]    ${result}

Get JIL
    [Arguments]    ${autosys_server_name}    ${job_name}
    [Documentation]    Get JIL of an autosys job
    ${autosys_server_name}    Convert to String    ${autosys_server_name}
    ${command}    Convert to String     autorep -J ${job_name} -q -l2
    SeleniumLibrary.Set Focus to Element    ${autosys_ecli_server_txtbox}
    Input Text    ${autosys_ecli_server_txtbox}    ${autosys_server_name}
    SeleniumLibrary.Set Focus to Element    ${autosys_ecli_cmdline_txt}
    Input Text    ${autosys_ecli_cmdline_txtbox}    ${command}
    Click Element    ${autosys_ecli_execute_btn}
    Wait until Element is not Visible    ${autosys_loader}    5m     Autosys is Still Loading
    ${result}    Get Text    ${autosys_ecli_cmdline_output_textarea}
    Should not be empty    ${result}

Autosys Test Suite Setup
    Set Autosys Environment Variables
    Create Directory Structures
    Setup Autosys Email Report Variables

Parse Autosys Job Information Log
    OperatingSystem.File Should Exist    ${input_jil_file_path}
    ${output_jil_file_path}    FileConverters.Parse Autosys Jil Extract    ${environment}    ${input_jil_file_path}    ${delimiter}
    OperatingSystem.File Should Exist    ${output_jil_file_path}

Set Autosys Environment Variables
    [Documentation]    Set Environment Variables
    Decode Autosys Credentials
    Set Log Level     INFO
    ${currdate}    Get System Date in yyyymmdd Format
    ${currdate_dash}    Get System Date in yyyy-mm-dd format
    # Create SQLite Database
    ${sqlite_db_file_path}    Convert to String    ${CURDIR}/../Database/Autosys_Automation.db
    FileCompare.Create Sqlite Database    ${sqlite_db_file_path}
    # Setting Global Variables
    Set Global Variable    ${currdate}
    Set Global Variable    ${currdate_dash}
    Set Global Variable    ${sqlite_db_file_path}

Create Directory Structures
    [Documentation]    Creates the necessary Directory Structures required for the framework
    ${source_folder_path}    Convert to String    ${CURDIR}/../Data/Source
    ${target_folder_path}    Convert to String    ${CURDIR}/../Data/Target
    ${sqlite_db_folder_path}    Convert to String    ${CURDIR}/../Database
    ${resultsDir}    Convert to String    ${CURDIR}/../Results/${currdate_dash}/Autosys_Automation
    ${config_folder_path}    Convert to String    ${CURDIR}/../Scripts/Config
    ${file_compare_folder_path}    Convert to String    ${resultsDir}/FileCompare
    ${autosys_input_folder_path}    Convert to String    ${CURDIR}/../Input/Autosys
    # Creating the directories
    OperatingSystem.Create Directory    ${source_folder_path}
    OperatingSystem.Create Directory    ${target_folder_path}
    OperatingSystem.Create Directory    ${sqlite_db_folder_path}
    OperatingSystem.Create Directory    ${resultsDir}
    OperatingSystem.Create Directory    ${config_folder_path}
    OperatingSystem.Create Directory    ${file_compare_folder_path}
    OperatingSystem.Create Directory    ${autosys_input_folder_path}
    # Set Global Variables
    Set Global Variable    ${source_folder_path}
    Set Global Variable    ${target_folder_path}
    Set Global Variable    ${sqlite_db_folder_path}
    Set Global Variable    ${resultsDir}
    Set Global Variable    ${config_folder_path}
    Set Global Variable    ${file_compare_folder_path}
    Set Global Variable    ${autosys_input_folder_path}

Decode Autosys Credentials
    Set Log Level     NONE
    ${autosys_user_name}    Unobscure Credential    ${autosys_user_name}
    ${autosys_password}    Unobscure Credential    ${autosys_password}
    Set Global Variable    ${autosys_user_name}
    Set Global Variable    ${autosys_password}

Get Autosys Job Count
    [Arguments]    ${table_name}
    ${sql_stmt}    Convert to String    select count(distinct JobName) as Total_Jobs from ${table_name};
    ${job_count}    SQLiteUtilities.Query Value from SQLite    ${sqlite_db_file_path}    ${sql_stmt}
    [Return]    ${job_count}

Query Autosys SQLite Database
    [Arguments]    ${sql_query_stmt}    ${output_file_path}    ${delimiter}
    [Documentation]    Query Autoss Automation SQLite Database
    OperatingSystem.Remove File    ${output_file}
    SQLite_Utilities.Query Sqlite Databse    ${sqlite_db_file_path}    ${sql_query_stmt}    ${output_file_path}    ${delimiter}    True
    OperatingSystem.File Should Exist    ${output_file_path}

Choose Autosys Environment Setup
    [Arguments]    ${ENV}
    # Choosing Environment Setup
    @{DEV}    Create List    ${autosys_dev_url}    ${autosys_dev_server_name}    ${autosys_dev_username}    ${autosys_dev_password}
    @{SIT}    Create List    ${autosys_sit_url}    ${autosys_sit_server_name}    ${autosys_sit_username}    ${autosys_sit_password}
    &{ENVIRONMENTS}    Create Dictionary    DEV=@{DEV}    SIT=@{SIT}
    @{CHOSEN_ENV}    Get from Dictionary    ${ENVIRONMENTS}    ${ENV}
    ${autosys_url}    Convert to String    @{CHOSEN_ENV}[0]
    ${autosys_server_name}    Convert to String    @{CHOSEN_ENV}[1]
    ${autosys_username}    Convert to String    @{CHOSEN_ENV}[2]
    ${autosys_password}    Convert to String    @{CHOSEN_ENV}[3]
    # Setting these as Global Variables
    Set Global Variable    ${autosys_url}
    Set Global Variable    ${autosys_server_name}
    Set Global Variable    ${autosys_username}
    Set Global Variable    ${autosys_password}
    [Return]    ${autosys_url}    ${autosys_username}    ${autosys_password}

Setup Autosys Email Report Variables
    ${generic_email_footer}    Convert to String    <br><br><br><font color="grey"><p> This report is auto-generated on demand. Please reach out to ${sender} in case you have feedback/questions.</p>
    Log    Setting up email addresses
    ${str_to_email_address}    Convert to String    gmail@yahoo.com
    ${str_cc_email_address}    Convert to String    yahoo@gmail.com
    # Setting Global Variables
    Set Global Variable    ${generic_email_footer}
    Set Global Variable    ${str_to_email_address}
    Set Global Variable    ${str_cc_email_address}
