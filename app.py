import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate Vn based on the provided conditions
def calculate_vn(b, d, a, fc, roh_l, fy, e):
    # Calculate a_d automatically
    a_d = a / d
    
    # Check conditions and calculate Vn
    if b <= 229.5:
        if a_d <= 3.25:
            # LM1
            Vn = 0.3499 * b + 0.1134 * d + 0.0262 * a - 38.0757 * a_d + 0.4744 * fc + 13.9273 * roh_l - 0.0277 * fy + 0.4406 * e + 9.4873
        else:
            # LM2
            Vn = 0.1043 * b + 0.3369 * d - 0.0609 * a + 7.3607 * a_d + 0.0262 * fc + 12.2679 * roh_l - 0.0043 * fy + 0.1629 * e - 59.5343
    else:
        if b <= 435:
            if d <= 237.5:
                # LM3
                Vn = 0.098 * b + 0.2522 * d - 0.0303 * a - 2.783 * a_d + 0.1203 * fc + 16.2091 * roh_l - 0.0107 * fy + 0.3162 * e - 31.0511
            else:
                if d <= 318:
                    if roh_l <= 1.44:
                        # LM4
                        Vn = 0.1552 * b + 0.2537 * d - 0.059 * a - 2.783 * a_d + 0.0995 * fc + 23.5769 * roh_l - 0.0107 * fy + 0.3925 * e - 26.8098
                    else:
                        # LM5
                        Vn = 0.1552 * b + 0.2621 * d - 0.059 * a - 2.783 * a_d + 0.0731 * fc + 24.5878 * roh_l - 0.0107 * fy + 0.3925 * e - 27.2859
                else:
                    # LM6
                    Vn = 0.376 * b + 0.3502 * d - 0.0995 * a - 2.783 * a_d + 0.0731 * fc + 26.3319 * roh_l - 0.0107 * fy + 0.4779 * e - 76.7875
        else:
            # LM7
            Vn = 0.0907 * b + 0.0731 * d + 0.0425 * a - 4.33 * a_d + 0.1026 * fc + 19.1667 * roh_l - 0.0139 * fy + 0.6346 * e - 36.8616
    
    return Vn

# Streamlit app interface
st.set_page_config(page_title="Joint Shear Capacity (Vn) Calculator", page_icon="⚙️", layout="centered")
st.title("⚙️ Joint Shear Capacity (Vn) Calculator")

# Definitions
st.write("""
### Definitions:
- **a (mm)**: Shear span of the concrete section in millimeters (distance from the center of gravity of the section to the point of load application).
- **d (mm)**: Effective depth of the concrete section in millimeters (distance from the extreme compression fiber to the centroid of the tension reinforcement).
- **fc (MPa)**: Concrete compressive strength in megapascals (MPa).
- **ρᵧ (dimensionless)**: Reinforcement ratio, which is the ratio of the area of reinforcement to the area of concrete in the section (input as percentage, e.g., 2 for 2%).
- **fy (MPa)**: Yield strength of steel reinforcement in megapascals (MPa).
- **e (mm)**: Eccentricity (in mm), which is the distance from the center of the section to the point of application of an eccentric load.
  
### Output:
- **Vn**: Nominal shear strength of the section in kilo-Newtons (kN), calculated based on the provided parameters.
""")

# Inputs with tooltips
st.write("Enter the following parameters:")

b = st.number_input("b (mm):", value=0.0, help="Width of the section (in mm).")
d = st.number_input("d (mm):", value=0.0, help="Depth of the section (in mm).")
a = st.number_input("a (mm):", value=0.0, help="Shear span of the section (in mm).")
fc = st.number_input("fc (MPa):", value=0.0, help="Concrete compressive strength (in MPa).")
roh_l_percent = st.number_input("ρᵧ (%)", value=0.0, help="Reinforcement ratio as a percentage (e.g., 2 for 0.02).")
roh_l = roh_l_percent  # Convert the percentage to dimensionless value
fy = st.number_input("fy (MPa):", value=0.0, help="Yield strength of steel (in MPa).")
e = st.number_input("e (mm):", value=0.0, help="Eccentricity (in mm).")

# Allow the user to choose which variable to plot against Vn
plot_variable = st.selectbox("Select a variable to plot against Vn:", ["b", "d", "a", "fc", "ρᵧ", "fy", "e"])

# Convert Vn to N or kN
convert_units = st.radio("Convert Vn to:", ('kN', 'N'))

# Calculate Vn when button is pressed
if st.button("Calculate Vn"):
    if b > 0 and d > 0 and a > 0 and fc > 0 and roh_l > 0 and fy > 0 and e > 0:
        Vn = calculate_vn(b, d, a, fc, roh_l, fy, e)
        
        # Convert to N or kN
        if convert_units == 'N':
            Vn *= 1000  # Convert to N
        
        st.subheader(f"Calculated Vn: {Vn:.2f} {convert_units}")
        
        # Plotting Vn against the selected variable
        if plot_variable == "b":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b_val, d, a, fc, roh_l, fy, e) for b_val in variable_values]
        elif plot_variable == "d":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d_val, a, fc, roh_l, fy, e) for d_val in variable_values]
        elif plot_variable == "a":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d, a_val, fc, roh_l, fy, e) for a_val in variable_values]
        elif plot_variable == "fc":
            variable_values = np.linspace(5, 100, 100)
            vn_values = [calculate_vn(b, d, a, fc_val, roh_l, fy, e) for fc_val in variable_values]
        elif plot_variable == "ρᵧ":
            variable_values = np.linspace(0.1, 2, 100)
            vn_values = [calculate_vn(b, d, a, fc, roh_l_val, fy, e) for roh_l_val in variable_values]
        elif plot_variable == "fy":
            variable_values = np.linspace(100, 600, 100)
            vn_values = [calculate_vn(b, d, a, fc, roh_l, fy_val, e) for fy_val in variable_values]
        elif plot_variable == "e":
            variable_values = np.linspace(10, 200, 100)
            vn_values = [calculate_vn(b, d, a, fc, roh_l, fy, e_val) for e_val in variable_values]
        
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
        
