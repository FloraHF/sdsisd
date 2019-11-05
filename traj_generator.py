from envelope import *

# k1s = np.linspace(1.5, 1.6, 5)
# k2s = np.linspace(1.3, 1.4, 5)
# for k1 in k1s:
# 	for k2 in k2s:
# 		r1 = k1*(rDcap_max - rDcap_min) + rDcap_min
# 		r2 = k2*(rIcap_max - rIcap_min) + rIcap_min
# 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
# 			print('new plot')
# 			traj, ss, phis, rrs = envelope_barrier(r1, r2)
# r1s = np.linspace(2., 4., 3)
# for r1 in r1s:
# 	k = (r1 - rDcap_min)/(rDcap_max - rDcap_min)
# 	r2 = 0.9999*k*(rIcap_max - rIcap_min) + rIcap_min
# 	if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
# 		print('new plot')
# 		traj, ss, phis, rrs = envelope_barrier(r1, r2)
r1s = np.linspace(6., 8., 3)
for r1 in r1s:
	for r2 in np.linspace(r1-r, r1+0.7*r, 7):
		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
			print('new plot')
			traj, ss, phis, rrs = envelope_barrier(r1, r2)
	for r2 in np.linspace(r1+.71*r, r1+r, 3):
		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
			print('new plot')
			traj, ss, phis, rrs = envelope_barrier(r1, r2)
# r1 = 6
# for r2 in np.linspace(r1-r, r1+r, 20):
# 	if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
# 			print('new plot')
# 			traj, ss, phis, rrs = envelope_barrier(r1, r2)
