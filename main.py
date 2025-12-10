from libprobe.probe import Probe
from lib.check.event_log import CheckEventLog
from lib.check.idrac import CheckIdrac
from lib.check.status import CheckStatus
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckEventLog,
        CheckIdrac,
        CheckStatus,
    )

    probe = Probe("idrac", version, checks)

    probe.start()
