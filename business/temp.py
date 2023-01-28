import json
import pickle
import numpy as np
model = pickle.load(open('model/modell.pkl','rb'))



f1 = open('model/country.json')
country = json.load(f1)

f2 = open('model/data.json')
data = json.load(f2)




def calculate(country1 , country2):
    
    country1_code = country[country1]
    distance = data[country2][country1_code]
    return distance



def predict_price(quantity, volume, distance):

    quantity = float(quantity)
    volume = float(volume)
    distance = float(distance)

    fv = [quantity,volume,distance]
    fv = np.array(fv).reshape((1,-1))
    p = model.predict(fv)
    
    return p
