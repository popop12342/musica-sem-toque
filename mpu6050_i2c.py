import smbus, time

def MPU6050_start():
    # alter sample rate (stability)
    samp_rate_div = 0 # sample rate = 8 kHz/(1+samp_rate_div)
    bus.write_byte_data(MPU6050_ADDR, SMPLRT_DIV, samp_rate_div)
    time.sleep(0.1)
    # reset all sensors
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0x00)
    time.sleep(0.1)
    # power management and crystal settings
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0x01)
    time.sleep(0.1)
    # write to configuration register
    bus.write_byte_data(MPU6050_ADDR, CONFIG, 0)
    time.sleep(0.1)
    # write to gyro configuration register
    gyro_config_sel = [0b00000, 0b01000, 0b10000, 0b11000]
    gyro_config_vals = [250.0, 500.0, 1000.0, 2000.0]
    gyro_indx = 0
    bus.write_byte_data(MPU6050_ADDR, GYRO_CONFIG, int(gyro_config_sel[gyro_indx]))
    time.sleep(0.1)
    # write to accel configuration register
    accel_config_sel = [0b00000, 0b01000, 0b10000, 0b11000]
    accel_config_vals = [1.0, 4.0, 8.0, 16.0]
    accel_indx = 0
    bus.write_byte_data(MPU6050_ADDR, ACCEL_CONFIG, int(accel_config_sel[accel_indx]))
    time.sleep(0.1)
    # interrupt register (related to overflow af data FIFO)
    bus.write_byte_data(MPU6050_ADDR, INT_ENABLE, 1)
    time.sleep(0.1)
    return gyro_config_vals[gyro_indx], accel_config_vals[accel_indx]

def read_raw_bits(register):
    # read accel and hyro values
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register+1)

    # combine high and low for unsigned bit value
    value = ((high << 8) | low)

    # convert to +- value
    if (value > 32768):
        value -= 65535
    return value

def mpu6050_conv():
    # raw acceleration bits
    acc_x = read_raw_bits(ACCEL_XOUT_H)
    acc_y = read_raw_bits(ACCEL_YOUT_H)
    acc_z = read_raw_bits(ACCEL_ZOUT_H)

    # raw temp bits
    # t_val = read_raw_bits(TEMP_OUT_H)

    # raw gyroscope bits
    gyro_x = read_raw_bits(GYRO_XOUT_H)
    gyro_y = read_raw_bits(GYRO_YOUT_H)
    gyro_z = read_raw_bits(GYRO_ZOUT_H)

    # convert to acceleration in g and gyro in dps
    a_x = (acc_x / (2.0 ** 15.0)) * accel_sens
    a_y = (acc_y / (2.0 ** 15.0)) * accel_sens
    a_z = (acc_z / (2.0 ** 15.0)) * accel_sens

    w_x = (gyro_x / (2.0 ** 15.0)) * gyro_sens
    w_y = (gyro_y / (2.0 ** 15.0)) * gyro_sens
    w_z = (gyro_z / (2.0 ** 15.0)) * gyro_sens

    # temp = ((t_val) / 333.87) + 21.0

    return a_x, a_y, a_z, w_x, w_y, w_z


# MPU6050 registers
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
TEMP_OUT_H   = 0x41
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


# start I2C driver
bus = smbus.SMBus(1)
gyro_sens, accel_sens = MPU6050_start()
