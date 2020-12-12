def detecta_gestos(sig):
    gesto = ""
    gesto = play_pause(sig)
    if not gesto:
        gesto = proxima_musica(sig)
    if not gesto:
        gesto = volta_musica(sig)
    if not gesto:
        gesto = gatilho(sig)
    if not gesto:
        gesto = aumentar_volume(sig)
    if not gesto:
        gesto = diminuir_volume(sig)
    return gesto

def play_pause(sig):
    max_ax = 0.0
    min_ax = -0.4
    tt = 30
    delta = sig.gy.index(min(sig.gy)) - sig.gy.index(max(sig.gy))

    if (max(sig.ax) > max_ax) and (min(sig.ax) < min_ax) and (0 < delta < tt):
        return "play_pause"

def proxima_musica(sig):
    max_ay = 0.4
    min_az = 0.4
    if (min(sig.az) < min_az) and (max(sig.ay) > max_ay):
        return "proxima"

def voltar_musica(sig):
    min_ay = -0.4
    min_az = 0.4
    if (min(sig.az) < min_az) and (min(sig.ay) < min_ay):
        return "voltar"

def gatilho(sig):
    max_ay = 0.1
    min_ay = -0.1
    t_az = 0.4
    if (min(sig.ay) < min_ay) and (max(sig.ay) > max_ay) and (min(sig.az) > t_az):
        return "gatilho"

def aumenta_volume(sig):
    max_ax = 0.3
    min_ax = 0.1
    tt = 30
    delta =  sig.gy.index(max(sig.gy)) - sig.gy.index(min(sig.gy))
    if (min(sig.ax) < min_ax) and (max(sig.ax) > max_ax) and (delta > tt):
        return "aumentar_vol"

def abaixa_volume(sig):
    max_ax = -0.1
    min_ax = -0.4
    tt = 30
    delta = sig.gy.index(min(sig.gy)) - sig.gy.index(max(sig.gy))
    if (min(sig.ax) < min_ax) and (max(sig.ax) > max_ax) and (delta > tt):
        return "abaixar_vol"
