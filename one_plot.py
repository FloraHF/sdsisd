from envelope import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit

if __name__ == '__main__':
	r1, r2 = 6., 6.5
	# fig, ax = plt.subplots()
	# plt.show(block=False)
	# draw_vecgram(fig, ax, r1, r2)
	# plt.show()

	traj, ss, phis, rrs = envelope_barrier(r1, r2)

	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1])
	ax.plot(traj[:,2], traj[:,3])
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
	# ax.plot(circ[:,0], circ[:,1], '--')
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
	ax.plot(ss[:,0], ss[:,2])
		# ax.plot(x[:,2], x[:,3])
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