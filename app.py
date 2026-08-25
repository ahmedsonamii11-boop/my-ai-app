import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم
# ==========================================
st.set_page_config(
    page_title="Smart Content Studio - Ultimate Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 50%, #020617 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    div.block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
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
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم
# ==========================================
HISTORY_FILE = "content_studio_history.json"
FAV_FILE = "content_studio_favorites.json"

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

if "history" not in st.session_state:
    st.session_state["history"] = load_data(HISTORY_FILE)

if "favorites" not in st.session_state:
    st.session_state["favorites"] = load_data(FAV_FILE)

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = 0

if "current_result" not in st.session_state:
    st.session_state["current_result"] = None

# تهيئة الحقول
for k in ["t1_val", "t2_val", "t3_val", "t4_val", "t5_val"]:
    if k not in st.session_state:
        st.session_state[k] = ""

# ==========================================
# 2. القاموس الشامل للنصوص
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚡ لوحة التحكم التجارية",
        "search_label": "🔍 بحث في السجل:",
        "fav_title": "⭐ العناصر المفضلة",
        "fav_empty": "لا توجد مفضلات مسجلة",
        "history_title": "📜 أرشيف العمليات",
        "history_empty": "الأرشيف فارغ حالياً",
        "clear_history": "🗑️ تفريغ الأرشيف",
        "stats_title": "📊 مؤشرات الأداء",
        "stat_total": "إجمالي المهام المنجزة:",
        "main_title": "🎙️ استوديو المحتوى التجاري (Ultimate Pro)",
        "main_caption": "منظومة ذكاء اصطناعي متكاملة مع ميزة النسخ السريع للمخرجات",
        
        "tabs": [
            "1️⃣ الأفكار والسكريبتات",
            "2️⃣ استوديو الأغاني",
            "3️⃣ تصميم الصور",
            "4️⃣ تحريك الفيديو",
            "5️⃣ استراتيجيات التسويق"
        ],
        
        "t1_header": "🎬 صانع الأفكار والسكريبتات الاحترافية",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو بالتفصيل...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": ["10 ثوانٍ", "15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق", "5 دقائق"],
        "t1_style": "🎨 النمط البصري:",
        "t1_style_opts": ["سينمائي واقعي", "وثائقي", "كوميدي", "تعليمي", "حماسي تحفيزي"],
        "t1_target": "🎯 الجمهور المستهدف:",
        "t1_target_opts": ["الشباب (Gen Z)", "رواد الأعمال", "العامة والترفيه", "عشاق التقنية"],
        "t1_btn": "🔥 توليد السكريبت والخطافات",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ توليد السكريبت...",

        "t2_header": "🎵 صناعة الأغاني والهندسة الصوتية",
        "t2_input_label": "💡 فكرة الأغنية أو موضوع الكلمات:",
        "t2_input_placeholder": "اكتب موضوع الأغنية...",
        "t2_dialect": "🗣️ اللهجة:",
        "t2_dialect_opts": ["عامية مصرية", "فصحى", "خليجي", "إنجليزي"],
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_style_opts": ["مهرجانات / شعبي", "راب / هيب هوب", "بوب", "أكوستيك"],
        "t2_vocal": "🎙️ أداء الصوت:",
        "t2_vocal_opts": ["رجالي عميق", "نسائي دافئ", "شبابي حماسي"],
        "t2_btn": "✨ توليد الكلمات والقالب",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات...",

        "t3_header": "🎨 مهندس برومبتات الصور",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه:",
        "t3_input_placeholder": "صف تفاصيل الصورة...",
        "t3_engine": "🎯 المحرك:",
        "t3_engine_opts": ["Midjourney v6", "Flux.1", "DALL-E 3", "Stable Diffusion"],
        "t3_aspect": "📐 الأبعاد:",
        "t3_aspect_opts": ["9:16 (Shorts/Reels)", "16:9 (YouTube)", "1:1 (Square)"],
        "t3_light": "💡 الإضاءة:",
        "t3_light_opts": ["سينمائية", "نيون سايبربانك", "ساعة ذهبية"],
        "t3_btn": "🎨 توليد البرومبتات",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة أولاً!",
        "t3_spin": "⚡ جارٍ هندسة البرومبت...",

        "t4_header": "🗣️ محرك تحريك الفيديو والأفاتار",
        "t4_input_label": "📜 النص الإلقائي أو وصف الحركة:",
        "t4_input_placeholder": "اكتب تفاصيل الحركة...",
        "t4_tool": "🤖 أداة التحريك:",
        "t4_tool_opts": ["Runway Gen-3", "Luma Dream Machine", "HeyGen Avatar"],
        "t4_cam": "🎥 حركة الكاميرا:",
        "t4_cam_opts": ["زوم إن بطيء", "بانورامي", "حركة ثابتة"],
        "t4_btn": "⚡ توليد أوامر التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أولاً!",
        "t4_spin": "⚡ جارٍ إعداد سيناريو الحركة...",

        "t5_header": "📊 استوديو التسويق والخطط الاستراتيجية",
        "t5_input_label": "🎯 موضوع المحتوى أو المنتج:",
        "t5_input_placeholder": "اكتب تفاصيل المشروع...",
        "t5_plat": "📱 المنصة:",
        "t5_plat_opts": ["TikTok", "Instagram Reels", "YouTube", "LinkedIn"],
        "t5_goal": "🎯 هدف الحملة:",
        "t5_goal_opts": ["زيادة المبيعات", "وعي بالعلامة التجارية", "تفاعل وزيادة متابعين"],
        "t5_btn": "🚀 تنفيذ الخطة الاستراتيجية",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل المنتج أولاً!",
        "t5_spin": "⚡ جارٍ تحليل السوق...",

        "result_label": "🚀 النتيجة الاحترافية:",
        "copy_btn": "📋 نسخ النص",
        "download_txt": "📥 تحميل ملف نصي",
        "rating_label": "⭐ التقييم:",
        "stats_res": "📊 الإحصائيات:"
    },
    "English": {
        "sidebar_title": "⚡ Control Panel",
        "search_label": "🔍 Search History:",
        "fav_title": "⭐ Favorites",
        "fav_empty": "No favorites yet",
        "history_title": "📜 Archive",
        "history_empty": "Archive is empty",
        "clear_history": "🗑️ Clear Archive",
        "stats_title": "📊 Metrics",
        "stat_total": "Total Tasks:",
        "main_title": "🎙️ Content Studio (Ultimate Pro)",
        "main_caption": "AI Suite with instant copy blocks",
        
        "tabs": [
            "1️⃣ Ideas & Scripts",
            "2️⃣ Music Studio",
            "3️⃣ Image Prompts",
            "4️⃣ Video Motion",
            "5️⃣ Marketing"
        ],
        
        "t1_header": "🎬 Script & Hooks Generator",
        "t1_input_label": "📽️ Video Core Idea:",
        "t1_input_placeholder": "Enter video idea...",
        "t1_dur": "⏱️ Duration:",
        "t1_dur_opts": ["10s", "15s", "30s", "60s", "3m", "5m"],
        "t1_style": "🎨 Style:",
        "t1_style_opts": ["Cinematic", "Documentary", "Comedy", "Educational"],
        "t1_target": "🎯 Target Audience:",
        "t1_target_opts": ["Gen Z", "Entrepreneurs", "General", "Techies"],
        "t1_btn": "🔥 Generate Script",
        "t1_warn": "⚠️ Please enter the video idea first!",
        "t1_spin": "⚡ Generating script...",

        "t2_header": "🎵 Music Production",
        "t2_input_label": "💡 Song Theme:",
        "t2_input_placeholder": "Enter theme...",
        "t2_dialect": "🗣️ Dialect:",
        "t2_dialect_opts": ["Egyptian Slang", "Classical Arabic", "English"],
        "t2_style": "🎼 Genre:",
        "t2_style_opts": ["Mahraganat", "Rap", "Pop", "Acoustic"],
        "t2_vocal": "🎙️ Vocal:",
        "t2_vocal_opts": ["Deep Male", "Warm Female", "Energetic"],
        "t2_btn": "✨ Generate Lyrics",
        "t2_warn": "⚠️ Please enter song theme first!",
        "t2_spin": "⚡ Crafting lyrics...",

        "t3_header": "🎨 Image Prompt Engineer",
        "t3_input_label": "🖼️ Scene Description:",
        "t3_input_placeholder": "Describe scene...",
        "t3_engine": "🎯 Engine:",
        "t3_engine_opts": ["Midjourney v6", "Flux.1", "DALL-E 3"],
        "t3_aspect": "📐 Aspect Ratio:",
        "t3_aspect_opts": ["9:16", "16:9", "1:1"],
        "t3_light": "💡 Lighting:",
        "t3_light_opts": ["Cinematic", "Neon", "Golden Hour"],
        "t3_btn": "🎨 Generate Prompts",
        "t3_warn": "⚠️ Please enter description first!",
        "t3_spin": "⚡ Engineering prompts...",

        "t4_header": "🗣️ Video Motion Prompts",
        "t4_input_label": "📜 Motion Description:",
        "t4_input_placeholder": "Enter text...",
        "t4_tool": "🤖 Tool:",
        "t4_tool_opts": ["Runway Gen-3", "Luma", "HeyGen"],
        "t4_cam": "🎥 Camera:",
        "t4_cam_opts": ["Slow Zoom", "Pan", "Static"],
        "t4_btn": "⚡ Generate Motion",
        "t4_warn": "⚠️ Please enter description first!",
        "t4_spin": "⚡ Preparing motion...",

        "t5_header": "📊 Marketing Strategy",
        "t5_input_label": "🎯 Product/Topic:",
        "t5_input_placeholder": "Enter product details...",
        "t5_plat": "📱 Platform:",
        "t5_plat_opts": ["TikTok", "Instagram", "YouTube", "LinkedIn"],
        "t5_goal": "🎯 Goal:",
        "t5_goal_opts": ["Sales Conversion", "Brand Awareness", "Engagement"],
        "t5_btn": "🚀 Execute Plan",
        "t5_warn": "⚠️ Please enter topic first!",
        "t5_spin": "⚡ Analyzing market...",

        "result_label": "🚀 Result:",
        "copy_btn": "📋 Copy Text",
        "download_txt": "📥 Download TXT",
        "rating_label": "⭐ Rating:",
        "stats_res": "📊 Stats:"
    }
}

# ==========================================
# 3. دالة التنفيذ
# ==========================================
def execute_ai_action(prompt_text, category_name="General", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ GEMINI_API_KEY is missing in Secrets!")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200:
            output_text = res_data['candidates'][0]['content']['parts'][0]['text']
            
            item = {
                "id": len(st.session_state["history"]) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "category": category_name,
                "topic": user_topic if user_topic else "New Request",
                "result": output_text,
                "tab_index": tab_index,
                "rating": 5
            }
            
            st.session_state["history"].insert(0, item)
            save_data(HISTORY_FILE, st.session_state["history"])
            st.session_state["current_result"] = item
            return output_text
        else:
            st.error("❌ Error connecting to Gemini API")
            return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# ==========================================
# 4. القائمة الجانبية
# ==========================================
with st.sidebar:
    lang = st.selectbox("🌐 Language / اللغة:", ["العربية", "English"])
    T = TEXTS[lang]
    
    st.title(T["sidebar_title"])
    st.divider()
    
    st.subheader(T["stats_title"])
    st.metric(label=T["stat_total"], value=len(st.session_state["history"]))
    
    st.divider()
    search_query = st.text_input(T["search_label"])
    
    st.divider()
    st.subheader(T["fav_title"])
    if not st.session_state["favorites"]:
        st.caption(T["fav_empty"])
    else:
        for fav in st.session_state["favorites"]:
            with st.expander(f"⭐ {fav['topic']} ({fav['category']})"):
                st.markdown(fav["result"])
    
    st.divider()
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.subheader(T["history_title"])
    with col_h2:
        if st.button(T["clear_history"]):
            st.session_state["history"] = []
            save_data(HISTORY_FILE, [])
            st.session_state["current_result"] = None
            st.rerun()

    if st.session_state["history"]:
        for item in st.session_state["history"]:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.button(f"📌 {item['topic'][:15]}", key=f"hist_{item['id']}"):
                    st.session_state["current_result"] = item
                    st.session_state["selected_tab"] = item["tab_index"]
                    st.rerun()
            with c2:
                if st.button("⭐", key=f"fav_btn_{item['id']}"):
                    if item not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item)
                        save_data(FAV_FILE, st.session_state["favorites"])
                        st.toast("Saved!")

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
st.title(T["main_title"])
st.caption(T["main_caption"])
st.divider()

selected_tab_name = st.radio(
    "Navigation",
    T["tabs"],
    index=st.session_state["selected_tab"],
    horizontal=True,
    key="nav_radio"
)
st.session_state["selected_tab"] = T["tabs"].index(selected_tab_name)
st.divider()

def render_active_result(tab_idx):
    res = st.session_state["current_result"]
    if res and res["tab_index"] == tab_idx:
        st.success(f"{T['result_label']} {res['topic']}")
        st.markdown(res["result"])
        
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            if st.button(T["copy_btn"], key=f"cp_{res['id']}_{tab_idx}"):
                st.toast("Copied!")
        with c_b2:
            st.download_button(
                label=T["download_txt"],
                data=res["result"],
                file_name=f"content_{res['id']}.txt",
                mime="text/plain",
                key=f"dl_{res['id']}_{tab_idx}"
            )
        with c_b3:
            res["rating"] = st.slider(T["rating_label"], 1, 5, res.get("rating", 5), key=f"rt_{res['id']}")

# التابات الخمسة
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_header']}")
    v_title = st.text_area(T['t1_input_label'], value=st.session_state["t1_val"], key="t1_val", height=100)
    c1, c2, c3 = st.columns(3)
    with c1: v_duration = st.selectbox(T['t1_dur'], T['t1_dur_opts'])
    with c2: v_style = st.selectbox(T['t1_style'], T['t1_style_opts'])
    with c3: v_target = st.selectbox(T['t1_target'], T['t1_target_opts'])
    
    if st.button(T['t1_btn'], type="primary"):
        if not v_title.strip():
            st.warning(T['t1_warn'])
        else:
            with st.spinner(T['t1_spin']):
                prompt = f"Create a professional script for '{v_title}', duration {v_duration}, style {v_style}, target audience {v_target}. Format final outputs inside markdown code blocks (```)."
                execute_ai_action(prompt, category_name="Script", user_topic=v_title[:20], tab_index=0)
                st.rerun()
    render_active_result(0)

elif st.session_state["selected_tab"] == 1:
    st.markdown(f"### {T['t2_header']}")
    song_idea = st.text_area(T['t2_input_label'], value=st.session_state["t2_val"], key="t2_val", height=100)
    c1, c2, c3 = st.columns(3)
    with c1: lyrics_dialect = st.selectbox(T['t2_dialect'], T['t2_dialect_opts'])
    with c2: song_style = st.selectbox(T['t2_style'], T['t2_style_opts'])
    with c3: vocal_type = st.selectbox(T['t2_vocal'], T['t2_vocal_opts'])

    if st.button(T['t2_btn'], type="primary"):
        if not song_idea.strip():
            st.warning(T['t2_warn'])
        else:
            with st.spinner(T['t2_spin']):
                prompt = f"Create song lyrics, dialect: {lyrics_dialect}, style: {song_style}, vocal: {vocal_type}, theme: '{song_idea}'. Place final lyrics inside markdown code blocks (
