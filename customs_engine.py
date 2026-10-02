"""
=============================================================================
 نظام المحاكاة الجمركية الذكي المطور - Business Gate DZ (Customs Web Engine)
 إشراف الخبير: أستاذ حوسين (خبرة 27 سنة في الإطار الجمركي والتشريعات)
=============================================================================
"""

import streamlit as st

# إعداد واجهة الصفحة
st.set_page_config(
    page_title="Business Gate DZ - Customs Engine",
    page_icon="سوم",
    layout="centered"
)

st.title("🏛️ Business Gate DZ - المحاكي الجمركي الذكي")
st.markdown("### نظام احترافي لتحديد البنود الجمركية (HS Code) وحساب الحقوق والرسوم (مع إعفاءات AAPI)")
st.markdown("---")

# قاعدة بيانات موسعة للبنود والرسوم الجبائية والجمارك
TARIFF_DATABASE = {
    "آلات ومعدات الرفع والمناولة (84.22)": {
        "code_sh": "84.22",
        "description": "آلات ومعدات الرفع أو المناولة أو التحميل",
        "dd": 5.0,  # حقوق الجمارك
        "tva": 19.0, # الرسم على القيمة المضافة
        "tic": 0.0,  # رسوم إضافية
        "aapi_eligible": True
    },
    "أجهزة الاتصالات والترددات (85.17)": {
        "code_sh": "85.17",
        "description": "أجهزة الاتصالات الهاتفية واللاسلكية",
        "dd": 15.0,
        "tva": 19.0,
        "tic": 3.0,
        "aapi_eligible": False
    },
    "بوليمرات الإيثيلين - مواد خام (39.01)": {
        "code_sh": "39.01",
        "description": "بوليمرات الإيثيلين بأشكالها الأولية",
        "dd": 0.0,
        "tva": 9.0,
        "tic": 0.0,
        "aapi_eligible": True
    },
    "معدات وخطوط الإنتاج الصناعي (84.38)": {
        "code_sh": "84.38",
        "description": "آلات ومعدات لصناعة الأغذية أو تحويل المواد",
        "dd": 5.0,
        "tva": 19.0,
        "tic": 0.0,
        "aapi_eligible": True
    }
}

# تصميم واجهة الإدخال للمستخدم
st.sidebar.header("⚙️ خيارات المحاكاة")
selected_item_key = st.sidebar.selectbox("اختر السلعة أو القطاع:", list(TARIFF_DATABASE.keys()))

item_data = TARIFF_DATABASE[selected_item_key]

cif_value = st.number_input("أدخل القيمة الجمركية للسلعة (CIF بالدج - DZD):", min_value=0.0, value=10000000.0, step=100000.0)

# حالة الاستثمار وإعفاءات AAPI
has_aapi = st.sidebar.checkbox("تطبيق إعفاءات الوكالة الوطنية لترقية الاستثمار (AAPI)", value=True)

# حالة السلعة (القواعد الست RGI)
st.sidebar.markdown("---")
st.sidebar.markdown("### تطبيق القواعد الست (RGI):")
state_type = st.sidebar.selectbox("حالة السلعة:", ["تامة الصنع (Finished)", "غير تامة/أجزاء لها خصائص الأساسية (Incomplete - RGI 2)"])
composition_type = st.sidebar.selectbox("تركيبة السلعة:", ["سلعة بسيطة (Single)", "مخلوط / مواد مركبة (Mixture - RGI 3)"])

# زر التنفيذ
if st.button("🚀 تنفيذ المحاكاة وحساب الرسوم بدقة"):
    
    # محاكاة القواعد
    st.info("📌 جاري تحليل السلعة عبر خوارزمية القواعد الست لتفسير النظام المنسق (RGI 1 إلى 6)...")
    if "Mixture" in composition_type:
        st.warning("⚠️ تم رصد مادة مركبة: يُطبق التسلسل الهرمي (الطابع الغالب / الوصف الأكثر تحديداً - القاعدة 3).")
    if "Incomplete" in state_type:
        st.warning("⚠️ تم رصد سلعة غير تامة الصنع: تُعامل معاملة التامة نظراً لامتلاكها الخصائص الأساسية (القاعدة 2-أ).")

    # الحسابات المالية
    dd_rate = item_data["dd"]
    tva_rate = item_data["tva"]
    tic_rate = item_data["tic"]
    
    exemption_note = "خاضع للحقوق والرسوم العامة العادية."
    if has_aapi and item_data["aapi_eligible"]:
        dd_rate = 0.0
        tic_rate = 0.0
        exemption_note = "✨ مستفيد من الإعفاء الجمركي الكلي/الجزئي في إطار استثمارات AAPI."

    # المعادلات الحسابية الدقيقة
    customs_duty_amount = cif_value * (dd_rate / 100.0)
    tic_amount = cif_value * (tic_rate / 100.0)
    base_tva = cif_value + customs_duty_amount + tic_amount
    tva_amount = base_tva * (tva_rate / 100.0)
    total_taxes = customs_duty_amount + tic_amount + tva_amount

    # عرض النتائج في لوحة قيادة احترافية (Dashboard)
    st.success("✅ تمت العملية بنجاح! إليك التقرير الجمركي المفصل:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="رمز البند الجمركي (HS Code)", value=item_data["code_sh"])
        st.metric(label="نسبة حقوق الجمارك (Dd)", value=f"{dd_rate}%")
        st.metric(label="مبلغ حقوق الجمارك", value=f"{customs_duty_amount:,.2f} DZD")
    
    with col2:
        st.metric(label="الرسم على القيمة المضافة (TVA)", value=f"{tva_rate}%")
        st.metric(label="مبلغ الرسم (TVA)", value=f"{tva_amount:,.2f} DZD")
        st.metric(label="إجمالي الرسوم والضرائب المستحقة", value=f"{total_taxes:,.2f} DZD")

    st.markdown("### 📋 الملاحظات التنظيمية والقانونية:")
    st.info(f"""
    - **وصف السلعة:** {item_data['description']}
    - **القيمة التعاقدية (CIF):** {cif_value:,.2f} دج
    - **الوضعية الجمركية:** {exemption_note}
    """)
