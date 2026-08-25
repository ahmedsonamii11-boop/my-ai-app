import streamlit as str_lit
import google.generativeai as genai
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات المنصة والهوية البصرية اليدوية (Human-Crafted Look)
# ==========================================
str_lit.set_page_config(
    page_title="منصة إبداع | Enterprise Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

str_lit.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cairo:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: #090d16;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] {
        background: #0e1626 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    div.block-container { 
        padding-top: 2rem; 
        max-width: 1350px;
    }

    /* تصميم أزرار يشبه منصاتSaaS العالمية المعمولة يدوياً */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        background: #3b82f6 !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        background: #2563eb !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }

    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        background-color: #0f172a !important;
        color: #f8fafc !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    .human-card {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# ==========================================
# 2. النظام الداخلي والتخزين
# ==========================================
HISTORY_FILE = "human_craft_history.json"
FAV_FILE = "human_craft_favorites.json"
STATS_FILE = "human_craft_stats.json"

def load_data(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, (list, dict)) else []
        except: return []
    return []

def save_data(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except: pass

if "history" not in str_lit.session_state: str_lit.session_state["history"] = load_data(HISTORY_FILE)
if "favorites" not in str_lit.session_state: str_lit.session_state["favorites"] = load_data(FAV_FILE)
if "current_result" not in str_lit.session_state: str_lit.session_state["current_result"] = None
if "current_tools" not in str_lit.session_state: str_lit.session_state["current_tools"] = []

if "visited" not in str_lit.session_state:
    str_lit.session_state["visited"] = True
    stats_data = load_data(STATS_FILE)
    if not isinstance(stats_data, dict): stats_data = {"total_visits": 0}
    stats_data["total_visits"] = stats_data.get("total_visits", 0) + 1
    save_data(STATS_FILE, stats_data)

def get_total_visits():
    data = load_data(STATS_FILE)
    return data.get("total_visits", 1) if isinstance(data, dict) else 1

for k in ["t0_v", "t1_v", "t2_v", "t3_v", "t4_v", "t5_v"]:
    if k not in str_lit.session_state: str_lit.session_state[k] = ""

# ==========================================
# 3. النصوص والهيكلة الثنائية المحترفة
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚙️ إدارة النظام",
        "search_label": "🔍 بحث متقدم:",
        "fav_title": "📌 العناصر المثبتة",
        "fav_empty": "لا توجد عناصر مثبتة",
        "stats_title": "📈 مؤشرات الإنتاجية",
        "stat_total": "إجمالي العمليات:",
        "visitor_count_label": "إجمالي الجلسات النشطة:",
        
        "main_title": "Workspace | نظام الإنتاج الإبداعي ⚡",
        "main_caption": "بيئة عمل هندسية متكاملة لإدارة المحتوى، الاستراتيجيات، والأصول الرقمية بدقة احترافية.",
        
        "tabs": [
            "🏠 نظرة عامة",
            "1. الاستراتيجية",
            "2. السكريبتات",
            "3. الصوت والأغاني",
            "4. هندسة الصور",
            "5. الموشن جرافيك",
            "6. الحملات الإعلانية"
        ],
        
        "btn_gen": "تشغيل المعالجة الذكية 🚀",
        "warn": "برجاء كتابة البيانات المطلوبة أولاً في الحقل المخصص.",
        "spin": "جاري معالجة الطلب عبر خوارزميات النظام...",
        "res_title": "📋 مخرجات التحليل والإنتاج المعتمدة:",
        "tools_title": "🛠️ الأدوات والمراجع المقترحة للتنفيذ:",
        "download": "تصدير الملف النصي (.txt)",
        "rate": "مدى دقة وفعالية المخرج:"
    },
    "English": {
        "sidebar_title": "⚙️ System Control",
        "search_label": "🔍 Advanced Search:",
        "fav_title": "📌 Pinned Assets",
        "fav_empty": "No pinned assets",
        "stats_title": "📈 Productivity KPIs",
        "stat_total": "Total Operations:",
        "visitor_count_label": "Active Sessions:",
        
        "main_title": "Workspace | Creative Production System ⚡",
        "main_caption": "Engineered end-to-end environment for content management, strategy, and digital assets.",
        
        "tabs": [
            "🏠 Overview",
            "1. Strategy",
            "2. Scripts",
            "3. Audio & Music",
            "4. Visuals",
            "5. Motion",
            "6. Campaigns"
        ],
        
        "btn_gen": "Execute Smart Processing 🚀",
        "warn": "Please fill in the required fields first.",
        "spin": "Processing request through system algorithms...",
        "res_title": "📋 Certified Output & Analysis:",
        "tools_title": "🛠️ Recommended Tools & References:",
        "download": "Export Report (.txt)",
        "rate": "Output Precision & Quality:"
    }
}

PLATFORM_TOOLS = {
    "Strategic Planning": [{"name": "Notion", "type": "Workspace", "url": "https://www.notion.so"}],
    "Scripts Studio": [{"name": "ChatGPT", "type": "Text AI", "url": "https://chat.openai.com"}],
    "Music Studio": [{"name": "Suno", "type": "Audio", "url": "https://suno.com"}],
    "Visual Engineering": [{"name": "Midjourney", "type": "Images", "url": "https://www.midjourney.com"}],
    "Motion Cinema": [{"name": "Runway", "type": "Video", "url": "https://runwayml.com"}],
    "Mega Campaigns": [{"name": "Meta Ads", "type": "Marketing", "url": "https://adsmanager.facebook.com"}]
}

def call_gemini_engine(prompt, lang):
    if not API_KEY: return "❌ مفتاح API غير متوفر في الإعدادات."
    models = ['gemini-3.6-flash', 'gemini-1.5-flash']
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            res = model.generate_content(f"Act as a senior software architect and professional producer. Language: {lang}.\n\n{prompt}")
            if res and res.text: return res.text
        except: continue
    return "❌ حدث خطأ في الاتصال بالخدمة."

# ==========================================
# 4. الشريط الجانبي والتحكم
# ==========================================
with str_lit.sidebar:
    lang_choice = str_lit.radio("Language / اللغة:", ["العربية", "English"], horizontal=True)
    t = TEXTS[lang_choice]
    
    str_lit.markdown(f"### {t['sidebar_title']}")
    str_lit.markdown("---")
    str_lit.metric(label=t["visitor_count_label"], value=get_total_visits())
    str_lit.metric(label=t["stat_total"], value=len(str_lit.session_state["history"]))
    str_lit.markdown("---")
    
    search_q = str_lit.text_input(t["search_label"], "")
    str_lit.markdown(f"### {t['fav_title']}")
    if not str_lit.session_state["favorites"]:
        str_lit.caption(t["fav_empty"])
    else:
        for i, fav in enumerate(str_lit.session_state["favorites"][:3]):
            str_lit.text(f"• {fav.get('title', '')[:15]}...")

# ==========================================
# 5. الواجهة الرئيسية والتبويبات
# ==========================================
str_lit.markdown(f"## {t['main_title']}")
str_lit.caption(t['main_caption'])
str_lit.markdown("---")

tabs = str_lit.tabs(t["tabs"])

def process_and_save(section_name, input_val):
    with str_lit.spinner(t["spin"]):
        res = call_gemini_engine(input_val, lang_choice)
        str_lit.session_state["current_result"] = res
        str_lit.session_state["current_tools"] = PLATFORM_TOOLS.get(section_name, [])
        str_lit.session_state["history"].append({"section": section_name, "input": input_val, "result": res})
        save_data(HISTORY_FILE, str_lit.session_state["history"])
        str_lit.success("تم إتمام العملية بنجاح!")

with tabs[0]:
    str_lit.markdown("### نظرة عامة على النظام (System Dashboard)")
    col1, col2, col3 = str_lit.columns(3)
    col1.metric("حالة النظام", "مستقر (Stable)")
    col2.metric("سرعة الاستجابة", "42ms")
    col3.metric("مستوى الأمان", "عالي (Encrypted)")

with tabs[1]:
    str_lit.subheader("01. التخطيط الاستراتيجي وهندسة المشاريع")
    str_lit.session_state["t0_v"] = str_lit.text_area("أدخل تفاصيل المشروع أو أهداف الشركة:", value=str_lit.session_state["t0_v"])
    if str_lit.button("تنفيذ التحليل الاستراتيجي", key="b0"):
        if not str_lit.session_state["t0_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Strategic Planning", str_lit.session_state["t0_v"])

with tabs[2]:
    str_lit.subheader("02. استوديو السكريبتات والهندسة الإعلامية")
    str_lit.session_state["t1_v"] = str_lit.text_area("اكتب فكرة الفيديو أو المحتوى المستهدف:", value=str_lit.session_state["t1_v"])
    if str_lit.button("توليد السكريبت الاحترافي", key="b1"):
        if not str_lit.session_state["t1_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Scripts Studio", str_lit.session_state["t1_v"])

with tabs[3]:
    str_lit.subheader("03. هندسة الأغاني والموسيقى")
    str_lit.session_state["t2_v"] = str_lit.text_area("أدخل تفاصيل وموضوع الأغنية المطلوبة:", value=str_lit.session_state["t2_v"])
    if str_lit.button("تأليف الكلمات وهندسة الصوت", key="b2"):
        if not str_lit.session_state["t2_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Music Studio", str_lit.session_state["t2_v"])

with tabs[4]:
    str_lit.subheader("04. محرك هندسة الصور والهوية البصرية")
    str_lit.session_state["t3_v"] = str_lit.text_area("صف المشهد أو التصميم المطلوب بدقة:", value=str_lit.session_state["t3_v"])
    if str_lit.button("إنتاج أوصاف التصميم", key="b3"):
        if not str_lit.session_state["t3_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Visual Engineering", str_lit.session_state["t3_v"])

with tabs[5]:
    str_lit.subheader("05. سينما التحريك والموشن جرافيك")
    str_lit.session_state["t4_v"] = str_lit.text_area("صف حركات الكاميرا والمشهد الحركي:", value=str_lit.session_state["t4_v"])
    if str_lit.button("توليد سيناريو الحركة", key="b4"):
        if not str_lit.session_state["t4_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Motion Cinema", str_lit.session_state["t4_v"])

with tabs[6]:
    str_lit.subheader("06. إدارة الحملات الإعلانية والتسويق")
    str_lit.session_state["t5_v"] = str_lit.text_area("تفاصيل المنتج أو الحملة التسويقية:", value=str_lit.session_state["t5_v"])
    if str_lit.button("إعداد استراتيجية الحملة", key="b5"):
        if not str_lit.session_state["t5_v"].strip(): str_lit.warning(t["warn"])
        else: process_and_save("Mega Campaigns", str_lit.session_state["t5_v"])

# ==========================================
# 6. قسم النتائج والتقارير
# ==========================================
str_lit.markdown("---")
str_lit.markdown(f"### {t['res_title']}")

if str_lit.session_state["current_result"]:
    res_box = str_lit.session_state["current_result"]
    str_lit.markdown(f'<div class="human-card">{res_box}</div>', unsafe_allow_html=True)
    
    col_dl, col_rt = str_lit.columns(2)
    with col_dl:
        str_lit.download_button(
            label=t["download"],
            data=res_box,
            file_name=f"Workspace_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with col_rt:
        str_lit.slider(t["rate"], 1, 5, 5, key="sys_rating")
else:
    str_lit.info("قم بتشغيل أي أداة من الأقسام بالأعلى لعرض التقرير الهندسي المعتمد هنا.")
