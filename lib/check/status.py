from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['IDRAC-MIB-SMIv2']['statusGroup'], False),
)


def do_rename(state: dict):
    new_state = {}
    if 'statusGroup' in state:
        new_state['statusGroup'] = [
            {k.removeprefix('system').removeprefix('global'): v
             for k, v in item.items()}
            for item in state['statusGroup']]

    return new_state


class CheckStatus(Check):
    key = 'status'
    unchanged_eol = 0

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        return do_rename(state)
