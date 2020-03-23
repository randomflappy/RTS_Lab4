#   RTS Lab4
#   IO-71 Fryzyuk
#   var: n, w_max, N = 12, 2700, 64
import time
import math
import random
import matplotlib.pyplot as plt
from numpy import fft as f


def signal(the_n, the_upper_n, the_w_max):
    amplitude = [random.random() for i in range(the_n)]
    phi = [random.random() for j in range(the_n)]
    cont = []
    for i in range(the_upper_n):
        tmp_sum = 0
        for p in range(the_n):
            tmp_sum += amplitude[p] * math.sin(the_w_max / the_n * p * i + phi[p])
        cont.append(tmp_sum)
    return cont


def furies(the_signal, the_upper_n):
    result = []
    for p in range(the_upper_n):
        real_part = 0
        imaginary_part = 0
        for k in range(the_upper_n):
            real_part += the_signal[k]*math.cos((2*math.pi*p*k)/the_upper_n)
            imaginary_part += the_signal[k] * math.sin((2 * math.pi * p * k) / the_upper_n)
        result.append(math.sqrt(real_part**2 + imaginary_part**2))
    return result


def fast_furies(the_signal, the_upper_n):
    result = []

    for p in range(int(the_upper_n/2)):
        re, re1, re2 = 0, 0, 0
        im, im1, im2 = 0, 0, 0

        for k in range(int(the_upper_n/2)):
            re1 += the_signal[2*k+1] * math.cos((4*math.pi*p*k) / the_upper_n)
            re2 += the_signal[2*k] * math.cos((4*math.pi*p*k) / the_upper_n)
            im1 += the_signal[2 * k + 1] * math.sin((4 * math.pi * p * k) / the_upper_n)
            im2 += the_signal[2 * k] * math.sin((4 * math.pi * p * k) / the_upper_n)

        rep = math.cos((2 * math.pi * p) / the_upper_n)
        imp = math.sin((2 * math.pi * p) / the_upper_n)

        wp = math.sqrt(rep**2 + imp**2)

        re = re1 + re2 * wp
        im = im1 + im2 * wp

        result.append(math.sqrt(re**2 + im**2))

    for p in range(int(the_upper_n / 2), the_upper_n):
        re, re1, re2 = 0, 0, 0
        im, im1, im2 = 0, 0, 0

        for k in range(int(the_upper_n / 2)):
            re1 += the_signal[2 * k + 1] * math.cos((4 * math.pi * p * k) / the_upper_n)
            re2 += the_signal[2 * k] * math.cos((4 * math.pi * p * k) / the_upper_n)
            im1 += the_signal[2 * k + 1] * math.sin((4 * math.pi * p * k) / the_upper_n)
            im2 += the_signal[2 * k] * math.sin((4 * math.pi * p * k) / the_upper_n)

        rep = math.cos((2 * math.pi * p) / the_upper_n)
        imp = math.sin((2 * math.pi * p) / the_upper_n)

        wp = math.sqrt(rep ** 2 + imp ** 2)

        re = re1 - re2 * wp
        im = im1 - im2 * wp

        result.append(math.sqrt(re ** 2 + im ** 2))

    return result


# Graph 1 -----------------
n, w_max, N = 12, 2700, 64

signals = []
number_of_signals = 100000

for i in range(number_of_signals):
    sig = signal(n, N, w_max)
    signals.append(sig)

my_fft_time = []
start = time.time()
for i in range(number_of_signals):
    fur = fast_furies(signals[i], N)
    if i % 10 == 0:
        my_fft_time.append(time.time() - start)

numpy_fft_time = []
start = time.time()
for i in range(number_of_signals):
    numpy_fur = f.fft(signals[i], N)
    if i % 10 == 0:
        numpy_fft_time.append(time.time() - start)

# Graphs comparison

fur = fast_furies(signals[0], N)
ax1 = plt.subplot(221)
ax1.set_title('my fft')
ax1.bar([i for i in range(N)], fur)

numpy_fur = f.fft(signals[0], N)
ax2 = plt.subplot(222)
ax2.set_title('numpy fft')
ax2.bar([i for i in range(N)], numpy_fur.real)

# Time comparison

ax3 = plt.subplot(224)
ax3.plot([i for i in range(0, number_of_signals, 10)], my_fft_time)

ax4 = plt.subplot(223)
ax4.plot([i for i in range(0, number_of_signals, 10)], numpy_fft_time)


plt.show()
