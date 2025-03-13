NEW
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate Vn based on the provided conditions
def calculate_vn(b, d, a, f_c, roh_t, f_f, E_f):
    # Calculate a_d automatically
    a_d = a / d
    
    # Check conditions and calculate Vn
    if b <= 229.5:
        if a_d <= 3.25:
            # LM1
            Vn = 0.3499 * b + 0.1134 * d + 0.0262 * a - 38.0757 * a_d + 0.4744 * f_c + 13.9273 * roh_t - 0.0277 * f_f + 0.4406 * E_f + 9.4873
        else:
            # LM2
            Vn = 0.1043 * b + 0.3369 * d - 0.0609 * a + 7.3607 * a_d + 0.0262 * f_c + 12.2679 * roh_t - 0.0043 * f_f + 0.1629 * E_f - 59.5343
    else:
        if b <= 435:
            if d <= 237.5:
                # LM3
                Vn = 0.098 * b + 0.2522 * d - 0.0303 * a - 2.783 * a_d + 0.1203 * f_c + 16.2091 * roh_t - 0.0107 * f_f + 0.3162 * E_f - 31.0511
            else:
                if d <= 318:
                    if roh_t <= 1.44:
                        # LM4
                        Vn = 0.1552 * b + 0.2537 * d - 0.059 * a - 2.783 * a_d + 0.0995 * f_c + 23.5769 * roh_t - 0.0107 * f_f + 0.3925 * E_f - 26.8098
                    else:
                        # LM5
                        Vn = 0.1552 * b + 0.2621 * d - 0.059 * a - 2.783 * a_d + 0.0731 * f_c + 24.5878 * roh_t - 0.0107 * f_f + 0.3925 * E_f - 27.2859
                else:
                    # LM6
                    Vn = 0.376 * b + 0.3502 * d - 0.0995 * a - 2.783 * a_d + 0.0731 * f_c + 26.3319 * roh_t - 0.0107 * f_f + 0.4779 * E_f - 76.7875
        else:
            # LM7
            Vn = 0.0907 * b + 0.0731 * d + 0.0425 * a - 4.33 * a_d + 0.1026 * f_c + 19.1667 * roh_t - 0.0139 * f_f + 0.6346 * E_f - 36.8616
    
    return Vn

# Streamlit app interface
st.set_page_config(page_title="Shear Capacity (Vn) Calculator", page_icon="⚙️", layout="centered")
st.title("⚙️ Shear Capacity (Vn) Calculator")

# Definitions
st.write("""
### Definitions:
- **b**: Section width in (mm).
- **a**: Shear span in (mm).
- **d**: Effective depth in (mm).
- **a/d**: Shear span-to-effective depth ratio (dimensionless).
- **f'_c**: Concrete compressive strength in (MPa).
- **ρ_t**: FRP longitudinal reinforcement ratio (input as percentage, e.g., 2 for 2%).
- **f_f**: FRP ultimate tensile strength in (MPa).
- **E_f**: FRP Young's modulus in (GPa).
  
### Output:
- **Vn**: Nominal shear strength of the section in kilo-Newtons (kN), calculated based on the provided parameters.
""")

# Inputs with tooltips
st.write("Enter the following parameters:")

b = st.number_input("b (mm) [Min=89 - Max=1200]:", value=0.0, help="Section width in (mm).")
d = st.number_input("d (mm) [Min=73 - Max=889]:", value=0.0, help="Effective depth in (mm).")
a = st.number_input("a (mm) [Min=180 - Max=3050]:", value=0.0, help="Shear span in (mm).")
K = st.number_input("a/d (mm) [Min=2.47 - Max=3.43]:", value=0.0, help="Shear span in (mm).")
f_c = st.number_input("f'_c (MPa) [Min=19.2 - Max=93]:", value=0.0, help="Concrete compressive strength in (MPa).")
roh_t_percent = st.number_input("ρ_t (%) [Min=0.11% - Max=4.12%]:", value=0.0, help="Reinforcement ratio as a percentage (e.g., 2 for 0.02).")
roh_t = roh_t_percent # Convert the percentage to dimensionless value
f_f = st.number_input("f_f (MPa) [Min=397 - Max=2840]:", value=0.0, help="FRP ultimate tensile strength in (MPa).")
E_f = st.number_input("E_f (GPa) [Min=24.8 - Max=192]:", value=0.0, help="FRP Young's modulus in (GPa).")

# Allow the user to choose which variable to plot against Vn
plot_variable = st.selectbox("Select a variable to plot against Vn:", ["b", "d", "a", "a/d", "f'_c", "ρ_t", "f_f", "E_f"])

# Convert Vn to N or kN
convert_units = st.radio("Convert Vn to:", ('kN', 'N'))

# Calculate Vn when button is pressed
if st.button("Calculate Vn"):
    if b > 0 and d > 0 and a > 0 and f_c > 0 and roh_t > 0 and f_f > 0 and E_f > 0:
        Vn = calculate_vn(b, d, a, f_c, roh_t, f_f, E_f)
        
        # Convert to N or kN
        if convert_units == 'N':
            Vn *= 1000  # Convert to N
        
        st.subheader(f"Calculated Vn: {Vn:.2f} {convert_units}")
        
        # Plotting Vn against the selected variable
        if plot_variable == "b":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b_val, d, a, a_d, f_c, roh_t, f_f, E_f) for b_val in variable_values]
        elif plot_variable == "d":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d_val, a, a_d, f_c, roh_t, f_f, E_f) for d_val in variable_values]
        elif plot_variable == "a":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d, a_val, a_d, f_c, roh_t, f_f, E_f) for a_val in variable_values]
        elif plot_variable == "a/d":
            variable_values = np.linspace(100, 500, 100)
            vn_values = [calculate_vn(b, d, a, a_d_val, f_c, roh_t, f_f, E_f) for a_d_val in variable_values]
        elif plot_variable == "f'_c":
            variable_values = np.linspace(5, 100, 100)
            vn_values = [calculate_vn(b, d, a, a_d, f_c_val, roh_t, f_f, E_f) for f_c_val in variable_values]
        elif plot_variable == "ρ_t":
            variable_values = np.linspace(0.1, 2, 100)
            vn_values = [calculate_vn(b, d, a, a_d, f_c, roh_t_val, f_f, E_f) for roh_t_val in variable_values]
        elif plot_variable == "f_f":
            variable_values = np.linspace(100, 600, 100)
            vn_values = [calculate_vn(b, d, a, a_d, f_c, roh_t, f_f_val, E_f) for f_f_val in variable_values]
        elif plot_variable == "E_f":
            variable_values = np.linspace(10, 200, 100)
            vn_values = [calculate_vn(b, d, a, a_d, f_c, roh_t, f_f, E_f_val) for E_f_val in variable_values]
        
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
