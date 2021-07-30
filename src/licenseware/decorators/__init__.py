"""

Useful decoratators.

from licenseware.decorators import (
    failsafe,
    authorization_check,
    machine_check,
    header_doc_decorator,
    namespace
)

or 

from licenseware import decorators


"""


from .auth_decorators import authorization_check, machine_check, authenticated_machine
from .failsafe_decorator import failsafe
from .doc_header_decorator import header_doc_decorator
from .namespace_decorator import namespace