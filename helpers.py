import requests

def get_state_codes():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class GetHCData():
    def __init__(self):
        self.params = {
            'provider_id': None,
            'hospital_name': None,
            'address': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'county_name': None,
            'phone_number': None,
            'measure_id': None,
            'measure_name': None,
            'compared_to_national': None,
            'denominator': None,
            'score': None,
            'lower_estimate': None,
            'higher_estimate': None,
            'measure_start_date': None,
            'measure_end_date': None   
        }

    def update_hc_params(self, new_params):
        self.params.update(new_params)

    def send_hc_request(self, limit=50):
        hc_url = 'https://data.medicare.gov/resource/ynj2-r877.json?'
        cnt = 0
        for i, j in self.params.items():
            if j != None:
                if cnt < len(self.params):
                    hc_url = hc_url + str(i) + '=' + str(j) + '&'
                else:
                    hc_url = hc_url + str(i) + '=' + str(j)
            cnt += 1
        hc_url = hc_url + '&$limit=' + str(limit)
        response = requests.get(hc_url)
        self.hc_data = response.json()

    def get_hc_data(self):
        return self.hc_data