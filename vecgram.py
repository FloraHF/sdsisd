import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import numpy as np
from math import pi, sqrt, acos, cos, sin, tan, atan2
from scipy.optimize import minimize, dual_annealing

from Config import Config

r = Config.CAP_RANGE
R = Config.TAG_RANGE
vd = Config.VD
vi = Config.VI
gmm = acos(vd / vi)
rIcap_min, rIcap_max = r / (sin(gmm)), r / (1 - cos(gmm))
rDcap_min, rDcap_max = rIcap_min * (vd / vi), rIcap_max * (vd / vi)


def velocity_vec(r1, r2, phi, backward=False):
    psi = acos(vd / vi * cos(phi))
    psi = -abs(psi)

    alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
    beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))
    if backward:
        vr1 = vd * cos(alpha + phi)
        vr2 = vi * cos(beta + psi)
        vtht1 = vd * sin(alpha + phi) / r1
        vtht2 = vi * sin(beta + psi) / r2
    else:
        vr1 = -vd * cos(alpha + phi)
        vr2 = -vi * cos(beta + psi)
        vtht1 = -vd * sin(alpha + phi) / r1
        vtht2 = -vi * sin(beta + psi) / r2

    return vr1, vr2, vtht1, vtht2


def get_phi(r1, r2):

    def get_v(phi, r1, r2):
        psi = acos(vd / vi * cos(phi))
        psi = -abs(psi)
        alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
        beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

        v1 = -vd * cos(alpha + phi)
        v2 = -vi * cos(beta + psi)

        return v1, v2

    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)

    phi_max_slope = minimize(slope_n, 0).x
    phi_min_slope = minimize(slope_p, -.0001).x
    ang_p = slope_p(phi_max_slope)
    ang_n = slope_p(phi_min_slope)
    if ang_p - ang_n > pi:
        # print(ang_p, ang_n)
        # print('set 0')
        return 0
    else:
        # if max(phi_max_slope, phi_min_slope) < 0:
        #     print('compute: both < 0')
        #     return max(phi_max_slope, phi_min_slope)
        # else:
        #     print('compute: one < 0, chose smaller')
        #     return min(phi_max_slope, phi_min_slope)
        if ang_p > 0:
            return phi_max_slope
        else:
            return phi_min_slope

    return sol.x


def get_phi_max(r1, r2):

    def get_v(phi, r1, r2):
        psi = acos(vd / vi * cos(phi))
        psi = -abs(psi)
        alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
        beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

        v1 = -vd * cos(alpha + phi)
        v2 = -vi * cos(beta + psi)

        return v1, v2

    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)
    
    return minimize(slope_n, 0).x

def draw_vecgram(r1, r2, id):
    v1s, v2s = [], []
    phis = np.concatenate([np.linspace(-pi, 0, 30),np.linspace(0.0, pi, 30), np.array([-pi])])
    for phi in phis:
        s = velocity_vec(r1, r2, phi, backward=False)
        v1s.append(s[0])
        v2s.append(s[1])
    vphi0 = velocity_vec(r1, r2, 0, backward=False)
    # print(r1, r2, vphi0[0], vphi0[1])

    phi_opt = get_phi(r1, r2)
    so = velocity_vec(r1, r2, phi_opt, backward=False)

    fig, ax = plt.subplots()
    # ax.clear()
    ax.plot(v1s[0:30], v2s[0:30], 'k-', label=r'$\phi\leq0$')
    ax.plot(v1s[30:-1], v2s[30:-1], 'k--', label=r'$\phi>0$')
    ax.plot(v1s[:1], v2s[:1], 'b.', label=r'$\phi = -\pi$')
    # ax.plot(v1s[29:30], v2s[29:30], 'y.')
    ax.plot(vphi0[0], vphi0[1], 'g.', label=r'$\phi = 0$')
    ax.plot([1.01 * so[0], 0], [1.01 * so[1], 0], 'r')
    ax.legend(fontsize=12)
    plt.xlabel(r'$\dot{\rho}_D$', fontsize=14)
    plt.ylabel(r'$\dot{\rho}_I$', fontsize=14)
    ax.grid()
    plt.title(r'$\phi=%.3f$, $(\rho_D, \rho_I)=(%.3f, %.3f)$' % (phi_opt, r1, r2), fontsize=14)
    # fig.canvas.draw()
    # ax.grid()
    ax.axis('equal')
    # plt.show()
    plt.savefig('vecgram_'+str(id)+'.png')
    plt.close('all')

def semipermeable_r(r1, r2):

    def get_v(phi, r1, r2):
            psi = acos(vd / vi * cos(phi))
            psi = -abs(psi)
            alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
            beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

            v1 = -vd * cos(alpha + phi)
            v2 = -vi * cos(beta + psi)

            return v1, v2
    
    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)

    ang_p = slope_p(minimize(slope_n, 0).x)
    ang_n = slope_p(minimize(slope_p, 0).x)
    # print(ang_p)
    # print(ang_n)
    # print(ang_p - ang_n)

    return pi - (ang_p - ang_n)