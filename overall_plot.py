import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os
import csv
import numpy as np
from math import cos, sin, acos
from vecgram import semipermeable_r

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
				print(len(S))
	return S, X, PHI, R

def triag_cnstr_1(r1):
	return r1 - r	

def triag_cnstr_2(r1):
	return r1 + r	

def triag_cnstr_3(r1):
	return r - r1

def plot_bds(ax, func, n=5):
	r1s = np.linspace(0, 15., n)
	r2s = np.zeros(n)
	for i, r1 in enumerate(r1s):
		r2s[i] = (func(r1))
	ax.plot(r1s, r2s, 'k--')

def plot_orbit(ax):
	ax.plot([rDcap_min, rDcap_max], [rIcap_min, rIcap_max], 'k--')

if __name__ == '__main__':
    ss, xs, phis, rs = read_data()
    fig, ax = plt.subplots()
    plot_bds(ax, triag_cnstr_3)
    plot_bds(ax, triag_cnstr_2)
    plot_bds(ax, triag_cnstr_1)
    plot_orbit(ax)
	# plot_bds(ax, stable_orbit)
    for s in ss:
    	ax.plot(s[:,0], s[:,2])
	# s = ss[20]
	# print(len(s))
	# ax.plot(s[1:200,0], s[1:200,2], '-o')
	# ax.plot(s[0,0], s[0,2], 'ro')
	# ax.plot(s[-1,0], s[-1,2], 'go')
		# ax.plot(x[:,2], x[:,3])

    # r1set = np.linspace(1., 10., 32)
    # r1s, r2s, cs = [], [], []
    # for r1 in r1set:
    # 	for r2 in np.linspace(r1-r, r1+0.7*r, 25):
    # 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1 and r2 >0:
    # 			c = semipermeable_r(r1, r2)
    # 			r1s.append(r1)
    # 			r2s.append(r2)
    # 			cs.append(c)
    # 	for r2 in np.linspace(r1+.71*r, r1+r, 9):
    # 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1 and r2>0:
    # 			c = semipermeable_r(r1, r2)
    # 			r1s.append(r1)
    # 			r2s.append(r2)
    # 			cs.append(c)

    # xi, yi = np.linspace(3., 7., 12), np.linspace(3., 7., 12)
    # triang = tri.Triangulation(r1s, r2s)
    # interpolator = tri.LinearTriInterpolator(triang, cs)
    # Xi, Yi = np.meshgrid(xi, yi)
    # zi = interpolator(Xi, Yi)

    # # fig, ax = plt.subplots()
    # ax.contour(xi, yi, zi, [.1], linewidths=2, colors='k')

    ax.grid()
    ax.axis('equal')
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])
    plt.show()
