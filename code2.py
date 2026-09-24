import streamlit as st
import pandas as pd
import numpy as np
import os

# ==========================================
# 1. Page Config & Language Dictionary
# ==========================================
st.set_page_config(page_title="MANAATY - Health System", layout="wide", page_icon="🛡️")

# Dictionary for Bilingual Support
TEXTS = {
    "English": {
        "view_mode_label": "👁️ Select Dashboard View:",
        "view_modes": ["🧑‍🦽 Patient Accessible View", "🩺 Caregiver Clinical View"],
        "scenario_label": "🔬 Select Live Patient Scenario:",
        "scenarios": ["1. Normal / Stable Patient", "2. Emerging Risk Patient (Fever & High HR)"],
        "title": "AI-Powered Health Monitoring for High-Risk Individuals",
        "controls": "⚙️ System Control",
        "demo_caption": "Demo Controller for Hackathon Judges",
        "hello": "Hello, Hassan 👋",
        "safe_title": "✅ You are doing great!",
        "safe_sub": "Your vitals are stable. No actions needed.",
        "danger_title": "🚨 Checking in...",
        "danger_sub": "We noticed a change in your readings. <br>Your caregiver <b>Sarah</b> has been automatically notified.",
        "call_btn": "📞 Start Voice Call with Sarah Now",
        "call_success": "🔊 Connecting to Caregiver... (Simulated)",
        "slogan": "Detect Early. Alert Smarter. Act Faster.",
        "patient_id_label": "Patient:",
        "patient_name": "Hassan",
        "condition": "Condition:",
        "condition_val": "Spinal Cord Injury (C5)",
        "wearable": "Primary Wearable:",
        "wearable_val": "Apple Watch Series 9",
        "vitals_title": "📊 Real-Time Vitals (vs. Baseline)",
        "temp": "Body Temp",
        "hr": "Heart Rate",
        "spo2": "SpO2",
        "trend_title": "📈 24-Hour Continuous Trend",
        "ai_title": "🧠 MANAATY AI Assessment",
        "low_risk": "🟢 LOW RISK: Pattern is stable.",
        "high_risk": "🔴 HIGH RISK: Emerging physiological pattern detected.",
        "confidence": "**Anomaly Confidence Score:**",
        "ai_caption": "AI dynamically analyzed wearable metrics against patient's baseline.",
        "action_title": "⚡ Care Team Action",
        "warning": "⚠️ **Protocol Triggered:**\n1. Call patient immediately.\n2. Schedule physical check.\n3. Verify vitals manually.",
        "escalate_btn": "🚨 Escalate to Dr. Khalid",
        "escalate_success": "✅ Full patient report securely sent to clinical team.",
        "no_action": "No immediate action required. Continue routine remote monitoring.",
        "phase2_title": "🔬 View Phase 2: Patch Integration",
        "phase2_text": "In future updates, MANAATY will integrate with our proprietary smart microneedle patch to ingest continuous CRP & IL-6 data directly into this dashboard.",
        "cg_disclaimer": "System provides AI-assisted risk stratification to support clinical teams."
    },
    "العربية": {
        "view_mode_label": "👁️ اختر واجهة العرض:",
        "view_modes": ["🧑‍🦽 واجهة المريض", "🩺 واجهة مقدم الرعاية (السريرية)"],
        "scenario_label": "🔬 اختر حالة المريض (للمحاكاة):",
        "scenarios": ["1. مريض مستقر / طبيعي", "2. خطر محتمل (ارتفاع الحرارة والنبض)"],
        "title": "مراقبة صحية مدعومة بالذكاء الاصطناعي للأشخاص ذوي المخاطر العالية",
        "controls": "⚙️ تحكم النظام",
        "demo_caption": "لوحة تحكم العرض للجنة التحكيم",
        "hello": "أهلاً، حسن 👋",
        "safe_title": "✅ أمورك ممتازة!",
        "safe_sub": "مؤشراتك الحيوية مستقرة. لا حاجة لأي إجراء.",
        "danger_title": "🚨 نطمئن عليك...",
        "danger_sub": "لاحظنا تغيراً في قراءاتك. <br>تم تنبيه مقدمة الرعاية <b>سارة</b> تلقائياً للتواصل معك.",
        "call_btn": "📞 ابدأ اتصال صوتي مع سارة الآن",
        "call_success": "🔊 جاري الاتصال بمقدم الرعاية... (محاكاة)",
        "slogan": "اكتشاف مبكر. تنبيه أذكى. استجابة أسرع.",
        "patient_id_label": "المريض:",
        "patient_name": "حسن",
        "condition": "الحالة:",
        "condition_val": "إصابة حبل شوكي (C5)",
        "wearable": "الجهاز المتصل:",
        "wearable_val": "Apple Watch Series 9",
        "vitals_title": "📊 المؤشرات اللحظية (مقارنة بالطبيعي)",
        "temp": "الحرارة Temp",
        "hr": "نبض القلب HR",
        "spo2": "الأكسجين SpO2",
        "trend_title": "📈 تحليل الاتجاه (24 ساعة)",
        "ai_title": "🧠 تقييم الذكاء الاصطناعي",
        "low_risk": "🟢 خطر منخفض: النمط الفسيولوجي مستقر.",
        "high_risk": "🔴 خطر عالٍ: رصد نمط فسيولوجي مقلق.",
        "confidence": "**نسبة الثقة بوجود خلل:**",
        "ai_caption": "حلل الذكاء الاصطناعي القراءات اللحظية مقارنة بالوضع الطبيعي للمريض.",
        "action_title": "⚡ إجراءات الفريق الطبي",
        "warning": "⚠️ **تفعيل البروتوكول:**\n1. الاتصال بالمريض فوراً.\n2. جدولة فحص سريري.\n3. التحقق من العلامات الحيوية يدوياً.",
        "escalate_btn": "🚨 تصعيد الحالة للدكتور خالد",
        "escalate_success": "✅ تم إرسال التقرير الطبي بأمان إلى لوحة تحكم الطبيب.",
        "no_action": "لا حاجة لإجراء فوري. استمر في المراقبة الروتينية عن بعد.",
        "phase2_title": "🔬 رؤية المرحلة الثانية: دمج اللاصقة",
        "phase2_text": "في التحديثات المستقبلية، سيتم دمج 'مناعتي' مع لاصقة الإبر الدقيقة الذكية لقراءة مؤشرات CRP و IL-6 الحيوية مباشرة في هذه اللوحة.",
        "cg_disclaimer": "مناعتي هو نظام مساندة بالذكاء الاصطناعي، وليس أداة للتشخيص الطبي."
    }
}

# ==========================================
# 2. Language Selector & Dynamic CSS (RTL/LTR)
# ==========================================
st.sidebar.markdown("### 🌐 Language / اللغة")
selected_lang = st.sidebar.radio("", ["English", "العربية"], horizontal=True, label_visibility="collapsed")
lang = TEXTS[selected_lang]

def inject_custom_css(language):
    # دمج الـ CSS كله في بلوك واحد بدون مسافات بادئة تكسر الـ Markdown
    css = """<style>
.block-container { padding-top: 1rem; }

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
"""
    
    # إضافة خصائص اليمين لليسار إذا كانت اللغة عربية
    if language == "العربية":
        css += """
.block-container, .stSidebar, [data-testid="stSidebar"], .stSelectbox, .stRadio, .stMarkdown, .stText, .stButton {
    direction: rtl !important;
    text-align: right !important;
}
[data-testid="stMetricDelta"] svg {
    margin-right: 0;
    margin-left: 0.5rem;
}
.patient-card-safe, .patient-card-danger {
    direction: rtl !important;
}
"""
        
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css(selected_lang)

# ==========================================
# 3. Data Loading Logic
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
# 4. Header & Logo Integration
# ==========================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("new_logo_manaty.jpeg", use_container_width=True)
    except Exception:
        st.markdown("<h1 style='text-align: center; color: #00C8FF;'>🛡️ MANAATY</h1>", unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; color: #a5b1d9; font-weight: 300; margin-top: -10px;'>{lang['title']}</h3>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 5. Sidebar: Scenario Controller
# ==========================================
st.sidebar.title(lang["controls"])
st.sidebar.caption(lang["demo_caption"])

# Dynamic mapping of translated scenarios to system logic
view_mapping = {lang["view_modes"][0]: "Patient", lang["view_modes"][1]: "Caregiver"}
scenario_mapping = {lang["scenarios"][0]: "Normal", lang["scenarios"][1]: "Risk"}

mode_selection = st.sidebar.radio(lang["view_mode_label"], lang["view_modes"])
mode = view_mapping[mode_selection]

st.sidebar.markdown("---")
scenario_selection = st.sidebar.selectbox(lang["scenario_label"], lang["scenarios"])
scenario = scenario_mapping[scenario_selection]

if scenario == "Normal":
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
# 6. VIEW 1: PATIENT ACCESSIBLE VIEW
# ==========================================
if mode == "Patient":
    st.markdown(f"<h2 style='text-align: center;'>{lang['hello']}</h2>", unsafe_allow_html=True)
    st.write("")
    
    col_space1, col_main, col_space3 = st.columns([1, 4, 1])
    
    with col_main:
        if risk_class == 0:
            st.markdown(f"""
                <div class="patient-card-safe">
                    <div class="big-text">{lang['safe_title']}</div>
                    <div class="sub-text">{lang['safe_sub']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="patient-card-danger">
                    <div class="big-text">{lang['danger_title']}</div>
                    <div class="sub-text">{lang['danger_sub']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button(lang['call_btn'], use_container_width=True, type="primary"):
                st.success(lang['call_success'])

    st.markdown(f"""
    <br>
    <div style='text-align: center;'>
        <p style='font-size: 22px; font-weight: 800; color: #00C8FF; margin-bottom: 5px; letter-spacing: 1px;'>
            {lang['slogan']}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. VIEW 2: CAREGIVER CLINICAL VIEW
# ==========================================
elif mode == "Caregiver":
    
    st.markdown(f"""
        <div style='background-color: #1a1e36; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between;'>
            <div><b>{lang['patient_id_label']}</b> {lang['patient_name']} (ID: {p_id})</div>
            <div><b>{lang['condition']}</b> {lang['condition_val']}</div>
            <div><b>{lang['wearable']}</b> {lang['wearable_val']}</div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1.2])

    with col_left:
        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{lang["vitals_title"]}</div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric(lang["temp"], f"{c_temp:.1f} °C", temp_delta, delta_color=status_color)
        m2.metric(lang["hr"], f"{int(c_hr)} bpm", hr_delta, delta_color=status_color)
        m3.metric(lang["spo2"], f"{int(c_spo2)} %", spo2_delta, delta_color=status_color)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{lang["trend_title"]}</div>', unsafe_allow_html=True)
        
        time_index = ["12h ago", "8h ago", "4h ago", "Now"]
        temp_trend = [b_temp, b_temp + ((c_temp-b_temp)*0.2), b_temp + ((c_temp-b_temp)*0.7), c_temp]
        hr_trend = [b_hr, b_hr + ((c_hr-b_hr)*0.2), b_hr + ((c_hr-b_hr)*0.7), c_hr]
        
        df_trend = pd.DataFrame({"HR (bpm)": hr_trend, "Temp (°C)": temp_trend}, index=time_index)
        st.line_chart(df_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{lang["ai_title"]}</div>', unsafe_allow_html=True)
        
        if risk_class == 0:
            st.success(lang["low_risk"])
        else:
            st.error(lang["high_risk"])
            
        st.write(f"{lang['confidence']} {ai_prob*100:.1f}%")
        st.progress(float(ai_prob))
        st.caption(lang["ai_caption"])
        st.caption(f"⚠️ *{lang['cg_disclaimer']}*")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="caregiver-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{lang["action_title"]}</div>', unsafe_allow_html=True)
        
        if risk_class >= 1:
            st.warning(lang["warning"])
            if st.button(lang["escalate_btn"], type="primary", use_container_width=True):
                st.toast(lang["escalate_success"])
        else:
            st.info(lang["no_action"])
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander(lang["phase2_title"]):
            st.write(lang["phase2_text"])
