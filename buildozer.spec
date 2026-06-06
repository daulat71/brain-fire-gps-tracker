[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# आवश्यक लाइब्रेरीज़ (यह बिल्कुल सही हैं)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, plyer, requests

orientation = portrait
fullscreen = 0

# जीपीएस और इंटरनेट के लिए आवश्यक परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# एरर से बचने के लिए सटीक API और NDK सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21

# ⚠️ सबसे महत्वपूर्ण सुधार: कंपाइलेशन एरर को रोकने के लिए NDK 25b लॉक किया गया है
android.ndk = 25b

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
