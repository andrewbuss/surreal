from matplotlib.pyplot import contour, show, contourf, pcolor
from numpy.fft.fftpack import ifft2
from numpy.ma.core import absolute
from numpy.random.mtrand import rand

def terrain(res, lin, exp):
    print "Creating noise"
    realnoise = rand(res, res)
    imagnoise = rand(res, res)
    print "Normalizing noise"
    realnoise = [[2*_-1 for _ in __] for __ in realnoise]
    imagnoise = [[2*_-1 for _ in __] for __ in imagnoise]
    complexnoise = [[complex(0) for _ in range(res)] for __ in range(res)]
    for i in range(res):
        for j in range(res):
            complexnoise[i][j] = complex(realnoise[i][j], imagnoise[i][j])
            x = (i+0.5)/res-0.5
            y = (j+0.5)/res-0.5
            dist = x*x+y*y
            nf = (lin*dist+0.1)**(-exp)
            complexnoise[i][j] = complex(realnoise[i][j]*nf, imagnoise[i][j]*nf)
    print "Performing backwards FFT2"
    fourier = ifft2(complexnoise)
    fourier = absolute(fourier)
    fourier -= fourier.min()
    fourier /= fourier.max()
    return fourier.tolist()
