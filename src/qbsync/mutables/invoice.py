from spnexus.mutables.base import MutableBase
from src.qbsync.mutables.customer_address import CustomerAddressMutable


class InvoiceMutable(MutableBase):
    id: str or None = None
    external_guid: str or None = None
    parent_id: str or None = None
    class_id: str or None = None
    ar_account_id: str or None = None
    template_id: str or None = None
    terms_id: str or None = None
    sales_rep_id: str or None = None
    shipping_method_id: str or None = None
    item_sales_tax_id: str or None = None
    currency_id: str or None = None
    customer_message_id: str or None = None
    customer_sales_tax_code_id: str or None = None
    edit_sequence: str or None = None
    transaction_number: str or None = None
    reference_number: str or None = None
    po_number: str or None = None
    freight_on_board: str or None = None
    memo: str or None = None
    other: str or None = None
    sub_total: float or None = None
    sales_tax_percentage: float or None = None
    sales_tax_total: float or None = None
    applied_amount: float or None = None
    balance_remaining: float or None = None
    balance_remaining_home_currency: float or None = None
    exchange_rate: float or None = None
    suggested_discount_amount: float or None = None
    created_date: str or None = None
    modified_date: str or None = None
    transaction_date: str or None = None
    due_date: str or None = None
    ship_date: str or None = None
    suggested_discount_date: str or None = None
    is_pending: bool or None = None
    is_finance_charge: bool or None = None
    is_paid: bool or None = None
    is_to_print: bool or None = None
    is_to_email: bool or None = None
    is_tax_included: bool or None = None
    billing_address: CustomerAddressMutable or None = None
    shipping_address: CustomerAddressMutable or None = None
    items: list or None = None

    _data_map: dict = {
        'TxnID': 'id',
        'TimeCreated': 'created_date',
        'TimeModified': 'modified_date',
        'EditSequence': 'edit_sequence',
        'TxnNumber': 'transaction_number',
        'CustomerRef': 'parent_id',
        'ClassRef': 'class_id',
        'ARAccountRef': 'ar_account_id',
        'TemplateRef': 'template_id',
        'TxnDate': 'transaction_date',
        'RefNumber': 'reference_number',
        'IsPending': 'is_pending',
        'IsFinanceCharge': 'is_finance_charge',
        'PONumber': 'po_number',
        'TermsRef': 'terms_id',
        'DueDate': 'due_date',
        'SalesRepRef': 'sales_rep_id',
        'FOB': 'freight_on_board',
        'ShipDate': 'ship_date',
        'ShipMethodRef': 'shipping_method_id',
        'Subtotal': 'sub_total',
        'ItemSalesTaxRef': 'item_sales_tax_id',
        'SalesTaxPercentage': 'sales_tax_percentage',
        'SalesTaxTotal': 'sales_tax_total',
        'AppliedAmount': 'applied_amount',
        'BalanceRemaining': 'balance_remaining',
        'CurrencyRef': 'currency_id',
        'ExchangeRate': 'exchange_rate',
        'BalanceRemainingInHomeCurrency': 'balance_remaining_home_currency',
        'Memo': 'memo',
        'IsPaid': 'is_paid',
        'CustomerMsgRef': 'customer_message_id',
        'IsToBePrinted': 'is_to_print',
        'IsToBeEmail': 'is_to_email',
        'IsTaxIncluded': 'is_tax_included',
        'CustomerSalesTaxCodeRef': 'customer_sales_tax_code_id',
        'SuggestedDiscountAmount': 'suggested_discount_amount',
        'SuggestedDiscountDate': 'suggested_discount_date',
        'Other': 'other',
        'ExternalGUID': 'external_guid',
    }
