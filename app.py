import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة وتصميم واجهة المستخدم
# ==========================================
str_lit.set_page_config(
    page_title="Smart Content Studio - Safe Pipeline Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

str_lit.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 50%, #020617 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
    }
    div.block-container { padding-top: 2rem; }
    .stButton>button {
        border-radius: 12px; font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white; border: none; padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
    }
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #f1f5f9 !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")

# ==========================================
# 2. نظام التخزين الدائم الآمن (لا يحذف الهيستوري أبداً)
# ==========================================
HISTORY_FILE = "safe_content_studio_history.json"
FAV_FILE = "safe_content_studio_favorites.json"

def load_persistent_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_persistent_data(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# ضمان عدم ضياع الهيستوري والمفضلة نهائياً عند الـ Refresh
if "history" not in str_lit.session_state:
    str_lit.session_state["history"] = load_persistent_data(HISTORY_FILE)

if "favorites" not in str_lit.session_state:
    str_lit.session_state["favorites"] = load_persistent_data(FAV_FILE)

if "current_result" not in str_lit.session_state:
    str_lit.session_state["current_result"] = None

# تهيئة حقول الإدخال للمراحل الستة لمنع تفريغها
for key in ["t0_val", "t1_val", "t2_val", "t3_val", "t4_val", "t5_val"]:
    if key not in str_lit.session_state:
        str_lit.session_state[key] = ""

# ==========================================
# 3. القاموس اللغوي الشامل
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚡ لوحة التحكم والأرشيف الآمن",
        "search_label": "🔍 بحث في الأرشيف القديم والجديد:",
        "fav_title": "⭐ العناصر المفضلة المحفوظة",
        "fav_empty": "لا توجد مفضلات مسجلة",
        "history_title": "📜 الأرشيف الدائم (محفوظ ضد الفقدان)",
        "history_empty": "الأرشيف فارغ حالياً",
        "clear_history": "🗑️ تفريغ الأرشيف",
        "stats_title": "📊 المؤشرات",
        "stat_total": "إجمالي العمليات المحفوظة:",
        "main_title": "🎙️ استوديو المحتوى والخطط الشامل (Safe Pipeline Pro)",
        "main_caption": "منظومة متكاملة لإنتاج المحتوى والخطط مع حماية تامة وثبات دائم للأرشيف",
        "tabs": [
            "0️⃣ 🗺️ التخطيط الاستراتيجي",
            "1️⃣ 💡 الأفكار والسكريبتات",
            "2️⃣ 🎵 الأغاني والصوت",
            "3️⃣ 🎨 تصميم الصور والهوية",
            "4️⃣ 🗣️ تحريك الفيديو",
            "5️⃣ 📊 التسويق والإعلانات"
        ],
        "t0_header": "🗺️ المرحلة الأولى: التخطيط الاستراتيجي وإدارة المشروع",
        "t0_input_label": "🎯 ما هو مشروعك أو الفكرة العامة؟",
        "t0_input_placeholder": "اكتب فكرة المشروع بالتفصيل...",
        "t0_goal": "🎯 الهدف الرئيسي من المشروع:",
        "t0_goal_opts": ["إطلاق مشروع أو براند جديد", "حملة تسويقية لمحتوى رقمي", "سلسلة بودكاست أو تعليم", "خطة نمو مبيعات"],
        "t0_btn": "🗺️ بناء الخطة الاستراتيجية",
        "t0_warn": "⚠️ يرجى إدخال تفاصيل المشروع أولاً!",
        "t0_spin": "⚡ جارٍ تحليل السوق وصياغة الخطة...",

        "t1_header": "🎬 المرحلة الثانية: صانع الأفكار والسكريبتات",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": ["15 ثانية (Shorts)", "30 ثانية", "60 ثانية (TikTok)", "3 دقائق", "10 دقائق"],
        "t1_style": "🎨 النمط البصري:",
        "t1_style_opts": ["سينمائي واقعي", "وثائقي", "تعليمي تفاعلي", "حماسي", "قصصي درامي"],
        "t1_target": "🎯 الجمهور المستهدف:",
        "t1_target_opts": ["الشباب (Gen Z)", "رواد الأعمال", "المهنيين", "العامة"],
        "t1_btn": "🔥 توليد السكريبت",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ توليد السكريبت...",

        "t2_header": "🎵 المرحلة الثالثة: الأغاني والموسيقى",
        "t2_input_label": "💡 فكرة الأغنية أو الكلمات:",
        "t2_input_placeholder": "اكتب موضوع الأغنية...",
        "t2_dialect": "🗣️ اللهجة أو الطابع:",
        "t2_dialect_opts": ["عامية مصرية", "فصحى", "خليجي", "إنجليزي بوب"],
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_style_opts": ["مهرجانات / شعبي", "راب سريع", "بوب هادئ", "أكوستيك"],
        "t2_vocal": "🎙️ صوت المغني:",
        "t2_vocal_opts": ["رجالي عميق", "شبابي حماسي", "نسائي دافئ", "أوتوتيون"],
        "t2_btn": "✨ توليد الكلمات والصوت",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات...",

        "t3_header": "🎨 المرحلة الرابعة: الصور والهوية البصرية",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه:",
        "t3_input_placeholder": "صف تفاصيل الصورة بدقة...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي:",
        "t3_engine_opts": ["Midjourney v6", "Flux.1", "DALL-E 3", "Adobe Firefly"],
        "t3_aspect": "📐 الأبعاد:",
        "t3_aspect_opts": ["9:16 (Reels/TikTok)", "16:9 (YouTube)", "1:1 (Square)", "4:5 (Portrait)"],
        "t3_light": "💡 الإضاءة:",
        "t3_light_opts": ["سينمائية استوديو", "سايبربانك نيون", "ساعة ذهبية", "درامي مظلم"],
        "t3_btn": "🎨 توليد أوامر الصور",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة!",
        "t3_spin": "⚡ هندسة الأوامر...",

        "t4_header": "🗣️ المرحلة الخامسة: تحريك الفيديو",
        "t4_input_label": "📜 النص أو حركة الكاميرا:",
        "t4_input_placeholder": "صف الحركة المطلوبة...",
        "t4_tool": "🤖 أداة التحريك:",
        "t4_tool_opts": ["Runway Gen-3", "Luma Dream Machine", "HeyGen Avatar", "Pika Labs"],
        "t4_cam": "🎥 حركة الكاميرا:",
        "t4_cam_opts": ["زوم إن بطيء", "زوم أوت درامي", "بانوراما", "تتبع حركي"],
        "t4_btn": "⚡ توليد أوامر التحريك",
        "t4_warn": "⚠️ يرجى إدخال تفاصيل الحركة!",
        "t4_spin": "⚡ إعداد مسار الحركة...",

        "t5_header": "📊 المرحلة السادسة: التسويق والإعلانات",
        "t5_input_label": "🎯 المنتج أو الخدمة للتسويق:",
        "t5_input_placeholder": "تفاصيل الحملة...",
        "t5_plat": "📱 المنصة:",
        "t5_plat_opts": ["TikTok Ads", "Instagram", "YouTube", "LinkedIn"],
        "t5_goal": "🎯 الهدف:",
        "t5_goal_opts": ["مبيعات", "وعي بالعلامة التجارية", "زيارات", "تجميع ليدز"],
        "t5_budget": "💰 الميزانية ($):",
        "t5_btn": "🚀 تنفيذ الخطة التسويقية",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل الحملة!",
        "t5_spin": "⚡ تحليل السوق...",

        "result_label": "🚀 النتيجة الاحترافية المحفوظة:",
        "copy_btn": "📋 نسخ",
        "download_txt": "📥 تحميل ملف (.txt)",
        "rating_label": "⭐ التقييم:"
    },
    "English": {
        "sidebar_title": "⚡ Safe Control Panel & Archive",
        "search_label": "🔍 Search Archive:",
        "fav_title": "⭐ Saved Favorites",
        "fav_empty": "No favorites saved yet",
        "history_title": "📜 Persistent Archive",
        "history_empty": "Archive is empty",
        "clear_history": "🗑️ Clear Archive",
        "stats_title": "📊 Metrics",
        "stat_total": "Total Saved Tasks:",
        "main_title": "🎙️ Unified Content Studio (Safe Pipeline Pro)",
        "main_caption": "End-to-end studio with guaranteed persistent archive protection",
        "tabs": ["0️⃣ Strategy", "1️⃣ Scripts", "2️⃣ Music", "3️⃣ Images", "4️⃣ Video", "5️⃣ Marketing"],
        "t0_header": "Phase 1: Strategy", "t0_input_label": "Core Idea:", "t0_input_placeholder": "Enter idea...",
        "t0_goal": "Goal:", "t0_goal_opts": ["Startup", "Campaign", "Podcast", "Growth"], "t0_btn": "Build Strategy",
        "t0_warn": "Enter details!", "t0_spin": "Analyzing...",
        "t1_header": "Phase 2: Scripts", "t1_input_label": "Video Idea:", "t1_input_placeholder": "Enter video...",
        "t1_dur": "Duration:", "t1_dur_opts": ["15s", "30s", "60s", "3m"], "t1_style": "Style:", "t1_style_opts": ["Cinematic", "Doc"],
        "t1_target": "Audience:", "t1_target_opts": ["Gen Z", "Entrepreneurs"], "t1_btn": "Generate Script", "t1_warn": "Enter idea!", "t1_spin": "Generating...",
        "t2_header": "Phase 3: Music", "t2_input_label": "Song Idea:", "t2_input_placeholder": "Song theme...",
        "t2_dialect": "Flavor:", "t2_dialect_opts": ["Egyptian", "Classical"], "t2_style": "Genre:", "t2_style_opts": ["Mahraganat", "Rap"],
        "t2_vocal": "Vocal:", "t2_vocal_opts": ["Deep", "Energetic"], "t2_btn": "Generate Song", "t2_warn": "Enter song!", "t2_spin": "Crafting...",
        "t3_header": "Phase 4: Images", "t3_input_label": "Scene Description:", "t3_input_placeholder": "Describe scene...",
        "t3_engine": "Engine:", "t3_engine_opts": ["Midjourney", "Flux"], "t3_aspect": "Aspect:", "t3_aspect_opts": ["9:16", "16:9"],
        "t3_light": "Lighting:", "t3_light_opts": ["Studio", "Neon"], "t3_btn": "Generate Prompts", "t3_warn": "Enter description!", "t3_spin": "Engineering...",
        "t4_header": "Phase 5: Video Motion", "t4_input_label": "Motion Text:", "t4_input_placeholder": "Motion details...",
        "t4_tool": "Tool:", "t4_tool_opts": ["Runway", "Luma"], "t4_cam": "Camera:", "t4_cam_opts": ["Slow Zoom", "Pan"],
        "t4_btn": "Generate Motion", "t4_warn": "Enter motion!", "t4_spin": "Preparing...",
        "t5_header": "Phase 6: Marketing", "t5_input_label": "Product:", "t5_input_placeholder": "Campaign details...",
        "t5_plat": "Platform:", "t5_plat_opts": ["TikTok", "Instagram"], "t5_goal": "Goal:", "t5_goal_opts": ["Sales", "Awareness"],
        "t5_budget": "Budget ($):", "t5_btn": "Execute", "t5_warn": "Enter details!", "t5_spin": "Analyzing...",
        "result_label": "🚀 Saved Professional Result:", "copy_btn": "Copy", "download_txt": "Download (.txt)", "rating_label": "Rating:"
    }
}

# ==========================================
# 4. دالة استدعاء النموذج
# ==========================================
def call_gemini(prompt_text, lang_choice):
    if not API_KEY:
        return "❌ الخطأ: مفتاح API الخاص بـ Gemini غير موجود في أسرار Streamlit Secrets."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    system_instruction = f"You are an elite AI Studio Expert. Language: {lang_choice}."
    payload = {"contents": [{"role": "user", "parts": [{"text": system_instruction + "\n\n" + prompt_text}]}]}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ خطأ في الاتصال: {response.status_code}"
    except Exception as e:
        return f"❌ خطأ غير متوقع: {str(e)}"

# ==========================================
# 5. الشريط الجانبي (منع تام لتأثر الأرشيف)
# ==========================================
with str_lit.sidebar:
    selected_lang = str_lit.radio("🌐 Language / اللغة:", ["العربية", "English"], horizontal=True, key="lang_radio")
    t = TEXTS[selected_lang]
    
    str_lit.markdown(f"### {t['sidebar_title']}")
    str_lit.markdown("---")
    
    str_lit.markdown(f"#### {t['stats_title']}")
    str_lit.metric(label=t["stat_total"], value=len(str_lit.session_state["history"]))
    str_lit.markdown("---")
    
    search_query = str_lit.text_input(t["search_label"], "")
    
    str_lit.markdown("---")
    str_lit.markdown(f"#### {t['fav_title']}")
    if not str_lit.session_state["favorites"]:
        str_lit.info(t["fav_empty"])
    else:
        for idx, fav in enumerate(str_lit.session_state["favorites"][:10]):
            with str_lit.expander(f"⭐ {fav.get('title', 'Item')} ({fav.get('time', '')})"):
                str_lit.write(fav.get("content", ""))
                if str_lit.button(f"🗑️ حذف_{idx}", key=f"del_fav_{idx}"):
                    str_lit.session_state["favorites"].pop(idx)
                    save_persistent_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.rerun()

    str_lit.markdown("---")
    str_lit.markdown(f"#### {t['history_title']}")
    if str_lit.button(t["clear_history"], key="clear_hist_btn"):
        str_lit.session_state["history"] = []
        save_persistent_data(HISTORY_FILE, [])
        str_lit.success("تم تفريغ الأرشيف بنجاح!")
        str_lit.rerun()
        
    if not str_lit.session_state["history"]:
        str_lit.info(t["history_empty"])
    else:
        reversed_history = list(reversed(str_lit.session_state["history"]))
        for i, item in enumerate(reversed_history):
            if search_query and search_query.lower() not in item.get("input", "").lower() and search_query.lower() not in item.get("result", "").lower():
                continue
            with str_lit.expander(f"📌 [{item.get('tab', '')}] {item.get('input', '')[:25]}..."):
                str_lit.text(f"الوقت: {item.get('time', '')}")
                str_lit.markdown(item.get("result", ""))
                if str_lit.button(f"⭐ مفضلة_{i}", key=f"fav_add_{i}"):
                    str_lit.session_state["favorites"].append({
                        "title": item.get('input', 'Item')[:30],
                        "content": item.get("result", ""),
                        "time": item.get("time", "")
                    })
                    save_persistent_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.success("تمت الإضافة للمفضلة!")

# ==========================================
# 6. الواجهة الرئيسية والتبويبات
# ==========================================
str_lit.title(t["main_title"])
str_lit.caption(t["main_caption"])
str_lit.markdown("---")

tabs = str_lit.tabs(t["tabs"])

def log_and_save(tab_name, input_val, result_text):
    record = {
        "tab": tab_name,
        "input": input_val,
        "result": result_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    str_lit.session_state["history"].append(record)
    save_persistent_data(HISTORY_FILE, str_lit.session_state["history"])
    str_lit.session_state["current_result"] = result_text

# تبويب 0: التخطيط
with tabs[0]:
    str_lit.subheader(t["t0_header"])
    str_lit.session_state["t0_val"] = str_lit.text_area(t["t0_input_label"], value=str_lit.session_state["t0_val"], placeholder=t["t0_input_placeholder"], key="t0_w")
    goal_0 = str_lit.selectbox(t["t0_goal"], t["t0_goal_opts"], key="t0_g")
    if str_lit.button(t["t0_btn"], key="t0_b"):
        if not str_lit.session_state["t0_val"].strip():
            str_lit.warning(t["t0_warn"])
        else:
            with str_lit.spinner(t["t0_spin"]):
                res = call_gemini(f"Strategic plan for: '{str_lit.session_state['t0_val']}'. Goal: {goal_0}", selected_lang)
                log_and_save("Strategic Planning", str_lit.session_state["t0_val"], res)
                str_lit.success("تم بنجاح!")

# تبويب 1: الأفكار والسكريبتات
with tabs[1]:
    str_lit.subheader(t["t1_header"])
    str_lit.session_state["t1_val"] = str_lit.text_area(t["t1_input_label"], value=str_lit.session_state["t1_val"], placeholder=t["t1_input_placeholder"], key="t1_w")
    c1, c2, c3 = str_lit.columns(3)
    dur = c1.selectbox(t["t1_dur"], t["t1_dur_opts"], key="t1_d")
    style = c2.selectbox(t["t1_style"], t["t1_style_opts"], key="t1_s")
    target = c3.selectbox(t["t1_target"], t["t1_target_opts"], key="t1_t")
    if str_lit.button(t["t1_btn"], key="t1_b"):
        if not str_lit.session_state["t1_val"].strip():
            str_lit.warning(t["t1_warn"])
        else:
            with str_lit.spinner(t["t1_spin"]):
                res = call_gemini(f"Video script for: '{str_lit.session_state['t1_val']}', Duration: {dur}, Style: {style}, Target: {target}", selected_lang)
                log_and_save("Ideas & Scripts", str_lit.session_state["t1_val"], res)
                str_lit.success("تم بنجاح!")

# تبويب 2: الأغاني والصوت
with tabs[2]:
    str_lit.subheader(t["t2_header"])
    str_lit.session_state["t2_val"] = str_lit.text_area(t["t2_input_label"], value=str_lit.session_state["t2_val"], placeholder=t["t2_input_placeholder"], key="t2_w")
    c1, c2, c3 = str_lit.columns(3)
    dialect = c1.selectbox(t["t2_dialect"], t["t2_dialect_opts"], key="t2_d")
    genre = c2.selectbox(t["t2_style"], t["t2_style_opts"], key="t2_s")
    vocal = c3.selectbox(t["t2_vocal"], t["t2_vocal_opts"], key="t2_v")
    if str_lit.button(t["t2_btn"], key="t2_b"):
        if not str_lit.session_state["t2_val"].strip():
            str_lit.warning(t["t2_warn"])
        else:
            with str_lit.spinner(t["t2_spin"]):
                res = call_gemini(f"Song lyrics and audio for: '{str_lit.session_state['t2_val']}', Dialect: {dialect}, Genre: {genre}, Vocal: {vocal}", selected_lang)
                log_and_save("Music & Audio", str_lit.session_state["t2_val"], res)
                str_lit.success("تم بنجاح!")

# تبويب 3: الصور والهوية
with tabs[3]:
    str_lit.subheader(t["t3_header"])
    str_lit.session_state["t3_val"] = str_lit.text_area(t["t3_input_label"], value=str_lit.session_state["t3_val"], placeholder=t["t3_input_placeholder"], key="t3_w")
    c1, c2, c3 = str_lit.columns(3)
    engine = c1.selectbox(t["t3_engine"], t["t3_engine_opts"], key="t3_e")
    aspect = c2.selectbox(t["t3_aspect"], t["t3_aspect_opts"], key="t3_a")
    light = c3.selectbox(t["t3_light"], t["t3_light_opts"], key="t3_l")
    if str_lit.button(t["t3_btn"], key="t3_b"):
        if not str_lit.session_state["t3_val"].strip():
            str_lit.warning(t["t3_warn"])
        else:
            with str_lit.spinner(t["t3_spin"]):
                res = call_gemini(f"Image prompt for: '{str_lit.session_state['t3_val']}', Engine: {engine}, Aspect: {aspect}, Lighting: {light}", selected_lang)
                log_and_save("Image Prompts", str_lit.session_state["t3_val"], res)
                str_lit.success("تم بنجاح!")

# تبويب 4: تحريك الفيديو
with tabs[4]:
    str_lit.subheader(t["t4_header"])
    str_lit.session_state["t4_val"] = str_lit.text_area(t["t4_input_label"], value=str_lit.session_state["t4_val"], placeholder=t["t4_input_placeholder"], key="t4_w")
    c1, c2 = str_lit.columns(2)
    tool = c1.selectbox(t["t4_tool"], t["t4_tool_opts"], key="t4_t")
    cam = c2.selectbox(t["t4_cam"], t["t4_cam_opts"], key="t4_c")
    if str_lit.button(t["t4_btn"], key="t4_b"):
        if not str_lit.session_state["t4_val"].strip():
            str_lit.warning(t["t4_warn"])
        else:
            with str_lit.spinner(t["t4_spin"]):
                res = call_gemini(f"Video motion prompt for: '{str_lit.session_state['t4_val']}', Tool: {tool}, Camera: {cam}", selected_lang)
                log_and_save("Video Motion", str_lit.session_state["t4_val"], res)
                str_lit.success("تم بنجاح!")

# تبويب 5: التسويق والإعلانات
with tabs[5]:
    str_lit.subheader(t["t5_header"])
    str_lit.session_state["t5_val"] = str_lit.text_area(t["t5_input_label"], value=str_lit.session_state["t5_val"], placeholder=t["t5_input_placeholder"], key="t5_w")
    c1, c2, c3 = str_lit.columns(3)
    plat = c1.selectbox(t["t5_plat"], t["t5_plat_opts"], key="t5_p")
    goal = c2.selectbox(t["t5_goal"], t["t5_goal_opts"], key="t5_g")
    budget = c3.number_input(t["t5_budget"], min_value=50, max_value=100000, value=1000, step=50, key="t5_bgt")
    if str_lit.button(t["t5_btn"], key="t5_b"):
        if not str_lit.session_state["t5_val"].strip():
            str_lit.warning(t["t5_warn"])
        else:
            with str_lit.spinner(t["t5_spin"]):
                res = call_gemini(f"Marketing campaign for: '{str_lit.session_state['t5_val']}', Platform: {plat}, Goal: {goal}, Budget: ${budget}", selected_lang)
                log_and_save("Marketing Strategy", str_lit.session_state["t5_val"], res)
                str_lit.success("تم بنجاح!")

# ==========================================
# 7. قسم النتائج والتصدير
# ==========================================
str_lit.markdown("---")
str_lit.subheader(t["result_label"])

if str_lit.session_state["current_result"]:
    current_res = str_lit.session_state["current_result"]
    str_lit.markdown(current_res)
    
    col_a, col_b = str_lit.columns(2)
    with col_a:
        str_lit.download_button(
            label=t["download_txt"],
            data=current_res,
            file_name=f"Studio_Result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with col_b:
        str_lit.slider(t["rating_label"], 1, 5, 5, key="result_rating")
else:
    str_lit.info("قم بتنفيذ أي خيار بالأعلى لعرض النتيجة الفورية هنا.")
