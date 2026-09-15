import streamlit as st
import pandas as pd
import numpy as np
import os

# ==========================================
# 1. Page Config & Custom CSS (Including Vibration Effect)
# ==========================================
st.set_page_config(page_title="MANAATY - Health System", layout="wide", page_icon="🛡️")

def inject_custom_css():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; }
        
        /* Vibration Animation for Emergency Box */
        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(0deg); }
        }

        .patient-card-safe { background: linear-gradient(135deg, #0f3d1b, #051c0a); padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #2ecc71; box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2); }
        
        /* Applying the vibration animation to the danger card */
        .patient-card-danger { 
            background: linear-gradient(135deg, #4a0f0f, #240505); 
            padding: 40px; 
            border-radius: 20px; 
            text-align: center; 
            border: 2px solid #e74c3c; 
            box-shadow: 0 4px 20px rgba(231, 76, 60, 0.4);
            animation: shake 0.5s;
            animation-iteration-count: infinite;
        }
        
        .big-text { font-size: 50px; font-weight: 900; color: white; margin-bottom: 15px; }
        .sub-text { font-size: 24px; color: #d0dcff; }
        .caregiver-panel { background-color: #111424; padding: 25px; border-radius: 15px; border: 1px solid #2a2e45; margin-bottom: 20px; }
        .section-title { color: #8fa0e0; font-size: 18px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #2a2e45; padding-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==========================================
# 2. Data Loading Logic
# ==========================================
@st.cache_data
def load_synthetic_data():
    file_name = "manaaty_wearable_data.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame({
            "patient_id": ["P-001", "P-002"],
            "baseline_temp_c": [36.6, 36.5], "current_temp_c": [36.6, 38.4],
            "baseline_hr_bpm": [72, 70], "current_hr_bpm": [74, 110],
            "baseline_spo2": [98, 99], "current_spo2": [98, 92],
            "risk_class": [0, 2]
        })

df_data = load_synthetic_data()

# ==========================================
# 3. Header & Logo Integration
# ==========================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("new_logo_manaty.jpeg", use_container_width=True)
    except Exception:
        st.markdown("<h1 style='text-align: center; color: #00C8FF;'>🛡️ MANAATY</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #a5b1d9; font-weight: 300; margin-top: -10px;'>AI-Powered Health Monitoring for High-Risk Individuals</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 4. Sidebar: Scenario Controller
# ==========================================
st.sidebar.title("⚙️ System Control")
st.sidebar.caption("Demo Controller for Hackathon Judges")

mode = st.sidebar.radio("👁️ Select Dashboard View:", 
                        ["🧑‍🦽 Patient Accessible View", "🩺 Caregiver Clinical View"])

st.sidebar.markdown("---")
scenario = st.sidebar.selectbox("🔬 Select Live Patient Scenario:", 
                                ["1. Normal / Stable Patient", "2. Emerging Risk Patient (Fever & High HR)"])

if "Normal" in scenario:
    patient_data = df_data[df_data["risk_class"] == 0].iloc[0] if len(df_data[df_data["risk_class"] == 0]) > 0 else df_data.iloc[0]
    ai_prob = np.random.uniform(0.01, 0.08)
    status_color = "normal"
else:
    patient_data = df_data[df_data["risk_class"] == 2].iloc[0] if len(df_data[df_data["risk_class"] == 2]) > 0 else df_data.iloc[-1]
    ai_prob = np.random.uniform(0.85, 0.95)
    status_color = "inverse"

risk_class = patient_data["risk_class"]
p_id = patient_data["patient_id"]

b_temp, c_temp = patient_data["baseline_temp_c"], patient_data["current_temp_c"]
b_hr, c_hr = patient_data["baseline_hr_bpm"], patient_data["current_hr_bpm"]
b_spo2, c_spo2 = patient_data["baseline_spo2"], patient_data["current_spo2"]

temp_delta = f"{c_temp - b_temp:+.1f} °C"
hr_delta = f"{int(c_hr - b_hr):+d} bpm"
spo2_delta = f"{int(c_spo2 - b_spo2):+d} %"

# ==========================================
# 5. VIEW 1: PATIENT ACCESSIBLE VIEW
# ==========================================
if mode == "🧑‍🦽 Patient Accessible View":
    st.markdown(f"<h2 style='text-align: center;'>Hello, Hassan 👋</h2>", unsafe_allow_html=True)
    st.write("")
    
    col_space1, col_main, col_space3 = st.columns([1, 4, 1])
    
    with col_main:
        if risk_class == 0:
            st.markdown("""
                <div class="patient-card-safe">
                    <div class="big-text">✅ You are doing great!</div>
                    <div class="sub-text">Your vitals are stable. No actions needed.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # هنا يظهر المربع المهتز (Vibrating Alert Box)
            st.markdown("""
                <div class="patient-card-danger">
                    <div class="big-text">🚨 Checking in...</div>
                    <div class="sub-text">We noticed a change in your readings. <br>Your caregiver <b>Sarah</b> has been automatically notified.</div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("📞 Start Voice Call with Sarah Now", use_container_width=True, type="primary"):
                st.success("🔊 Connecting to Caregiver... (Simulated)")

    st.markdown("<br><p style='text-align: center; color: gray;'>* MANAATY is an AI support system, not a diagnostic tool.</p>", unsafe_allow_html=True)

# ==========================================
# 6. VIEW 2: CAREGIVER CLINICAL VIEW
# ==========================================
elif mode == "🩺 Caregiver Clinical View":
    
    st.markdown(f"""
        <div style='background-color: #1a1e36; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between;'>
            <div><b>Patient:</b> Hassan (ID: {p_id})</div>
            <div><b>Condition:</b> Spinal Cord Injury (C5)</div>
            <div><b>Primary Wearable:</b> Apple Watch Series 9</div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1.2])

    with col_left:
        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Real-Time Vitals (vs. Baseline)</div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Body Temp", f"{c_temp:.1f} °C", temp_delta, delta_color=status_color)
        m2.metric("Heart Rate", f"{int(c_hr)} bpm", hr_delta, delta_color=status_color)
        m3.metric("SpO2", f"{int(c_spo2)} %", spo2_delta, delta_color=status_color)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 24-Hour Continuous Trend</div>', unsafe_allow_html=True)
        
        time_index = ["12h ago", "8h ago", "4h ago", "Now"]
        temp_trend = [b_temp, b_temp + ((c_temp-b_temp)*0.2), b_temp + ((c_temp-b_temp)*0.7), c_temp]
        hr_trend = [b_hr, b_hr + ((c_hr-b_hr)*0.2), b_hr + ((c_hr-b_hr)*0.7), c_hr]
        
        df_trend = pd.DataFrame({"HR (bpm)": hr_trend, "Temp (°C)": temp_trend}, index=time_index)
        st.line_chart(df_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🧠 MANAATY AI Assessment</div>', unsafe_allow_html=True)
        
        if risk_class == 0:
            st.success("🟢 LOW RISK: Pattern is stable.")
        else:
            st.error("🔴 HIGH RISK: Emerging physiological pattern detected.")
            
        st.write(f"**Anomaly Confidence Score:** {ai_prob*100:.1f}%")
        st.progress(float(ai_prob))
        st.caption("AI dynamically analyzed wearable metrics against patient's baseline.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Care Team Action</div>', unsafe_allow_html=True)
        
        if risk_class >= 1:
            st.warning("⚠️ **Protocol Triggered:**\n1. Call patient immediately.\n2. Schedule physical check.\n3. Verify vitals manually.")
            if st.button("🚨 Escalate to Dr. Khalid", type="primary", use_container_width=True):
                st.toast("✅ Full patient report securely sent to clinical team.")
        else:
            st.info("No immediate action required. Continue routine remote monitoring.")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("🔬 View Phase 2: Patch Integration"):
            st.write("In future updates, MANAATY will integrate with our proprietary smart microneedle patch to ingest continuous CRP & IL-6 data directly into this dashboard.")