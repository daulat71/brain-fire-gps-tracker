[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# आवश्यक रिक्वायरमेंट्स
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, plyer, requests, urllib3, openssl, certifi

orientation = portrait
fullscreen = 0

# एंड्रॉइड परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, FOREGROUND_SERVICE_LOCATION, POST_NOTIFICATIONS

# गिटहब रनर के अनुसार स्टेबल सेटिंग्स (पाथ खाली रखें ताकि एनवायरनमेंट से लोड हो सके)
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True
android.sdk_path = 
android.ndk_path = 

# आर्किटेक्चर सेटिंग्स
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
