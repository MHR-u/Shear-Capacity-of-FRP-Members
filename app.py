import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate Vn based on the provided conditions
def calculate_vn(b, d, a, a_d, fc, ρt, fƒ, Eƒ):
    if b <= 229.5:
        if a_d <= 3.25:
            Vn = 0.3499 * b + 0.1134 * d + 0.0262 * a - 38.0757 * a_d + 0.4744 * fc + 13.9273 * ρt - 0.0277 * fƒ + 0.4406 * Eƒ + 9.4873
        else:
            Vn = 0.1043 * b + 0.3369 * d - 0.0609 * a + 7.3607 * a_d + 0.0262 * fc + 12.2679 * ρt - 0.0043 * fƒ + 0.1629 * Eƒ - 59.5343
    else:
        if b <= 435:
            if d <= 237.5:
                Vn = 0.098 * b + 0.2522 * d - 0.0303 * a - 2.783 * a_d + 0.1203 * fc + 16.2091 * ρt - 0.0107 * fƒ + 0.3162 * Eƒ - 31.0511
            else:
                if d <= 318:
                    if ρt <= 1.44:
                        Vn = 0.1552 * b + 0.2537 * d - 0.059 * a - 2.783 * a_d + 0.0995 * fc + 23.5769 * ρt - 0.0107 * fƒ + 0.3925 * Eƒ - 26.8098
                    else:
                        Vn = 0.1552 * b + 0.2621 * d - 0.059 * a - 2.783 * a_d + 0.0731 * fc + 24.5878 * ρt - 0.0107 * fƒ + 0.3925 * Eƒ - 27.2859
                else:
                    Vn = 0.376 * b + 0.3502 * d - 0.0995 * a - 2.783 * a_d + 0.0731 * fc + 26.3319 * ρt - 0.0107 * fƒ + 0.4779 * Eƒ - 76.7875
        else:
            Vn = 0.0907 * b + 0.0731 * d + 0.0425 * a - 4.33 * a_d + 0.1026 * fc + 19.1667 * ρt - 0.0139 * fƒ + 0.6346 * Eƒ - 36.8616
    
    return Vn

# Streamlit app interface
st.set_page_config(
    page_title="Nominal Shear Strength (Vn) Calculator",
    page_icon="https://ars.els-cdn.com/content/image/1-s2.0-S2352012424006726-gr1.jpg",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f6;
        }
        .title-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }
        .title-text {
            font-size: 2.2rem;
            font-weight: bold;
            margin-right: 10px;
        }
        .image-container {
            margin-top: 10px;
        }
        .note-box {
            background-color: #e0f7fa;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
        }
        hr {
            border: none;
            height: 1px;
            background-color: #ddd;
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Stylish header with title and image
st.markdown("""
    <div class="title-container">
        <div class="title-text">Nominal Shear Strength (Vn) Calculator</div>
        <div class="image-container">
            <img src="https://ars.els-cdn.com/content/image/1-s2.0-S2352012424006726-gr1.jpg" width="120">
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

# Stylish Note Section
st.markdown("""
<div class="note-box">
    <strong>Note:</strong> The more accurate the output, the more inputs are within the MIN-MAX ranges shown.<br>
    <strong>Vn:</strong> Nominal Shear Strength of the section in (kN), calculated based on the provided parameters.
</div>
""", unsafe_allow_html=True)

# Get inputs from user
b = st.number_input("Width of the section (b) in mm", min_value=100, max_value=300, value=150)
d = st.number_input("Effective depth of the section (d) in mm", min_value=200, max_value=800, value=400)
a = st.number_input("Shear span (a) in mm", min_value=50, max_value=400, value=200)
a_d = st.number_input("Shear span-to-effective depth ratio (a/d)", min_value=2.47, max_value=3.43, value=2.8)
fc = st.number_input("Concrete compressive strength (fc) in MPa", min_value=19.2, max_value=93, value=30)
ρt = st.number_input("Reinforcement ratio (ρt) in %", min_value=0.11, max_value=4.12, value=1.5)
fƒ = st.number_input("FRP ultimate tensile strength (fƒ) in MPa", min_value=397, max_value=2840, value=1000)
Eƒ = st.number_input("FRP Young's modulus (Eƒ) in GPa", min_value=24.8, max_value=192, value=70)

# Allow the user to choose which variable to plot against Vn
plot_variable = st.selectbox("Select a variable to plot against Vn:", ["b", "d", "a", "a_d", "fc", "ρt", "fƒ", "Eƒ"])

# Convert Vn to N or kN
convert_units = st.radio("Convert Vn to:", ('kN', 'N'))

# Calculate Vn when button is pressed
if st.button("Calculate Vn"):
    if b > 0 and d > 0 and a > 0 and a_d > 0 and fc > 0 and ρt > 0 and fƒ > 0 and Eƒ > 0:
        Vn = calculate_vn(b, d, a, a_d, fc, ρt, fƒ, Eƒ)
        
        # Convert to N or kN
        if convert_units == 'N':
            Vn *= 1000  # Convert to N
        
        st.subheader(f"Calculated Vn: {Vn:.2f} {convert_units}")
        
        # Plotting Vn against the selected variable
        if plot_variable == "b":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b_val, d, a, a_d, fc, ρt, fƒ, Eƒ) for b_val in variable_values]
        elif plot_variable == "d":
            variable_values = np.linspace(200, 800, 100)
            vn_values = [calculate_vn(b, d_val, a, a_d, fc, ρt, fƒ, Eƒ) for d_val in variable_values]
        elif plot_variable == "a":
            variable_values = np.linspace(50, 400, 100)
            vn_values = [calculate_vn(b, d, a_val, a_d, fc, ρt, fƒ, Eƒ) for a_val in variable_values]
        elif plot_variable == "a_d":
            variable_values = np.linspace(2.47, 3.43, 100)
            vn_values = [calculate_vn(b, d, a, a_d_val, fc, ρt, fƒ, Eƒ) for a_d_val in variable_values]
        elif plot_variable == "fc":
            variable_values = np.linspace(19.2, 93, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc_val, ρt, fƒ, Eƒ) for fc_val in variable_values]
        elif plot_variable == "ρt":
            variable_values = np.linspace(0.11, 4.12, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt_val, fƒ, Eƒ) for ρt_val in variable_values]
        elif plot_variable == "fƒ":
            variable_values = np.linspace(397, 2840, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt, fƒ_val, Eƒ) for fƒ_val in variable_values]
        elif plot_variable == "Eƒ":
            variable_values = np.linspace(24.8, 192, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt, fƒ, Eƒ_val) for Eƒ_val in variable_values]
        
        # Plot the results
        plt.figure(figsize=(8, 6))
        plt.plot(variable_values, vn_values, label=f"Vn vs {plot_variable}")
        plt.xlabel(plot_variable)
        plt.ylabel(f"Nominal Shear Strength (Vn) [{convert_units}]")
        plt.title(f"Vn vs {plot_variable}")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)
