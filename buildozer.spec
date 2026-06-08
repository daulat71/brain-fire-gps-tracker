[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# आवश्यक रिक्वायरमेंट्स - (इसे एक ही लाइन में बिना किसी स्पेस के रखें)
requirements = python3,kivy,kivymd==1.2.0,pillow,plyer,requests

orientation = portrait
fullscreen = 0

# एंड्रॉइड परमिशन्स
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,FOREGROUND_SERVICE,FOREGROUND_SERVICE_LOCATION,POST_NOTIFICATIONS

# गिटहब के लेटेस्ट रनर के अनुसार सेटिंग्स
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True

# आर्किटेक्चर सेटिंग्स
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
