import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os
import csv
import numpy as np
from math import cos, sin, acos, sqrt
from vecgram import semipermeable_r, velocity_vec, get_phi, get_phi_max

from Config import Config
r = Config.CAP_RANGE
R = Config.TAG_RANGE
vd = Config.VD
vi = Config.VI 
gmm = acos(vd/vi)
rIcap_min, rIcap_max = r/(sin(gmm)), r/(1-cos(gmm))
rDcap_min, rDcap_max = rIcap_min*(vd/vi), rIcap_max*(vd/vi)

def save_traj_plot(traj, dirc):
	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1])
	ax.plot(traj[:,2], traj[:,3])
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
	# ax.plot(circ[:,0], circ[:,1], '--')
	ax.grid()
	ax.axis('equal')
	plt.savefig(dirc)
	plt.close()

def read_data():
	S, X, PHI, R = [], [], [], []
	for root, dirs, files in os.walk('res'):
		for dname in dirs:
			# print(dname)
			if os.path.exists('res/'+dname+'/data.csv'):
				# print('exists')
				with open('res/'+dname+'/data.csv') as f:
					# print('reading')
					reader = csv.reader(f, delimiter=',')
					ss, xs, phis, ratios = [], [], [], []
					for row in reader:
						# print(row)
						s = list(map(float, row))
						ss.append(s[:4])
						phis.append(s[-1])
						xd = s[0]*cos(s[1])
						yd = s[0]*sin(s[1])
						xi = s[2]*cos(s[3])
						yi = s[2]*sin(s[3])
						x = [xd, yd, xi, yi]
						xs.append(x)
						ratios.append(s[2]/s[0])
				save_traj_plot(np.asarray(xs), 'res/'+dname+'/traj.png')					
				S.append(np.asarray(ss))
				X.append(np.asarray(xs))
				PHI.append(np.asarray(phis))
				R.append(np.asarray(ratios))
				# print(len(S))
	return S, X, PHI, R

def triag_cnstr_1(r1):
	return r1 - r	

def triag_cnstr_2(r1):
	return r1 + r	

def triag_cnstr_3(r1):
	return r - r1

def plot_bds(ax, func, n=5):
	r1s = np.linspace(0, 10., n)
	r2s = np.zeros(n)
	for i, r1 in enumerate(r1s):
		r2s[i] = (func(r1))
	ax.plot(r1s, r2s, 'k--')

def plot_orbit(ax):
	ax.plot([rDcap_min, rDcap_max], [rIcap_min, rIcap_max], 'k--')

if __name__ == '__main__':

	# print('generating velocity contour')
	# r1s, r2s, vs = [], [], []
	# r0s = np.linspace(0.2*r, 5*r, 66)
	# for r0 in r0s:
	# 	r1l, r1u = (r0 - r)/2, (r0 + r)/2
	# 	for r1 in np.linspace(r1l+0.06, r1u-0.06, 66):
	# 		r2 = r0 - r1
	# 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
	# 			r1s.append(r1)
	# 			r2s.append(r2)	
	# 		for r2 in np.linspace(r1/vd*vi-0.1, r1/vd*vi+0.1, 5):
	# 			if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
	# 				r1s.append(r1)
	# 				r2s.append(r2)		

	# for r1, r2 in zip(r1s, r2s):
	# 	vr1, vr2, vtht1, vtht2 = velocity_vec(r1, r2, get_phi(r1, r2))
	# 	vs.append(vr1)
	
	# r1s = np.asarray(r1s)
	# r2s = np.asarray(r2s)
	# vs = np.asarray(vs)

	# xi, yi = np.linspace(0., 8., 39), np.linspace(0., 8., 39)
	# triang = tri.Triangulation(r1s, r2s)
	# interpolator = tri.LinearTriInterpolator(triang, vs)
	# Xi, Yi = np.meshgrid(xi, yi)
	# zi = interpolator(Xi, Yi)

	#################### get controur for phi_max=0 ##############
	print('getting switch line')
	r1s, r2s, phis = [], [], []
	r0s = np.linspace(0.2*r, 8*r, 66)
	for r0 in r0s:
		r1l, r1u = (r0 - r)/2, (r0 + r)/2
		for r1 in np.linspace(r1l+0.06, r1u-0.06, 66):
			r2 = r0 - r1
			if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
				r1s.append(r1)
				r2s.append(r2)
				phis.append(get_phi_max(r1, r2)[0])	
    	# 	for r2 in np.linspace(r1/vd*vi-0.1, r1/vd*vi+0.1, 5):
    	# 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
					# r1s.append(r1)
					# r2s.append(r2)		
    	
	r1s = np.asarray(r1s)
	r2s = np.asarray(r2s)
	phis = np.asarray(phis)

	xi, yi = np.linspace(1., 10., 50), np.linspace(1., 10., 50)
	triang = tri.Triangulation(r1s, r2s)
	interpolator = tri.LinearTriInterpolator(triang, phis)
	Xi, Yi = np.meshgrid(xi, yi)
	zi = interpolator(Xi, Yi)

	print('reading trajectory')
	ss, xs, phis, rs = read_data()
	fig, ax = plt.subplots()
	plot_bds(ax, triag_cnstr_3)
	plot_bds(ax, triag_cnstr_2)
	plot_bds(ax, triag_cnstr_1)
	plot_orbit(ax)
	# ax.contour(xi, yi, zi, levels=14, linewidths=2, colors='k')
	cntr = ax.contour(xi, yi, zi, [0])

	# fig.colorbar(cntr, ax=ax)

	for i, s in enumerate(ss):
		# ax.plot(s[:,0], s[:,2], 'bo-', ms=3, markevery=10)
		if i%5 == 0:
			ax.plot(s[:,0], s[:,2], 'b')

	ax.grid()
	ax.axis('equal')
	ax.set_xlim([0, 10])
	ax.set_ylim([0, 10])
	plt.show()
