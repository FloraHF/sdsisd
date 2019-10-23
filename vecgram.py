import matplotlib.pyplot as plt
import numpy as np
from math import pi, acos, cos, sin, tan
from scipy.optimize import minimize

from Config import Config
r = Config.CAP_RANGE
R = Config.TAG_RANGE
vd = Config.VD
vi = Config.VI 

def velocity_vec(r1, r2, phi):
	psi = acos(vd/vi*cos(phi))
	psi = -abs(psi)

	alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
	beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))
	v1 = -vd*cos(alpha + phi)
	v2 = -vi*cos(beta + psi)

	return v1, v2

def get_phi(r1, r2):

	def dk_dphi(phi, r1=r1, r2=r2):
		psi = acos(vd/vi*cos(phi))
		psi = -abs(psi)

		alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
		beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))

		dk = - vi*tan(alpha+phi)*sin(psi) + vd*tan(beta+psi)*sin(phi)

		return dk**2

	sol = minimize(dk_dphi, -pi/2)
	return sol.x[0]



# r1, r2 = .8*R, 1.*R
# v1s, v2s = [], []
# for phi in np.linspace(-pi, 0, 40):
# 	v1, v2 = velocity_vec(r1, r2, phi)
# 	v1s.append(v1)
# 	v2s.append(v2)
# v1o, v2o = velocity_vec(r1, r2, get_phi(r1, r2))

# print(v1o, v2o)

# fig, ax = plt.subplots()
# ax.plot(v1s, v2s)
# ax.plot([1.2*v1o, 0], [1.2*v2o, 0], 'r')
# ax.grid()
# ax.axis('equal')
# plt.show()
