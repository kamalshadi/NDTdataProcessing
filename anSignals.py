import math
import pylab as pl

def genSignal(N=1000):
	f=10
	fs=10*f
	s=[0]*N
	l=[x for x in range(N)]
	i=0
	for x in l:
		if i==0:
			s[x]=math.cos(2*math.pi*f*float(x)/float(fs))
			if (x%500 == 0 and x!=0) :
				i=1
				continue
		if i==1:
			if x%500 == 0:
				i=0
	return [s,fs]
	
def sigPower(z):
	l=len(z)
	return float(sum([abs(x)**2 for x in z]))/float(l)
	
def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * num.log10 (abs(h))
    subplot(211)
    plot(w/max(w),h_dB)
    ylim(-150, 5)
    ylabel('Magnitude (db)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Frequency response')
    subplot(212)
    h_Phase = unwrap(arctan2(imag(h),real(h)))
    plot(w/max(w),h_Phase)
    ylabel('Phase (radians)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Phase response')
    subplots_adjust(hspace=0.5)

#Plot step and impulse response
def impz(b,a=1):
    l = len(b)
    impulse = repeat(0.,l); impulse[0] =1.
    x = arange(0,l)
    response = signal.lfilter(b,a,impulse)
    subplot(211)
    stem(x, response)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Impulse response')
    subplot(212)
    step = cumsum(response)
    stem(x, step)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Step response')
    subplots_adjust(hspace=0.5)
		
