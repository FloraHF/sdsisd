from envelope import *

r0s = np.linspace(r, 7*r, 13)
for r0 in r0s:
	r1l, r1u = (r0 - r)/2, (r0 + r)/2
	for r1 in np.linspace(r1l+0.1, r1u-0.1, 13):
		r2 = r0 - r1
		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
			print('new plot')
			traj, ss, phis, rrs = envelope_barrier(r1, r2)		

