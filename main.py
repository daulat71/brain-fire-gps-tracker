import os
import json
import threading
import requests
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore

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
        
        # एंड्रॉइड के लिए सुरक्षित स्टोरेज पाथ
        if platform == 'android':
            from android.storage import app_context
            data_dir = app_context().getFilesDir().getAbsolutePath()
            store_path = os.path.join(data_dir, 'user_config.json')
        else:
            store_path = 'user_config.json'
            
        self.store = JsonStore(store_path)
        self.tracking_active = False
        self.current_lat = 24.5854
        self.current_lon = 73.7125

        self.main_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # सुधार १: एंड्रॉइड परमिशन्स को सही और सुरक्षित तरीके से लोड करना
        if platform == 'android':
            try:
                # POST_NOTIFICATIONS को स्ट्रिंग के रूप में सुरक्षित तरीके से पास किया ताकि पुराना SDK क्रैश न हो
                request_permissions([
                    Permission.ACCESS_FINE_LOCATION, 
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.FOREGROUND_SERVICE,
                    "android.permission.POST_NOTIFICATIONS"
                ])
            except Exception as e:
                print(f"Permission Request Error: {e}")
        
        if self.store.exists('user'):
            self.show_tracking_screen()
        else:
            self.show_registration_screen()
            
        return self.main_layout

    def show_registration_screen(self):
        self.main_layout.clear_widgets()
        
        title = MDLabel(text="Engineer Registration", halign="center")
        title.font_style = "H5"
        self.main_layout.add_widget(title)
        
        # KivyMD 1.2.0 के अनुकूल आउटलाइन टेक्सटफ़ील्ड्स
        self.name_input = MDTextField(hint_text="Enter Your Full Name", mode="outline", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.phone_input = MDTextField(hint_text="Enter Mobile Number", mode="outline", input_filter="int", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        
        self.ip_input = MDTextField(
            hint_text="Enter Django Server IP", 
            mode="outline",
            size_hint_x=0.9, 
            pos_hint={'center_x': 0.5}
        )
        self.ip_input.text = "192.168.100.66:8000"
        
        reg_btn = MDRaisedButton(
            text="Confirm & Save", 
            pos_hint={'center_x': 0.5},
            on_release=self.register_user
        )
        
        self.main_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.phone_input)
        self.main_layout.add_widget(self.ip_input)
        self.main_layout.add_widget(reg_btn)

    def register_user(self, *args):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        django_ip = self.ip_input.text.strip()
        
        if name and phone and django_ip:
            if not django_ip.startswith("http://") and not django_ip.startswith("https://"):
                django_ip = "http://" + django_ip
            if not django_ip.endswith("/"):
                django_ip = django_ip + "/"
                
            final_url = f"{django_ip}api/log-location/"
            self.store.put('user', name=name, phone=phone, server_url=final_url)
            self.show_tracking_screen()
        else:
            print("Error: Fill all details")

    def show_tracking_screen(self):
        self.main_layout.clear_widgets()
        
        user_data = self.store.get('user')
        self.user_name = user_data['name']
        self.user_phone = user_data['phone']
        self.django_url = user_data['server_url']

        welcome_lbl = MDLabel(text=f"Welcome, {self.user_name}", halign="center")
        welcome_lbl.font_style = "H6"
        self.main_layout.add_widget(welcome_lbl)
        
        self.status_label = MDLabel(text="Status: Ready", halign="center", theme_text_color="Hint")
        
        clean_ip = self.django_url.replace("http://", "").replace("/api/log-location/", "")
        self.gps_label = MDLabel(
            text=f"Phone: {self.user_phone}\nServer: {clean_ip}\nGPS: Ready to track", 
            halign="center"
        )
        
        self.start_btn = MDRaisedButton(text="Start Sharing Location", size_hint=(1, None), on_release=self.start_tracking)
        
        # सुधार २: KivyMD 1.2.0 में कलर सेटिंग्स को टुपल/लिस्ट फॉर्मेट में सुरक्षित किया
        self.stop_btn = MDRaisedButton(text="Stop Sharing", size_hint=(1, None), md_bg_color=[1, 0, 0, 1], on_release=self.stop_tracking)
        
        reset_btn = MDRaisedButton(
            text="Change IP / Settings", 
            size_hint=(0.6, None), 
            pos_hint={'center_x': 0.5},
            md_bg_color=[0.5, 0.5, 0.5, 1], 
            on_release=self.reset_settings
        )
        
        self.main_layout.add_widget(self.status_label)
        self.main_layout.add_widget(self.gps_label)
        self.main_layout.add_widget(self.start_btn)
        self.main_layout.add_widget(self.stop_btn)
        self.main_layout.add_widget(reset_btn)

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
            
            # पुराना शेड्यूल हटाया ताकि डुप्लीकेट न बने, फिर फ्रेश शेड्यूल किया
            Clock.unschedule(self.trigger_network_thread)
            Clock.schedule_interval(self.trigger_network_thread, 5)

    def on_gps_location(self, **kwargs):
        # थ्रेड से आने वाले डेटा को मुख्य थ्रेड पर सुरक्षित रूप से अपडेट करना
        Clock.schedule_once(lambda dt: self._update_gps_ui(kwargs))

    def _update_gps_ui(self, kwargs):
        self.current_lat = kwargs.get('lat', self.current_lat)
        self.current_lon = kwargs.get('lon', self.current_lon)
        clean_ip = self.django_url.replace("http://", "").replace("/api/log-location/", "")
        self.gps_label.text = f"Phone: {self.user_phone}\nServer: {clean_ip}\nGPS: {self.current_lat}, {self.current_lon}"

    def trigger_network_thread(self, dt):
        if self.tracking_active:
            payload = {
                "phone": str(self.user_phone),
                "lat": str(self.current_lat),
                "lon": str(self.current_lon)
            }
            # बैकग्राउंड थ्रेड में रिक्वेस्ट भेजना ताकि UI हैंग न हो
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
        self.stop_tracking()
        if self.store.exists('user'):
            self.store.delete('user')
        self.show_registration_screen()

if __name__ == '__main__':
    GPSTrackerApp().run()
