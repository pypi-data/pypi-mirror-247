from coinbase.constants import API_PREFIX


def schedule_cfm_sweep(self, usd_amount: str, **kwargs):
    """
    Schedules a sweep of funds from FCM wallet to USD Spot wallet.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/sweeps/schedule"

    data = {"usd_amount": usd_amount}

    if kwargs:
        data.update(kwargs)

    return self.post(endpoint, data=data)


def cancel_cfm_sweep(self, **kwargs):
    """
    Cancel the pending sweep of funds from FCM wallet to USD Spot wallet.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/sweeps"

    data = {}

    if kwargs:
        data.update(kwargs)

    return self.delete(endpoint, data=data)


def get_cfm_sweeps(self, **kwargs):
    """
    Get pending and processing sweeps of funds from FCM wallet to USD Spot wallet.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/sweeps"

    params = {}

    if kwargs:
        params.update(kwargs)

    return self.get(endpoint, params=params)


def get_cfm_positions(self, **kwargs):
    """
    Get a list of positions in CFM products.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/positions"

    params = {}

    if kwargs:
        params.update(kwargs)

    return self.get(endpoint, params=params)


def get_cfm_position(self, product_id: str, **kwargs):
    """
    Get positions for a specific CFM product.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/positions/{product_id}"

    params = {}

    if kwargs:
        params.update(kwargs)

    return self.get(endpoint, params=params)


def get_cfm_balance_summary(self, **kwargs):
    """
    Get a summary of balances for CFM trading.

    #TODO: Add link once documented
    """
    endpoint = f"{API_PREFIX}/cfm/balance_summary"

    params = {}

    if kwargs:
        params.update(kwargs)

    return self.get(endpoint, params=params)
