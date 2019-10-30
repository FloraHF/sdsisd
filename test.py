from vecgram import *

k1, k2 = 0.8, 0.8

r1 = k1*(rDcap_max - rDcap_min) + rDcap_min
r2 = k2*(rIcap_max - rIcap_min) + rIcap_min
v1, v2, _, _ = velocity_vec(r1, r2, get_phi(r1, r2))
print(v1, v2)
## # r1, r2 = 8.33016, 10.32174
v1s, v2s = [], []
n = 50
for phi in np.linspace(-pi, 0.9*pi, n):
	s = velocity_vec(r1, r2, phi, backward=False)
	v1s.append(s[0])
	v2s.append(s[1])
vphi0 = velocity_vec(r1, r2, 0, backward=False)
so = velocity_vec(r1, r2, get_phi(r1, r2), backward=False)

fig, ax = plt.subplots()
ax.plot(v1s, v2s)
ax.plot(v1s[:3], v2s[:3], 'r.')
ax.plot(v1s[int(n/2-1):int(n/2+2)], v2s[int(n/2-1):int(n/2+2)], 'y.')
ax.plot(vphi0[0], vphi0[1], 'k.')
ax.plot([1.2*so[0], 0], [1.2*so[1], 0], 'r')
ax.grid()
# ax.axis('equal')
plt.show()