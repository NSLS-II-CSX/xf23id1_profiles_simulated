# Modified in order to create a safe simulation environment 2018/01/30

# added to suppress hkl import warning
import gi
gi.require_version("Hkl", "5.0")

from csx1.startup import *

#from IPython import get_ipython
#import nslsii
#
#nslsii.configure_olog(get_ipython().user_ns)
