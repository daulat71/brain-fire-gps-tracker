[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# फालतू की भारी लाइब्रेरी हटाकर केवल सटीक आवश्यकताओं को रखा है
requirements = python3, kivy==2.3.0, kivymd==1.2.0, plyer, requests

orientation = portrait
fullscreen = 0

# आवश्यक परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# ⚠️ उबंटू सर्वर पर कंपाइलेशन को फ़ास्ट और एरर-फ़्री बनाने के लिए सटीक API सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
