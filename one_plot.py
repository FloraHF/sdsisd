import matplotlib 
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14) 
from envelope import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit
import matplotlib.tri as tri

if __name__ == '__main__':

	# r1, r2 = 6.5, 6.54 # barrier
	r1, r2 = 6.5, 6.1 # iwin
	# r1, r2 = 6.1, 6.6 # dwin
	traj, ss, phis, rrs, ts = envelope_barrier(r1, r2)

	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1], 'b', alpha=0.8)
	ax.plot(traj[:,2], traj[:,3], color='xkcd:crimson', alpha=0.8)
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'k--')
			ax.plot(x[0], x[1], marker='o', color='b')
			ax.plot(x[2], x[3], marker='o', color='xkcd:crimson')
	# ax.plot(circ[:,0], circ[:,1], 'r-')
	plt.xlabel('x', fontsize=14)
	plt.ylabel('y', fontsize=14)
	ax.grid()
	ax.axis('equal')
	ax.legend(['D', 'I'], fontsize=14)
	plt.savefig('traj.png')
	plt.show()

	########################## phi ###########################
	fig, ax = plt.subplots()
	ax.plot(ts, np.asarray(phis)*180/pi, 'b.-', markevery=5)
	plt.xlabel('time', fontsize=14)
	plt.ylabel(r'$\phi(^\circ)$', fontsize=14)
	ax.grid()
	plt.show()

	########################## flow field ###########################
	# fig, ax = plt.subplots()
	# plot_bds(ax, triag_cnstr_3)
	# plot_bds(ax, triag_cnstr_2)
	# plot_bds(ax, triag_cnstr_1)
	# # plot_bds(ax, stable_orbit)
	# plot_orbit(ax)
	# ax.plot(ss[:,0], ss[:,2], 'bo-', ms=3, markevery=10)
	# 	# ax.plot(x[:,2], x[:,3])
	# cntr = ax.contour(xi, yi, zi, [0])
	# ax.grid()
	# ax.axis('equal')
	# ax.set_xlim([0, 15.])
	# ax.set_ylim([0, 15.])
	# plt.savefig('state.png')
	# plt.show()

	########################## vecgram ###########################
	for i, s in enumerate(ss):
		if i%1 == 0:
			draw_vecgram(s[0], s[2], i)
			# time.sleep(.1)
	plt.show()