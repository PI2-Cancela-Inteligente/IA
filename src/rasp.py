import time
import RPi.GPIO as GPIO

# Define the GPIO pins for the motor control
RPWM = 9
LPWM = 10
PWM = 11


# Function to run the motor clockwise
def motor_cw():
    # Set the anti-clockwise control pin to low and the clockwise control pin
    # to high
    GPIO.output(LPWM, GPIO.LOW)
    GPIO.output(RPWM, GPIO.HIGH)
    # Set the speed of the motor to high
    GPIO.output(PWM, GPIO.HIGH)
    # Print a message indicating the motor is running clockwise
    print("MOTOR RUNS CW")


# Function to run the motor anti-clockwise
def motor_ccw():
    # Set the anti-clockwise control pin to high and the clockwise control pin
    # to low
    GPIO.output(LPWM, GPIO.HIGH)
    GPIO.output(RPWM, GPIO.LOW)
    # Set the speed of the motor to high
    GPIO.output(PWM, GPIO.HIGH)
    # Print a message indicating the motor is running anti-clockwise
    print("MOTOR RUNS CCW")


# Function to stop the motor
def motor_stop():
    # Set both control pins to low to stop the motor
    GPIO.output(LPWM, GPIO.LOW)
    GPIO.output(RPWM, GPIO.LOW)
    # Set the speed of the motor to 0
    GPIO.output(PWM, GPIO.LOW)
    # Print a message indicating the motor has stopped
    print("STOP")


# Initial setup of the GPIO pins
def setup():
    # Set the GPIO pin numbering mode
    GPIO.setmode(GPIO.BCM)
    # Set the control pins as outputs
    GPIO.setup(RPWM, GPIO.OUT)
    GPIO.setup(PWM, GPIO.OUT)
    GPIO.setup(LPWM, GPIO.OUT)
    # Print a start message
    print("START")


# Main loop to control the motor
def loop():
    # Wait 1 second
    time.sleep(1)
    # Stop the motor
    motor_stop()

    # Wait 1 second
    time.sleep(1)
    # Run the motor clockwise
    motor_cw()

    # Wait 1 second
    time.sleep(1)
    # Stop the motor
    motor_stop()

    # Wait 1 second
    time.sleep(1)
    # Run the motor anti-clockwise
    motor_ccw()


def open_door():
    motor_cw()
    time.sleep(10)
    motor_stop()
    time.sleep(20)
    motor_ccw()
    time.sleep(10)
    motor_stop()


# Call the setup function
setup()

# Run the loop indefinitely
while True:
    loop()
