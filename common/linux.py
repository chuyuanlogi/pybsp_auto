import os
import signal

def _killall(proc_name):
    if proc_name ==None or len(proc_name) == 0:
        print("please input process name")
        return 

    try:
        for line in os.popen("ps aux | grep {} | grep -v grep".format(proc_name)):
            items = line.split()
            pid = items[0]
            os.kill(int(pid), signal.SIGKILL)

            print("killed all {} process".format(proc_name))
    except:
        print("some error raise")

def start_zoom(room_id, password):
    os.system("xdg-open \"zoommtg://zoom.us/join?action=join&confno={}&pwd={}\"".format(room_id, password))

def start_scrcpy(serial):
    if serial == None or len(serial) == 0:
        os.system("scrcpy")
    else:
        os.system("os -s {}".format(serial))