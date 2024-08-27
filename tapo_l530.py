from PyP100 import PyL530

l530 = ""

# Login Command
def l530_login(ip, email, password):
    global l530
    l530 = PyL530.L530(ip, email, password)
    l530.handshake()
    l530.login()

# On/Off Command
def l530_off():
    l530.turnOff()


def l530_on():
    l530.turnOn()


# Hue Change
def l530_huechange(hue, sat):
    l530.setColor(hue, sat)


# Colour Temp Change
def l530_colour_temp_change(temp):
    l530.setColorTemp(temp)


# TODO: Satuation Change
def l530_colour_sat(sat):
    l530.setBrightness(sat)
