import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate Vn based on the provided conditions
def calculate_vn(b, d, a, a_d, fc, ρt, fƒ, Eƒ):
       
    # Check conditions and calculate Vn
    if b <= 229.5:
        if a_d <= 3.25:
            # LM1
            Vn = 0.3499 * b + 0.1134 * d + 0.0262 * a - 38.0757 * a_d + 0.4744 * fc + 13.9273 * ρt - 0.0277 * fƒ + 0.4406 * Eƒ + 9.4873
        else:
            # LM2
            Vn = 0.1043 * b + 0.3369 * d - 0.0609 * a + 7.3607 * a_d + 0.0262 * fc + 12.2679 * ρt - 0.0043 * fƒ + 0.1629 * Eƒ - 59.5343
    else:
        if b <= 435:
            if d <= 237.5:
                # LM3
                Vn = 0.098 * b + 0.2522 * d - 0.0303 * a - 2.783 * a_d + 0.1203 * fc + 16.2091 * ρt - 0.0107 * fƒ + 0.3162 * Eƒ - 31.0511
            else:
                if d <= 318:
                    if ρt <= 1.44:
                        # LM4
                        Vn = 0.1552 * b + 0.2537 * d - 0.059 * a - 2.783 * a_d + 0.0995 * fc + 23.5769 * ρt - 0.0107 * fƒ + 0.3925 * Eƒ - 26.8098
                    else:
                        # LM5
                        Vn = 0.1552 * b + 0.2621 * d - 0.059 * a - 2.783 * a_d + 0.0731 * fc + 24.5878 * ρt - 0.0107 * fƒ + 0.3925 * Eƒ - 27.2859
                else:
                    # LM6
                    Vn = 0.376 * b + 0.3502 * d - 0.0995 * a - 2.783 * a_d + 0.0731 * fc + 26.3319 * ρt - 0.0107 * fƒ + 0.4779 * Eƒ - 76.7875
        else:
            # LM7
            Vn = 0.0907 * b + 0.0731 * d + 0.0425 * a - 4.33 * a_d + 0.1026 * fc + 19.1667 * ρt - 0.0139 * fƒ + 0.6346 * Eƒ - 36.8616
    
    return Vn

# Streamlit app interface
st.set_page_config(
    page_title="Nominal Shear Strength (Vn) Calculator",
    page_icon="https://ars.els-cdn.com/content/image/1-s2.0-S2352012424006726-gr1.jpg",
    layout="centered"
)

# Creating two columns
col1, col2 = st.columns([3, 2])

with col1:
    st.title("Nominal Shear Strength (Vn) Calculator")

with col2:
    st.image("https://ars.els-cdn.com/content/image/1-s2.0-S2352012424006726-gr1.jpg", width=400)


# Definitions
st.write(""" 
### Definitions:
- **b**: Section width in (mm).
- **a**: Shear span in (mm).
- **d**: Effective depth in (mm).
- **a/d**: Shear span-to-effective depth ratio (dimensionless).
- **fc**: Concrete compressive strength in (MPa).
- **ρt**: FRP longitudinal reinforcement ratio (input as percentage, e.g., 2 for 2%).
- **fƒ**: FRP ultimate tensile strength in (MPa).
- **Eƒ**: FRP Young's modulus in (GPa).
  
### Note:
- **The more accurate the output, the more inputs are within the MIN-MAX ranges shown.**
- **Vn**: Nominal Shear Strength of the section in (kN), calculated based on the provided parameters.
""")

# Inputs with tooltips
st.write("Enter the following parameters:")

b = st.number_input("b (mm) [Min=89 - Max=1200]:", value=0.0, help="Section width in (mm).")
d = st.number_input("d (mm) [Min=73 - Max=889]:", value=0.0, help="Effective depth in (mm).")
a = st.number_input("a (mm) [Min=180 - Max=3050]:", value=0.0, help="Shear span in (mm).")
a_d = st.number_input("a/d (mm) [Min=2.47 - Max=3.43]:", value=0.0, help="Shear span in (mm).")
fc = st.number_input("fc (MPa) [Min=19.2 - Max=93]:", value=0.0, help="Concrete compressive strength in (MPa).")
ρt = st.number_input("ρt (%) [Min=0.11% - Max=4.12%]:", value=0.0, help="Reinforcement ratio as a percentage (e.g., 2 for 0.02).")
fƒ = st.number_input("fƒ (MPa) [Min=397 - Max=2840]:", value=0.0, help="FRP ultimate tensile strength in (MPa).")
Eƒ = st.number_input("Eƒ (GPa) [Min=24.8 - Max=192]:", value=0.0, help="FRP Young's modulus in (GPa).")

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
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d_val, a, a_d, fc, ρt, fƒ, Eƒ) for d_val in variable_values]
        elif plot_variable == "a":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d, a_val, a_d, fc, ρt, fƒ, Eƒ) for a_val in variable_values]
        elif plot_variable == "a_d":
            variable_values = np.linspace(2.47, 3.43, 100)
            vn_values = [calculate_vn(b, d, a, a_d_val, fc, ρt, fƒ, Eƒ) for a_d_val in variable_values]
        elif plot_variable == "fc":
            variable_values = np.linspace(5, 100, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc_val, ρt, fƒ, Eƒ) for fc_val in variable_values]
        elif plot_variable == "ρt":
            variable_values = np.linspace(0.1, 2, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt_val, fƒ, Eƒ) for ρt_val in variable_values]
        elif plot_variable == "fƒ":
            variable_values = np.linspace(100, 600, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt, fƒ_val, Eƒ) for fƒ_val in variable_values]
        elif plot_variable == "Eƒ":
            variable_values = np.linspace(10, 200, 100)
            vn_values = [calculate_vn(b, d, a, a_d, fc, ρt, fƒ, Eƒ_val) for Eƒ_val in variable_values]
       
        if convert_units == 'N':
            vn_values = [vn * 1000 for vn in vn_values]  # Convert to N for graph
        
        fig, ax = plt.subplots()
        ax.plot(variable_values, vn_values, label=f"Vn vs. {plot_variable}")
        ax.set_xlabel(plot_variable)
        ax.set_ylabel(f"Vn ({convert_units})")
        ax.legend()
        st.pyplot(fig)

    else:
        st.error("Please input valid values for all parameters.")
