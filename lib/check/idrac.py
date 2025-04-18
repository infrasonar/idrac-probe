from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['IDRAC-MIB-SMIv2']['systemStateTableEntry'], True),
    (MIB_INDEX['IDRAC-MIB-SMIv2']['eventLogTableEntry'], True),
    (MIB_INDEX['IDRAC-MIB-SMIv2']['firmwareTableEntry'], True),
)


def do_rename(state: dict):
    new_state = {}
    if 'systemStateTableEntry' in state:
        new_state['systemState'] = [
            {k.removeprefix('systemState'): v for k, v in item.items()}
            for item in state['systemStateTableEntry']]
    else:
        raise CheckException('missing systemStateTableEntry in SNMP result')

    if 'eventLogTableEntry' in state:
        new_state['eventLog'] = [
            {k.removeprefix('eventLog'): v for k, v in item.items()}
            for item in state['eventLogTableEntry']]

    if 'firmwareTableEntry' in state:
        new_state['firmware'] = [
            {k.removeprefix('firmware'): v for k, v in item.items()}
            for item in state['firmwareTableEntry']]
    return new_state


async def check_idrac(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)

    for item in state.get('systemStateTableEntry', []):
        item.pop('systemStatePowerUnitStateDetails', None)
        item.pop('systemStatePowerUnitStatusDetails', None)
        item.pop('systemStatePowerSupplyStateDetails', None)
        item.pop('systemStatePowerSupplyStatusDetails', None)
        item.pop('systemStateVoltageStateDetails', None)
        item.pop('systemStateVoltageStatusDetails', None)
        item.pop('systemStateAmperageStateDetails', None)
        item.pop('systemStateAmperageStatusDetails', None)
        item.pop('systemStateCoolingDeviceStateDetails', None)
        item.pop('systemStateCoolingDeviceStatusDetails', None)
        item.pop('systemStateCoolingUnitStateDetails', None)
        item.pop('systemStateCoolingUnitStatusDetails', None)
        item.pop('systemStateTemperatureStateDetails', None)
        item.pop('systemStateTemperatureStatusDetails', None)
        item.pop('systemStateMemoryDeviceStateDetails', None)
        item.pop('systemStateMemoryDeviceStatusDetails', None)
        item.pop('systemStateChassisIntrusionStateDetails', None)
        item.pop('systemStateChassisIntrusionStatusDetails', None)
        item.pop('systemStateTemperatureStatisticsStateDetails', None)
        item.pop('systemStateTemperatureStatisticsStatusDetails', None)
        item.pop('systemStatePowerUnitStatusList', None)
        item.pop('systemStateCoolingUnitStatusList', None)
        item.pop('systemStateProcessorDeviceStatusList', None)
        item.pop('systemStateBatteryStatusList', None)

    return do_rename(state)
