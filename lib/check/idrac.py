from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpquery import snmpquery

QUERIES = (
    MIB_INDEX['IDRAC-MIB-SMIv2']['systemStateTableEntry'],
    MIB_INDEX['IDRAC-MIB-SMIv2']['eventLogTableEntry'],
    MIB_INDEX['IDRAC-MIB-SMIv2']['firmwareTableEntry'],
)
ObjectStatusEnum = MIB_INDEX['IDRAC-MIB-SMIv2'][None][
    'ObjectStatusEnum']['syntax']['values']
StateSettingsFlags = MIB_INDEX['IDRAC-MIB-SMIv2'][None][
    'StateSettingsFlags']['syntax']['values']
StatusRedundancyEnum = MIB_INDEX['IDRAC-MIB-SMIv2'][None][
    'StatusRedundancyEnum']['syntax']['values']


def state_details(item: dict, metric: str):
    octet_string = item.pop(metric, None)
    if octet_string is None:
        return
    item[metric] = [
        StateSettingsFlags.get(o, '?')  # fallback needs to be string
        for o in octet_string
    ]


def status_details(item: dict, metric: str):
    octet_string = item.pop(metric, None)
    if octet_string is None:
        return
    item[metric] = [
        StatusRedundancyEnum.get(o, '?')  # fallback needs to be string
        for o in octet_string
    ]


def status_list(item: dict, metric: str):
    octet_string = item.pop(metric, None)
    if octet_string is None:
        return
    item[metric] = [
        ObjectStatusEnum.get(o, '?')  # fallback needs to be string
        for o in octet_string
    ]


def do_rename(state: dict):
    return {
        'systemState': [
            {k.lstrip('systemState'): v for k, v in item}
            for item in state.get('systemStateTableEntry', [])],
        'eventLog': [
            {k.lstrip('eventLog'): v for k, v in item}
            for item in state.get('eventLogTableEntry', [])],

        'firmware': [
            {k.lstrip('firmware'): v for k, v in item}
            for item in state.get('firmwareTableEntry', [])],
    }


async def check_idrac(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    state = await snmpquery(asset, asset_config, check_config, QUERIES)

    for item in state.get('systemStateTableEntry', []):
        state_details(item, 'systemStatePowerUnitStateDetails')
        status_details(item, 'systemStatePowerUnitStatusDetails')
        state_details(item, 'systemStatePowerSupplyStateDetails')
        status_details(item, 'systemStatePowerSupplyStatusDetails')
        state_details(item, 'systemStateVoltageStateDetails')
        status_details(item, 'systemStateVoltageStatusDetails')
        state_details(item, 'systemStateAmperageStateDetails')
        status_details(item, 'systemStateAmperageStatusDetails')
        state_details(item, 'systemStateCoolingUnitStateDetails')
        status_details(item, 'systemStateCoolingUnitStatusDetails')
        state_details(item, 'systemStateTemperatureStateDetails')
        status_details(item, 'systemStateTemperatureStatusDetails')
        state_details(item, 'systemStateMemoryDeviceStateDetails')
        status_details(item, 'systemStateMemoryDeviceStatusDetails')
        state_details(item, 'systemStateChassisIntrusionStateDetails')
        status_details(item, 'systemStateChassisIntrusionStatusDetails')
        state_details(item, 'systemStateChassisIntrusionStateDetails')
        status_details(item, 'systemStateChassisIntrusionStatusDetails')
        state_details(item, 'systemStateTemperatureStatisticsStateDetails')
        status_details(item, 'systemStateTemperatureStatisticsStatusDetails')
        status_list(item, 'systemStateBatteryStatusList')
        status_list(item, 'systemStateCoolingUnitStatusList')
        status_list(item, 'systemStatePowerUnitStatusList')
        status_list(item, 'systemStateProcessorDeviceStatusList')

    return do_rename(state)
