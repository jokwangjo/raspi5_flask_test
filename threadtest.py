'''
import threading
import time

def thread_test1(test):
    print(f"thread1 {test}")

def thread_test2(test):
    print(f"thread2 {test}")
    

try:
    while True:
        th1 =threading.Thread(target=thread_test1,args=("1",))
        th2 =threading.Thread(target=thread_test2,args=("2",))
        th1.start()
        th2.start()
        time.sleep(1)
        th1.join()
        time.sleep(1)
        th2.join()
except KeyboardInterrupt:
    pass
        
 '''

import threading
import time

# 스레드에서 실행할 함수
def thread_function(name, stop_after, stop_event):
    print(f"Thread {name}: starting")
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        if elapsed_time >= stop_after:
            break
        print(f"Thread {name}: {stop_after - elapsed_time:.2f} seconds remaining")
        time.sleep(1)
    print(f"Thread {name}: finishing after {stop_after} seconds")

# 스레드를 저장할 리스트
threads = []
stop_events = []

# 첫 번째 스레드 생성 (10초 후 종료)
stop_event1 = threading.Event()
thread1 = threading.Thread(target=thread_function, args=("1", 10, stop_event1))
threads.append(thread1)
stop_events.append(stop_event1)

# 두 번째 스레드 생성 (30초 후 종료)
stop_event2 = threading.Event()
thread2 = threading.Thread(target=thread_function, args=("2", 30, stop_event2))
threads.append(thread2)
stop_events.append(stop_event2)

# 스레드 시작
for thread in threads:
    thread.start()

print("Main thread continues to run while other threads are running")
print("All threads are started but not necessarily finished")

# 메인 스레드가 스레드의 상태를 주기적으로 확인하는 while 루프
while any(thread.is_alive() for thread in threads):
    # 스레드 상태를 주기적으로 확인
    print("Threads are still running...")
    time.sleep(1)  # 1초 대기 후 다시 확인

# 스레드 종료 이벤트 설정
for stop_event in stop_events:
    stop_event.set()

# 모든 스레드가 종료되기를 대기
for thread in threads:
    thread.join()

print("All threads finished")


# 메인 스레드는 스레드가 종료되기를 기다리지 않고 계속 실행됩니다.
