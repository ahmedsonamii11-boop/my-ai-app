import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم التجاري الفاخر
# ==========================================
str_lit.set_page_config(
    page_title="Smart Content Studio - Unified Pipeline Pro v12",
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
        box-shadow: 0 6px 25px rgba(129, 140, 248, 0.6);
    }

    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #f1f5f9 !important;
        padding: 10px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }

    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم الفوري (ترتيب تنازلي)
# ==========================================
HISTORY_FILE = "content_studio_v12_history.json"
FAV_FILE = "content_studio_v12_favorites.json"

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    return []

def save_data(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

if "history" not in str_lit.session_state:
    str_lit.session_state["history"] = load_data(HISTORY_FILE)

if "favorites" not in str_lit.session_state:
    str_lit.session_state["favorites"] = load_data(FAV_FILE)

if "current_result" not in str_lit.session_state:
    str_lit.session_state["current_result"] = None

if "last_lang" not in str_lit.session_state:
    str_lit.session_state["last_lang"] = "العربية"

# تهيئة جميع الحقول لمنع فقدان الحالة بين التبويبات
default_states = {
    "t0_val": "", "t0_goal": 0,
    "t1_val": "", "t1_dur": 0, "t1_style": 0, "t1_target": 0, "t1_extra": [],
    "t2_val": "", "t2_dialect": 0, "t2_style": 0, "t2_vocal": 0, "t2_extra": [],
    "t3_val": "", "t3_engine": 0, "t3_aspect": 0, "t3_light": 0, "t3_extra": [],
    "t4_val": "", "t4_tool": 0, "t4_cam": 0, "t4_extra": [],
    "t5_val": "", "t5_plat": 0, "t5_goal": 0, "t5_budget": 1000, "t5_extra": []
}

for k, val in default_states.items():
    if k not in str_lit.session_state:
        str_lit.session_state[k] = val

# ==========================================
# 2. القاموس الشامل والمرتب (حسب المراحل)
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚡ لوحة التحكم المتكاملة",
        "search_label": "🔍 بحث في الأرشيف:",
        "fav_title": "⭐ العناصر المفضلة",
        "fav_empty": "لا توجد مفضلات مسجلة",
        "history_title": "📜 الأرشيف الدائم (ترتيب تنازلي)",
        "history_empty": "الأرشيف فارغ حالياً",
        "clear_history": "🗑️ تفريغ الأرشيف",
        "stats_title": "📊 مؤشرات الأداء",
        "stat_total": "إجمالي المهام المنجزة:",
        "main_title": "🎙️ استوديو المحتوى والخطط الشامل (Unified Pipeline Pro v12)",
        "main_caption": "منظومة متكاملة لإنتاج المحتوى، الخطط الاستراتيجية، الصور، الفيديوهات والأغاني من مكان واحد",
        
        "tabs": [
            "0️⃣ 🗺️ التخطيط الاستراتيجي",
            "1️⃣ 💡 الأفكار والسكريبتات",
            "2️⃣ 🎵 الأغاني والصوت",
            "3️⃣ 🎨 تصميم الصور والهوية",
            "4️⃣ 🗣️ تحريك الفيديو",
            "5️⃣ 📊 التسويق والإعلانات"
        ],
        
        "extra_features_label": "✨ إضافات الذكاء الاصطناعي المتقدمة:",
        "extra_options": [
            "توليد عناوين فيروسية جذابة (Viral Titles)",
            "استخراج هاشتاغات تريند مخصصة (Smart Hashtags)",
            "تحليل النبرة العاطفية ونسبة النجاح (Sentiment Analysis)",
            "اقتراح أفكار صور مصغرة CTR Thumbnails",
            "ترجمة ملخصة لأهم النقاط للإنجليزية"
        ],

        "t0_header": "🗺️ المرحلة الأولى: التخطيط الاستراتيجي وإدارة المشروع",
        "t0_input_label": "🎯 ما هو مشروعك أو الفكرة العامة للمنتج/المحتوى؟",
        "t0_input_placeholder": "اكتب فكرة المشروع بالتفصيل أو استخدم المايك الصوتي...",
        "t0_goal": "🎯 الهدف الرئيسي من المشروع:",
        "t0_goal_opts": [
            "إطلاق مشروع أو براند جديد (Startup Launch)",
            "حملة تسويقية لمحتوى رقمي (Digital Campaign)",
            "إعداد سلسلة بودكاست أو فيديوهات تعليمية",
            "خطة عمل متكاملة لتطوير المبيعات والجمهور"
        ],
        "t0_btn": "🗺️ بناء الخطة الاستراتيجية الشاملة",
        "t0_warn": "⚠️ يرجى إدخال تفاصيل المشروع أولاً!",
        "t0_spin": "⚡ جارٍ تحليل السوق وصياغة الخطة التنفيذية...",

        "t1_header": "🎬 المرحلة الثانية: صانع الأفكار والسكريبتات الاحترافية",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو بالتفصيل أو استخدم المايك الصوتي...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": [
            "15 ثانية (Shorts/Reels)", "30 ثانية (Standard Promo)", 
            "60 ثانية (TikTok/Reels Full)", "3 دقائق (YouTube Standard)", "10 دقائق (Full Tutorial)"
        ],
        "t1_style": "🎨 النمط البصري والأسلوب:",
        "t1_style_opts": [
            "سينمائي واقعي (Cinematic)", "وثائقي تشويقي (Documentary)", "تعليمي تفاعلي (Educational)", 
            "حماسي تحفيزي (Motivational)", "قصصي سردي درامي (Storytelling)", "تسويقي مبيعات مباشر (Direct Response)"
        ],
        "t1_target": "🎯 الجمهور المستهدف:",
        "t1_target_opts": [
            "الشباب والمراهقين (Gen Z)", "رواد الأعمال والمهنيين (Entrepreneurs)", "المبرمجون وعشاق التقنية", 
            "العامة والمهتمين بالترفيه", "المهتمون بالتطوير الذاتي والمالي"
        ],
        "t1_btn": "🔥 توليد السكريبت والخطافات الفيروسية",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ معالجة وتوليد السكريبت الشامل...",

        "t2_header": "🎵 المرحلة الثالثة: صناعة الأغاني والمؤثرات الصوتية",
        "t2_input_label": "💡 فكرة الأغنية أو الكلمات المطلوبة:",
        "t2_input_placeholder": "اكتب موضوع الأغنية أو استخدم المايك الصوتي...",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_dialect_opts": [
            "عامية مصرية عصرية", "فصحى بلاغية فصيحة", "خليجي طربي أصيل", 
            "لبناني / شامي ناعم", "إنجليزي أمريكي (US Pop)", "مزيج عربي إنجليزي"
        ],
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_style_opts": [
            "مهرجانات / شعبي سريع", "راب / هيب هوب أندرجراوند", "بوب عربي رومانسي", 
            "أكوستيك هادئ جيتار", "إي دي إم إلكتروني راقص", "لوفي تشิล هادئ"
        ],
        "t2_vocal": "🎙️ أداء صوت المغني:",
        "t2_vocal_opts": [
            "صوت رجالي قوي وعميق (Deep Baritone)", "صوت شبابي حماسي ومرن", "صوت نسائي ناعم ودافئ", 
            "صوت روبوتي مدمج أوتوتيون", "أداء راب سريع وحاد"
        ],
        "t2_btn": "✨ توليد الكلمات وتجهيز القالب الصوتي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات والهندسة الصوتية...",

        "t3_header": "🎨 المرحلة الرابعة: مهندس برومبتات الصور والهوية البصرية",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه بدقة:",
        "t3_input_placeholder": "صف تفاصيل الصورة، العناصر، أو استخدم المايك الصوتي...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي:",
        "t3_engine_opts": [
            "Midjourney v6 (سينمائي احترافي)", "Flux.1 (واقعية مذهلة وتفاصيل دقيقة)", 
            "DALL-E 3 (فهم عميق للنصوص)", "Adobe Firefly v3 (تصميم تجاري)"
        ],
        "t3_aspect": "📐 الأبعاد والمنصة المستهدفة:",
        "t3_aspect_opts": [
            "9:16 (TikTok / Shorts / Reels)", "16:9 (YouTube Videos / Desktop)", 
            "1:1 (Instagram / Facebook Post)", "4:5 (Portrait Feed)"
        ],
        "t3_light": "💡 نمط الإضاءة:",
        "t3_light_opts": [
            "إضاءة استوديو سينمائية", "إضاءة نيون سايبربانك", "إضاءة شمس طبيعية (Golden Hour)", "مظلم درامي غامض"
        ],
        "t3_btn": "🎨 توليد الأوامر البرمجية للصورة",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة أولاً!",
        "t3_spin": "⚡ جارٍ هندسة البرومبت وتجهيز المقاسات القياسية...",

        "t4_header": "🗣️ المرحلة الخامسة: محرك تحريك الفيديو والأفاتار",
        "t4_input_label": "📜 النص الإلقائي أو وصف الحركة البصرية:",
        "t4_input_placeholder": "اكتب تفاصيل حركة الكاميرا أو استخدم المايك الصوتي...",
        "t4_tool": "🤖 أداة التحريك المستهدفة:",
        "t4_tool_opts": [
            "Runway Gen-3 Alpha (سينمائية واقعية)", "Luma Dream Machine (حركات ديناميكية)", 
            "HeyGen Avatar (أفاتار ناطق)", "Pika Labs 2.0 (تأثيرات بصرية)"
        ],
        "t4_cam": "🎥 حركة الكاميرا:",
        "t4_cam_opts": [
            "زوم إن بطيء (Slow Zoom In)", "زوم أوت درامي (Dramatic Zoom Out)", 
            "حركة بانورامية يميناً ويساراً", "تتبع الحركة الديناميكي"
        ],
        "t4_btn": "⚡ توليد أوامر التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أو تفاصيل الحركة أولاً!",
        "t4_spin": "⚡ جارٍ إعداد سيناريو الحركة والفيديوهات...",

        "t5_header": "📊 المرحلة السادسة: استوديو التسويق والإعلانات",
        "t5_input_label": "🎯 المنتج أو الخدمة المراد تسويقها:",
        "t5_input_placeholder": "اكتب تفاصيل الحملة أو استخدم المايك الصوتي...",
        "t5_plat": "📱 المنصة المستهدفة:",
        "t5_plat_opts": [
            "TikTok Ads", "Instagram Reels & Stories", "YouTube Campaigns", 
            "LinkedIn B2B", "Facebook Community"
        ],
        "t5_goal": "🎯 هدف الحملة الإعلانية:",
        "t5_goal_opts": [
            "زيادة المبيعات والتحويلات (Sales Conversion)", "بناء الوعي بالعلامة التجارية (Brand Awareness)", 
            "جذب زيارات للموقع (Traffic Generation)", "جمع ليدز وتسجيلات عملاء (Lead Gen)"
        ],
        "t5_budget": "💰 الميزانية التقريبية المقترحة ($):",
        "t5_btn": "🚀 تنفيذ الخطة التسويقية",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل الحملة أولاً!",
        "t5_spin": "⚡ جارٍ تحليل السوق واستخراج الخطة التسويقية...",

        "result_label": "🚀 النتيجة الاحترافية المنفذة:",
        "copy_btn": "📋 نسخ النص للحافظة",
        "download_txt": "📥 تحميل كملف نصي (.txt)",
        "rating_label": "⭐ تقييم النتيجة:"
    },
    "English": {
        "sidebar_title": "⚡ Integrated Control Panel",
        "search_label": "🔍 Search Archive:",
        "fav_title": "⭐ Saved Favorites",
        "fav_empty": "No favorites saved yet",
        "history_title": "📜 Archive (Descending)",
        "history_empty": "Archive is currently empty",
        "clear_history": "🗑️ Clear Archive",
        "stats_title": "📊 Performance Metrics",
        "stat_total": "Total Completed Tasks:",
        "main_title": "🎙️ Unified Content & Strategy Studio (Unified Pipeline Pro v12)",
        "main_caption": "End-to-end AI pipeline for strategy, scripts, images, videos, and audio production",
        
        "tabs": [
            "0️⃣ 🗺️ Strategic Planning",
            "1️⃣ 💡 Ideas & Scripts",
            "2️⃣ 🎵 Music & Audio",
            "3️⃣ 🎨 Pro Images & Brand Kit",
            "4️⃣ 🗣️ Video Motion",
            "5️⃣ 📊 Marketing & Ads"
        ],
        
        "extra_features_label": "✨ Advanced AI Add-ons:",
        "extra_options": [
            "Viral Catchy Titles",
            "Smart Trend Hashtags",
            "Sentiment & Success Analysis",
            "CTR Thumbnail Ideas",
            "English Executive Summary"
        ],

        "t0_header": "🗺️ Phase 1: Strategic Planning & Project Management",
        "t0_input_label": "🎯 What is your project core idea or product theme?",
        "t0_input_placeholder": "Enter project details or use continuous mic...",
        "t0_goal": "🎯 Main Project Goal:",
        "t0_goal_opts": [
            "Startup or Brand Launch",
            "Digital Content Campaign",
            "Podcast Series or Educational Videos",
            "Comprehensive Business Growth Plan"
        ],
        "t0_btn": "🗺️ Build Comprehensive Strategy",
        "t0_warn": "⚠️ Please enter project details first!",
        "t0_spin": "⚡ Analyzing market and formulating strategic plan...",

        "t1_header": "🎬 Phase 2: Professional Script & Viral Hooks Generator",
        "t1_input_label": "📽️ Video Title or Core Idea:",
        "t1_input_placeholder": "Enter video idea or use continuous mic...",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_dur_opts": ["15 Seconds (Shorts/Reels)", "30 Seconds (Standard)", "60 Seconds (Full)", "3 Minutes", "10 Minutes"],
        "t1_style": "🎨 Visual Style & Tone:",
        "t1_style_opts": ["Cinematic Realism", "Documentary", "Educational", "Motivational", "Storytelling", "Direct Response"],
        "t1_target": "🎯 Target Audience:",
        "t1_target_opts": ["Gen Z & Youth", "Entrepreneurs", "Techies", "General Entertainment", "Self-Improvement"],
        "t1_btn": "🔥 Generate Script & Smart Add-ons",
        "t1_warn": "⚠️ Please enter the video idea first!",
        "t1_spin": "⚡ Generating professional script...",

        "t2_header": "🎵 Phase 3: Music Production & Sound Engineering",
        "t2_input_label": "💡 Song Idea or Lyrics Theme:",
        "t2_input_placeholder": "Enter song theme or use continuous mic...",
        "t2_dialect": "🗣️ Cultural Flavor / Dialect:",
        "t2_dialect_opts": ["Modern Egyptian Slang", "Classical Arabic", "Khaleeji Traditional", "US Pop", "Arabic/English Fusion"],
        "t2_style": "🎼 Music Genre:",
        "t2_style_opts": ["Fast Mahraganat", "Underground Rap", "Romantic Pop", "Acoustic Guitar", "EDM / Dance", "Lo-Fi Beats"],
        "t2_vocal": "🎙️ Vocal Performance:",
        "t2_vocal_opts": ["Deep Baritone Male", "Energetic Tenor", "Warm Female Soprano", "Auto-Tune / Robotic", "Fast Rap"],
        "t2_btn": "✨ Generate Song Lyrics & Layout",
        "t2_warn": "⚠️ Please enter the song idea first!",
        "t2_spin": "⚡ Crafting lyrics and audio layout...",

        "t3_header": "🎨 Phase 4: Pro Image Prompt & Brand Identity Engineer",
        "t3_input_label": "🖼️ Describe your scene precisely:",
        "t3_input_placeholder": "Describe details or use continuous mic...",
        "t3_engine": "🎯 AI Image Engine:",
        "t3_engine_opts": ["Midjourney v6", "Flux.1", "DALL-E 3", "Adobe Firefly v3"],
        "t3_aspect": "📐 Aspect Ratio & Resolution:",
        "t3_aspect_opts": ["9:16 (TikTok/Reels)", "16:9 (YouTube)", "1:1 (Square)", "4:5 (Portrait)"],
        "t3_light": "💡 Lighting Style:",
        "t3_light_opts": ["Cinematic Studio", "Cyberpunk Neon", "Golden Hour", "Dark Moody"],
        "t3_btn": "🎨 Generate Pro Image Prompts",
        "t3_warn": "⚠️ Please enter image description first!",
        "t3_spin": "⚡ Engineering visual prompts...",

        "t4_header": "🎬 Phase 5: Video Engine & Avatar Motion Prompts",
        "t4_input_label": "📜 Motion Description or Script:",
        "t4_input_placeholder": "Enter text or use continuous mic...",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_tool_opts": ["Runway Gen-3 Alpha", "Luma Dream Machine", "HeyGen Avatar", "Pika Labs 2.0"],
        "t4_cam": "🎥 Camera Movement:",
        "t4_cam_opts": ["Slow Zoom In", "Dramatic Zoom Out", "Pan Right/Left", "Dynamic Tracking"],
        "t4_btn": "⚡ Generate Motion Prompts",
        "t4_warn": "⚠️ Please enter motion details first!",
        "t4_spin": "⚡ Preparing motion scripts...",

        "t5_header": "📊 Phase 6: Marketing Strategy & Campaign Studio",
        "t5_input_label": "🎯 Product or Service to Market:",
        "t5_input_placeholder": "Enter campaign details or use continuous mic...",
        "t5_plat": "📱 Target Platform:",
        "t5_plat_opts": ["TikTok Ads", "Instagram Reels", "YouTube Campaigns", "LinkedIn B2B"],
        "t5_goal": "🎯 Campaign Goal:",
        "t5_goal_opts": ["Sales Conversion", "Brand Awareness", "Traffic Generation", "Lead Generation"],
        "t5_budget": "💰 Estimated Budget ($):",
        "t5_btn": "🚀 Execute Marketing Strategy",
        "t5_warn": "⚠️ Please enter campaign details first!",
        "t5_spin": "⚡ Analyzing market and building strategy...",

        "result_label": "🚀 Executed Professional Result:",
        "copy_btn": "📋 Copy to Clipboard",
        "download_txt": "📥 Download Text File (.txt)",
        "rating_label": "⭐ Rate Result:"
    }
}

# ==========================================
# 3. دالة استدعاء Gemini API
# ==========================================
def call_gemini(prompt_text, lang_choice):
    if not API_KEY:
        return "❌ الخطأ: مفتاح API الخاص بـ Gemini غير موجود في الأسرار (Secrets)."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    system_instruction = (
        "You are an elite, professional Commercial Content Studio & Strategy AI Expert. "
        "Provide rich, structured, highly professional, and creative outputs based on user parameters. "
        f"The user's preferred language for output is: {lang_choice}."
    )
    
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": system_instruction + "\n\n" + prompt_text}]}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            try:
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return "❌ تعذر استخراج النص من استجابة نموذج الذكاء الاصطناعي."
        else:
            return f"❌ خطأ في الاتصال بالخادم: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ حدث خطأ غير متوقع: {str(e)}"

# ==========================================
# 4. الشريط الجانبي (Sidebar)
# ==========================================
with str_lit.sidebar:
    selected_lang = str_lit.radio("🌐 Language / اللغة:", ["العربية", "English"], horizontal=True, key="lang_radio")
    str_lit.session_state["last_lang"] = selected_lang
    t = TEXTS[selected_lang]
    
    str_lit.markdown(f"### {t['sidebar_title']}")
    str_lit.markdown("---")
    
    str_lit.markdown(f"#### {t['stats_title']}")
    total_tasks = len(str_lit.session_state["history"])
    str_lit.metric(label=t["stat_total"], value=total_tasks)
    str_lit.markdown("---")
    
    search_query = str_lit.text_input(t["search_label"], "")
    
    str_lit.markdown("---")
    str_lit.markdown(f"#### {t['fav_title']}")
    if not str_lit.session_state["favorites"]:
        str_lit.info(t["fav_empty"])
    else:
        for idx, fav in enumerate(str_lit.session_state["favorites"][:5]):
            with str_lit.expander(f"⭐ {fav.get('title', 'Element')} ({fav.get('time', '')})"):
                str_lit.write(fav.get("content", ""))
                if str_lit.button(f"🗑️ حذف_{idx}", key=f"del_fav_{idx}"):
                    str_lit.session_state["favorites"].pop(idx)
                    save_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.rerun()

    str_lit.markdown("---")
    str_lit.markdown(f"#### {t['history_title']}")
    if str_lit.button(t["clear_history"]):
        str_lit.session_state["history"] = []
        save_data(HISTORY_FILE, [])
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
                if str_lit.button(f"⭐ إضافة للمفضلة_{i}", key=f"fav_add_{i}"):
                    str_lit.session_state["favorites"].append({
                        "title": item.get('input', 'Item')[:30],
                        "content": item.get("result", ""),
                        "time": item.get("time", "")
                    })
                    save_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.success("تمت الإضافة للمفضلة!")

# ==========================================
# 5. الواجهة الرئيسية والتبويبات المرتبة بالخطوات
# ==========================================
t = TEXTS[selected_lang]

str_lit.title(t["main_title"])
str_lit.caption(t["main_caption"])
str_lit.markdown("---")

tabs = str_lit.tabs(t["tabs"])

def log_and_save_execution(tab_name, input_val, result_text):
    record = {
        "tab": tab_name,
        "input": input_val,
        "result": result_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    str_lit.session_state["history"].append(record)
    save_data(HISTORY_FILE, str_lit.session_state["history"])
    str_lit.session_state["current_result"] = result_text

# ------------------------------------------
# تبويب 0: التخطيط الاستراتيجي (المرحلة الأولى)
# ------------------------------------------
with tabs[0]:
    str_lit.subheader(t["t0_header"])
    
    str_lit.session_state["t0_val"] = str_lit.text_area(
        t["t0_input_label"],
        value=str_lit.session_state["t0_val"],
        placeholder=t["t0_input_placeholder"],
        key="t0_input_widget"
    )
    str_lit.session_state["t0_val"] = str_lit.session_state["t0_input_widget"]
    
    goal_choice_0 = str_lit.selectbox(t["t0_goal"], t["t0_goal_opts"], key="t0_goal_widget")
    
    if str_lit.button(t["t0_btn"], key="t0_execute"):
        if not str_lit.session_state["t0_val"].strip():
            str_lit.warning(t["t0_warn"])
        else:
            with str_lit.spinner(t["t0_spin"]):
                full_prompt = (
                    f"Create a comprehensive professional strategic plan and project roadmap for: '{str_lit.session_state['t0_val']}'.\n"
                    f"Main Goal: {goal_choice_0}\n"
                    "Include target audience analysis, timeline phases, resource allocation, and key performance indicators (KPIs)."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Strategic Planning", str_lit.session_state["t0_val"], res)
                str_lit.success("تم إنشاء الخطة الاستراتيجية بنجاح!")

# ------------------------------------------
# تبويب 1: الأفكار والسكريبتات (المرحلة الثانية)
# ------------------------------------------
with tabs[1]:
    str_lit.subheader(t["t1_header"])
    
    str_lit.session_state["t1_val"] = str_lit.text_area(
        t["t1_input_label"],
        value=str_lit.session_state["t1_val"],
        placeholder=t["t1_input_placeholder"],
        key="t1_input_widget"
    )
    str_lit.session_state["t1_val"] = str_lit.session_state["t1_input_widget"]
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        dur_choice = str_lit.selectbox(t["t1_dur"], t["t1_dur_opts"], key="t1_dur_widget")
    with col2:
        style_choice = str_lit.selectbox(t["t1_style"], t["t1_style_opts"], key="t1_style_widget")
    with col3:
        target_choice = str_lit.selectbox(t["t1_target"], t["t1_target_opts"], key="t1_target_widget")
        
    extra_feats = str_lit.multiselect(t["extra_features_label"], t["extra_options"], key="t1_extra_widget")
    
    if str_lit.button(t["t1_btn"], key="t1_execute"):
        if not str_lit.session_state["t1_val"].strip():
            str_lit.warning(t["t1_warn"])
        else:
            with str_lit.spinner(t["t1_spin"]):
                full_prompt = (
                    f"Create a professional video script and content layout for the idea: '{str_lit.session_state['t1_val']}'.\n"
                    f"Duration: {dur_choice}\nVisual Style: {style_choice}\nTarget Audience: {target_choice}\n"
                    f"Include these advanced AI add-ons: {', '.join(extra_feats) if extra_feats else 'None'}."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Ideas & Scripts", str_lit.session_state["t1_val"], res)
                str_lit.success("تم التوليد بنجاح!")

# ------------------------------------------
# تبويب 2: الأغاني والصوت (المرحلة الثالثة)
# ------------------------------------------
with tabs[2]:
    str_lit.subheader(t["t2_header"])
    
    str_lit.session_state["t2_val"] = str_lit.text_area(
        t["t2_input_label"],
        value=str_lit.session_state["t2_val"],
        placeholder=t["t2_input_placeholder"],
        key="t2_input_widget"
    )
    str_lit.session_state["t2_val"] = str_lit.session_state["t2_input_widget"]
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        dialect_choice = str_lit.selectbox(t["t2_dialect"], t["t2_dialect_opts"], key="t2_dialect_widget")
    with col2:
        genre_choice = str_lit.selectbox(t["t2_style"], t["t2_style_opts"], key="t2_style_widget")
    with col3:
        vocal_choice = str_lit.selectbox(t["t2_vocal"], t["t2_vocal_opts"], key="t2_vocal_widget")
        
    extra_feats_2 = str_lit.multiselect(t["extra_features_label"], t["extra_options"], key="t2_extra_widget")
    
    if str_lit.button(t["t2_btn"], key="t2_execute"):
        if not str_lit.session_state["t2_val"].strip():
            str_lit.warning(t["t2_warn"])
        else:
            with str_lit.spinner(t["t2_spin"]):
                full_prompt = (
                    f"Create comprehensive song lyrics and musical prompts for: '{str_lit.session_state['t2_val']}'.\n"
                    f"Cultural Flavor: {dialect_choice}\nMusic Genre: {genre_choice}\nVocal Performance: {vocal_choice}\n"
                    f"Extra elements: {', '.join(extra_feats_2) if extra_feats_2 else 'None'}."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Music & Audio", str_lit.session_state["t2_val"], res)
                str_lit.success("تم التوليد بنجاح!")

# ------------------------------------------
# تبويب 3: تصميم الصور والهوية (المرحلة الرابعة)
# ------------------------------------------
with tabs[3]:
    str_lit.subheader(t["t3_header"])
    
    str_lit.session_state["t3_val"] = str_lit.text_area(
        t["t3_input_label"],
        value=str_lit.session_state["t3_val"],
        placeholder=t["t3_input_placeholder"],
        key="t3_input_widget"
    )
    str_lit.session_state["t3_val"] = str_lit.session_state["t3_input_widget"]
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        engine_choice = str_lit.selectbox(t["t3_engine"], t["t3_engine_opts"], key="t3_engine_widget")
    with col2:
        aspect_choice = str_lit.selectbox(t["t3_aspect"], t["t3_aspect_opts"], key="t3_aspect_widget")
    with col3:
        light_choice = str_lit.selectbox(t["t3_light"], t["t3_light_opts"], key="t3_light_widget")
        
    extra_feats_3 = str_lit.multiselect(t["extra_features_label"], t["extra_options"], key="t3_extra_widget")
    
    if str_lit.button(t["t3_btn"], key="t3_execute"):
        if not str_lit.session_state["t3_val"].strip():
            str_lit.warning(t["t3_warn"])
        else:
            with str_lit.spinner(t["t3_spin"]):
                full_prompt = (
                    f"Engineer expert AI image generation prompts for: '{str_lit.session_state['t3_val']}'.\n"
                    f"Target Engine: {engine_choice}\nAspect Ratio: {aspect_choice}\nLighting: {light_choice}\n"
                    f"Extra options: {', '.join(extra_feats_3) if extra_feats_3 else 'None'}."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Image Prompts", str_lit.session_state["t3_val"], res)
                str_lit.success("تم التوليد بنجاح!")

# ------------------------------------------
# تبويب 4: تحريك الفيديو (المرحلة الخامسة)
# ------------------------------------------
with tabs[4]:
    str_lit.subheader(t["t4_header"])
    
    str_lit.session_state["t4_val"] = str_lit.text_area(
        t["t4_input_label"],
        value=str_lit.session_state["t4_val"],
        placeholder=t["t4_input_placeholder"],
        key="t4_input_widget"
    )
    str_lit.session_state["t4_val"] = str_lit.session_state["t4_input_widget"]
    
    col1, col2 = str_lit.columns(2)
    with col1:
        tool_choice = str_lit.selectbox(t["t4_tool"], t["t4_tool_opts"], key="t4_tool_widget")
    with col2:
        cam_choice = str_lit.selectbox(t["t4_cam"], t["t4_cam_opts"], key="t4_cam_widget")
        
    extra_feats_4 = str_lit.multiselect(t["extra_features_label"], t["extra_options"], key="t4_extra_widget")
    
    if str_lit.button(t["t4_btn"], key="t4_execute"):
        if not str_lit.session_state["t4_val"].strip():
            str_lit.warning(t["t4_warn"])
        else:
            with str_lit.spinner(t["t4_spin"]):
                full_prompt = (
                    f"Create professional video motion prompts and AI avatar direction for: '{str_lit.session_state['t4_val']}'.\n"
                    f"Target Tool: {tool_choice}\nCamera Movement: {cam_choice}\n"
                    f"Extra options: {', '.join(extra_feats_4) if extra_feats_4 else 'None'}."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Video Motion", str_lit.session_state["t4_val"], res)
                str_lit.success("تم التوليد بنجاح!")

# ------------------------------------------
# تبويب 5: التسويق والإعلانات (المرحلة السادسة)
# ------------------------------------------
with tabs[5]:
    str_lit.subheader(t["t5_header"])
    
    str_lit.session_state["t5_val"] = str_lit.text_area(
        t["t5_input_label"],
        value=str_lit.session_state["t5_val"],
        placeholder=t["t5_input_placeholder"],
        key="t5_input_widget"
    )
    str_lit.session_state["t5_val"] = str_lit.session_state["t5_input_widget"]
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        plat_choice = str_lit.selectbox(t["t5_plat"], t["t5_plat_opts"], key="t5_plat_widget")
    with col2:
        goal_choice = str_lit.selectbox(t["t5_goal"], t["t5_goal_opts"], key="t5_goal_widget")
    with col3:
        budget_val = str_lit.number_input(t["t5_budget"], min_value=50, max_value=100000, value=1000, step=50, key="t5_budget_widget")
        
    extra_feats_5 = str_lit.multiselect(t["extra_features_label"], t["extra_options"], key="t5_extra_widget")
    
    if str_lit.button(t["t5_btn"], key="t5_execute"):
        if not str_lit.session_state["t5_val"].strip():
            str_lit.warning(t["t5_warn"])
        else:
            with str_lit.spinner(t["t5_spin"]):
                full_prompt = (
                    f"Design a comprehensive digital marketing strategy and ad campaign plan for: '{str_lit.session_state['t5_val']}'.\n"
                    f"Platform: {plat_choice}\nGoal: {goal_choice}\nBudget: ${budget_val}\n"
                    f"Extra options: {', '.join(extra_feats_5) if extra_feats_5 else 'None'}."
                )
                res = call_gemini(full_prompt, selected_lang)
                log_and_save_execution("Marketing Strategy", str_lit.session_state["t5_val"], res)
                str_lit.success("تم التوليد بنجاح!")

# ==========================================
# 6. قسم عرض النتائج الموحد والتصدير
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
            file_name=f"Unified_Studio_Result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with col_b:
        str_lit.slider(t["rating_label"], 1, 5, 5, key="result_rating")
else:
    str_lit.info("قم بتنفيذ أي خطوة من التبويبات بالأعلى لعرض النتيجة التفاعلية هنا مباشرة.")
