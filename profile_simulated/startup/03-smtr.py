
from ophyd.epics_motor import EpicsMotor
from ophyd.device import Component as Cpt
from ophyd.signal import EpicsSignal, EpicsSignalRO
from ophyd.utils.epics_pvs import (raise_if_disconnected, AlarmSeverity)
from ophyd.status import (DeviceStatus, wait as status_wait, StatusBase)
from ophyd.positioner import PositionerBase
import time

class KeithleyK2611B_SourceMeter(EpicsMotor):
    _default_read_attrs = ('user_readback', 'user_readback_v', 'user_readback_r', 'user_setpoint','done_signal')
    #read_attrs = ('user_readback', 'user_readback_v', 'user_readback_r', 'user_setpoint','done_signal')
    _default_configuration_attrs = ('velocity',)
    #configuration_attrs = ['velocity']
    user_readback = Cpt(EpicsSignalRO, 'Val:RB-I')
    user_readback_v = Cpt(EpicsSignalRO, 'Val:RB-E')
    user_readback_r = Cpt(EpicsSignalRO, 'Val:RB-R')
    user_setpoint = Cpt(EpicsSignal, 'Val:SP-I_u')
    done_signal = Cpt(EpicsSignalRO, 'DMOV-I')

    velocity = Cpt(EpicsSignal, 'Speed-I')
    #acceleration = Cpt(EpicsSignal, '.ACCL')
    motor_egu = Cpt(EpicsSignal, 'Val:SP-I_u.EGU')

    # commands
    motor_stop = Cpt(EpicsSignal, 'STOP-I')
    """
    def __init__(self, *args, **kwargs):
        _default_read_attrs = ('user_readback', 'user_readback_v', 'user_readback_r', 'user_setpoint','done_signal')
        #read_attrs = ('user_readback', 'user_readback_v', 'user_readback_r', 'user_setpoint','done_signal')
        _default_configuration_attrs = ('velocity',)
        super().__init__(*args, **kwargs)

    """

    def set(self, value):
        #self.connected=True
        st = DeviceStatus(self)
        # these arg sames matter
        #def am_done(old_value, value, **kwargs):
        def am_done(old_value,value, **kwargs):
            #if old_value == 1 and value == 0:
            #print("running",old_value,value,self.done_signal.value)
            #print("done_signal: ",smtr.done_signal.value)
            """
            if self.done_signal.value==1:
                if self.last_value==0:
                    st._finished()
                self.last_value=1
            else:
                self.last_value=0
            """
            if old_value==0 and value==1:
                st._finished()

        self.done_signal.subscribe(am_done, run=False)
        self.user_setpoint.set(value)
        return st


smtr= KeithleyK2611B_SourceMeter('XF:23ID1-ES{K2611:1}', name='smtr')

smtr.read_attrs=smtr._default_read_attrs
smtr.configuration_attrs=smtr._default_configuration_attrs
#smtr.last_value=smtr.done_signal.value




BlueskyMagics.positioners += [smtr]

sd.baseline += [smtr]


