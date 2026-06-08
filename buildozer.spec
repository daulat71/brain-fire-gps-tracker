[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# आवश्यक रिक्वायरमेंट्स (यह बिल्कुल सही हैं)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, plyer, requests, urllib3, openssl, certifi

orientation = portrait
fullscreen = 0

# एंड्रॉइड परमिशन्स (लोकेशन और बैकग्राउंड सर्विस के लिए सही हैं)
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, FOREGROUND_SERVICE_LOCATION, POST_NOTIFICATIONS

# गिटहब रनर के अनुसार स्टेबल एपीआई सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21

# ध्यान दें: हमने 'android.ndk' को हटा दिया है ताकि उपयुक्त वर्ज़न अपने आप डाउनलोड हो सके।
# ध्यान दें: हमने 'sdk_path' और 'ndk_path' की खाली लाइनों को हटा दिया है ताकि एरर न आए।

android.private_storage = True
android.accept_sdk_license = True

# आर्किटेक्चर सेटिंग्स (64-bit आधुनिक फोन के लिए सही है)
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
