from spnexus.mutables.base import MutableBase


class InvoiceItemGroupMutable(MutableBase):
    id: str or None = None
    item_group_id: str or None = None
    override_uom_set_id: str or None = None
    description: str or None = None
    unit_of_measure: str or None = None
    quantity: float or None = None
    total_amount: float or None = None
    is_printed: bool or None = None
    items: list or None = None

    _data_map: dict = {
        'TxnLineID': 'id',
        'ItemGroupRef': 'item_group_id',
        'Desc': 'description',
        'Quantity': 'quantity',
        'UnitOfMeasure': 'unit_of_measure',
        'OverrideUOMSetRef': 'override_uom_set_id',
        'IsPrintItemsInGroup': 'is_printed',
        'TotalAmount': 'total_amount',
    }
