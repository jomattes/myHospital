from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem, OneLineListItem
from helpers import GetHCData

# def get_hospitals(params, limit=50):
#     hc_url = 'https://data.medicare.gov/resource/ynj2-r877.json?'
#     cnt = 0
#     for i, j in params.items():
#         if j != None:
#             if cnt < len(params):
#                 hc_url = hc_url + str(i) + '=' + str(j) + '&'
#             else:
#                 hc_url = hc_url + str(i) + '=' + str(j)
#         cnt += 1
#     hc_url = hc_url + '&$limit=' + str(limit)
#     response = requests.get(hc_url)
#     return response.json()

# params = {
#     'provider_id': None,
#     'hospital_name': None,
#     'address': None,
#     'city': "PORTLAND",
#     'state': "OR",
#     'zip_code': None,
#     'county_name': None,
#     'phone_number': None,
#     'measure_id': None,
#     'measure_name': None,
#     'compared_to_national': None,
#     'denominator': None,
#     'score': None,
#     'lower_estimate': None,
#     'higher_estimate': None,
#     'measure_start_date': None,
#     'measure_end_date': None
# }

# KIVY APP BUILD
#====================================================================================
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

    # def get_hc_params(self, new_params=None):
    #     if new_params == None:
    #         # FIXME change to load default params only if new ones have not been added yet
    #         self.params = params
    #     else:
    #         # FIXME change to update only specific params in the dict
    #         self.params = new_params

    # def get_hc_data(self, params):
    #     self.hc_data = get_hospitals(params=self.params)

    # def get_hc_measures(self):
    #     pass

class MenuScreen(Screen):
    pass

class SearchScreen(Screen):
    pass

class LocationScreen(Screen):
    pass

class MeasureScreen(Screen):
    def add_meas_list(self):
        # hc_data = get_hospitals(params=params)
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
        # hc_data = get_hospitals(params=params)
        hc_data = HCData.get_hc_data()
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