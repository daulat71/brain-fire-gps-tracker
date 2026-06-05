import os
# पीसी पर टेस्टिंग के लिए बैकएंड सेट करना
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

import json
import threading
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
import requests

# एंड्रॉइड पर परमिशन और जीपीएस चेक करने के लिए
if platform == 'android':
    from android.permissions import request_permissions, Permission
    try:
        from plyer import gps
    except ImportError:
        gps = None
else:
    gps = None

class GPSTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        
        # फोन मेमोरी में डेटा स्टोर करने के लिए फाइल
        self.store = JsonStore('user_config.json')
        self.tracking_active = False
        
        # डिफॉल्ट कोडिनेट्स (उदयपुर का शुरुआती डेटा)
        self.current_lat = 24.5854
        self.current_lon = 73.7125

        self.main_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # अगर एंड्रॉइड है तो ऐप खुलते ही परमिशन मांगो
        if platform == 'android':
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])
        
        # यूजर और आईपी पहले से मौजूद है या नहीं चेक करें
        if self.store.exists('user'):
            self.show_tracking_screen()
        else:
            self.show_registration_screen()
            
        return self.main_layout

    def show_registration_screen(self):
        """पहली बार ऐप खुलने पर रजिस्ट्रेशन और आईपी कॉन्फ़िगरेशन फॉर्म"""
        self.main_layout.clear_widgets()
        
        title = MDLabel(text="Engineer Registration", halign="center")
        title.font_style = "H5"
        self.main_layout.add_widget(title)
        
        self.name_input = MDTextField(hint_text="Enter Your Full Name", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.phone_input = MDTextField(hint_text="Enter Mobile Number", input_filter="int", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        
        # 👈 नया बॉक्स: कंप्यूटर/जंगो सर्वर का आईपी डालने के लिए
        self.ip_input = MDTextField(
            hint_text="Enter Django Server IP (e.g. 192.168.100.66:8000)", 
            size_hint_x=0.9, 
            pos_hint={'center_x': 0.5}
        )
        # पहले से पुराना आईपी याद दिलाने के लिए डिफॉल्ट वैल्यू सेट कर दी है
        self.ip_input.text = "192.168.100.66:8000"
        
        reg_btn = MDRaisedButton(
            text="Confirm & Save", 
            pos_hint={'center_x': 0.5},
            on_release=self.register_user
        )
        
        self.main_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.phone_input)
        self.main_layout.add_widget(self.ip_input) # आईपी इनपुट को स्क्रीन पर जोड़ा
        self.main_layout.add_widget(reg_btn)

    def register_user(self, *args):
        """यूजर का डेटा और आईपी एड्रेस सेव करना"""
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        django_ip = self.ip_input.text.strip()
        
        if name and phone and django_ip:
            # आईपी को साफ करके यूआरएल फॉर्मेट में बदलना
            if not django_ip.startswith("http://") and not django_ip.startswith("https://"):
                django_ip = "http://" + django_ip
            if not django_ip.endswith("/"):
                django_ip = django_ip + "/"
                
            final_url = f"{django_ip}api/log-location/"
            
            # डेटाबेस (JsonStore) में सेव करें
            self.store.put('user', name=name, phone=phone, server_url=final_url)
            self.show_tracking_screen()
        else:
            print("Error: Fill all details")

    def show_tracking_screen(self):
        """ट्रैकिंग कंट्रोल स्क्रीन"""
        self.main_layout.clear_widgets()
        
        user_data = self.store.get('user')
        self.user_name = user_data['name']
        self.user_phone = user_data['phone']
        self.django_url = user_data['server_url'] # 👈 मेमोरी से यूआरएल निकाला

        welcome_lbl = MDLabel(text=f"Welcome, {self.user_name}", halign="center")
        welcome_lbl.font_style = "H6"
        self.main_layout.add_widget(welcome_lbl)
        
        self.status_label = MDLabel(text="Status: Ready", halign="center", theme_text_color="Hint")
        
        # यह दिखाने के लिए कि डेटा किस आईपी पर जा रहा है
        clean_ip = self.django_url.replace("http://", "").replace("/api/log-location/", "")
        self.gps_label = MDLabel(
            text=f"Phone: {self.user_phone}\nServer: {clean_ip}\nGPS: Ready to track", 
            halign="center"
        )
        
        self.start_btn = MDRaisedButton(text="Start Sharing Location", size_hint=(1, None), on_release=self.start_tracking)
        self.stop_btn = MDRaisedButton(text="Stop Sharing", size_hint=(1, None), md_bg_color=(1, 0, 0, 1), on_release=self.stop_tracking)
        
        # ऐप के अंदर से ही आईपी रीसेट/चेंज करने के लिए एक बटन (ताकि ऐप अनइंस्टॉल न करना पड़े)
        reset_btn = MDRaisedButton(
            text="Change IP / Settings", 
            size_hint=(0.6, None), 
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.5, 0.5, 0.5, 1), 
            on_release=self.reset_settings
        )
        
        self.main_layout.add_widget(self.status_label)
        self.main_layout.add_widget(self.gps_label)
        self.main_layout.add_widget(self.start_btn)
        self.main_layout.add_widget(self.stop_btn)
        self.main_layout.add_widget(reset_btn) # रीसेट बटन जोड़ा

    def start_tracking(self, *args):
        if not self.tracking_active:
            self.tracking_active = True
            if platform == 'android' and gps:
                try:
                    gps.configure(on_location=self.on_gps_location)
                    gps.start(minTime=5000, minDistance=1)
                    self.status_label.text = "Status: Live GPS Tracking ON"
                except Exception as e:
                    self.status_label.text = f"GPS Error: {str(e)}"
            else:
                self.status_label.text = "Status: PC Test Mode (Sending Default GPS)"
            
            Clock.schedule_interval(self.trigger_network_thread, 5)

    def on_gps_location(self, **kwargs):
        self.current_lat = kwargs.get('lat', self.current_lat)
        self.current_lon = kwargs.get('lon', self.current_lon)
        clean_ip = self.django_url.replace("http://", "").replace("/api/log-location/", "")
        self.gps_label.text = f"Phone: {self.user_phone}\nServer: {clean_ip}\nGPS: {self.current_lat}, {self.current_lon}"

    def trigger_network_thread(self, dt):
        if self.tracking_active:
            payload = {
                "phone": self.user_phone,
                "lat": str(self.current_lat),
                "lon": str(self.current_lon)
            }
            threading.Thread(target=self.send_data_to_django, args=(payload,), daemon=True).start()

    def send_data_to_django(self, payload):
        try:
            response = requests.post(self.django_url, json=payload, headers={"Content-Type": "application/json"}, timeout=4)
            if response.status_code in [200, 201]:
                print(f"Location Synced for {payload['phone']}")
            else:
                print(f"Server Error: {response.status_code}")
        except Exception as e:
            print(f"Network Connection Error: {e}")

    def stop_tracking(self, *args):
        if self.tracking_active:
            Clock.unschedule(self.trigger_network_thread)
            if platform == 'android' and gps:
                try:
                    gps.stop()
                except:
                    pass
            self.tracking_active = False
            self.status_label.text = "Status: Stopped"
            clean_ip = self.django_url.replace("http://", "").replace("/api/log-location/", "")
            self.gps_label.text = f"Phone: {self.user_phone}\nServer: {clean_ip}\nGPS: Off"

    def reset_settings(self, *args):
        """अगर भविष्य में आईपी बदलना हो, तो यह बटन डेटा डिलीट करके रजिस्ट्रेशन स्क्रीन पर ले जाएगा"""
        self.stop_tracking()
        self.store.delete('user')
        self.show_registration_screen()

if __name__ == '__main__':
    GPSTrackerApp().run()
