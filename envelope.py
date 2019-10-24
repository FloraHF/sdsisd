import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, sin, cos, acos, pi

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
	vr1, vr2, vtht1, vtht2 = velocity_vec(s[0], s[2], get_phi(s[0], s[2]))
	print('%.5f, %.5f'%(s[0], s[2]))
	return np.array([vr1, vtht1, vr2, vtht2])


def envelope_barrier(r1, r2, tht1=0, dt=0.05):
	dtht = acos((r1**2 + r2**2 - r**2)/(2*r1*r2))
	ss = [np.array([r1, tht1, r2, tht1-dtht])]
	t = 0
	while t < 10:
		s_ = rk4(envelope_dx, ss[-1], dt)
		ss.append(s_)
		# print(s_)
		t += dt
	xs = []
	for s in ss:
		# pritn(s)
		xd = s[0]*cos(s[1])
		yd = s[0]*sin(s[1])
		xi = s[2]*cos(s[3])
		yi = s[2]*sin(s[3])
		x = [xd, yd, xi, yi]
		xs.append(x)
		# print(sqrt((xd - xi)**2 + (yd - yi)**2))
	return np.asarray(xs)
k = .5
r1 = k*(rDcap_max - rDcap_min) + rDcap_min
r2 = k*(rIcap_max - rIcap_min) + rIcap_min
# print(get_phi(r1, r2))
traj = envelope_barrier(r1, r2)

circ = []
for tht in np.linspace(0, 2*pi, 50):
	x = r2*cos(tht)
	y = r2*sin(tht)
	circ.append([x, y])
circ = np.asarray(circ)

fig, ax = plt.subplots()

ax.plot(traj[:,0], traj[:,1])
ax.plot(traj[:,2], traj[:,3])
for i, x in enumerate(traj):
	if i%50 == 0:
		ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
ax.plot(circ[:,0], circ[:,1], '--')
ax.grid()
ax.axis('equal')
plt.show()