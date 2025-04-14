import machine
import select
import sys

# Onboard LED setup (GPIO 25 is onboard)
led = machine.PWM(machine.Pin(25))
led.freq(1000)

# Dummy placeholders for sensors (can be connected and used later)
humidity = 60
temperature = 37.0
phototherapy = machine.PWM(machine.Pin(15))  # Example pin for phototherapy
phototherapy.freq(1000)

# Function to safely set duty cycle (0–65535) from percent (25–100)
def set_pwm(pwm, percent):
    if 25 <= percent <= 100:
        duty = int((percent / 100.0) * 65535)
        pwm.duty_u16(duty)

while True:
    try:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip()
            if not line:
                continue

            prefix = line[0]
            value = line[1:]

            if prefix == "L":
                try:
                    intensity = int(value)
                    if 25 <= intensity <= 100:
                        set_pwm(led, intensity)
                except:
                    pass

            elif prefix == "H":
                try:
                    humidity = int(value)
                    if 60 <= humidity <= 100:
                        print(f"Humidity set to: {humidity}%")
                        #place humidity control system here
                except:
                    pass

            elif prefix == "T":
                try:
                    temp = float(value)
                    if 37.0 <= temp <= 38.0:
                        temperature = temp
                        print(f"Temperature set to: {temperature}°C")
                        #place temperature control system here
                except:
                    pass

            elif prefix == "P":
                try:
                    pt = int(value)
                    if 25 <= pt <= 100:
                        set_pwm(phototherapy, pt)
                except:
                    pass

            elif line == "exit_program":
                set_pwm(led, 0)
                set_pwm(phototherapy, 0)
                break

    except KeyboardInterrupt:
        set_pwm(led, 0)
        set_pwm(phototherapy, 0)
        break

