import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import sqrt, sin, cos, acos, pi
import time

from RK4 import rk4 
from vecgram import *

def envelope_dx(s):
	phi = get_phi(s[0], s[2])
	vr1, vr2, vtht1, vtht2 = velocity_vec(s[0], s[2], phi, backward=False)
	# print('dr: [%.5f, %.5f]'%(s[0], s[2]), 'dv: [%.5f, %.5f]'%(vr1, vr2), 'phi: [%.5f]'%(phi))
	return np.array([vr1, vtht1, vr2, vtht2])

def envelope_barrier(r1, r2, tht1=0, dt=0.03):
	dtht = acos((r1**2 + r2**2 - r**2)/(2*r1*r2))
	ss = [np.array([r1, tht1, r2, tht1-dtht])]
	# with open('data.csv', 'a') as f:
	# 	f.write(','.join(list(map(str,ss[-1]))) + ',%.5f\n'%get_phi(ss[-1][0], ss[-1][2]))
	t = 0
	while t < 30:
		if abs(ss[-1][0] - ss[-1][2]) >= r - dt*vi:
			break
		s_ = rk4(envelope_dx, ss[-1], dt)
		ss.append(s_)
		t += dt
	xs, phis, rrs = [], [], []
	for s in ss:
		# pritn(s)
		xd = s[0]*cos(s[1])
		yd = s[0]*sin(s[1])
		xi = s[2]*cos(s[3])
		yi = s[2]*sin(s[3])
		x = [xd, yd, xi, yi]
		xs.append(x)
		phis.append(get_phi(s[0], s[2]))
		rrs.append(s[2]/s[0])
		# print(sqrt((xd - xi)**2 + (yd - yi)**2))
	return np.asarray(xs), np.asarray(ss), phis, rrs


k1, k2 = 0.1, 0.05
r1 = k1*(rDcap_max - rDcap_min) + rDcap_min
r2 = k2*(rIcap_max - rIcap_min) + rIcap_min
# print(vi/vd)
# print(get_phi(r1, r2))
traj, ss, phis, rrs = envelope_barrier(r1, r2)

# circ = []
# for tht in np.linspace(0, 2*pi, 50):
# 	x = r2*cos(tht)
# 	y = r2*sin(tht)
# 	circ.append([x, y])
# circ = np.asarray(circ)

fig, ax = plt.subplots()
ax.plot(traj[:,0], traj[:,1])
ax.plot(traj[:,2], traj[:,3])
for i, x in enumerate(traj):
	if i%50 == 0:
		ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
# ax.plot(circ[:,0], circ[:,1], '--')
ax.grid()
ax.axis('equal')
plt.show()

fig, ax = plt.subplots()
ax.plot(range(len(phis)), phis)
ax.grid()
plt.show()

fig, ax = plt.subplots()
ax.plot(range(len(rrs)), rrs)
ax.grid()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(ss[:,0], ss[:,2], ss[:,1]-ss[:,3])
ax.grid()
plt.show()

fig, ax = plt.subplots()
plt.show(block=False)
for s in ss:
	draw_vecgram(fig, ax, s[0], s[2])
	time.sleep(.1)