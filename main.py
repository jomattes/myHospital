from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from helpers import GetHCData, get_state_codes

from kivy.clock import Clock

from kivy.logger import Logger
Logger.info('Load Logger')

# globals
global_state = None



# KIVY APP BUILD
#====================================================================================
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

class MenuScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        # adds check mark to selected items
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        
        # updates global state value
        global global_state
        global_state = self.text

class DialogContent(BoxLayout):
    # allows for blank box in text-entry dialogs, see kivy file for formatting
    pass


class LocationScreen(Screen):
    def add_state_dialog(self):
        # popup to select state code
        states = get_state_codes()

        self.dialog = MDDialog(
            title='State',
            type='confirmation',
            items= [ItemConfirm(text=state) for state in states],
            buttons=[
                MDFlatButton(text='CANCEL', on_release=self.close_dialog),
                MDFlatButton(text='OK', on_release=self.update_state_param)
            ]
            )
        self.dialog.set_normal_height()
        self.dialog.open()

    def add_city_dialog(self):
        # popup to enter city name
        self.dialog = MDDialog(
            title='City',
            type='custom',
            content_cls=DialogContent(),
            buttons=[
                MDFlatButton(text='CANCEL', on_release=self.close_dialog),
                MDFlatButton(text='OK', on_release=self.update_city_param)
            ]
            )
        self.dialog.set_normal_height()
        self.dialog.open()
    
    def grab_text(self, inst):
        # gets text from textbox in dialog popup
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                return obj.text

    def update_state_param(self, inst):
        # updates parameters based on add_state_dialog() option
        HCData.update_hc_params({'state': global_state})
        self.dialog.dismiss()

    def update_city_param(self, inst):
        # updates parameters based on add_city_dialog() option
        city_text = self.grab_text(inst)
        HCData.update_hc_params({'city': city_text})
        self.dialog.dismiss()

    def close_dialog(self, inst):
        # closes popup, used when CANCEL button is pressed
        self.dialog.dismiss()

class MeasureScreen(Screen):
    def add_meas_list(self):
        hc_data = HCData.get_hc_data()
        measure_list = []
        for hosp in hc_data:
            measure_list.append(hosp['measure_name'])
        measures = set(measure_list)
        for meas in measures:
            self.ids.meas_contain.add_widget(OneLineListItem(text=meas))


class ResultsScreen(Screen):
    pass

class HospitalScreen(Screen):
    # hospital_screen = ObjectProperty()
    
    def add_hosp_list(self):
        HCData.send_hc_request()
        hc_data = HCData.get_hc_data()

        self.ids.hosp_contain.clear_widgets()  # refreshes list

        for hosp in hc_data:
            self.ids.hosp_contain.add_widget(ThreeLineListItem(text=hosp['hospital_name'],
                                                            secondary_text=hosp['address'],
                                                            tertiary_text='{}, {} {}'.format(\
                                                                hosp['city'], hosp['state'], hosp['zip_code']),
                                                            on_release=self.switch_screen))
    
    def switch_screen(self, list_item):
        self.manager.current = 'detail_screen'
        self.manager.get_screen('detail_screen').ids.screen2_label.text = list_item.text

class DetailScreen(Screen):
    # detail_screen = ObjectProperty()

    def screen_switch_details(self):
        self.manager.current = 'hospital_screen'

class myHospitalApp(MDApp):
    def build(self):
        Builder.load_file('screen.kv')
        sm = MyScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen())
        sm.add_widget(SearchScreen())
        sm.add_widget(LocationScreen())
        sm.add_widget(MeasureScreen())
        sm.add_widget(ResultsScreen())
        sm.add_widget(HospitalScreen())
        sm.add_widget(DetailScreen())
        sm.current = 'menu_screen'
        return sm

if __name__ == '__main__':
    HCData = GetHCData()
    HCData.send_hc_request()

    myHospitalApp().run()

#====================================================================================