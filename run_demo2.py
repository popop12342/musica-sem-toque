import time
from windowed_signal import WindowedSignal
from multiprocessing import Process, Queue
from mpu6050_i2c import *
time.sleep(1)
from gestos import detecta_gestos
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import os

q = Queue()

def set_volume(x):
    x = str(x)
    os.system("amixer sset 'Master' " + x + "%")

def run_gestos(window_size=2, t_delta=0.01, stride=1.0):
    total_time = 0
    n_window = 0
    samples = [[[],[],[]], [[],[],[]]]
    print('start')
    last_gesto = ''
    last_last_gesto = ''
    t_last_gesto = 0
    gatilho_ativo = False
#    f = open('gestos.txt', 'w')
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
            gesto = detecta_gestos(sig)
            comando = None
            if gesto:
                print(gesto, last_gesto, last_last_gesto)
                if gesto != last_gesto or total_time - t_last_gesto > 1.1 or (gesto==last_gesto==last_last_gesto):
                    comando = gesto
                if comando:
                    if comando == 'gatilho':
                        gatilho_ativo = not gatilho_ativo
                    elif gatilho_ativo:
                        q.put(comando)
                        print(0, comando)
                last_last_gesto = last_gesto
                last_gesto = gesto
                t_last_gesto = total_time


        total_time += t_delta
        time.sleep(t_delta)

def on_property_changed(interface, changed, invalidated):
    pass

playing = True
volume = 50
set_volume(volume)
def on_playback_control(fd, condition):
#    gesto = fd.readline()
    gesto = q.get()
    global playing
    global volume
    if gesto == 'play_pause':
        if not playing:
            player_iface.Play()
            playing = True
        else:
            player_iface.Pause()
            playing = False
    elif gesto == 'proxima':
        player_iface.Next()
    elif gesto == 'voltar':
        player_iface.Previous()
    elif gesto == 'aumentar_vol':
        volume = min(100, volume+10)
        set_volume(volume)
    elif gesto == 'abaixar_vol':
        volume = max(0, volume-10)
        set_volume(volume)
    return True
    
if __name__ == "__main__":
  p1 = Process(target=run_gestos)
  p1.start()
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
  bus = dbus.SystemBus()
  obj = bus.get_object('org.bluez', '/')
  mgr = dbus.Interface(obj,  'org.freedesktop.DBus.ObjectManager')
  player_iface = None
  transport_prop_iface = None
  for path, ifaces in mgr.GetManagedObjects().items():
#    for s in ifaces:
#      print(s)
    if 'org.bluez.MediaControl1' in ifaces:
      player_iface = dbus.Interface(bus.get_object('org.bluez', path), 'org.bluez.MediaControl1')
      print(player_iface)
    elif 'org.bluez.MediaTransport1' in ifaces:
      transport_prop_iface = dbus.Interface(bus.get_object('org.bluez', path), 'org.freedesktop.DBus.Properties')
  if not player_iface:
    sys.exit('Error: Media Player not found.')
  if not transport_prop_iface:
    sys.exit('Error: DBus.Properties iface not found')

  bus.add_signal_receiver(on_property_changed,bus_name='org.bluez',signal_name='PropertiesChanged',dbus_interface='org.freedesktop.DBus.Properties')
  fout = open('gestos.txt', 'r')
  playing = True
  GLib.io_add_watch(fout, GLib.IO_IN, on_playback_control)
  GLib.MainLoop().run()
  p1.join()
