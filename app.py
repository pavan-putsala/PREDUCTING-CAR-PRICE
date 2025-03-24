import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st

# Load the trained model
model = pk.load(open('model.pkl', 'rb'))

st.header('Car Price Prediction ML Model')

# Load the dataset to extract valid feature names
cars_data = pd.read_csv('Cardetails_fixed.csv')

def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()

cars_data['name'] = cars_data['name'].apply(get_brand_name)

# User input fields
name = st.selectbox('Select Car Brand', cars_data['name'].unique())
year = st.slider('Car Manufactured Year', 1994, 2024)
km_driven = st.slider('No of kms Driven', 11, 200000)
fuel = st.selectbox('Fuel Type', cars_data['fuel'].unique())
seller_type = st.selectbox('Seller Type', cars_data['seller_type'].unique())
transmission = st.selectbox('Transmission Type', cars_data['transmission'].unique())
owner = st.selectbox('Owner Type', cars_data['owner'].unique())
mileage = st.slider('Car Mileage', 10.0, 40.0)
engine = st.slider('Engine CC', 700, 5000)
max_power = st.slider('Max Power', 0.0, 200.0)
seats = st.slider('No of Seats', 2, 10)

if st.button("Predict"):
    # Create a DataFrame with user input
    input_data_model = pd.DataFrame({
        'name': [name],
        'year': [year],
        'km_driven': [km_driven],
        'fuel': [fuel],
        'seller_type': [seller_type],
        'transmission': [transmission],
        'owner': [owner],
        'mileage': [mileage],
        'engine': [engine],
        'max_power': [max_power],
        'seats': [seats]
    })
    
    # Apply one-hot encoding to match training data
    input_data_model = pd.get_dummies(input_data_model)
    
    # Ensure the input features match the model's trained features
    for col in model.feature_names_in_:
        if col not in input_data_model.columns:
            input_data_model[col] = 0  # Add missing columns with default value
    
    # Reorder columns to match training data
    input_data_model = input_data_model[model.feature_names_in_]
    
    # Predict the price
    car_price = model.predict(input_data_model)
    
    st.markdown(f'Predicted Car Price: ₹{car_price[0]:,.2f}')
