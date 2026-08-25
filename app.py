import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم التجاري الفاخر
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

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم الفوري
# ==========================================
HISTORY_FILE = "content_studio_ultimate_v8_history.json"
FAV_FILE = "content_studio_ultimate_v8_favorites.json"

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
    except Exception as e:
        print(f"Error saving data: {e}")

if "history" not in st.session_state:
    st.session_state["history"] = load_data(HISTORY_FILE)

if "favorites" not in st.session_state:
    st.session_state["favorites"] = load_data(FAV_FILE)

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = 0

if "current_result" not in st.session_state:
    st.session_state["current_result"] = None

# تهيئة الحقول الخاصة بكل تابة لمنع فقدان البيانات
default_states = {
    "t1_val": "", "t1_dur": 0, "t1_style": 0, "t1_target": 0,
    "t2_val": "", "t2_dialect": 0, "t2_style": 0, "t2_vocal": 0,
    "t3_val": "", "t3_engine": 0, "t3_aspect": 0, "t3_light": 0,
    "t4_val": "", "t4_tool": 0, "t4_cam": 0,
    "t5_val": "", "t5_plat": 0, "t5_goal": 0
}

for k, val in default_states.items():
    if k not in st.session_state:
        st.session_state[k] = val

# ==========================================
# 2. القاموس الشامل
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚡ لوحة التحكم التجارية",
        "search_label": "🔍 بحث متقدم في السجل:",
        "fav_title": "⭐ العناصر المفضلة",
        "fav_empty": "لا توجد مفضلات مسجلة",
        "history_title": "📜 أرشيف العمليات (حفظ دائم)",
        "history_empty": "الأرشيف فارغ حالياً",
        "clear_history": "🗑️ تفريغ الأرشيف",
        "stats_title": "📊 مؤشرات الأداء",
        "stat_total": "إجمالي المهام المنجزة:",
        "main_title": "🎙️ استوديو المحتوى التجاري (Ultimate Pro Suite v8)",
        "main_caption": "منظومة ذكاء اصطناعي مع إتاحة زرار النسخ السريع لجميع البرومبتات والمخرجات",
        
        "tabs": [
            "1️⃣ 💡 الأفكار والسكريبتات",
            "2️⃣ 🎵 استوديو الأغاني والصوت",
            "3️⃣ 🎨 تصميم الصور والبرومبتات",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار",
            "5️⃣ 📊 استراتيجيات التسويق"
        ],
        
        "t1_header": "🎬 صانع الأفكار والسكريبتات الاحترافية",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو بالتفصيل أو املِها بالمايك...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": [
            "10 ثوانٍ (Ultra Short)", "15 ثانية (Shorts/Reels)", "30 ثانية (Standard Promo)", 
            "60 ثانية (TikTok/Reels Full)", "90 ثانية (Deep Hook)", "3 دقائق (YouTube Standard)", 
            "5 دقائق (Mini Documentary)", "10 دقائق (Full Tutorial)", "15+ دقيقة (Masterclass)", "حلقة بودكاست كاملة (30+ دقيقة)"
        ],
        "t1_style": "🎨 النمط البصري والأسلوب:",
        "t1_style_opts": [
            "سينمائي واقعي (Cinematic)", "وثائقي تشويقي (Documentary)", "كوميدي ساخر (Sarcastic/Comedy)", 
            "تعليمي تفاعلي (Educational)", "حماسي تحفيزي (Motivational)", "غامض ومثير للفضول (Mystery/Suspense)", 
            "قصصي سردي درامي (Storytelling)", "تقني وموضوعي (Tech/Professional)", "مباشر وعفوي (Vlog Style)", "تسويقي مبيعات مباشر (Direct Response Sales)"
        ],
        "t1_target": "🎯 الجمهور المستهدف:",
        "t1_target_opts": [
            "الشباب والمراهقين (Gen Z)", "رواد الأعمال والمهنيين (Entrepreneurs)", "المبرمجون وعشاق التقنية (Techies)", 
            "العامة والمهتمين بالترفيه", "الأطفال والعائلات (Family Friendly)", "المهتمون بالتطوير الذاتي والمالي", 
            "عشاق الألعاب والـ Gaming", "المهتمون بالصحة والرياضة والفتنس", "المستثمرون وأصحاب رأس المال", "صناع المحتوى والمؤثرون"
        ],
        "t1_btn": "🔥 توليد السكريبت والخطافات الاحترافية",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ معالجة وتوليد السكريبت بخيارات متقدمة...",

        "t2_header": "🎵 صناعة الأغاني، الهندسة الصوتية ومكتبة القوافي",
        "t2_input_label": "💡 فكرة الأغنية أو موضوع الكلمات:",
        "t2_input_placeholder": "اكتب موضوع الأغنية والجو العام المطلوب...",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_dialect_opts": [
            "عامية مصرية عصرية", "فصحى بلاغية فصيحة", "خليجي طربي أصيل", "مغربي / شمال إفريقي سريع", 
            "لبناني / شامي ناعم", "عراقي رومانسي حزين", "خليجي بوب حديث", "إنجليزي أمريكي (US Pop)", "إنجليزي بريطاني (UK Rap)", "مزيج عربي إنجليزي (Arabic/English Fusion)"
        ],
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_style_opts": [
            "مهرجانات / شعبي سريع (Mahraganat)", "راب / هيب هوب أندرجراوند (Rap/Hip-Hop)", "بوب عربي رومانسي (Pop)", 
            "أكوستيك هادئ جيتار (Acoustic)", "إي دي إم إلكتروني راقص (EDM/Dance)", "لوفي تشิล هادئ (Lo-Fi Beats)", 
            "تكنو / ترانس حماسي (Techno/Trance)", "روك كلاسيكي قوي (Rock)", "جاز كافيه هادئ (Jazz)", "أوبرا / كلاسيكيات أوركسترالية (Orchestral)"
        ],
        "t2_vocal": "🎙️ أداء صوت المغني:",
        "t2_vocal_opts": [
            "صوت رجالي قوي وعميق (Deep Baritone)", "صوت شبابي حماسي ومرن (Energetic Tenor)", "صوت نسائي ناعم ودافئ (Warm Soprano)", 
            "صوت روبوتي مدمج أوتوتيون (Auto-Tune / Robotic)", "جوقة جماعية حماسية (Choir/Harmonies)", "صوت أطفال نقي وبریء", 
            "أداء راب سريع وحاد (Fast Rap Delivery)", "همس درامي عاطفي (Whisper Vocal)", "صوت إلكتروني مجهول (Voiceless/Vocoder)", "أداء طربي أصيل بعرب صوته قوية"
        ],
        "t2_btn": "✨ توليد الكلمات وتجهيز قالب الأغنية",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات والهندسة الصوتية...",

        "t3_header": "🎨 مهندس برومبتات الصور",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه بدقة:",
        "t3_input_placeholder": "صف تفاصيل الصورة، العناصر، والألوان بدقة...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي:",
        "t3_engine_opts": [
            "Midjourney v6 (أعلى جودة وسينمائية)", "Flux.1 (واقعية مذهلة وتفاصيل دقيقة)", "DALL-E 3 (فهم عميق للنصوص)", 
            "Stable Diffusion XL (تحكم حر كامل)", "Adobe Firefly v3 (تصميم تجاري احترافي)", "Leonardo AI (إضاءات وفنتازيا)", 
            "Ideogram 2.0 (أفضل دمج للنصوص داخل الصور)", "BlueWillow (تنوع وسرعة)", "Kandinsky 3.0 (فنون تشكيلية ورسوم)", "DeepAI Classic (ستايل فني قديم)"
        ],
        "t3_aspect": "📐 الأبعاد والمنصة المستهدفة:",
        "t3_aspect_opts": [
            "9:16 (TikTok / YouTube Shorts / Reels)", "16:9 (YouTube Videos / Desktop)", "1:1 (Instagram / Facebook Post)", 
            "4:5 (Portrait Feed / Carousel)", "21:9 (Ultra-Wide Cinematic Banner)", "3:2 (Photography Standard)", 
            "2:3 (Pinterest Pin)", "4:3 (Classic TV / Presentation)", "5:4 (Art Print)", "مخصص احترافي (Custom Pro Grid)"
        ],
        "t3_light": "💡 نمط الإضاءة:",
        "t3_light_opts": [
            "إضاءة استوديو سينمائية (Cinematic Studio)", "إضاءة نيون سايبربانك (Cyberpunk Neon)", "إضاءة شمس طبيعية ساحرة (Golden Hour)", 
            "مظلم درامي غامض (Dark Moody)", "ألوان زاهية نابضة بالحياة (Vibrant Pop)", "إضاءة ليلية مقمرة (Moonlight Glow)", 
            "إضاءة حجرية متحفية (Museum Spotlight)", "إضاءة ريترو قديمة (Retro Vintage)", "إضاءة بيضاء ناصعة ساطعة (High Key Bright)", "إضاءة فخمة داكنة (Dark Luxury)"
        ],
        "t3_btn": "🎨 توليد الأوامر البرمجية للصور",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة أولاً!",
        "t3_spin": "⚡ جارٍ هندسة البرومبت وتجهيز المقاسات القياسية...",

        "t4_header": "🗣️ محرك تحريك الفيديو والأفاتار",
        "t4_input_label": "📜 النص الإلقائي أو وصف الحركة البصرية:",
        "t4_input_placeholder": "اكتب تفاصيل حركة الكاميرا أو النص الإلقائي...",
        "t4_tool": "🤖 أداة التحريك المستهدفة:",
        "t4_tool_opts": [
            "Runway Gen-3 Alpha (سينمائية واقعية)", "Luma Dream Machine (حركات ديناميكية)", "HeyGen Avatar (أفاتار ناطق احترافي)", 
            "Pika Labs 2.0 (تأثيرات بصرية وموشن)", "Sora OpenAI (واقعية مطلقة)", "Kling AI (حركات فيزيائية معقدة)", 
            "Minimax Video (تحريك سلس وسريع)", "Stable Video Diffusion (SVD)", "AnimateDiff (رسوم متحركة متقدمة)", "D-ID Studio (محادثات وجوه ناطقة)"
        ],
        "t4_cam": "🎥 حركة الكاميرا:",
        "t4_cam_opts": [
            "زوم إن بطيء (Slow Zoom In)", "زوم أوت درامي (Dramatic Zoom Out)", "حركة بانورامية يميناً ويساراً (Pan Right/Left)", 
            "تتبع الحركة الديناميكي (Dynamic Tracking)", "لقطة ثابتة مع تفاصيل حية (Static Ambient)", "دوران 360 درجة حول العنصر (Orbit 360)", 
            "حركة طائرة درونز علوية (Drone FPV Flyover)", "اهتزاز خفيف يدوي (Handheld Cam Shake)", "انتقال سريع فجائي (Fast Whip Pan)", "هبوط تدريجي للأرض (Crane Down)"
        ],
        "t4_btn": "⚡ توليد أوامر التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أو تفاصيل الحركة أولاً!",
        "t4_spin": "⚡ جارٍ إعداد سيناريو الحركة والفيديوهات...",

        "t5_header": "📊 استوديو التسويق والخطط الاستراتيجية",
        "t5_input_label": "🎯 موضوع المحتوى أو المنتج المراد تسويقه:",
        "t5_input_placeholder": "اكتب تفاصيل المشروع أو المنتج المراد وضع خطة له...",
        "t5_plat": "📱 المنصة المستهدفة:",
        "t5_plat_opts": [
            "TikTok (تريندات وفيديوهات قصيرة)", "Instagram Reels & Stories (براند وبصريات)", "YouTube Shorts & Long (تعليمي وترفيهي)", 
            "LinkedIn (تسويق احترافي وبزنس B2B)", "Facebook Community (تفاعل جماهيري واسع)", "X / Twitter (حملات تويتات ونقاشات)", 
            "Snapchat Spotlight (إعلانات جيل صاعد)", "Pinterest Boards (أفكار وتسوق بصري)", "WhatsApp Business (رسائل تسويقية مباشرة)", "Podcast Networks (منصات البودكاست الصوتية)"
        ],
        "t5_goal": "🎯 هدف الحملة:",
        "t5_goal_opts": [
            "زيادة المبيعات والتحويلات (Sales Conversion)", "بناء الوعي بالعلامة التجارية (Brand Awareness)", "زيادة التفاعل والمشاركات (Engagement & Shares)", 
            "جذب زيارات للموقع أو القناة (Traffic Generation)", "جمع ليدز وتسجيلات عملاء (Lead Generation)", "إطلاق منتج جديد في السوق (Product Launch)", 
            "إعادة استهداف العملاء القدامى (Retargeting)", "تحسين السمعة وبناء الثقة (Trust & PR)", "زيادة تحميل التطبيقات (App Installs)", "بناء مجتمع ولاء دائم (Community Loyalty)"
        ],
        "t5_btn": "🚀 تنفيذ الخطة الاستراتيجية",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل المنتج أو المحتوى أولاً!",
        "t5_spin": "⚡ جارٍ تحليل السوق واستخراج الاستراتيجية التسويقية...",

        "result_label": "🚀 النتيجة الاحترافية المنفذة:",
        "copy_btn": "📋 نسخ كامل النص",
        "download_txt": "📥 تحميل كملف نصي (.txt)",
        "rating_label": "⭐ تقييم النتيجة:",
        "stats_res": "📊 إحصائيات الناتج:"
    },
    "English": {
        "sidebar_title": "⚡ Commercial Control Panel",
        "search_label": "🔍 Advanced History Search:",
        "fav_title": "⭐ Saved Favorites",
        "fav_empty": "No favorites saved yet",
        "history_title": "📜 Execution Archive",
        "history_empty": "Archive is currently empty",
        "clear_history": "🗑️ Clear Archive",
        "stats_title": "📊 Performance Metrics",
        "stat_total": "Total Completed Tasks:",
        "main_title": "🎙️ Commercial Content Studio (Ultimate Pro Suite v8)",
        "main_caption": "Expanded AI suite with instant code block copy buttons across all tools",
        
        "tabs": [
            "1️⃣ 💡 Ideas & Scripts",
            "2️⃣ 🎵 Suno Music Studio",
            "3️⃣ 🎨 Pro Image Prompts",
            "4️⃣ 🗣️ Video & Avatar Motion",
            "5️⃣ 📊 Marketing Strategies"
        ],
        
        "t1_header": "🎬 Professional Script & Viral Hooks Generator",
        "t1_input_label": "
