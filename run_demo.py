import time
from windowed_signal import WindowedSignal
from mpu6050_i2c import *

time.sleep(1)

def run(window_size=2, t_delta=0.01, stride=0.5):
    total_time = 0
    n_window = 0
    samples = [[[],[],[]], [[],[],[]]]
    print('start')
    while True:

        # le o sensor
        try:
            ax, ay, az, wx, wy, wz = mpu6050_conv()
        except:
            continue

        samples[0][0].append(ax)
        samples[0][1].append(ay)
        samples[0][2].append(az)
        samples[1][0].append(gx)
        samples[1][1].append(gy)
        samples[1][2].append(gz)

        if total_time >= window_size and (total_time+t_delta % stride == 0):
            # nova janela do sinal
            sig = WindowedSignal()
            b = n_window * stride / t_delta
            e = (n_window * stride + window_size) / t_delta
            sig.ax = samples[0][0][b:e]
            sig.ay = samples[0][1][b:e]
            sig.az = samples[0][2][b:e]
            sig.gx = samples[1][0][b:e]
            sig.gy = samples[1][1][b:e]
            sig.gz = samples[1][2][b:e]
            n_window += 1
            print(n_window, sig)

        total_time += t_delta
        time.sleep(t_delta)
