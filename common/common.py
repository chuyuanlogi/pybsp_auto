import adbutils
import threading
import time
import ipaddress
from types import SimpleNamespace as sns
import pathlib
from os.path import exists

def _logcat(d, file):
    if d is None or file is None:
        return
    
    d.shell("logcat -c")
    stream = d.shell("logcat -b all", stream=True)

    out = open(file, 'w')

    while stream:
        if adbutils._adb._check_server(host = "127.0.0.1", port=5037) == False:
            out.close()
            return

        s = stream.conn.makefile()
        for _ in range(100):
            l = s.readline().rstrip()
            if len(l) > 0:
                out.write(l + "\n")
        s.close()

    out.close()


def start_log(d, file):
    t = threading.Thread(target = _logcat, args=(d, file))
    t.start()
    return t

def countdown(t):
    while t:
        m, s = divmod(t, 60)
        timer = "{:02d}:{02d}\r".format(m, s)
        print(timer)
        time.sleep(1)
        t -= 1

def __run_test(initfunc, actionfunc):
    if initfunc == None or actionfunc == None:
        print("init or action is null, ignore this test")
        return

    ns = initfunc()

    # repeat:
    #   0: no loop
    #  -1: infinite loop
    # num: loop count
    # default vaule is 0
    #
    # tcid: the test description
    #
    # expect:
    #   0: ignore expectation
    #   1: has expectiation function
    # default value is 0

    if not hasattr(ns, 'repeat'):
        ns.repeat = 0

    if hasattr(ns, 'tcid'):
        print("staring run test: {}".format(ns.tcid))
    else:
        print("staring run test: {}".format(initfunc.__name__))

    ret = None
    if ns.repeat == 0:
        ret = actionfunc(ns)
    elif ns.repeat != -1:
        count = ns.repeat
        while count > 0:
            ret = actionfunc(ns)
            count -= 1
        return ret
    elif ns.repeat == -1:
        while True:
            ret = actionfunc(ns)

    print("finish test: {}".format(actionfunc.__name__))
    return ret

def pre_main(func):
    def inner_func():
        t = time.localtime()
        print("starting test on: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", t)))
        func()
    return inner_func

g_test_threads = []

def run_test(initfunc, actionfunc):
    global g_test_threads

    if initfunc == None or actionfunc == None:
        print("init or action is null, ignore this test")
        return

    t = threading.Thread(target = __run_test, args = (initfunc, actionfunc))
    g_test_threads.append(t)
    t.start()

def append_thread(t):
    if t == None:
        return
    g_test_threads.append(t)
    t.start()

def end_test():
    global g_test_threads

    for t in g_test_threads:
        t.join()
        g_test_threads.remove(t)

class android_device:
    def __init__(self):
        self.device = None
        self.serialno = None
        self.ip = None
        self.TAG = "TestAction"

    def open(self, serialno):
        self.serialno = serialno

        d = adbutils.adb.device_list()

        if len(d) == 1:
            self.device = adbutils.adb.device()

        if serialno != None:
            try:
                ip = ipaddress.ip_address(serialno)
                adbutils.adb.connect(ip)
                self.device = adbutils.adb.device(serial = '{}:5555'.format(ip))
            except ValueError:
                self.device = adbutils.adb.device(serial = serialno)
            except:
                return

    def close(self):
        self.device = None
        self.serialno = None
        self.ip = None
        self.TAG = "TestAction"
    
    def abs_event(self, *args):
        if self.device == None:
            raise Exception("device is null")
        
        cmd = "sendevent "
        for i in range(0, len(args)):
            cmd = cmd + args[i] + " "
        
        self.device.shell(cmd)

    def ip_info(self, iface):
        if self.device == None:
            raise Exception("device is null")

        res = self.device.shell("ip addr show {} | grep \"inet \"".format(iface))

        if len(res) != 0:
            items = res.split()
            res = items[1].split('/')[0]

        self.ip = res
        return res

    def enable_tcpip(self):
        if self.device == None:
            raise Exception("device is null")

        self.device.tcpip(5555)

    def reconnect_ip(self):
        if self.device == None or self.ip == None:
            print("no device or ip information")
            return
        
        enable_tcpip(self)
        open(self, self.ip)
    
    def info(self):
        if self.serialno == None:
            print("no serial information")
        
        print("serial: {}".format(self.serialno))
        return self.serialno
    
    def center_key(self):
        if self.device == None:
            raise Exception("device is null")

        self.device.shell("input keyevent 149")

    def touch_tap(self, x, y):
        if self.device == None:
            raise Exception("device is null")

        self.device.shell("input touchscreen tap {} {}".format(x, y))

    def shell(self, *args):
        if self.device == None:
            raise Exception("device is null")

        return self.device.shell(*args)

    def shell2(self, *args):
        if self.device == None:
            raise Exception("device is null")

        return self.device.shell2(*args)

    def log_message(self, msg):
        if self.device == None:
            raise Exception("device is null")

        self.device.shell("log -pi -t {} \"{}\"".format(self.TAG, msg))

    def push_file(self, source: str, dest: str):
        if self.device == None:
            raise Exception("device is null")
        if source == None or source == "":
            return
        if dest == None or dest == "":
            return

        srcpath = "{}/testcases/files/{}".format(pathlib.Path().resolve(), source)
        if not exists(srcpath):
            print("{} is not exists".format(srcpath))
            return

        self.device.sync.push(srcpath, dest)

    def root(self):
        if self.device == None:
            raise Exception("device is null")

        self.device.root()
        time.sleep(1.2)
        if self.ip == None:
            self.open(self.serialno)
        else:
            reconnect_ip()

class logi_android(android_device):
    def disalbe_whitelist(self):
        if self.device == None:
            raise Exception("device is null")
        
        self.root()
        self.device.shell("setprop persist.logitech.platform.security.app_whitelist_enable false")
