from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from helpers import GetHCData, get_state_codes

from kivy.clock import Clock

from kivy.logger import Logger
Logger.info('Load Logger')



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

    def update_state_param(self):
        # updates HCData with selected item
        HCData.update_hc_params({'state': self.text})
        HCData.send_hc_request()


class LocationScreen(Screen):
    # def close_dialog(self, press):
    #     # self.dialog.close()
    #     if press == 'ok':
    #         HCData.send_hc_request()

    def add_state_codes(self):
        states = get_state_codes()

        self.dialog = MDDialog(
            title='Select State',
            type='confirmation',
            items= [ItemConfirm(text=state) for state in states],
            buttons=[
                MDFlatButton(text='CANCEL'),
                MDFlatButton(text='OK')
            ]
        )
        self.dialog.open()

    # def ok_press(self):
    #     self.dialog.close()

    # def cancel_press(self):
    #     pass

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