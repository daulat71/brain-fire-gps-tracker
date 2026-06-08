[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# सुधार: KivyMD 1.2.0 और Kivy 2.3.0 के साथ कंपाइलेशन एरर रोकने के लिए सही रिक्वायरमेंट्स
requirements = python3==3.10.11, hostpython3==3.10.11, kivy==2.3.0, kivymd==1.2.0, pillow, plyer, requests, urllib3, openssl, certifi

orientation = portrait
fullscreen = 0

# आवश्यक एंड्रॉइड परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, FOREGROUND_SERVICE_LOCATION, POST_NOTIFICATIONS

# स्थिर एंड्रॉइड सेटिंग्स (Kivy 2.3.0 के लिए एकदम सही कॉम्बिनेशन)
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True

# शुरुआत में सिर्फ arm64-v8a रखें ताकि एरर ढूंढना और बिल्ड करना आसान हो (फास्ट बिल्ड)
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
