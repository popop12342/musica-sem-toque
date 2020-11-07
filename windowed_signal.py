def parse_line(l):
    l = l[l.index('x = ')+4:]
    x = float(l[:l.index(',')])
    l = l[l.index('y = ')+4:]
    y = float(l[:l.index(',')])
    l = l[l.index('z = ')+4:]
    z = float(l[:-1])
    return x, y, z

class WindowedSignal:
    def __init__(self):
        self.t = []
        self.ax = []
        self.ay = []
        self.az = []
        self.gx = []
        self.gy = []
        self.gz = []
        
    def from_file(self, filepath):
        with open(filepath, 'r') as f:
            t_step = f.readline()
            while t_step:
                self.t.append(float(t_step[:-1]))
                acc_line = f.readline()
                ax, ay, az = parse_line(acc_line)
                gyro_line = f.readline()
                gx, gy, gz = parse_line(gyro_line)
                self.ax.append(ax)
                self.ay.append(ay)
                self.az.append(az)
                self.gx.append(gx)
                self.gy.append(gy)
                self.gz.append(gz)
                t_step = f.readline()