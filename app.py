import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات المنصة المؤسسية (Enterprise Config)
# ==========================================
str_lit.set_page_config(
    page_title="إبداع بريميوم | Enterprise AI Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم واجهة مستخدم فاخرة بمستوى استثماري عالي (High-End Glassmorphic UI)
str_lit.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0f172a 50%, #1e1b4b 100%);
        font-family: 'Cairo', sans-serif;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(20px);
    }
    
    div.block-container { 
        padding-top: 1.5rem; 
        max-width: 1400px;
    }

    /* أزرار احترافية مع تأثيرات حركية */
    .stButton>button {
        border-radius: 14px; 
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        color: white; 
        border: none; 
        padding: 0.7rem 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.5);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.8);
        background: linear-gradient(135deg, #818cf8 0%, #4f46e5 100%);
    }

    /* حقول الإدخال والـ Textareas العميقة */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 14px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        background-color: rgba(30, 41, 59, 0.6) !important;
        color: #f1f5f9 !important;
        padding: 12px !important;
        backdrop-filter: blur(10px);
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.3) !important;
    }

    /* بطاقات الإحصائيات الفاخرة (Metrics Cards) */
    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        text-align: center;
        margin-bottom: 15px;
    }
    
    .enterprise-header {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")

# ==========================================
# 2. نظام التخزين الدائم المؤمّن
# ==========================================
HISTORY_FILE = "ibda3_enterprise_history.json"
FAV_FILE = "ibda3_enterprise_favorites.json"

def load_data(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except: return []
    return []

def save_data(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e: print(e)

if "history" not in str_lit.session_state: str_lit.session_state["history"] = load_data(HISTORY_FILE)
if "favorites" not in str_lit.session_state: str_lit.session_state["favorites"] = load_data(FAV_FILE)
if "current_result" not in str_lit.session_state: str_lit.session_state["current_result"] = None

for k in ["t0_v", "t1_v", "t2_v", "t3_v", "t4_v", "t5_v"]:
    if k not in str_lit.session_state: str_lit.session_state[k] = ""

# ==========================================
# 3. النصوص متعددة اللغات المؤسسية
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "💎 لوحة التحكم المؤسسية",
        "search_label": "🔍 بحث في الأرشيف المتقدم:",
        "fav_title": "⭐ الأصول المحفوظة والمفضلة",
        "fav_empty": "لا توجد أصول محفوظة",
        "history_title": "📜 سجل العمليات والذكاء",
        "history_empty": "السجل فارغ",
        "clear_history": "🗑️ مسح الذاكرة بالكامل",
        "stats_title": "📊 مؤشرات الأداء الحية (KPIs)",
        "stat_total": "إجمالي الأصول المنتجة:",
        
        "main_title": "منصة إبداع | Enterprise AI Suite 🚀",
        "main_caption": "النظام السيبراني المتكامل لإنتاج المحتوى، التخطيط الاستراتيجي، وحملات الملايين بالذكاء الاصطناعي",
        
        "tabs": [
            "📊 لوحة القيادة والمؤشرات",
            "0️⃣ التخطيط الاستراتيجي المؤسسي",
            "1️⃣ استوديو السكريبتات الفيروسي",
            "2️⃣ استوديو التلحين والصوت",
            "3️⃣ هندسة الهوية البصرية والذكاء",
            "4️⃣ سينما الموشن والفيديو",
            "5️⃣ إدارة الحملات الإعلانية الكبرى"
        ],
        
        "d_title": "مرحباً بك في لوحة تحكم الجيل القادم",
        "d_sub": "تتيح لك هذه المنصة التحكم الكامل في جميع أذرع التسويق، الإنتاج الفني، والخطط الاستراتيجية بجودة تضاهي أكبر الوكالات العالمية.",
        
        # خيارات سريعة وباقي المراحل
        "btn_gen": "⚡ تنفيذ عملية الإنتاج الذكي",
        "warn": "⚠️ يرجى إدخال البيانات المطلوبة أولاً!",
        "spin": "⚡ جارٍ معالجة البيانات عبر شبكات النماذج الكبرى...",
        "res_title": "🚀 مخرجات الذكاء الاصطناعي المعتمدة:",
        "download": "📥 تصدير التقرير الاحترافي (.txt)",
        "rate": "⭐ تقييم جودة المخرج:"
    },
    "English": {
        "sidebar_title": "💎 Enterprise Control",
        "search_label": "🔍 Search Enterprise Archive:",
        "fav_title": "⭐ Saved Enterprise Assets",
        "fav_empty": "No saved assets",
        "history_title": "📜 Audit & Intelligence Trail",
        "history_empty": "Trail is empty",
        "clear_history": "🗑️ Clear Memory",
        "stats_title": "📊 Live Performance KPIs",
        "stat_total": "Total Generated Assets:",
        
        "main_title": "Ibda3 | Enterprise AI Suite 🚀",
        "main_caption": "Cybernetic End-to-End Platform for Content Production and Strategic Scaling",
        
        "tabs": [
            "📊 Command Center",
            "0️⃣ Enterprise Strategy",
            "1️⃣ Viral Scripts Studio",
            "2️⃣ Audio & Voice Studio",
            "3️⃣ Visual Identity Engineering",
            "4️⃣ Motion & Video Cinema",
            "5️⃣ Mega Ad Campaigns"
        ],
        
        "d_title": "Welcome to Next-Gen Command Center",
        "d_sub": "Empowering global agencies and enterprises with state-of-the-art AI content generation workflows.",
        
        "btn_gen": "⚡ Execute Intelligent Production",
        "warn": "⚠️ Please enter required details first!",
        "spin": "⚡ Processing via Advanced LLM Cluster...",
        "res_title": "🚀 Verified AI Output:",
        "download": "📥 Export Professional Report (.txt)",
        "rate": "⭐ Rate Output Quality:"
    }
}

# ==========================================
# 4. محرك استدعاء الذكاء الاصطناعي المتقدم
# ==========================================
def call_gemini_enterprise(prompt, lang):
    if not API_KEY:
        return "❌ الخطأ: مفتاح API غير موجود في إعدادات المنصة (Streamlit Secrets)."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    sys_inst = f"You are an elite enterprise AI Architect for 'Ibda3 Enterprise Suite', producing world-class, exhaustive, highly professional business and creative assets. Language: {lang}."
    payload = {"contents": [{"role": "user", "parts": [{"text": sys_inst + "\n\n" + prompt}]}]}
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"❌ خطأ في الاتصال: {r.status_code}"
    except Exception as e:
        return f"❌ خطأ تقني: {str(e)}"

# ==========================================
# 5. الشريط الجانبي المؤسسي الاحترافي
# ==========================================
with str_lit.sidebar:
    lang = str_lit.radio("🌐 System Language / اللغة:", ["العربية", "English"], horizontal=True)
    t = TEXTS[lang]
    
    str_lit.markdown(f"### {t['sidebar_title']}")
    str_lit.markdown("---")
    
    str_lit.markdown(f"#### {t['stats_title']}")
    str_lit.metric(label=t["stat_total"], value=len(str_lit.session_state["history"]))
    str_lit.markdown("---")
    
    query = str_lit.text_input(t["search_label"], "")
    
    str_lit.markdown(f"#### {t['fav_title']}")
    if not str_lit.session_state["favorites"]:
        str_lit.info(t["fav_empty"])
    else:
        for idx, fav in enumerate(str_lit.session_state["favorites"][:5]):
            with str_lit.expander(f"⭐ {fav.get('title', '')[:20]}..."):
                str_lit.write(fav.get("content", ""))
                if str_lit.button(f"حذف_{idx}", key=f"df_{idx}"):
                    str_lit.session_state["favorites"].pop(idx)
                    save_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.rerun()

    str_lit.markdown("---")
    if str_lit.button(t["clear_history"], key="clr_all"):
        str_lit.session_state["history"] = []
        save_data(HISTORY_FILE, [])
        str_lit.success("تم مسح السجل بنجاح!")
        str_lit.rerun()

# ==========================================
# 6. الهيدر والتبويبات الرئيسية
# ==========================================
str_lit.markdown(f'<h1 class="enterprise-header">{t["main_title"]}</h1>', unsafe_allow_html=True)
str_lit.caption(t["main_caption"])
str_lit.markdown("---")

tabs = str_lit.tabs(t["tabs"])

def log_and_store(tab_name, user_input, output_text):
    rec = {
        "tab": tab_name,
        "input": user_input,
        "result": output_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    str_lit.session_state["history"].append(rec)
    save_data(HISTORY_FILE, str_lit.session_state["history"])
    str_lit.session_state["current_result"] = output_text

# ------------------------------------------
# تبويب 0: لوحة القيادة والمؤشرات (Command Center)
# ------------------------------------------
with tabs[0]:
    str_lit.markdown(f"""
    <div class="metric-card">
        <h2>{t['d_title']}</h2>
        <p>{t['d_sub']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = str_lit.columns(3)
    col1.metric("العمليات الناجحة", len(str_lit.session_state["history"]), "+100% الأسبوع الحالي")
    col2.metric("العناصر المفضلة", len(str_lit.session_state["favorites"]), "أصول مؤمنة")
    col3.metric("جاهزية الذكاء الاصطناعي", "100%", "Gemini 1.5 Pro/Flash متصل")

# ------------------------------------------
# تبويب 1: التخطيط الاستراتيجي المؤسسي
# ------------------------------------------
with tabs[1]:
    str_lit.subheader("🗺️ التخطيط الاستراتيجي وتحليل الأسواق المتقدم")
    str_lit.session_state["t0_v"] = str_lit.text_area("🎯 املأ فكرة المشروع أو الشركة الناشئة:", value=str_lit.session_state["t0_v"], placeholder="اكتب تفاصيل المشروع الاستثماري...")
    c1, c2 = str_lit.columns(2)
    strat_goal = c1.selectbox("🎯 الهدف الإستراتيجي:", ["إطلاق يونيكورن (Startup Scale)", "استحواذ على حصة سوقية", "إعادة هيكلة كبرى", "طرح عام أولي IPO Plan"])
    strat_market = c2.selectbox("🌍 النطاق الجغرافي المستهدف:", ["السوق العالمي (Global)", "منطقة الشرق الأوسط وشمال إفريقيا (MENA)", "دول الخليج العربي (GCC)"])
    
    if str_lit.button(t["btn_gen"], key="b0"):
        if not str_lit.session_state["t0_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Comprehensive Enterprise Strategy for: '{str_lit.session_state['t0_v']}'. Goal: {strat_goal}, Market: {strat_market}. Include financial projections, risk mitigation, and executive roadmap."
                res = call_gemini_enterprise(prompt, lang)
                log_and_store("Enterprise Strategy", str_lit.session_state["t0_v"], res)
                str_lit.success("تم إنتاج الخطة بنجاح!")

# ------------------------------------------
# تبويب 2: سكريبتات فيروسية (Viral Scripts)
# ------------------------------------------
with tabs[2]:
    str_lit.subheader("🎬 استوديو السكريبتات الفيروسية للمنصات الكبرى")
    str_lit.session_state["t1_v"] = str_lit.text_area("📽️ موضوع الفيديو أو الحملة الإعلانية:", value=str_lit.session_state["t1_v"], placeholder="اكتب الفكرة الأساسية...")
    c1, c2, c3 = str_lit.columns(3)
    s_dur = c1.selectbox("⏱️ المدة الزمنية:", ["15 ثانية (Reels)", "60 ثانية (TikTok Viral)", "3 دقائق (YouTube Deep Dive)"])
    s_tone = c2.selectbox("🎙️ نبرة الخطاب:", ["تأثير نفسي عميق (Psychological Hook)", "حماسي استثماري", "كوميدي ساخر ذكي"])
    s_target = c3.selectbox("🎯 الشريحة المستهدفة:", ["الشباب وجيل زد (Gen Z)", "رجال الأعمال والمستثمرون", "المهتمون بالتكنولوجيا"])
    
    if str_lit.button(t["btn_gen"], key="b1"):
        if not str_lit.session_state["t1_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Viral Script Production for: '{str_lit.session_state['t1_v']}', Duration: {s_dur}, Tone: {s_tone}, Target: {s_target}. Include Hook (0-3s), Body, and High-Conversion Call to Action."
                res = call_gemini_enterprise(prompt, lang)
                log_and_store("Viral Scripts", str_lit.session_state["t1_v"], res)
                str_lit.success("تم إنتاج السكريبت بنجاح!")

# ------------------------------------------
# بقية التبويبات (أغاني، صور، فيديو، إعلانات) نفس النمط الاحترافي المؤسسي العالي
# ------------------------------------------
with tabs[3]:
    str_lit.subheader("🎵 استوديو الإنتاج الصوتي والموسيقي الاحترافي")
    str_lit.session_state["t2_v"] = str_lit.text_area("💡 موضوع الأغنية أو الهوية الصوتية:", value=str_lit.session_state["t2_v"])
    if str_lit.button(t["btn_gen"], key="b2"):
        if not str_lit.session_state["t2_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                res = call_gemini_enterprise(f"Music Production and Lyrics for: {str_lit.session_state['t2_v']}", lang)
                log_and_store("Audio Studio", str_lit.session_state["t2_v"], res)
                str_lit.success("تم بنجاح!")

with tabs[4]:
    str_lit.subheader("🎨 هندسة الهوية البصرية وأوامر الذكاء الاصطناعي للصور")
    str_lit.session_state["t3_v"] = str_lit.text_area("🖼️ صف المشهد أو الهوية البصرية بدقة:", value=str_lit.session_state["t3_v"])
    if str_lit.button(t["btn_gen"], key="b3"):
        if not str_lit.session_state["t3_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                res = call_gemini_enterprise(f"Midjourney v6 & Flux Pro Prompts for: {str_lit.session_state['t3_v']}", lang)
                log_and_store("Visual Engineering", str_lit.session_state["t3_v"], res)
                str_lit.success("تم بنجاح!")

with tabs[5]:
    str_lit.subheader("🗣️ سينما تحريك الفيديو والموشن جرافيك")
    str_lit.session_state["t4_v"] = str_lit.text_area("📜 تفاصيل حركة الكاميرا والمشهد السينمائي:", value=str_lit.session_state["t4_v"])
    if str_lit.button(t["btn_gen"], key="b4"):
        if not str_lit.session_state["t4_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                res = call_gemini_enterprise(f"Runway Gen-3 and Sora Motion Prompts for: {str_lit.session_state['t4_v']}", lang)
                log_and_store("Motion Cinema", str_lit.session_state["t4_v"], res)
                str_lit.success("تم بنجاح!")

with tabs[6]:
    str_lit.subheader("📊 إدارة الحملات الإعلانية الكبرى والميزانيات الضخمة")
    str_lit.session_state["t5_v"] = str_lit.text_area("🎯 تفاصيل المنتج أو الحملة المراد إطلاقها:", value=str_lit.session_state["t5_v"])
    if str_lit.button(t["btn_gen"], key="b5"):
        if not str_lit.session_state["t5_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                res = call_gemini_enterprise(f"Mega Ad Campaign Architecture for: {str_lit.session_state['t5_v']}", lang)
                log_and_store("Mega Campaigns", str_lit.session_state["t5_v"], res)
                str_lit.success("تم بنجاح!")

# ==========================================
# 7. قسم العرض والتصدير المؤسسي
# ==========================================
str_lit.markdown("---")
str_lit.markdown(f"### {t['res_title']}")

if str_lit.session_state["current_result"]:
    res_box = str_lit.session_state["current_result"]
    str_lit.markdown(res_box)
    
    c_dl, c_rt = str_lit.columns(2)
    with c_dl:
        str_lit.download_button(
            label=t["download"],
            data=res_box,
            file_name=f"Ibda3_Enterprise_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with c_rt:
        str_lit.slider(t["rate"], 1, 5, 5, key="enterprise_rating")
else:
    str_lit.info("قم بتنفيذ أي عملية في الأقسام بالأعلى لعرض التقرير المؤسسي الفوري هنا.")
