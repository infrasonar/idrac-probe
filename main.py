from libprobe.probe import Probe
from lib.check.idrac import CheckIdrac
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckIdrac,
    )

    probe = Probe("idrac", version, checks)

    probe.start()
