import matplotlib.pyplot as plt
import matplotlib.tri as tri
from vecgram import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit

if __name__ == '__main__':
    # fig, ax = plt.subplots()
    # draw_vecgram(fig, ax, 1.5, 2.56)
    # plt.show()

    #################### get controur for there's no semipermeable direction ##############
    # r1set = np.linspace(3., 10., 32)
    # r1s, r2s, cs = [], [], []
    # for r1 in r1set:
    # 	for r2 in np.linspace(r1-r, r1+0.7*r, 25):
    # 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
    # 			c = semipermeable_r(r1, r2)
    # 			r1s.append(r1)
    # 			r2s.append(r2)
    # 			cs.append(c)
    # 	for r2 in np.linspace(r1+.71*r, r1+r, 9):
    # 		if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
    # 			c = semipermeable_r(r1, r2)
    # 			r1s.append(r1)
    # 			r2s.append(r2)
    # 			cs.append(c)

    # xi, yi = np.linspace(3., 7., 12), np.linspace(3., 7., 12)
    # triang = tri.Triangulation(r1s, r2s)
    # interpolator = tri.LinearTriInterpolator(triang, cs)
    # Xi, Yi = np.meshgrid(xi, yi)
    # zi = interpolator(Xi, Yi)

    #################### get controur for phi_max=0 ##############
    r1s, r2s, phis = [], [], []
    r0s = np.linspace(0.2*r, 5*r, 66)
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

    xi, yi = np.linspace(3., 7., 50), np.linspace(3., 7., 50)
    triang = tri.Triangulation(r1s, r2s)
    interpolator = tri.LinearTriInterpolator(triang, phis)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)

    fig, ax = plt.subplots()
    ax.contour(xi, yi, zi, [.1], linewidths=2, colors='k')

    # cntr = ax.contourf(xi, yi, zi, levels=3, cmap="RdBu_r")
    # fig.colorbar(cntr, ax=ax)

    plot_bds(ax, triag_cnstr_3)
    plot_bds(ax, triag_cnstr_2)
    plot_bds(ax, triag_cnstr_1)

    ax.grid()
    ax.axis('equal')
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])
    plt.show()
    # ax.plot(r1s, r2s, 'ko', ms=3)