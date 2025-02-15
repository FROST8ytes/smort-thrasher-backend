import scikit-learn as sklearn
import numpy as np
import pandas as pd
from datetime import datetime

# key features, cyclical linear correlation ( reset after certain level)
class SmortML:
    def __init__(self, trash_level_dict:dict, sensor_ID:int):
        self.trash_level_dict = trash_level_dict
        self.sensor_ID = sensor_ID
        
        # not completed yet for now Convert the dictionary to a pandas DataFrame 
        self.data = pd.DataFrame(list(trash_level_dict.items()), columns=['timestamp', 'level'])
    def train(self):
       
   
        pass

    def predict(self, input_data):
     
        pass

    def evaluate(self):
      
        pass



if name == "__main__":
    db=Database()
    dataRow=db.get_sensor_record(1)
    

    sensor=smortML(trash_level_dict, sensor_ID)
    pass