from src.qbsync.mutables.customer_address import CustomerAddressMutable


class CustomerShippingAddressMutable(CustomerAddressMutable):
    default: bool = False

    _data_map: dict = {
        **CustomerAddressMutable.get_data_map(),
        **{
            'DefaultShipTo': 'default',
        }
    }
