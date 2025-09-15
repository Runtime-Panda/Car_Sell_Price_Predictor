import streamlit as st
import pickle
import pandas as pd

# Load the model and feature names
model_data = pickle.load(open("car_model.pkl", "rb"))
model = model_data["model"]
feature_names = model_data["features"]

st.set_page_config(page_title="Car Selling Price Predictor", page_icon="🚗")
st.title("🚗 Car Selling Price Predictor")
st.markdown("Estimate the selling price of your car based on its features.")

# Input widgets
year = st.slider("Year of Manufacture", 2000, 2023, 2015)
present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=5.0)
kms_driven = st.number_input("Kilometers Driven", min_value=0, value=30000)
owner = st.slider("Number of Previous Owners", 0, 3, 0)
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# Encode categorical inputs
fuel = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}[fuel_type]
seller = {'Dealer': 0, 'Individual': 1}[seller_type]
trans = {'Manual': 0, 'Automatic': 1}[transmission]

# Create input DataFrame with correct feature order
input_data = pd.DataFrame([[year, present_price, kms_driven, owner, fuel, seller, trans]],
                          columns=feature_names)

# Prediction
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"💰 Estimated Selling Price: ₹{prediction:.2f} lakhs")

        # Feedback based on price
        if prediction < 3:
            st.write("🟢 Budget-friendly deal!")
        elif prediction < 8:
            st.write("🟡 Mid-range value. Consider mileage and condition.")
        else:
            st.write("🔴 Premium car! Make sure it’s worth the price.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")