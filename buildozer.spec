[app]
title = GPS Tracker
package.name = gpstracker
package.domain = org.daulat
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# सबसे महत्वपूर्ण सुधार: KivyMD का वह वर्जन जो कंपाइल होते समय क्रैश नहीं होता
requirements = python3, cython==0.29.36, kivy==2.3.0, https://github.com/kivymd/KivyMD/archive/master.zip, plyer, requests

orientation = portrait
fullscreen = 0

# एंड्रॉइड परमिशन्स
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# स्थिर (Stable) एंड्रॉइड सेटिंग्स
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
