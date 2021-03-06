"""

Validator for streams of files and files.

from licenseware import GeneralValidator, validate_filename

or 

from licenseware.file_validators import GeneralValidator, validate_filename


A class that validates files and text
    
Usage

from file_validators import GeneralValidator, validate_filename

v = GeneralValidator(
    input_object,           - required: file path, string or stream
    required_input_type = None,    - required: 'excel', 'csv', 'txt', 'string', 'stream'
    required_sheets   = [], - sheets names list that needs to be found in 'excel'
    required_columns  = [], - columns names list that needs to be found in 'excel', 'csv'
    text_contains_all = [], - text list that needs to be found in 'txt', 'string', 'stream'
    text_contains_any = [], - text list that needs to be found in 'txt', 'string', 'stream'
    min_rows_number   = 0,  - minimum rows needed for 'excel', 'csv'
    header_starts_at  = 0   - row number where the header with columns starts (count starts from 0)
    buffer = 9000           - bytes buffer to read from stream FileStorage object
)

if v.validate():
    # stuff


# or with json message

res = v.validate(show_reason=True)
if res['status'] == 'success':
    return res['message']
elif res['status'] == 'fail':
    return res['message']


"""


import os, re
import itertools
import pandas as pd
from io import BytesIO
from licenseware.utils.log_config import log


def validate_text_contains_all(text, text_contains_all):
    """
        Raise exception if contents of the text file don't contain all items in text_contains_all list
    """

    if not text_contains_all: return

    matches = []
    for txt_to_find in text_contains_all:
        pattern = re.compile(re.escape(txt_to_find), flags=re.IGNORECASE)
        match = re.search(pattern, text)
        if match:
            if match[0] not in matches:
                matches.append(match[0])

    if sorted(matches) != sorted(text_contains_all):
        raise Exception(f'File must contain the all following keywords: {", ".join(text_contains_all)}')
    

def validate_text_contains_any(text, text_contains_any):
    """
        Raise exception if contents of the text file don't contain at least one item in text_contains_any list
    """

    if not text_contains_any: return

    matches = []
    for txt_to_find in text_contains_any:
        pattern = re.compile(re.escape(txt_to_find), flags=re.IGNORECASE)
        match = re.search(pattern, text)
        if match:
            if match.group(0) not in matches:
                matches.append(match.group(0))

    if not matches:
        raise Exception(f'File must contain at least one of the following keywords: {", ".join(text_contains_any)}')


def validate_columns(df, required_columns, required_sheets=[]):
    """
        Raise an error if columns required are not found in the table
    """

    if not required_columns: return

    if isinstance(df, dict):
        given_columns = []
        for sheet, table in df.items():
            if sheet not in required_sheets: continue
            given_columns.append(table.columns.tolist())
        given_columns = set(itertools.chain.from_iterable(given_columns))
    else:
        given_columns = df.columns

    commun_cols = list(set.intersection(set(required_columns), set(given_columns)))
    if sorted(required_columns) != sorted(commun_cols):
        missing_cols = set.difference(set(required_columns), set(given_columns))
        raise Exception(f'Table has the following columns missing: {missing_cols}')


def validate_rows_number(df, min_rows_number, required_sheets=[]):
    """
        Raise error if minimum_rows_number is not satisfied
    """

    if not min_rows_number: return

    if isinstance(df, dict):
        for sheet, table in df.items():
            if sheet not in required_sheets: continue
            if table.shape[0] < min_rows_number:
                raise Exception(f'Expected {sheet} to have at least {min_rows_number} row(s)')
    else:
        if df.shape[0] < min_rows_number:
            raise Exception(f'Expected table to have at least {min_rows_number} row(s)')


def validate_sheets(file, required_sheets):
    """
        Raise error if required_sheets are not found in file
    """

    if not required_sheets: return

    sheets = pd.ExcelFile(file).sheet_names

    common_sheets = list(set.intersection(set(sheets), set(required_sheets)))

    if sorted(required_sheets) != sorted(common_sheets):
        missing_sheets = set.difference(set(required_sheets), set(sheets))
        raise Exception(f"File doesn't contain the following needed sheets: {missing_sheets}")


def validate_filename(fname, fname_contains=[], fname_endswith=[]):
    """
        Check if filename contains all needed keywords and all accepted file types
    """

    if not isinstance(fname, str): raise ValueError("fname must be a string")

    try:
        validate_text_contains_any(fname, fname_contains)
    except:
        return False

    for file_type in fname_endswith:
        if fname.lower().endswith(file_type): return True

    return False


class GeneralValidator:

    def __init__(
            self,
            input_object,
            required_input_type=None,
            required_sheets=[],
            required_columns=[],
            text_contains_all=[],
            text_contains_any=[],
            min_rows_number=0,
            header_starts_at=0,
            buffer=9000,
    ):

        self.input_object = input_object
        self.required_input_type = required_input_type
        self.required_sheets = required_sheets
        self.required_columns = required_columns
        self.text_contains_all = text_contains_all
        self.text_contains_any = text_contains_any
        self.min_rows_number = min_rows_number
        self.header_starts_at = header_starts_at
        self.skip_validate_type = False
        # Making sure we don't miss characters
        self.buffer = buffer + sum([len(c) for c in required_columns]) + len(text_contains_all) + len(text_contains_any)

    def _validate_type(self):
        """
            Determine which handler to use based on input type provided 
            Raise error if file/obj type is not as expected (excel/txt file, or string/stream) 
        """

        if "stream" in str(dir(self.input_object)):
            if self.required_input_type == 'excel':
                self.required_input_type = 'excel-stream'
                return
            else:
                self.required_input_type = 'stream'
                return

        if (
                self.required_columns == []
                and
                self.text_contains_any or self.text_contains_all
        ):
            self.required_input_type = 'txt'
            return

        if os.path.exists(self.input_object):

            if self.input_object.endswith('.xlsx') or self.input_object.endswith('.xls'):
                self.required_input_type = "excel"

            elif self.input_object.endswith('.csv'):
                self.required_input_type = "csv"

            elif self.input_object.endswith('.txt'):
                self.required_input_type = "txt"
        else:
            self.required_input_type = "string"

    def _check_required_input_type(self):
        allowed_input_types = ['excel', 'csv', 'txt', 'string', 'stream', 'excel-stream']
        if not self.required_input_type: return
        if self.required_input_type not in allowed_input_types:
            raise Exception('Only ".xlsx", ".xls", ".csv", ".txt" files types are accepted!')

    def _parse_excel_stream(self):
        
        self.input_object.seek(0)
        xlobj = pd.ExcelFile(BytesIO(self.input_object.stream.read()))
        sheets = xlobj.sheet_names

        if len(sheets) == 1:
            return pd.read_excel(
                xlobj,
                nrows=self.min_rows_number,
                skiprows=self.header_starts_at
            )

        dfs = {}
        for sheet in sheets:
            if sheet not in self.required_sheets: continue
            dfs[sheet] = pd.read_excel(
                xlobj,
                sheet_name=sheet,
                nrows=self.min_rows_number,
                skiprows=self.header_starts_at
            )
        return dfs

    def _parse_excel(self):

        sheets = pd.ExcelFile(self.input_object).sheet_names

        if len(sheets) == 1:
            return pd.read_excel(
                self.input_object, nrows=self.min_rows_number, skiprows=self.header_starts_at
            )

        dfs = {}
        for sheet in sheets:
            if sheet not in self.required_sheets: continue
            dfs[sheet] = pd.read_excel(
                self.input_object, sheet_name=sheet, nrows=self.min_rows_number, skiprows=self.header_starts_at
            )

        return dfs

    def _parse_data(self):

        if self.required_input_type == "excel-stream":
            return self._parse_excel_stream()

        if self.required_input_type == "excel":
            return self._parse_excel()


        elif self.required_input_type == "csv":
            return pd.read_csv(
                self.input_object, nrows=self.min_rows_number, skiprows=self.header_starts_at
            )

        elif self.required_input_type == "txt":
            with open(self.input_object, 'r', encoding='utf8', errors='ignore') as f:
                text = f.read(self.buffer)
            return text

        elif self.required_input_type == "string":
            return self.input_object

        elif self.required_input_type == "stream":
            self.input_object.seek(0)
            return self.input_object.stream.read(self.buffer).decode('utf8', 'ignore')

        else:
            raise Exception("File contents are badly formated and cannot be read!")

    def validate(self, show_reason=False):
        """ 
            param: show_reason - if true will return a dict with status and message 
        """

        try:

            self._check_required_input_type()
            self._validate_type()

            data = self._parse_data()

            validate_text_contains_all(data, self.text_contains_all)
            validate_text_contains_any(data, self.text_contains_any)
            validate_sheets(self.input_object, self.required_sheets)
            validate_columns(data, self.required_columns, self.required_sheets)
            validate_rows_number(data, self.min_rows_number, self.required_sheets)

            res = {"status": "success", "message": "File validation succeded"}
            return res if show_reason else True

        except Exception as e:
            # log.warning(e)
            # import traceback
            # print(traceback.format_exc())
            res = {"status": "fail", "message": str(e)}
            return res if show_reason else False
