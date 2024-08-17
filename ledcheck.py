from gpiozero import LED
import threading
led= LED(2)


def led_out():
    
    led.on()

if __name__== "__main__":
    status_thread = threading.Thread(target=led_out)
    status_thread.daemon = True
    status_thread.start()