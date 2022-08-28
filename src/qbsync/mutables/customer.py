from spnexus.mutables.base import MutableBase
from src.qbsync.mutables.customer_address import CustomerAddressMutable


class CustomerMutable(MutableBase):
    id: str or None = None
    parent_id: str or None = None
    org_name: str or None = None
    full_name: str or None = None
    salutation: str or None = None
    first_name: str or None = None
    middle_name: str or None = None
    last_name: str or None = None
    job_title: str or None = None
    billing_address: CustomerAddressMutable or None = None
    shipping_address: CustomerAddressMutable or None = None
    shipping_addresses: list or None = None
    phone: str or None = None
    alt_phone: str or None = None
    fax: str or None = None
    email: str or None = None
    email_cc: str or None = None
    contact: str or None = None
    alt_contact: str or None = None

    _data_map: dict = {
        'ListID': 'id',
        'ParentRef': 'parent_id',
        'CompanyName': 'org_name',
        'FullName': 'full_name',
        'Salutation': 'salutation',
        'FirstName': 'first_name',
        'MiddleName': 'middle_name',
        'LastName': 'last_name',
        'JobTitle': 'job_title',
        'Phone': 'phone',
        'AltPhone': 'alt_phone',
        'Fax': 'fax',
        'Email': 'email',
        'Cc': 'email_cc',
        'Contact': 'contact',
        'AltContact': 'alt_contact',
    }
