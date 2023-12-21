import time
import threading

clk = 0


def get_time():
    global clk
    clk = time.strftime('\t%H:%M\r')
    return clk


def manage_time():
    while True:
        print(get_time())
        time.sleep(60)


threading.Thread(target=manage_time()).start()
