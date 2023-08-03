from libprobe.probe import Probe
from lib.check.idrac import check_idrac
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'idrac': check_idrac,
    }

    probe = Probe("idrac", version, checks)

    probe.start()
