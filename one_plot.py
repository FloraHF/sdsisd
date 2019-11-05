from envelope import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit
import matplotlib.tri as tri

if __name__ == '__main__':
	r1, r2 = 6.1, 4.6
	# fig, ax = plt.subplots()
	# plt.show(block=False)
	# draw_vecgram(fig, ax, r1, r2)
	# plt.show()
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

	R = 5
	circ = []
	for a in np.linspace(0, 2*pi, 50):
		x = r*cos(a)
		y = r*sin(a)
		circ.append([x, y])
	circ = np.asarray(circ)
	r1, r2 = 6.1, 6.6
	traj, ss, phis, rrs = envelope_barrier(r1, r2)

	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1])
	ax.plot(traj[:,2], traj[:,3])
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
	ax.plot(circ[:,0], circ[:,1], 'r-')
	ax.grid()
	ax.axis('equal')
	plt.savefig('traj.png')
	plt.show()



	fig, ax = plt.subplots()
	plot_bds(ax, triag_cnstr_3)
	plot_bds(ax, triag_cnstr_2)
	plot_bds(ax, triag_cnstr_1)
	# plot_bds(ax, stable_orbit)
	plot_orbit(ax)
	ax.plot(ss[:,0], ss[:,2], 'bo-', ms=3, markevery=10)
		# ax.plot(x[:,2], x[:,3])
	cntr = ax.contour(xi, yi, zi, [0])
	ax.grid()
	ax.axis('equal')
	ax.set_xlim([0, 15.])
	ax.set_ylim([0, 15.])
	plt.savefig('state.png')
	plt.show()


	fig, ax = plt.subplots()
	plt.show(block=False)
	for i, s in enumerate(ss):
		draw_vecgram(fig, ax, s[0], s[2])
		time.sleep(.1)
	plt.show()