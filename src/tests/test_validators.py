import pytest
from assertpy import assert_that
from licenseware.file_validators import GeneralValidator, validate_filename
from licenseware.registry.uploader import reason_response
import os


# pytest -s tests/test_validators.py
# pytest -s tests/test_validators.py::test_sccm


test_files_path = "/home/acmt/Documents/files_test"


def columns_check(file: str, reason: bool):
    """
        Checking if columns are present in the given file
        If one case is valid the success result is returned 
        If no case is valid a fail response is returned
    """
    
    columns_software  = ['SoftwareKey', 'Publisher', 'Product', 'Version', 'Language', 'ProductCode']
    columns_inventory = ['HardwareKey', 'SoftwareKey']
    columns_hardware  = ['HardwareKey', 'Machine Name', 'Organizational Unit', 'IP Addresses',
        'MAC Address', 'Has Client', 'Last Login', 'Operating System',
        'Manufacturer', 'Model', 'Asset Tag', 'Number Of Processors',
        'Serial Number', 'Processor Architecture', 'Processor Vendor',
        'Procssor Brand', 'Domain', 'Hardware Class', 'Number of Cores',
        'HT Capable', 'HT Enabled', 'Platform', 'Virtual Flag', 'Cluster Name',
        'MultiUser Flag']

    
    valid_software_csv = GeneralValidator(
        input_object=file,
        text_contains_all=columns_software
    ).validate(show_reason=reason)
    
    if reason:
        if valid_software_csv['status'] == 'success': return valid_software_csv
    else:
        if valid_software_csv: return True
    
    
    valid_inventory_csv = GeneralValidator(
        input_object=file,
        text_contains_all=columns_inventory
    ).validate(show_reason=reason)
    
    if reason:
        if valid_inventory_csv['status'] == 'success': return valid_inventory_csv
    else:
        if valid_inventory_csv: return True
    
    
    valid_hardware_csv = GeneralValidator(
        input_object=file,
        text_contains_all=columns_hardware
    ).validate(show_reason=reason)
    
    if reason:
        if valid_hardware_csv['status'] == 'success': return valid_hardware_csv
    else:
        if valid_hardware_csv: return True
        
        
    # If all files fail
    if reason:
        return {"status": "fail", "message": "File does not contain all the required columns needed for processing"}
    else:
        return False
    
    
def test_sccm():
    
    files_path = os.path.join(test_files_path, "SCCM") 
    files = ['HardwareQuery.csv', 'InventoryQuery.csv',  'SoftwareQueryMicrosoft.csv']
    
    for file in files:
        res = columns_check(file=os.path.join(files_path, file), reason=False)
        assert_that(res).is_true()
    


def test_powercli():
    
    columns_required = ['VCenterServerName', 'VCenterVersion',
    'HostName','IsStandAlone', 'Datacenter',
    'Cluster', 'VMs', 'Vendor',
    'Model', 'FullName', 'Version',
    'CpuModel', 'CpuMhz', 'CPU',
    'CpuCores', 'HyperThreading', 'CpuThreads',
    'PowerState', 'ConnectionState', 'Datastores']


    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "PowerCLI/seskusvcenter-HW-Inventory-Information.csv"), 
        text_contains_all = columns_required
    )

    assert_that(v.validate()).is_true()

    


def test_validate_filename():
    valid_fname = validate_filename("cpuq_original.txt", ["cpuq"], [".txt"])
    assert_that(valid_fname).is_true()



def test_validate_cpuq_file_ok():

    v = GeneralValidator(
        input_object = os.path.join(test_files_path, "cpuq.txt"), 
        required_input_type = "txt",
        text_contains_all   = ["[BEGIN SCRIPT INFO]", "Virtual CPUs"]
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
        required_input_type = "csv",
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
        required_input_type = "csv",
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
        required_input_type = "csv",
        text_contains_any   = [
            'DBA_FEATURE_USAGE_STATISTICS',
            'ORACLE PARTITIONING INSTALLED',
            'DATABASE VERSION'
        ]
    )

    assert_that(v.validate()).is_true()


