from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
import requests

KV = """

"""

KV = """
<ContentNavigationDrawer>:

    ScrollView:

        MDList:

            OneLineListItem:
                text: 'Screen 1'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'scr 1'

            OneLineListItem:
                text: 'Screen 2'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'scr 2'


Screen:

    MDToolbar:
        id: toolbar
        pos_hint: {'top': 1}
        elevation: 10
        title: 'MDNavigationDrawer'
        left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]

    NavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager
            pos_hint:{'top': 0.88}

            Screen:
                name: 'scr 1'

                ScrollView:

                    MDList:
                        id: container

            Screen:
                name: 'scr 2'

                MDLabel:
                    text: 'Screen 2'
                    halign: 'center'

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
"""

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()



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
    print(hc_url)
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

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        hc_data = get_hospitals(params)
        for hosp in hc_data:
            self.root.ids.container.add_widget(
                ThreeLineListItem(text=hosp['hospital_name'],
                                  secondary_text=hosp['address'],
                                  tertiary_text= '{}, {} {}'.format(\
                                      hosp['city'], hosp['state'], hosp['zip_code'])
                                 )
            )

MainApp().run()