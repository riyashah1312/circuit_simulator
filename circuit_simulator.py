import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



# =============================================================================
# def instructions():
#     print("Howdy! Welcome to the circuit simulator!")
#     print("Here, you can perform quick circuit calculations by just simply inputting the values that the simulator asks for.")
# =============================================================================

#instructions()

st.title("⚡ Circuit Simulator")
st.write("Howdy! Welcome to the circuit simulator! Here, you can perform quick circuit calculations by simply inputting the values that the simulator asks for.")


# func for resistors in series and parallel
def combo_resistance(series_resistors,parallel_resistors):
    S_resistors = sum(series_resistors)
    current_r = 0
    for r in parallel_resistors:
        resistance = 1/r
        current_r = current_r + resistance
    R_resistors = 1/current_r
    Req = R_resistors + S_resistors
    return Req
    

# func for series resistors
def series_resistance(resistors):
    Req = sum(resistors)
    return Req


# func for parallel resistors

def parallel_resistance(resistors):
    Req = (sum(1/r for r in resistors))**-1
    return Req

# func that solves for current and voltage drops when given voltage and resistance

def solve_dc_circuit(voltage, resistors, connection_type):
    connection_type = connection_type.lower()
    
    if connection_type == "series":
        R_total = series_resistance(resistors)
        I_total = voltage / R_total
        voltage_drops = [I_total * r for r in resistors]
        return {"Req": R_total, "I_total": I_total, "voltage_drops": voltage_drops}
    elif connection_type == 'parallel':
        R_total = parallel_resistance(resistors)
        I_total = voltage / R_total
        branch_currents = [voltage / r for r in resistors]
        return {"Req": R_total, "I_total": I_total, "branch_currents": branch_currents}
# sidebar menu

choice = st.sidebar.radio(
    "Choose an option:",
    ["Equivalent Resistance", "Current & Voltage Drops", "RC Charging Curve", "Quit"]
)

# Equivalent resistance
if choice == "Equivalent Resistance":
    st.header("Equivalent Resistance Calculator")
    resistor_type = st.radio("Does your circuit have both series and parallel resistors?", ["Yes", "No"])
    if resistor_type == "Yes":
        series = st.text_input("Enter resistors in series (comma-separated):", "100,200")
        parallel = st.text_input("Enter resistors in parallel (comma-separated):", "300,400")
        if st.button("Calculate"):
            series_resistors = [float(x) for x in series.split(",")]
            parallel_resistors = [float(x) for x in parallel.split(",")]
            Req = combo_resistance(series_resistors, parallel_resistors)
            st.success(f"Equivalent Resistance: {Req:.2f} Ω")
    else:
        r_type = st.radio("Are they all in series?", ["Yes", "No"])
        resistors = st.text_input("Enter resistor values (comma-separated):", "100,200,300")
        if st.button("Calculate"):
            resistors = [float(x) for x in resistors.split(",")]
            if r_type == "Yes":
                Req = series_resistance(resistors)
            else:
                Req = parallel_resistance(resistors)
            st.success(f"Equivalent Resistance: {Req:.2f} Ω")

elif choice == "Current & Voltage Drops":
    st.header("DC Circuit Solver")
    voltage = st.number_input("Enter source voltage (V):", min_value=0.0, value=10.0)
    connection_type = st.radio("Connection type:", ["Series", "Parallel"])
    resistors = st.text_input("Enter resistor values (comma-separated):", "100,200")

    if st.button("Solve Circuit"):
        resistors = [float(x) for x in resistors.split(",")]
        result = solve_dc_circuit(voltage, resistors, connection_type)

        st.write(f"**Equivalent Resistance:** {result['Req']:.2f} Ω")
        st.write(f"**Total Current:** {result['I_total']:.2f} A")

        if connection_type == "Series":
            st.write("**Voltage drops across resistors:**")
            st.write(result["voltage_drops"])
        elif connection_type == "Parallel":
            st.write("**Branch currents:**")
            st.write(result["branch_currents"])

# --- RC Charging Curve ---
elif choice == "RC Charging Curve":
    st.header("RC Circuit Charging Curve")
    V = st.number_input("Enter supply voltage (V):", min_value=0.0, value=5.0)
    R = st.number_input("Enter resistance (Ω):", min_value=0.1, value=100.0)
    C = st.number_input("Enter capacitance (F):", min_value=0.0001, value=0.01)
    t_max = st.number_input("Enter max time (s):", min_value=1.0, value=5.0)

    if st.button("Plot Curve"):
        t = np.linspace(0, t_max, 1000)
        Vc = V * (1 - np.exp(-t / (R * C)))
        fig, ax = plt.subplots()
        ax.plot(t, Vc)
        ax.set_title("RC Charging Curve")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage across capacitor (V)")
        st.pyplot(fig)

# --- Quit ---
elif choice == "Quit":
    st.write("👋 Exiting... Goodbye!")


# =============================================================================
# def questions():
#     while True:
#         print("Choose an option:")
#         print("1. Equivalent Resistance")
#         print("2. Current & Voltage Drops")
#         print("3. RC Charging Curve")
#         print("4. Quit")
#     
#         choice = input("Enter the number of your choice: ")
#         if choice == "1":
#             resistor_type = input("Does your circuit have both series and parallel resistors? (yes/no): ")
#             if resistor_type.lower() == "yes":
#                 series = input("Enter resistors in series (comma-separated): ")
#                 parallel = input("Enter resistors in parallel (comma-separated): ")
#                 series_resistors = [float(x) for x in series.split(",")]
#                 parallel_resistors = [float(x) for x in parallel.split(",")]
#                 Req = combo_resistance(series_resistors, parallel_resistors)
#                 print(f"Equivalent Resistance: {Req:.2f} Ω")
#             else:
#                 r_type = input("Are they all in series? (yes/no): ")
#                 resistors = input("Enter resistor values (comma-separated): ")
#                 resistors = [float(x) for x in resistors.split(",")]
#                 if r_type.lower() == "yes":
#                     Req = series_resistance(resistors)
#                 else:
#                     Req = parallel_resistance(resistors)
#                 print(f"Equivalent Resistance: {Req:.2f} Ω")
#             
#         elif choice == "2":
#             voltage = float(input('Enter the source voltage: '))
#             
#             connection_type = input("Are the resistors in series, parallel, or a combination?: ")
#             if connection_type.lower() == "series":
#                 resistors = [float(x) for x in input("Enter the resistor values (comma-separated): ").split(",")]
#                 result = solve_dc_circuit(voltage, resistors, connection_type)
#                 print(f"Total Resistance: {result['Req']:.2f} Ω")
#                 print(f"Total Current: {result['I_total']:.2f} A")
#             elif connection_type.lower() == "parallel":
#                 resistors = [float(x) for x in input("Enter the resistor values (comma-separated): ").split(",")]
#                 Req = parallel_resistance(resistors)
#                 I_total = voltage / Req
#                 print(f"Total current: {I_total:.2f} A")
#                 branch_currents = [voltage / r for r in resistors]
#                 print("Branch currents:", branch_currents)
#     
#             elif connection_type.lower() == "combination":
#                 print("This feature is under development!")
#                 
#         elif choice == "3":
#                 V = float(input("Enter supply voltage (V): "))
#                 R = float(input("Enter resistance (Ω): "))
#                 C = float(input("Enter capacitance (F): "))
#                 t_max = float(input("Enter max time (s): "))
#                 t = np.linspace(0, t_max, 1000)
#                 Vc = V * (1 - np.exp(-t / (R * C)))
#                 plt.plot(t, Vc)
#                 plt.title("RC Charging Curve")
#                 plt.xlabel("Time (s)")
#                 plt.ylabel("Voltage across capacitor (V)")
#                 plt.show()
#                
#             
#             
#         elif choice == "4":
#                 print("Exiting... Goodbye!")
#                 break
#                 
#     
#         else:
#             print("Invalid choice, please try again.")
#         
# questions()
# =============================================================================



    