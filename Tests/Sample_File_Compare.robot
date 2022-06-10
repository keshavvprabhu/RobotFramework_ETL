*** Settings ***
Resource          ../Resources/Common_Keywords.robot

*** Test Cases ***
Sample1
    ${source_file_name}    Convert to String    Source_File_Name.psv
    ${target_file_name}    Convert to String    Target_File_Name.psv
    ${source_file_path}    Convert to String    ${CURDIR}/../Data/Source/${source_file_name}
    ${target_file_path}    Convert to String    ${CURDIR}/../Data/Target/${target_file_name}
    ${delimiter}    Convert to String    |
    OperatingSystem.File Should Exist    ${source_file_path}
    OperatingSystem.File Should Exist    ${target_file_path}
    # File Compare Part
    ${load_table_name}    Convert to String    ${TESTNAME}
    ${source_file_name}    Convert to String    ${source_file_name}
    ${source_file_delimiter}    Convert to String    ${delimiter}
    ${target_file_name}    Convert to String    ${target_file_name}
    ${target_file_delimiter}    Convert to String    ${delimiter}
    ${source_header_string}    FileConverters.Get File Header    ${source_folder_path}/${source_file_name}    ${delimiter}
    ${source_file_columns}    Convert to String    ${source_header_string}
    ${target_header_string}    FileConverters.Get File Header    ${target_folder_path}/${target_file_name}    ${delimiter}
    ${target_file_columns}    Convert to String    ${target_header_string}
    ${key_columns}    Convert to String    KeyAttribute1|KeyAttribute2
    ${ignore_columns}    Convert to String    ${EMPTY}
    ${result_stats_file_name}    Convert to String    FileCompare_Summary_Report.psv
    ${result_derlimiter}    Convert to String    |
    ${result_file_name}    Convert to String    ComparisonResult_${load_table_name}.psv
    ${limit_mismatch_count}    Convert to String    0
    ${config_file_name}    Convert to String    ${load_table_name}.cfg
    ${config_file_path}    Create File Compare Config File    ${config_file_name}    ${sqlite_db_file_path}    ${source_file_name}    ${source_file_delimiter}    ${target_file_name}    ${target_file_delimiter}    ${source_file_columns}    ${target_file_columns}    ${key_columns}    ${ignore_columns}    ${result_stats_file_name}    ${result_delimiter}    ${result_file_name}    ${limit_mismatch_count}    False
    ...    ${ENV}    ${TESTNAME}
