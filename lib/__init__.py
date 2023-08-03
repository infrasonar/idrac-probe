import time
from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.mib.syntax_funs import SYNTAX_FUNS


def eventlog_date_name(value):
    '''
    DateName dates are defined in the displayable format
      yyyymmddHHMMSS.uuuuuu+ooo
    where yyyy is the year, mm is the month number, dd is the day of the month,
    HHMMSS are the hours, minutes and seconds, respectively, uuuuuu is the
    number of microseconds, and +ooo is the offset from UTC in minutes. If east
    of UTC, the number is preceded by a plus (+) sign, and if west of UTC, the
    number is preceded by a minus (-) sign.
    For example, Wednesday, May 25, 1994, at 1:30:15 PM EDT
    would be represented as: 19940525133015.000000-300
    Values must be zero-padded if necessary, like "05" in the example above.
    If a value is not supplied for a field, each character in the field
    must be replaced with asterisk ('*') characters.
    src: IDRAC-MIB-SMIv2.mib
    '''
    timetuple = time.strptime(value[:-4].decode(), '%Y%m%d%H%M%S.%f')

    ts = int(time.mktime(timetuple))
    if value[-4] == '+':
        ts -= int(value[-3:]) * 60
    else:
        ts += int(value[-3:]) * 60
    return ts


SYNTAX_FUNS['hp_eventlog_date_name'] = eventlog_date_name

# patch the syntax function because we need the raw bytes for these metrics
MIB_INDEX[MIB_INDEX['IDRAC-MIB-SMIv2']['eventLogDateName']]['syntax'] = {
    'tp': 'CUSTOM', 'func': 'hp_eventlog_date_name',
}
