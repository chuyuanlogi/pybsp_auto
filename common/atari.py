import sys
import adbutils
import common as c

class dev(c.logi_android):
    def new_call(self):
        c.logi_android.touch_tap(self, 780, 450)

    def join(self):
        c.logi_android.touch_tap(self, 960, 450)

    def meeting_onoff_mute(self):
        c.logi_android.touch_tap(self, 450, 270)

    def meeting_onoff_video(self):
        c.logi_android.touch_tap(self, 650, 270)