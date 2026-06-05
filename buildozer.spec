[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ⚠️ यहाँ हमने वर्शन्स को एकदम सटीक और स्थिर (Stable) कर दिया है ताकि Gradle फेल न हो
requirements = python3, kivy==2.3.0, kivymd==1.2.0, plyer, requests, urllib3, idna, charset-normalizer, certifi

orientation = portrait
fullscreen = 0

# एंड्रॉइड परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# ⚠️ 2026 के लेटेस्ट एंड्रॉइड स्टैंडर्ड्स के अनुसार सेटिंग्स
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
