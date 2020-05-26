import requests

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
        self.limit = 50

    def update_hc_params(self, new_params):
        self.params.update(new_params)

    def send_hc_request(self, hcahps=False):
        if hcahps:
            hc_url = 'https://data.medicare.gov/resource/dgck-syfz.json?'
        else:
            hc_url = 'https://data.medicare.gov/resource/ynj2-r877.json?'
        cnt = 0
        for i, j in self.params.items():
            if j != None:
                if cnt < len(self.params):
                    hc_url = hc_url + str(i) + '=' + str(j) + '&'
                else:
                    hc_url = hc_url + str(i) + '=' + str(j)
            cnt += 1
        hc_url = hc_url + '&$limit=' + str(self.limit)
        response = requests.get(hc_url)
        self.hc_data = response.json()

    def get_hc_data(self):
        return self.hc_data

def get_state_codes():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def get_comp_measures():
    return {
        'MORT_30_PN': 'Death rate for pneumonia patients',
        'MORT_30_STK': 'Death rate for stroke patients',
        'MORT_30_AMI': 'Death rate for heart attack patients',
        'COMP_HIP_KNEE': 'Rate of complications for hip/knee replacement patients',
        'MORT_30_HF': 'Death rate for heart failure patients',
        'MORT_30_CABG': 'Death rate for CABG surgery patients',
        'PSI_90_SAFETY': 'Serious complications',
        'PSI_3_ULCER': 'Pressure sores',
        'PSI_13_POST_SEPSIS': 'Blood stream infection after surgery',
        'PSI_12_POSTOP_PULMEMB_DVT': 'Serious blood clots after surgery',
        'PSI_14_POSTOP_DEHIS': 'A wound that splits open after surgery on the abdomen or pelvis',
        'PSI_4_SURG_COMP': 'Deaths among Patients with Serious Treatable Complications after Surgery',
        'PSI_15_ACC_LAC': 'Accidental cuts and tears from medical treatment',
        'PSI_6_IAT_PTX': 'Collapsed lung due to medical treatment',
        'MORT_30_COPD': 'Death rate for COPD patients',
        'PSI_9_POST_HEM': 'Perioperative Hemorrhage or Hematoma Rate',
        'PSI_11_POST_RESP': 'Postoperative Respiratory Failure Rate',
        'PSI_10_POST_KIDNEY': 'Postoperative Acute Kidney Injury Requiring Dialysis Rate',
        'PSI_8_POST_HIP': 'Broken hip from a fall after surgery'
    }