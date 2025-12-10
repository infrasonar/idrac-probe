from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['IDRAC-MIB-SMIv2']['statusGroup'], False),
)


class CheckStatus(Check):
    key = 'status'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        items = state.get('statusGroup')
        if not items:
            raise CheckException('missing statusGroup in SNMP result')

        item = items[0]  # single item
        return {
            'status': [{
                'GlobalSystemStatus': item['globalSystemStatus'],
                'GlobalStorageStatus ': item['globalStorageStatus'],
                'LCDStatus': item['systemLCDStatus'],
                'PowerState': item['systemPowerState'],
                'PowerUpTime': item['systemPowerUpTime'],
            }]
        }
