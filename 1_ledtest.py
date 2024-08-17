from flask import Flask, render_template, url_for, redirect, request
from gpiozero import LED, Button, PWMLED
import threading
import time
import os
import signal
import sys

# LED 핀 번호와 초기 상태 정의
led_pin_dict = {'led1': 2, 'led2': 3, 'led3': 4}
button_pin_dict= {'button1':14,'button2':15,'button3':18}
pwmled_pin_dict ={'led17':17,'led27':27}

# LED 객체 초기화
led_objects = {key: LED(pin) for key, pin in led_pin_dict.items()}
led_object_list= list(led_objects.values())

button_objects={key: Button(pin,pull_up=False) for key, pin in button_pin_dict.items()}
button_object_list= list(button_objects.values())
button_monitor_list = [None] * len(button_object_list)

pwmled_objects= {key:PWMLED(pin) for key, pin in pwmled_pin_dict.items()}
pwmled_object_list = list(pwmled_objects.values())

pwmled_state_dict = {key:0 for key in pwmled_pin_dict.keys()}




thread_list=[]
stop_threads = False

class CustomThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.stop_event= threading.Event()
        self.name = name
        
        
    def led_on_1cycle(self,led_out,stop_after):
        print(f"Thread {self.name}:led_on_cycle: starting")
        start_time= time.time()
        while not self.stop_event.is_set():
            elapsed_time = time.time()-start_time
            if elapsed_time< stop_after:
                led_control(led_out,1)
            else:
                led_control(led_out,0)
                break
            print(f"Thread LED_on_{stop_after}_core: {stop_after - elapsed_time:.2f} seconds remaining")
            time.sleep(1)
        
    def stop(self):
        self.stop_event.set        

def create_thread(name):
    thread= CustomThread(name)
    thread_list.append(thread)
    return thread
    
    


'''
# 만든 스레드들을 실행시킴
for led_idx in thread_dict.keys():
    thread_dict[led_idx].start()
'''
    
def led_control(led, state):
    led_out = led_objects[led]
    if state == 1:
        led_out.on()
    else:
        led_out.off()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    i=0
    for button_is_active in button_object_list:
        button_monitor_list[i]=button_is_active.is_active
        #print(button_monitor_list[i])
        i+=1
    '''
    active_threads = []
    for thread in thread_list:
        if thread.is_alive():
            active_threads.append(thread.name)
    print("Active threads:", active_threads)
    ''' 
              # 각각의 LED 색상을 설정하기 위한 주소
    return render_template('index.html',button_monitor_list= button_monitor_list)
        
@app.route('/led_control', methods=['GET'])
def LED_brightness_control():        
    for led_pin in pwmled_pin_dict.keys():
        value = request.args.get(led_pin)
        if value is not None:
            try:
                brightness = float(value)/100
                pwmled_state_dict[led_pin]= brightness*100
                pwmled_objects[led_pin].value= brightness
            except ValueError:
                pass #입력값 유효하지 않을 경우 무시.
    return render_template('led_control.html',led17=pwmled_state_dict['led17'], led27=pwmled_state_dict['led27'])
            
        
    


#램프 온오프 스위치
@app.route('/<led>/<int:state>')  
def LED_control(led, state):
    
    if led in led_pin_dict:
        led_control(led, state)
    return redirect(url_for('home'))

#렘프 3초 점등 스위치
@app.route('/<led>/on_3_sec')
def LED_on_3_sec(led):
    thread=create_thread("LED_on_3_sec")
    thread.led_on_1cycle(led,3)
    return redirect(url_for('home'))

#blink 스위치
@app.route('/<led>/blink')
def LED_blink_1sec_core(led):
    blink_time= 1
    while True:
        thread=create_thread(f"LED_on_{blink_time}_sec")
        thread.led_on_1cycle(led,blink_time)
        time.sleep(blink_time)
        thread=create_thread(f"LED_on_{blink_time}_sec")
        thread.led_on_1cycle(led,blink_time)
        break
    
    return redirect(url_for('home'))

    



def monitor_button_status():
    while not stop_threads:
        if button_monitor_list[0]==1:
            
            for led_pin_key in led_pin_dict.keys():
                led_control(led_pin_key, 1)
            
        elif button_monitor_list[1]==1:
            for led_pin_key in led_pin_dict.keys():
                led_control(led_pin_key, 0)
            
        elif button_monitor_list[2]==1:
            count=[3,2,1]
            i=0
            for led_pin_key in led_pin_dict.keys():
                thread=create_thread("LED_on_3_sec")
                thread.led_on_1cycle(led_pin_key,count[i])
                i+=1
        
        time.sleep(1)

def signal_handler(sig, frame):
    global stop_threads
    stop_threads = True
    print('Exiting gracefully...')
    for thread in thread_list:
        if thread.is_alive():
            thread.stop()
            thread.join()
    sys.exit(0)



if __name__== "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the monitor thread
    monitor_thread = threading.Thread(target=monitor_button_status)
    monitor_thread.start()
    
    app.run(host="0.0.0.0",port="8080")
    #status_thread.join()
    monitor_thread.join()

    
        
