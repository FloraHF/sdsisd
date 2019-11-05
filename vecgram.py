import matplotlib.pyplot as plt
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
    phi_min_slope = minimize(slope_p, 0).x
    ang_p = slope_p(phi_max_slope)
    ang_n = slope_p(phi_min_slope)
    if ang_p - ang_n > pi:
        return 0
    else:
        if max(phi_max_slope, phi_min_slope) < 0:
            return max(phi_max_slope, phi_min_slope)
        else:
            return min(phi_max_slope, phi_min_slope)

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

def draw_vecgram(fig, ax, r1, r2):
    v1s, v2s = [], []
    n = 50
    for phi in np.linspace(-pi, 0.9 * pi, n):
        s = velocity_vec(r1, r2, phi, backward=False)
        v1s.append(s[0])
        v2s.append(s[1])
    vphi0 = velocity_vec(r1, r2, 0, backward=False)
    # print(r1, r2, vphi0[0], vphi0[1])

    phi_opt = get_phi(r1, r2)
    so = velocity_vec(r1, r2, phi_opt, backward=False)

    # fig, ax = plt.subplots()
    ax.clear()
    ax.plot(v1s, v2s)
    ax.plot(v1s[:3], v2s[:3], 'r.')
    ax.plot(v1s[int(n / 2 - 1):int(n / 2 + 2)], v2s[int(n / 2 - 1):int(n / 2 + 2)], 'y.')
    ax.plot(vphi0[0], vphi0[1], 'k.')
    ax.plot([1.01 * so[0], 0], [1.01 * so[1], 0], 'r')
    ax.grid()
    plt.title('phi=%.3f, r=[%.3f, %.3f], r1/r2=%.3f' % (phi_opt, r1, r2, r2 / r1))
    fig.canvas.draw()
    ax.grid()
# ax.axis('equal')
# plt.show(block=False)

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