import streamlit as st
import pickle
import numpy as np
import json

st.title("Bengaluru Real Estate Price Predictor")

st.write("""
Enter values and get the predicted price of the house
"""
)

__locations = None
__data_columns = None
__model = None
__area = None

def get_estimated_price(area,location,sqft,bhk,bath,balcony):
    try:
        loc_index = __data_columns.index(location.lower()) #our column.json has columns in lowercase
        area_indec = __data_columns.index(area.lower())
    except:
        loc_index = -1
        area_indec = -1
    
    x = np.zeros(len(__data_columns))
    x[0] = int(sqft)
    x[1] = bath
    x[2] = balcony
    x[3] = bhk
    if loc_index >= 0 and area_indec >=0:
        x[loc_index] = 1
        x[area_indec] = 1
    return round(__model.predict([x])[0],2)


with open("columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']
    __locations = __data_columns[4:-3]  # first 3 columns are sqft, bath, bhk
    __area = __data_columns[len(__data_columns)-3:]
if __model is None:
    with open('banglore_home_prices_model.pickle', 'rb') as f:
        __model = pickle.load(f)
def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns
def get_areas():
    return __area

input = st.sidebar.empty()
sqft = input.text_input("Input Area(in square feet): ",1)
balcony = st.sidebar.selectbox("Number of balcony: ",[i for i in range(0,4)])
bath = st.sidebar.slider("Number of bathrooms:",1,10)
bhk = st.sidebar.selectbox("Number of BHK",[i for i in range(1,9)])
location = st.sidebar.selectbox("Locations:",get_location_names())
area = st.sidebar.selectbox("Area:",get_areas())


price = get_estimated_price(area,location,sqft,bhk,bath,balcony)

st.write(""" ## Predicted Price is  """,price,""" lakhs """)