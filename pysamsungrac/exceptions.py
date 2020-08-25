class DeviceCommuncationError(Exception):
    """The token we're using is wrong"""

    pass


class DeviceTimeoutError(Exception):
    """The device timed out when trying to communicate"""

    pass

class DeviceMissingToken(Exception):
    """We don't have a token to communicate with"""