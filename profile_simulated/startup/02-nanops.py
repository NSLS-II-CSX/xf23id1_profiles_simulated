from ophyd.epics_motor import EpicsMotor
from ophyd.device import Component as Cpt
from ophyd.signal import EpicsSignal
from ophyd import MotorBundle
from epics import caget,caput


class NanoMotor(EpicsMotor):
    _default_configuration_attrs = (
        EpicsMotor._default_configuration_attrs +
        ('dly', 'rdbd', 'rmod', 'cnen', 'pcof', 'icof'))
    user_setpoint = Cpt(EpicsSignal, 'PA_sm')
    dly = Cpt(EpicsSignal, '.DLY')
    rdbd = Cpt(EpicsSignal, '.RDBD')
    rmod = Cpt(EpicsSignal, '.RMOD')
    cnen = Cpt(EpicsSignal, '.CNEN')
    pcof = Cpt(EpicsSignal, '.PCOF')
    icof = Cpt(EpicsSignal, '.ICOF')

class NanoBundle(MotorBundle):
    tx = Cpt(NanoMotor, 'TopX}Mtr')
    ty = Cpt(NanoMotor, 'TopY}Mtr')
    tz = Cpt(NanoMotor, 'TopZ}Mtr')
    bx = Cpt(NanoMotor, 'BtmX}Mtr')
    by = Cpt(NanoMotor, 'BtmY}Mtr')
    bz = Cpt(NanoMotor, 'BtmZ}Mtr')

nanop = NanoBundle('XF:23ID1-ES{Dif:Nano-Ax:', name='nanop')


# Velocity (tested 0.5, 0.1, 0.05, 0.01)

# this was 0.30 but AB tried scanning with larger step
# size and had difficulty in that bluesky will never trigger the
# cube_beam because bsui is waiting on this to move??

# Settling time (tested 0.1 - 0.3)
temp_settle_time = 0.2

_base_nano_setting = {'velocity': .10,
                      'dly': temp_settle_time,
                      'rdbd': 1e-5,
                      'rmod': 1,
                      'cnen': 1,
                      'pcof': 0.1,
                      'icof': 0.010}

for nn in nanop.component_names:
    getattr(nanop, nn).configure(_base_nano_setting)

BlueskyMagics.positioners += [getattr(nanop, nn) for nn in nanop.component_names]

#sd.baseline += [getattr(nanop, nn) for nn in nanop.component_names]
sd.baseline += [nanop]
