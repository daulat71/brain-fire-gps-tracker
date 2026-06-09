import os
# Windows पर ग्राफिक्स एरर से बचने के लिए
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
import requests

# GPS लाइब्रेरी लोड करना
try:
    from plyer import gps
except ImportError:
    gps = None

class GPSTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        
        # मोबाइल में डेटा स्टोर करने के लिए सही रास्ता (Path) तय करना
        data_dir = self.user_data_dir
        self.store = JsonStore(os.path.join(data_dir, 'user_config.json'))
        
        self.tracking_active = False
        self.current_lat = 24.5854
        self.current_lon = 73.7125
        self.event = None 

        self.main_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # अगर डेटा पहले से है तो ट्रैकिंग स्क्रीन, नहीं तो सेटअप स्क्रीन
        if self.store.exists('user'):
            self.show_tracking_screen()
        else:
            self.show_setup_screen()
            
        return self.main_layout

    def show_setup_screen(self):
        """सेटिंग्स और रजिस्ट्रेशन स्क्रीन"""
        self.main_layout.clear_widgets()
        
        self.main_layout.add_widget(MDLabel(
            text="App Settings & Registration", 
            font_style="H5", 
            halign="center",
            size_hint_y=None, height=50
        ))
        
        # इनपुट फील्ड्स
        self.name_input = MDTextField(hint_text="Full Name", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.phone_input = MDTextField(hint_text="Mobile Number", input_filter="int", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.ip_input = MDTextField(text="192.168.100.66", hint_text="Django Server IP", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        
        # यहाँ बदलाव किया है: डिफ़ॉल्ट टाइम 5 से बदलकर 60 (1 मिनट) कर दिया है
        self.time_input = MDTextField(text="60", hint_text="Send Interval (Seconds)", input_filter="int", size_hint_x=0.9, pos_hint={'center_x': 0.5})
        
        save_btn = MDRaisedButton(
            text="Save Configuration", 
            pos_hint={'center_x': 0.5},
            on_release=self.save_settings
        )
        
        self.main_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.phone_input)
        self.main_layout.add_widget(self.ip_input)
        self.main_layout.add_widget(self.time_input)
        self.main_layout.add_widget(save_btn)

    def save_settings(self, *args):
        """डेटा को JsonStore में सेव करना"""
        name = self.name_input.text
        phone = self.phone_input.text
        ip = self.ip_input.text
        interval = self.time_input.text

        if name and phone and ip and interval:
            self.store.put('user', 
                           name=name, 
                           phone=phone,
                           ip=ip,
                           interval=int(interval))
            self.show_tracking_screen()
        else:
            print("All fields are required!")

    def show_tracking_screen(self):
        """मुख्य ट्रैकिंग स्क्रीन"""
        self.main_layout.clear_widgets()
        
        # स्टोर से डेटा लोड करना
        user_data = self.store.get('user')
        self.user_name = user_data['name']
        self.user_phone = user_data['phone']
        self.django_ip = user_data['ip']
        self.update_interval = user_data['interval']

        self.main_layout.add_widget(MDLabel(text=f"Welcome, {self.user_name}", font_style="H6", halign="center"))
        
        self.status_label = MDLabel(
            text=f"Server: {self.django_ip}\nInterval: {self.update_interval} sec\nStatus: Ready", 
            halign="center", 
            theme_text_color="Secondary"
        )
        
        self.start_btn = MDRaisedButton(text="START SHARING", size_hint=(1, None), on_release=self.start_tracking)
        self.stop_btn = MDRaisedButton(text="STOP SHARING", size_hint=(1, None), md_bg_color=(1, 0, 0, 1), on_release=self.stop_tracking)
        
        # वापस सेटिंग में जाने का बटन
        self.change_btn = MDFlatButton(
            text="Change IP or Settings", 
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.show_setup_screen()
        )

        self.main_layout.add_widget(self.status_label)
        self.main_layout.add_widget(self.start_btn)
        self.main_layout.add_widget(self.stop_btn)
        self.main_layout.add_widget(self.change_btn)

    def start_tracking(self, *args):
        if not self.tracking_active:
            self.tracking_active = True
            
            # GPS चालू करना (सिर्फ एंड्रॉइड पर काम करेगा)
            if platform == 'android' and gps:
                try:
                    gps.configure(on_location=self.on_gps_location)
                    gps.start()
                except Exception as e:
                    print(f"GPS Error: {e}")
            
            self.status_label.text = "Status: Tracking LIVE..."
            # टाइम इंटरवल के हिसाब से डेटा भेजना
            self.event = Clock.schedule_interval(self.send_data_to_django, self.update_interval)

    def on_gps_location(self, **kwargs):
        """GPS से लोकेशन मिलने पर अपडेट करना"""
        self.current_lat = kwargs.get('lat', self.current_lat)
        self.current_lon = kwargs.get('lon', self.current_lon)

    def send_data_to_django(self, dt):
        """Django सर्वर को डेटा भेजना"""
        if self.tracking_active:
            url = f"http://{self.django_ip}:8000/api/log-location/"
            payload = {
                "phone": self.user_phone,
                "lat": self.current_lat,
                "lon": self.current_lon
            }
            try:
                # यहाँ बदलाव किया है: टाइमआउट 3 से बढ़ाकर 55 सेकंड कर दिया है
                requests.post(url, json=payload, timeout=55)
                print(f"Location sent to {self.django_ip}")
            except:
                print("Network Error: Could not connect to Server")

    def stop_tracking(self, *args):
        """ट्रैकिंग रोकना"""
        if self.event:
            Clock.unschedule(self.event)
        
        if platform == 'android' and gps:
            gps.stop()
            
        self.tracking_active = False
        self.status_label.text = "Status: Stopped"

if __name__ == '__main__':
    GPSTrackerApp().run()
