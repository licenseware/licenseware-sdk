# Licenseware SDK

Common utilities for Licenseware.


## Quickstart

Install this package using the following pip command:
```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk.git

```

Install from a specific branch

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk.git@branch_name

```


You can use `git+ssh` if you have ssh keys configured. 
Uninstall with `pip3 uninstall licenseware`.

To see documentation of the package run:
```bash

python3 -m pydoc -p 0 -b

```

It will start a localhost server with the documentation.



Available components:

```py

import licenseware.mongodata as m

from licenseware import (
    Authenticator,
    AppDefinition,
    Quota,
    Uploader, 
    reason_response,
    SchemaApiFactory,
    save_file,
    unzip,
    GeneralValidator, 
    validate_filename,
    StandardReport, 
    StandardReportComponent,
    ReportFilteringComponent,
    RedisService,
    get_mongo_connection,
    notify_status,
    RedisEventDispacher
)

from licenseware.decorators import (
    failsafe,
    authorization_check,
    machine_check,
    header_doc_decorator
)



```