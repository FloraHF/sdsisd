import matplotlib.pyplot as plt
import numpy as np
from math import pi, sqrt, acos, cos, sin, tan
from scipy.optimize import minimize, minimize_scalar

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
#	def dk_dphi(phi, r1=r1, r2=r2):
#		psi = acos(vd/vi*cos(phi))
#		psi = -abs(psi)
#
#		alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
#		beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))
#
#		dk = - vi*tan(alpha+phi)*sin(psi) + vd*tan(beta+psi)*sin(phi)
#
#		return dk**2
    def get_v(phi, r1, r2):
        psi = acos(vd/vi*cos(phi))
        psi = -abs(psi)
        alpha = acos((r**2 + r1**2 - r2**2)/(2*r1*r))
        beta = pi - acos((r**2 + r2**2 - r1**2)/(2*r2*r))
        
        v1 = -vd*cos(alpha + phi)
        v2 = -vi*cos(beta + psi)
        v = sqrt(v1**2 + v2**2)
        v1, v2 = v1/v, v2/v
#        print(v1**2 + v2**2)
        
        dv1 = vd*sin(alpha + phi)
        dv2 = vd*sin(beta + psi)*sin(phi)/sin(psi)
        dv = sqrt(dv1**2 + dv2**2)
        dv1, dv2 = dv1/dv, dv2/dv

        return v1, v2, dv1, dv2

    def err_u(phi, r1=r1, r2=r2):
    	v1, v2, dv1, dv2 = get_v(phi, r1, r2)
    	return (v1 - dv1)**2 + (v2 - dv2)**2

    def err_l(phi, r1=r1, r2=r2):
    	v1, v2, dv1, dv2 = get_v(phi, r1, r2)
    	return (v1 + dv1)**2 + (v2 + dv2)**2

    sol = minimize(err_u, 0)
    if sol.x > 0:
    	sol = minimize(err_l, 0)
    # sol = minimize(err_l, 0)
    return sol.x

def draw_vecgram(fig, ax, r1, r2):
	v1s, v2s = [], []
	n = 50
	for phi in np.linspace(-pi, 0.9*pi, n):
		s = velocity_vec(r1, r2, phi, backward=False)
		v1s.append(s[0])
		v2s.append(s[1])
	vphi0 = velocity_vec(r1, r2, 0, backward=False)

	phi_opt = get_phi(r1, r2)
	so = velocity_vec(r1, r2, phi_opt, backward=False)

	# fig, ax = plt.subplots()
	ax.clear()
	ax.plot(v1s, v2s)
	ax.plot(v1s[:3], v2s[:3], 'r.')
	ax.plot(v1s[int(n/2-1):int(n/2+2)], v2s[int(n/2-1):int(n/2+2)], 'y.')
	ax.plot(vphi0[0], vphi0[1], 'k.')
	ax.plot([1.2*so[0], 0], [1.2*so[1], 0], 'r')
	ax.grid()
	plt.title('phi=%.3f, r=[%.3f, %.3f], r1/r2=%.3f'%(phi_opt, r1, r2, r2/r1))
	fig.canvas.draw()
	# ax.grid()
	# # ax.axis('equal')
	# plt.show(block=False)