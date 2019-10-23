import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, acos

from RK4 import rk4 
from vecgram import velocity_vec, get_phi
from Config import Config
r = Config.CAP_RANGE
R = Config.TAG_RANGE
vd = Config.VD
vi = Config.VI 
gmm = acos(vd/vi)
rIcap_min, rIcap_max = r/(sin(gmm)), r/(1-cos(gmm))
rDcap_min, rDcap_max = rIcap_min*(vd/vi), rIcap_max*(vd/vi)

def envelope_dx(s):
	v1, v2 = velocity_vec(s[0], s[1], get_phi(s[0], s[1]))
	return np.array([v1, v2])


def envelope_barrier(se, dt=0.05):
	ss = [se]
	t = 0
	while t < 5:
		ss.append(rk4(envelope_dx, ss[-1], dt))
		t += dt
	return np.asarray(ss)





se = np.array([rDcap_min, rIcap_min])
env_traj = envelope_barrier(se)
print(env_traj)