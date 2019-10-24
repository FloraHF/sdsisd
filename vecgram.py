import matplotlib.pyplot as plt
import numpy as np
from math import pi, acos, cos, sin, tan
from scipy.optimize import minimize

from Config import Config
r = Config.CAP_RANGE
R = Config.TAG_RANGE
vd = Config.VD
vi = Config.VI 
gmm = acos(vd/vi)
rIcap_min, rIcap_max = r/(sin(gmm)), r/(1-cos(gmm))
rDcap_min, rDcap_max = rIcap_min*(vd/vi), rIcap_max*(vd/vi)

def velocity_vec(r1, r2, phi, backward=True):
	psi = acos(vd/vi*cos(phi))
	psi = -abs(psi)

	alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
	beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))
	if backward:
		vr1 = vd*cos(alpha + phi)
		vr2 = vi*cos(beta + psi)
		vtht1 = vd*sin(alpha + phi)/r1
		vtht2 = vi*sin(beta + psi)/r2		
	else:
		vr1 = -vd*cos(alpha + phi)
		vr2 = -vi*cos(beta + psi)
		vtht1 = -vd*sin(alpha + phi)/r1
		vtht2 = -vi*sin(beta + psi)/r2

	return vr1, vr2, vtht1, vtht2

def get_phi(r1, r2):

	def dk_dphi(phi, r1=r1, r2=r2):
		psi = acos(vd/vi*cos(phi))
		psi = -abs(psi)

		alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
		beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))

		dk = - vi*tan(alpha+phi)*sin(psi) + vd*tan(beta+psi)*sin(phi)

		return dk**2

	sol = minimize(dk_dphi, -pi/2)
	return sol.x


# k1, k2 = 0.5, 0.6
# r1 = k1*(rDcap_max - rDcap_min) + rDcap_min
# r2 = k2*(rIcap_max - rIcap_min) + rIcap_min
r1, r2 = 8.33016, 10.32174
v1s, v2s = [], []
n = 50
for phi in np.linspace(-pi, 0.9*pi, n):
	s = velocity_vec(r1, r2, phi, backward=False)
	v1s.append(s[0])
	v2s.append(s[1])
so = velocity_vec(r1, r2, get_phi(r1, r2), backward=False)

fig, ax = plt.subplots()
ax.plot(v1s, v2s)
ax.plot(v1s[:3], v2s[:3], 'r.')
ax.plot(v1s[int(n/2-1):int(n/2+2)], v2s[int(n/2-1):int(n/2+2)], 'y.')
ax.plot([1.2*so[0], 0], [1.2*so[1], 0], 'r')
ax.grid()
# ax.axis('equal')
plt.show()