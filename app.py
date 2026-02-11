import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Sustainable Brine Management Decision Support System",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM HEADER WITH BRINEX BRANDING
# ---------------------------------------------------
col1, col2 = st.columns([6,1])

with col1:
    st.title("🌊 Sustainable Brine Management Decision Support System")
    st.markdown("#### Chemical Engineering Tool for Optimizing Desalination Brine Treatment in Oman")

with col2:
    st.markdown(
        """
        <div style='text-align:right; font-size:20px; font-weight:bold; color:#0E5A8A;'>
        BrineX
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------
st.sidebar.header("🔬 Brine Input Parameters")

TDS = st.sidebar.number_input("Total Dissolved Solids (mg/L)", 0, 150000, 65000)
Na = st.sidebar.number_input("Na⁺ (mg/L)", 0, 60000, 22000)
Mg = st.sidebar.number_input("Mg²⁺ (mg/L)", 0, 10000, 1800)
Ca = st.sidebar.number_input("Ca²⁺ (mg/L)", 0, 10000, 900)
flow = st.sidebar.number_input("Flow Rate (m³/day)", 0, 600000, 120000)

location = st.sidebar.selectbox(
    "Environmental Sensitivity",
    ["Low", "Medium", "High"]
)

st.sidebar.markdown("---")
st.sidebar.info("All calculations are engineering-based estimations for prototype demonstration.")

# ---------------------------------------------------
# DECISION LOGIC FUNCTION
# ---------------------------------------------------
def treatment_decision(TDS, Mg, location):
    if TDS > 80000:
        return "High Salinity: Evaporation & Salt Recovery System"
    elif Mg > 1500:
        return "Magnesium Recovery via Chemical Precipitation"
    elif location == "High":
        return "Zero Liquid Discharge (ZLD)"
    else:
        return "Controlled Dilution with Diffuser System"

recommendation = treatment_decision(TDS, Mg, location)

# ---------------------------------------------------
# MASS BALANCE CALCULATIONS
# ---------------------------------------------------
mg_recovery = (Mg * flow) / 1_000_000   # kg/day
na_recovery = (Na * flow) / 1_000_000   # kg/day
ca_recovery = (Ca * flow) / 1_000_000   # kg/day

# ---------------------------------------------------
# ECONOMIC ESTIMATION (Rough Model)
# ---------------------------------------------------
mg_value = mg_recovery * 2.5
na_value = na_recovery * 0.12
ca_value = ca_recovery * 0.08

total_daily_value = mg_value + na_value + ca_value

# ---------------------------------------------------
# ENVIRONMENTAL SCORE
# ---------------------------------------------------
score = 100 - (TDS / 1200)

if location == "High":
    score -= 15
elif location == "Medium":
    score -= 8

environmental_score = max(0, int(score))

# ---------------------------------------------------
# RISK CLASSIFICATION
# ---------------------------------------------------
if environmental_score >= 75:
    risk_level = "Low Risk"
elif environmental_score >= 45:
    risk_level = "Moderate Risk"
else:
    risk_level = "High Risk"

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Chemical Analysis", "⚙️ Treatment Strategy", "🌱 Sustainability Impact", "📄 Generate Report"]
)

# ---------------------------------------------------
# TAB 1 – CHEMICAL ANALYSIS
# ---------------------------------------------------
with tab1:
    st.subheader("Brine Composition Overview")

    df = pd.DataFrame({
        "Component": ["Na⁺", "Mg²⁺", "Ca²⁺"],
        "Concentration (mg/L)": [Na, Mg, Ca]
    })

    st.dataframe(df, use_container_width=True)

    fig, ax = plt.subplots()
    ax.bar(df["Component"], df["Concentration (mg/L)"])
    ax.set_ylabel("mg/L")
    ax.set_title("Ion Distribution in Brine")
    st.pyplot(fig)

    st.markdown("### Mass Balance Estimation (kg/day)")
    st.write(f"Magnesium: **{mg_recovery:.2f} kg/day**")
    st.write(f"Sodium: **{na_recovery:.2f} kg/day**")
    st.write(f"Calcium: **{ca_recovery:.2f} kg/day**")

# ---------------------------------------------------
# TAB 2 – TREATMENT STRATEGY
# ---------------------------------------------------
with tab2:
    st.subheader("Recommended Treatment Strategy")
    st.success(recommendation)

    st.markdown("### Estimated Economic Potential")
    st.write(f"Magnesium Value per Day: ${mg_value:,.2f}")
    st.write(f"Sodium Value per Day: ${na_value:,.2f}")
    st.write(f"Calcium Value per Day: ${ca_value:,.2f}")

    st.markdown("### Total Estimated Daily Recovery Value")
    st.metric("Projected Revenue", f"${total_daily_value:,.2f}")

# ---------------------------------------------------
# TAB 3 – ENVIRONMENTAL IMPACT
# ---------------------------------------------------
with tab3:
    st.subheader("Environmental Sustainability Assessment")

    st.metric("Environmental Score", f"{environmental_score}/100")
    st.write(f"Risk Classification: **{risk_level}**")

    salinity_reduction = TDS * 0.35
    st.write(f"Estimated Salinity Reduction Potential: {int(salinity_reduction)} mg/L")

    fig2, ax2 = plt.subplots()
    ax2.bar(["Initial TDS", "Post-Treatment (Estimated)"],
            [TDS, TDS - salinity_reduction])
    ax2.set_ylabel("mg/L")
    ax2.set_title("Salinity Reduction Impact")
    st.pyplot(fig2)

# ---------------------------------------------------
# TAB 4 – REPORT GENERATION
# ---------------------------------------------------
with tab4:
    st.subheader("Download Project Report")

    current_time = datetime.datetime.now()

    report = f"""
    Sustainable Brine Management Decision Support System
    Developed by BrineX

    Date: {current_time}

    INPUT DATA
    -----------------------
    TDS: {TDS} mg/L
    Na: {Na} mg/L
    Mg: {Mg} mg/L
    Ca: {Ca} mg/L
    Flow Rate: {flow} m3/day
    Location Sensitivity: {location}

    RESULTS
    -----------------------
    Recommended Strategy:
    {recommendation}

    Magnesium Recovery: {mg_recovery:.2f} kg/day
    Sodium Recovery: {na_recovery:.2f} kg/day
    Calcium Recovery: {ca_recovery:.2f} kg/day

    Estimated Daily Economic Value: ${total_daily_value:,.2f}

    Environmental Score: {environmental_score}/100
    Risk Level: {risk_level}
    """

    st.download_button(
        label="Download Full Report",
        data=report,
        file_name="BrineX_Sustainability_Report.txt"
    )

st.markdown("---")
st.markdown("##### Developed by BrineX | Sustainable Engineering Solutions for Oman 🇴🇲")
