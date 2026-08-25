import streamlit as str_lit
from datetime import datetime

# إعداد الصفحة لتكون واسعة وتدعم التجاوب
str_lit.set_page_config(
    page_title="Smart AI Content Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# تفعيل التصميم المتجاوب (Responsive CSS)
# ==========================================
str_lit.markdown("""
<style>
    /* التعديلات العامة للوضع الداكن الموحد */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* تصميم متجاوب لشاشات الهواتف المحمولة (Mobile View) */
    @media (max-width: 768px) {
        /* تقليل الهوامش الجانبية للشاشات الصغيرة لتوفير مساحة عرض */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 2rem !important;
        }
        
        /* جعل العناوين الرئيسية متناسقة مع حجم الشاشة الصغيرة */
        h1 {
            font-size: 1.6rem !important;
        }
        h2 {
            font-size: 1.3rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* جعل الأزرار تأخذ العرض بالكامل لتسهيل الضغط عليها بالإصبع */
        .stButton button {
            width: 100% !important;
            margin-bottom: 5px;
        }
        
        /* تحسين مساحة حقول النص ومربعات الحوار على الموبايل */
        .stTextArea textarea, .stTextInput input {
            font-size: 16px !important; /* يمنع التكبير التلقائي المزعج في آي فون/أندرويد */
        }
    }

    /* تصميم مخصص لشاشات الكمبيوتر والـ PC (Desktop View) */
    @media (min-width: 769px) {
        .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        
        /* تأثيرات جمالية تظهر فقط على شاشات الكمبيوتر الكبيرة */
        .stButton button:hover {
            transform: translateY(-2px);
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }
    }
</style>
""", unsafe_allow_html=True)
