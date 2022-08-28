from spnexus.mutables.base import MutableBase


class CustomerAddressMutable(MutableBase):
    id: str or None = None
    parent_id: str or None = None
    line1: str or None = None
    line2: str or None = None
    line3: str or None = None
    line4: str or None = None
    line5: str or None = None
    city: str or None = None
    state: str or None = None
    postal_code: str or None = None
    country: str or None = None
    notes: str or None = None

    _data_map: dict = {
        '%auto_id': 'id',
        '%parent_id': 'parent_id',
        'Addr1': 'line1',
        'Addr2': 'line2',
        'Addr3': 'line3',
        'Addr4': 'line4',
        'Addr5': 'line5',
        'City': 'city',
        'State': 'state',
        'PostalCode': 'postal_code',
        'Country': 'country',
        'Note': 'notes',
    }
