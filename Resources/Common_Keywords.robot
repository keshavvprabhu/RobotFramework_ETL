*** Settings ***
Library           OperatingSystem
Library           DateTime

*** Keywords ***
Create Important Directory Structures
    ${input_folder_path}    Convert to String    ${CURDIR}/../Input
    ${scripts_folder_path}    Convert to String    ${CURDIR}/../Scripts
    ${results_folder_path}    Convert to String    ${CURDIR}/../Results/${currdate}/${ENV}
    ${source_folder_path}    Convert to String    ${CURDIR}/../Data/Source
    ${target_folder_path}    Convert to String    ${CURDIR}/../Data/Target

Setup Date Variables
    ${currdate}    DateTime.Get Current Date
