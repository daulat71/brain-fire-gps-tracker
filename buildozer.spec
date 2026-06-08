[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# रिक्वायरमेंट्स को बिना फिक्स वर्जन के रखा ताकि वो लेटेस्ट बिल्ड टूल्स के साथ सेट हो सकें
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, plyer, requests, urllib3, openssl, certifi

orientation = portrait
fullscreen = 0

# परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, FOREGROUND_SERVICE_LOCATION, POST_NOTIFICATIONS

# सबसे स्थिर आर्किटेक्चर सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True

# शुरुआत के लिए सिर्फ arm64-v8a रखें ताकि बिना किसी एरर के एक बार APK बन जाए
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
