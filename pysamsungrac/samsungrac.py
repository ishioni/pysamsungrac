import json
import logging

from pysamsungrac.network import SamsungRacConnection as Conn
from pysamsungrac.exceptions import DeviceMissingToken
_LOGGER = logging.getLogger(__name__)


class SamsungRac:
    """Class representing a physical device, it's state and properties.

        Devices must have a token to authenticate with

        Once a device is bound occasionally call `update` to request and update state from
        the HVAC, as it is possible that it changes state from other sources.

        Attributes:
            name: Current name of the HVAC device
            description: Usually the model number of the external unit
            uuid: The unique identifier on the samsung cloud
            power: A string indicating if the unit is on or off
            temperature unit: An string indicating temperature units
            target_temperature: The target temperature
            current_temperature: The current temperature as reported by the indoor unit
            max_temp: An int indicating maximum supported temperature
            min_temp: An int indicating maximum supported temperature
            hvac_mode: The current selected operating mode
            hvac_modes: Supported hvac modes
            fan_speed: int indicating current fan speed
            fan_speeds: int indicating supported fan speeds
            swing_mode: current swing mode
            swing_modes: supported swing modes
            preset_mode: current preset mode
            preset_modes: supported preset modes
            sleep_timer: int for setting sleep time for the Sleep preset. Setting this automatically engages Sleep preset
            purifier: Indicates of the ionizer is on or off
            filter_time: Indicates the time since last filter alarm reset
            filter_alarm_time: Number of hours for the filter alarm to trigger
            filter_alarm: Status of the filter alarm
            autoclean: Start autoclean on the indoor unit
            cool_capability: Cooling power expressed in kW as reported by the outdoor unit
            warm_capability: Heating power expressed in kW as reported by the outdoor unit
            options: a dict of untranslated options of the device
        """

    ENDPOINTS = {
        'Operation': '/devices/0',
        'Wind': '/devices/0/wind',
        'Temperature': '/devices/0/temperatures/0',
        'Modes': '/devices/0/mode',
        'Energy': '/files/usage.db'
    }

    SWING_MODES = [
        'Fix',
        'Up_And_Low',
        'Left_And_Right',
        'All'
    ]

    COMODE_MODES = [
        'Off',
        'Sleep',  # Good Sleep
        '2Step',
        'Speed',  # Fast Turbo
        'Comfort',
        'Quiet',
        'Smart'  # Single User
    ]

    def __init__(self, address, token=None):
        self._address = address
        self._token = token
        self._control = Conn(address, token)
        self._name = None
        self._description = None
        self._uuid = None
        self._state = {}

    async def _set(self, endpoint, command):
        await self._control.put(
            command=command,
            resource=self.ENDPOINTS[endpoint],
        )

    async def update(self):
        if not self._token:
            raise DeviceMissingToken

        _LOGGER.debug("Updating device infor for (%s)", str(self._address))

        ac_data = json.loads(await self._control.get(resource=self.ENDPOINTS['Operation']))['Device']

        self._name = ac_data['name']
        self._description = ac_data['description']
        self._uuid = ac_data['uuid']
        self._state['power'] = ac_data['Operation']['power']
        self._state['temperature_unit'] = ac_data['Temperatures'][0]['unit']
        self._state['current_temperature'] = ac_data['Temperatures'][0]['current']
        self._state['target_temperature'] = ac_data['Temperatures'][0]['desired']
        self._state['max_temp'] = ac_data['Temperatures'][0]['maximum']
        self._state['min_temp'] = ac_data['Temperatures'][0]['minimum']
        self._state['hvac_mode'] = str(ac_data['Mode']['modes']).strip("'[]")
        self._state['hvac_modes'] = ac_data['Mode']['supportedModes']
        self._state['fan_speed'] = ac_data['Wind']['speedLevel']
        self._state['fan_speeds'] = ac_data['Wind']['maxSpeedLevel']
        self._state['swing_mode'] = ac_data['Wind']['direction']
        self._state['options'] = {x.split('_')[0]: x.split('_')[1] for x in ac_data['Mode']['options']}

    def get_attribute(self, attribute):
        return self._state[attribute]

    def get_option(self, option):
        return self._state['options'][option]

    async def set_power(self, state: str):
        data = {'Operation': {'power': state}}
        return await self._set("Operation", data)

    async def set_hvac_mode(self, mode: str):
        data = {'modes': [mode]}
        return await self._set('Modes', data)

    async def set_target_temperature(self, temperature: int):
        data = {'desired': int(temperature)}
        return await self._set('Temperature', data)

    async def set_fan_speed(self, speed: int):
        data = {'speedLevel': int(speed)}
        return await self._set('Wind', data)

    async def set_swing_mode(self, mode: str):
        data = {'direction': mode}
        return await self._set('Wind', data)

    async def set_option(self, option: str, value: str):
        data = {'options': [f'{option}_{value}']}
        return await self._set('Modes', data)

    async def set_preset(self, value: str):
        return await self.set_option('Comode', value)

    async def set_sleep_timer(self, value: int):
        return await self.set_option('Sleep', str(value))

    async def set_purifier(self, value: str):
        return await self.set_option('Spi', value)

    async def set_beep(self, value:str):
        if value == 'On':
            return await self.set_option('Volume', '100')
        else:
            return await self.set_option('Volume', 'Mute')

    async def set_filter_alarm_time(self, value):
        return await self.set_option('FilterAlarmTime', value)

    async def reset_filter(self):
        # Not implemented yet
        pass

    async def set_clean(self, value):
        return await self.set_option('Autoclean', value)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def power(self) -> str:
        return self.get_attribute('power')

    @property
    def temperature_unit(self) -> str:
        return self.get_attribute('temperature_unit')

    @property
    def current_temperature(self) -> int:
        return int(self.get_attribute('current_temperature'))

    @property
    def target_temperature(self) -> int:
        return int(self.get_attribute('target_temperature'))

    @property
    def max_temp(self) -> int:
        return int(self.get_attribute('max_temp'))

    @property
    def min_temp(self) -> int:
        return int(self.get_attribute('min_temp'))

    @property
    def hvac_mode(self) -> str:
        return self.get_attribute('hvac_mode')

    @property
    def hvac_modes(self) -> list:
        modes = self.get_attribute('hvac_modes')
        # The API lies
        modes.append('Heat')
        return modes

    @property
    def fan_speed(self) -> int:
        return int(self.get_attribute('fan_speed'))

    @property
    def fan_speeds(self) -> list:
        return list(range(self.get_attribute('fan_speeds') + 1))

    @property
    def swing_mode(self) -> str:
        return self.get_attribute('swing_mode')

    @property
    def swing_modes(self) -> list:
        return self.SWING_MODES

    @property
    def preset_mode(self) -> str:
        return self.get_option('Comode')

    @property
    def preset_modes(self) -> list:
        return self.COMODE_MODES

    @property
    def sleep_timer(self) -> int:
        return int(self.get_option('Sleep'))

    @property
    def purifier(self) -> str:
        return self.get_option('Spi')

    @property
    def filter_time(self) -> float:
        return float(self.get_option('FilterTime')) / 10

    @property
    def filter_alarm_time(self) -> int:
        return int(self.get_option('FilterAlarmTime'))

    @property
    def filter_alarm(self) -> int:
        return self.get_option('FilterCleanAlarm')

    @property
    def autoclean(self) -> str:
        return self.get_option('Autoclean')

    @property
    def beep(self) -> str:
        if self.get_option('Volume') == 'Mute':
            return "Off"
        else:
            return "On"

    @property
    def cool_capability(self) -> float:
        return float(self.get_option('CoolCapa')) / 10

    @property
    def warm_capability(self) -> float:
        return float(self.get_option('WarmCapa')) / 10

    @property
    def options(self) -> dict:
        return self._state['options']
