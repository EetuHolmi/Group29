from machine import Pin, SoftI2C
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
print(i2c.scan())
