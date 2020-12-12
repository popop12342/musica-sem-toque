import time
from windowed_signal import WindowedSignal
from mpu6050_i2c import *

time.sleep(1)

def run(window_size=2, t_delta=0.01, stride=1.0):
    total_time = 0
    n_window = 0
    samples = [[[],[],[]], [[],[],[]]]
    print('start')
    while True:

        # le o sensor
        try:
            ax, ay, az, gx, gy, gz = mpu6050_conv()
        except:
            continue

        samples[0][0].append(ax)
        samples[0][1].append(ay)
        samples[0][2].append(az)
        samples[1][0].append(gx)
        samples[1][1].append(gy)
        samples[1][2].append(gz)

        #print(total_time)
        if total_time+t_delta >= window_size and (len(samples[0][0]) % int(stride/t_delta) == 0):
            # nova janela do sinal
            sig = WindowedSignal()
            b = int(n_window * stride / t_delta)
            e = int((n_window * stride + window_size) / t_delta)
            sig.ax = samples[0][0][b:e]
            sig.ay = samples[0][1][b:e]
            sig.az = samples[0][2][b:e]
            sig.gx = samples[1][0][b:e]
            sig.gy = samples[1][1][b:e]
            sig.gz = samples[1][2][b:e]
            n_window += 1
#            print(n_window)
            # testes dos comandos
            play_pause(sig)
            proxima_musica(sig)
            voltar_musica(sig)
            gatilho(sig)
            aumenta_volume(sig)
            abaixa_volume(sig)

        total_time += t_delta
        time.sleep(t_delta)

def play_pause(sig):
    max_ax = 0.0
    min_ax = -0.4
    tt = 30
    delta = sig.gy.index(min(sig.gy)) - sig.gy.index(max(sig.gy))

    if (max(sig.ax) > max_ax) and (min(sig.ax) < min_ax) and (0 < delta < tt):
        print("Detectado comando para play/pause")

def proxima_musica(sig):
    max_ay = 0.4
    min_az = 0.4
    if (min(sig.az) < min_az) and (max(sig.ay) > max_ay):
        print("Detectado o comando para próxima música")

def voltar_musica(sig):
    min_ay = -0.4
    min_az = 0.4
    if (min(sig.az) < min_az) and (min(sig.ay) < min_ay):
        print("Detectado o comando para voltar música")

def gatilho(sig):
    max_ay = 0.1
    min_ay = -0.1
    t_az = 0.4
    if (min(sig.ay) < min_ay) and (max(sig.ay) > max_ay) and (min(sig.az) > t_az):
        print("Detectado o comando para gatilho")

def aumenta_volume(sig):
    max_ax = 0.3
    min_ax = 0.1
    if (min(sig.ax) < min_ax) and (max(sig.ax) > max_ax):
        print("Detectado o comando para aumentar o volume")

def abaixa_volume(sig):
#    maximos = [[0.0,0.04,0.5],[]]
#    minimos = [[-0.4,-0.15,0.35],[]]
#    if (min(sig.ax) < minimos[0][0]) and (max(sig.ax)>maximos[0][0]) and (min(sig.az)<minimos[0][2]) and (max(sig.az) > maximos[0][2]) and (sig.ax.index(min(sig.ax))<sig.ax.index(max(sig.ax))) and sig.az.index(min(sig.az))>sig.az.index(max(sig.az)) and (minimos[0][1] < min(sig.ay) < maximos[0][1]) and (minimos[0][1] < max(sig.ay) < maximos[0][1]):
#    if (min(sig.ax) < minimos[0][0]) and (max(sig.ax) > maximos[0][0]) and sig.ax.index(min(sig.ax)) < sig.ax.index(max(sig.ax)):
    max_ax = -0.1
    min_ax = -0.4
    tt = 30
    delta = sig.gy.index(min(sig.gy)) - sig.gy.index(max(sig.gy))
    if (min(sig.ax) < min_ax) and (max(sig.ax) > max_ax) and (delta > tt):
        print("Detectado o comando para abaixar o volume")

if __name__ == "__main__":
    run()
