from ophyd import Component as Cpt
from ophyd import (PseudoSingle, EpicsMotor, SoftPositioner, Signal)
#from hkl.diffract import E6C  #this works for mu=0
from hkl.diffract import Petra3_p09_eh2
from ophyd.pseudopos import (pseudo_position_argument, real_position_argument)

# Add MuR and MuT to bluesky list of motors and detectors.
muR = EpicsMotor('XF:23ID1-ES{Dif-Ax:MuR}Mtr', name='muR')
# use the line below if very paranoid
# muR = EpicsSignal('XF:23ID1-ES{Dif-Ax:MuR}Mtr.RBV', name='muR')
muT = EpicsMotor('XF:23ID1-ES{Dif-Ax:MuT}Mtr', name='muT')


# TODO: fix upstream!!
class NullMotor(SoftPositioner):
    @property
    def connected(self):
        return True


class Tardis(Petra3_p09_eh2):
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '')
    l = Cpt(PseudoSingle, '')

    theta = Cpt(EpicsMotor, 'XF:23ID1-ES{Dif-Ax:Th}Mtr')
    mu =    Cpt(NullMotor)
    chi =   Cpt(NullMotor)
    phi =   Cpt(NullMotor)
    delta = Cpt(EpicsMotor, 'XF:23ID1-ES{Dif-Ax:Del}Mtr')
    gamma = Cpt(EpicsMotor, 'XF:23ID1-ES{Dif-Ax:Gam}Mtr')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # prime the 3 null-motors with initial values
        # otherwise, position == None --> describe, etc gets borked
        self.chi.move(0.0)
        self.phi.move(0.0)
        self.mu.move(0.0)

        ## This part should address the mu motor(s) problem..
        #def muR_updater(value, **kwargs):
        #    self.mu.move(value)
        #
        #muR.subscribe(muR_updater)

    @pseudo_position_argument
    def set(self, position):
        return super().set([float(_) for _ in position])

tardis = Tardis('', name='tardis')

# re-map Tardis' axis names onto what an E6C expects
name_map = {'mu': 'mu', 'omega': 'theta', 'chi': 'chi', 'phi': 'phi', 'gamma': 'gamma', 'delta': 'delta'}
tardis.calc.physical_axis_names = name_map

tardis.calc.engine.mode = 'lifting detector omega'

# from this point, we can configure the Tardis instance
from hkl.util import Lattice


# Define suitable limits for real axes

# Theta
tardis.calc['theta'].limits = (-181, 181)
tardis.calc['theta'].value = 0
tardis.calc['theta'].fit = True

# Phi, we don't have it. Fix to 0
tardis.calc['phi'].limits = (0, 0)
tardis.calc['phi'].value = 0
tardis.calc['phi'].fit = False

# Chi, we don't have it. Fix to 0
tardis.calc['chi'].limits = (0, 0)
tardis.calc['chi'].value = 0
tardis.calc['chi'].fit = False

# Mu, we don't want it to move except for surface scattering!
tardis.calc['mu'].limits = (0, 0)
tardis.calc['mu'].value = 0
tardis.calc['mu'].fit = True

# Delta
tardis.calc['delta'].limits = (-5, 180)
tardis.calc['delta'].value = 0
tardis.calc['delta'].fit = True

# Gamma
tardis.calc['gamma'].limits = (-5, 180)
tardis.calc['gamma'].value = 0
tardis.calc['gamma'].fit = True



### Example for testing calculations in essentially vertical geometry and mu = 0.0

## lengths are in Angstrom, angles are in degrees, energies in eV
#
## Lattice definition
#lattice = Lattice(a=9.069, b=9.069, c=10.390, alpha=90.0, beta=90.0, gamma=120.0)
#
## add the sample to the calculation engine
#tardis.calc.new_sample('test_sample', lattice=lattice)
#
## set the wavelenght
#tardis.calc.wavelength = 1.61198 # angstroms
## or the energy (pay attention to the conversion factor, necessary to keep lattice spacing in Angstrom!)
#tardis.calc.energy = (pgm.energy.setpoint + offset)/10000

## two, known reflections and UB computation
#r1 = tardis.calc.sample.add_reflection(3, 3, 0,
#                           position=tardis.calc.Position(delta=64.449, theta=25.285, chi=0.0, phi=0.0, mu=0.0, gamma=-0.871))
#
#r2 = tardis.calc.sample.add_reflection(5, 2, 0,
#                           position=tardis.calc.Position(delta=79.712, theta=46.816, chi=0.0, phi=0.0, mu=0.0, gamma=-1.374))
#
#tardis.calc.sample.compute_UB(r1, r2)

## test computed real positions against the table below
## recall, lambda is 1.61198 A now
#
# Experimentally found reflections @ Lambda = 1.61198 A
# (4, 4, 0) = [90.628, 38.373, 0, 0, 0, -1.156]
# (4, 1, 0) = [56.100, 40.220, 0, 0, 0, -1.091]
# @ Lambda = 1.60911
# (6, 0, 0) = [75.900, 61.000, 0, 0, 0, -1.637]
# @ Lambda = 1.60954
# (3, 2, 0) = [53.090, 26.144, 0, 0, 0, -.933]
# (5, 4, 0) = [106.415, 49.900, 0, 0, 0, -1.535]
# (4, 5, 0) = [106.403, 42.586, 0, 0, 0, -1.183]

## Useful basic commands
# tardis.position -> HKL related to the current physical position
# tardis.real_position -> current physical position
# tardis.forward(H,K,L) -> calculates physical motor positions given an HKL
# tardis.move(H,K,L) -> physical motion corresponding to a given HKL
