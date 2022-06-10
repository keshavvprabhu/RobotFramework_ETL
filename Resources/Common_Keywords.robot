*** Settings ***
Library           OperatingSystem
Library           DateTime
Library           SSHLibrary

*** Keywords ***
Create Important Directory Structures
    ${input_folder_path}    Convert to String    ${CURDIR}/../Input
    ${scripts_folder_path}    Convert to String    ${CURDIR}/../Scripts
    ${results_folder_path}    Convert to String    ${CURDIR}/../Results/${currdate}/${ENV}
    ${source_folder_path}    Convert to String    ${CURDIR}/../Data/Source
    ${target_folder_path}    Convert to String    ${CURDIR}/../Data/Target

Setup Date Variables
    ${currdate}    DateTime.Get Current Date

Linux Server Login
    [Arguments]    ${linux_host}    ${username}    ${password}
    Log     ${linux_host}
    SSHLibrary.OpenConnection    ${linux_host}    port=22
    SSHLibrary.Login    ${username}    ${password}
    Set Client Configuration    timeout=1000s
    ${linux_hostname}    SSHLibrary.Execute Command    hostname
    Log    ${linux_hostname}

Create File Comapre Config File
    [Arguments]    ${config_file_name}    ${database_file_path}    ${source_file_name}    ${source_file_delimiter}    ${target_file_name}    ${target_file_delimiter}    ${source_file_columns}    ${target_file_columns}    ${key_columns}    ${ignore_columns}    ${result_stats_file_name}    ${result_delimiter}    ${result_file_name}    ${limit_mismatch_count}    ${compare_file_headers}    ${test_environment}='NA'
    ...    ${test_name}='NA'
    [Documentation]    Creates File Compare Config File
    OperatingSystem.Empty Directory    ${config_folder_path}
    ${database_file_path}    Convert to String    ${database_file_path}
    ${source_file_path}    Convert to String    ${source_folder_path}/${source_file_name}
    ${target_file_path}    Convert to String    ${target_folder_path}/${target_file_name}
    ${result_stats_file_path}    Convert to String    ${resultsDir}/${result_stats_file_name}
    ${result_file_path}    Convert to String    ${resultsDir}/${result_file_name}
    Operating System.File Should not be Empty    ${source_file_path}
    Operating System.File Should not be Empty    ${target_file_path}
    ${config_file_path}    Convert to String    ${config_folder_path}/${config_file_name}
    Run Keyword and Ignore Error    OperatingSystem.Remove File    ${config_file_path}
    Append to File    ${config_file_path}    database_file_path=${database_file_path}\n    encoding=UTF-8
    Append to File    ${config_file_path}    source_file_path=${source_file_path}\n    encoding=UTF-8
    Append to File    ${config_file_path}    source_file_delimiter=${source_file_delimiter}    encoding=UTF-8
    Append to File    ${config_file_path}    target_file_path=${target_file_path}\n    encoding=UTF-8
    Append to File    ${config_file_path}    target_file_delimiter=${target_file_delimiter}\n    encoding=UTF-8
    Append to File    ${config_file_path}    source_file_columns=${source_file_columns}\n    encoding=UTF-8
    Append to File    ${config_file_path}    target_file_columns=${target_file_columns}\n    encoding=UTF-8
    Append to File    ${config_file_path}    key_columns=${key_columns}\n    encoding=UTF-8
    Append to File    ${config_file_path}    ignore_columns=${ignore_columns}\n    encoding=UTF-8
    Append to File    ${config_file_path}    result_stats_file_path=${result_stats_file_path}\n    encoding=UTF-8
    Append to File    ${config_file_path}    result_delimiter=${result_delimiter}\n    encoding=UTF-8
    Append to File    ${config_file_path}    result_file_path=${result_file_path}\n    encoding=UTF-8
    Append to File    ${config_file_path}    limit_mismatch_count=${limit_mismatch_count}\n    encoding=UTF-8
    Append to File    ${config_file_path}    compare_file_headers=${compare_file_headers}\n    encoding=UTF-8
    Append to File    ${config_file_path}    test_environment=${test_environment}\n    encoding=UTF-8
    Append to File    ${config_file_path}    test_name=${test_name}\n    encoding=UTF-8
    OperatingSystem.File Should not be Empty    ${config_file_path}
    OperatingSystem.File Should Exist    ${config_file_path}
    Set Global Variable    ${result_stats_file_path}
    [Return]    ${config_file_path}
