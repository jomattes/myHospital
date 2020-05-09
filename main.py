from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
import requests

def get_hospitals(params, limit=50):
    hc_url = 'https://data.medicare.gov/resource/ynj2-r877.json?'
    cnt = 0
    for i, j in params.items():
        if j != None:
            if cnt < len(params):
                hc_url = hc_url + str(i) + '=' + str(j) + '&'
            else:
                hc_url = hc_url + str(i) + '=' + str(j)
        cnt += 1
    hc_url = hc_url + '&$limit=' + str(limit)
    response = requests.get(hc_url)
    return response.json()

params = {
    'provider_id': None,
    'hospital_name': None,
    'address': None,
    'city': "PORTLAND",
    'state': "OR",
    'zip_code': None,
    'county_name': None,
    'phone_number': None,
    'measure_id': "MORT_30_PN",
    'measure_name': None,
    'compared_to_national': None,
    'denominator': None,
    'score': None,
    'lower_estimate': None,
    'higher_estimate': None,
    'measure_start_date': None,
    'measure_end_date': None
}

# KIVY APP BUILD
#====================================================================================
class MenuScreen(Screen):
    pass

class SearchScreen(Screen):
    pass
    
    
    
    # def add_params_list(self, params=params):
    #     for param, value in params.items():
    #         self.ids.box.add_widget(MDExpansionPanel(
    #             content=,
    #             panel_cls=MDExpansionPanelOneLine(
    #                 text=param
    #             )
    #         )
    #     )

    

class HospitalScreen(Screen):
    # hospital_screen = ObjectProperty()
    
    def add_hosp_list(self):
        hc_data = get_hospitals(params=params)
        for hosp in hc_data:
            self.ids.container.add_widget(ThreeLineListItem(text=hosp['hospital_name'],
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
        sm = ScreenManager()
        sm.add_widget(MenuScreen())
        sm.add_widget(SearchScreen())
        sm.add_widget(HospitalScreen())
        sm.add_widget(DetailScreen())
        sm.current = 'menu_screen'
        return sm

if __name__ == '__main__':
    myHospitalApp().run()

#====================================================================================