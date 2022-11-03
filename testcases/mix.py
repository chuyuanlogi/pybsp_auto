import common as c

from adbutils import adb
import threading
import time
import random
from types import SimpleNamespace as sns

tc_id = "1.1.1 - on/off audio and video with randomly remove external camera/audio device"

auth = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxOTY4NmQ2MjNlY2Y0MTMzYTkxYjAzNzM3ODY0ZjNiYSIsImlhdCI6MTY2MDM4NjI2MiwiZXhwIjoxOTc1NzQ2MjYyfQ.Ex7iKb7pCHusJPUKIaKsT0iZVZWqROztue7UKdkg-6E"
url = "192.168.10.10"

def meetup_power_init():
    ns = sns()
    ns.repeat = 15
    ns.ha = c.iot.hass()
    ns.ha.set_auth(auth)
    ns.ha.set_url(url)
    ns.d = c.atari.dev()
    ns.d.open("2129FDJS9QG2")
    return ns

def meetup_power_action(ns):
    time.sleep(random.uniform(59, 67))
    ns.d.log_message("trun off meetup")
    ns.ha.switch("switch.zhong_jian_dian_shan", False)
    time.sleep(0.5)
    ns.d.log_message("trun on meetup")
    ns.ha.switch("switch.zhong_jian_dian_shan", True)

def av_process_init():
    ns = sns()
    ns.repeat = 180
    ns.d = c.atari.dev()
    ns.d.open("2129FDJS9QG2")
    return ns

def av_process_action(ns):
    time.sleep(1)
    ns.d.meeting_onoff_mute()
    ns.d.meeting_onoff_video()
    time.sleep(3)

def run():
    c.run_test(initfunc = meetup_power_init, actionfunc = meetup_power_action)
    c.run_test(initfunc = av_process_init, actionfunc = av_process_action)
    c.end_test()

def test():
    print("yes {}".format(123))

if __name__ == '__main__':
    run()