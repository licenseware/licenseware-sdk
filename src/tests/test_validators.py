import pytest
from assertpy import assert_that
from licenseware.file_validators import GeneralValidator, validate_filename
from licenseware.registry.uploader import reason_response
import os

# pytest -s tests/test_validators.py


test_files_path = "/home/acmt/Documents/files_test"



def test_validate_filename():
    valid_fname = validate_filename("cpuq_original.txt", ["cpuq"], [".txt"])
    assert_that(valid_fname).is_true()



def test_validate_cpuq_file_ok():

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "cpuq.txt"), 
        required_input_type = "txt",
        text_contains_all   = ["[BEGIN SCRIPT INFO]"]
    )

    assert_that(v.validate()).is_true()



def test_validate_lms_detail_file_ok():

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "lms_detail.csv"), 
        required_input_type = "csv",
        min_rows_number = 1,
        required_columns = [
            'RL_SCRIPT_VERSION',
            'TIMESTAMP',
            'MACHINE_ID',
            'VMACHINE_ID',
            'BANNER',
            'DB_NAME',
            'USER_COUNT',
            'SERVER_MANUFACTURER',
            'SERVER_MODEL',
            'OPERATING_SYSTEM',
            'SOCKETS_POPULATED_PHYS',
            'TOTAL_PHYSICAL_CORES',
            'PROCESSOR_IDENTIFIER',
            'PROCESSOR_SPEED',
            'TOTAL_LOGICAL_CORES',
            'PARTITIONING_METHOD',
            'DB_ROLE',
            'INSTALL_DATE'
        ]
    )

    assert_that(v.validate()).is_true()





def test_validate_rvtools_file_ok():

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "RVTools.xlsx"), 
        required_input_type = "excel",
        min_rows_number = 1,
        required_sheets = ['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
        required_columns = [
            'VM', 
            'Host', 
            'OS',
            'Sockets', 
            'CPUs',
            'Model',
            'CPU Model',
            'Cluster',
            '# CPU',
            '# Cores',
            'ESX Version',
            'HT Active',
            'Name', 
            'NumCpuThreads', 
            'NumCpuCores'
        ] 
    )

    assert_that(v.validate()).is_true()



def test_validate_lms_options_file_ok():

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "lms_options_small.csv"), 
        required_input_type = "csv",
        min_rows_number = 1,
        required_columns = [
            'MACHINE_ID',
            'DB_NAME',
            'TIMESTAMP',
            'HOST_NAME',
            'INSTANCE_NAME',
            'OPTION_NAME',
            'OPTION_QUERY',
            'SQL_ERROR_CODE',
            'SQL_ERROR_MESSAGE',
            'COL010',
            'COL020',
            'COL030',
            'COL040',
            'COL050',
            'COL060',
            'COL070',
            'COL080',
            'COL090',
            'COL100',
            'COL110',
            'COL120',
            'COL130',
            'COL140',
            'COL150',
            'COL160'
        ]
    )

    assert_that(v.validate()).is_true()




def test_validate_review_lite_dba_feature_file_ok():
    # server-name_database-name_filename.csv

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "anjin_SD2213_dba_feature.csv"), 
        # required_input_type = "csv",
        text_contains_any   = [
            'DBA_FEATURE_USAGE_STATISTICS',
            'ORACLE PARTITIONING INSTALLED',
            'DATABASE VERSION'
        ]
    )
    
    assert_that(v.validate()).is_true()



def test_validate_review_lite_options_file_ok():
    # server-name_database-name_filename.csv

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "anjin_SD2213_options.csv"), 
        # required_input_type = "csv",
        text_contains_any   = [
            'DBA_FEATURE_USAGE_STATISTICS',
            'ORACLE PARTITIONING INSTALLED',
            'DATABASE VERSION'
        ]
    )

    assert_that(v.validate()).is_true()



def test_validate_review_lite_version_file_ok():
    # server-name_database-name_filename.csv

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "anjin_SD2213_version.csv"), 
        # required_input_type = "csv",
        text_contains_any   = [
            'DBA_FEATURE_USAGE_STATISTICS',
            'ORACLE PARTITIONING INSTALLED',
            'DATABASE VERSION'
        ]
    )

    assert_that(v.validate()).is_true()


