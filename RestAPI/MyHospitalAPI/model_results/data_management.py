from model_results.models import Results
from model_results.serializers import ResultSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import pandas as pd

# load data in loop
def load_row(row):
    provider_id = row['provider_id']
    measure_id = row['measure_id']
    performance_class = row['performance_class']

    result = Results(provider_id=provider_id,
                     measure_id=measure_id,
                     performance_class=performance_class)
    result.save()

def data_load():
    data_dir = 'D:/Dropbox/Northwestern/Capstone/model_data/'
    f_path = data_dir + 'test_model_results_data.csv'
    model_data = pd.read_csv(f_path)

    model_data.apply(lambda x: load_row(x), axis=1)


# to run the above:
"""
run python manage.py shell
from data_management import data_load
data_load()

Be sure to update the model data!
"""
# to delete the database:
"""
run python manage.py flush 
"""