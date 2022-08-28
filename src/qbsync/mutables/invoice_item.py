from spnexus.mutables.base import MutableBase


class InvoiceItemMutable(MutableBase):
    id: str or None = None
    item_id: str or None = None
    override_uom_set_id: str or None = None
    class_id: str or None = None
    inventory_site_id: str or None = None
    inventory_site_location_id: str or None = None
    sales_tax_code_id: str or None = None
    description: str or None = None
    unit_of_measure: str or None = None
    serial_number: str or None = None
    lot_number: str or None = None
    other1: str or None = None
    other2: str or None = None
    quantity: float or None = None
    rate: float or None = None
    rate_percent: float or None = None
    amount: float or None = None
    service_date: str or None = None

    _data_map: dict = {
        'TxnLineID': 'id',
        'ItemRef': 'item_id',
        'Desc': 'description',
        'Quantity': 'quantity',
        'UnitOfMeasure': 'unit_of_measure',
        'OverrideUOMSetRef': 'override_uom_set_id',
        'Rate': 'rate',
        'RatePercent': 'rate_percent',
        'ClassRef': 'class_id',
        'Amount': 'amount',
        'InventorySiteRef': 'inventory_site_id',
        'InventorySiteLocationRef': 'inventory_site_location_id',
        'SerialNumber': 'serial_number',
        'LotNumber': 'lot_number',
        'ServiceDate': 'service_date',
        'SalesTaxCodeRef': 'sales_tax_code_id',
        'Other1': 'other1',
        'Other2': 'other2',
    }
