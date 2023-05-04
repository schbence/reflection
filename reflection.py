from pylab import *
from scipy.io import wavfile


# Room sizes in meters
W,H = 10, 10

# Reflection constant
# (ratio of amplitude reduction after each bounce)
REF_CONST = 0.9999999999999

# Distance constant
# Decay of amplitude caused by distance
DIST_CONST = -1

# Source position
S = array([7.2,7.1])

# Listener position
L = [1.1,1.2]




infile = 'gityo.wav'
outfile = 'out-size-%sx%s-ref-%s-dist-%s.wav' % (str(W), str(H), str(REF_CONST).replace('.','p'), str(DIST_CONST).replace('.','p'))

def r(p,n,m):
	x,y = p
	xp = ((((-1)**(n+1)+1)/2)+n)*W + (-1)**n*x
	yp = ((((-1)**(m+1)+1)/2)+m)*H + (-1)**m*y
	return array([xp, yp])


rs = []
ns = []
for n in range(-50,50):
	for m in range(-50,50):
		rs.append(r(S,n,m))
		ns.append(abs(n) + abs(m))

rs = array(rs)
ls = array([L]*len(rs))
ds = sqrt(sum((rs-L)**2, axis=1))

delays = ds / 300.
amps = REF_CONST ** array(ns)

dur = 3
FS = 44100

ir = histogram(delays, bins=linspace(0,dur,dur*FS), weights=amps*ds**DIST_CONST)

dry = wavfile.read(infile)[1]

kernel = ir[0]#[:80000]
kernel = kernel

wet = convolve(dry, kernel)#, mode='same')

wavfile.write(outfile, 44100, wet/wet.std()*0.05)

