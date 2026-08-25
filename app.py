import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم التجاري الفاخر (مع دعم الموبايل والـ PC)
# ==========================================
str_lit.set_page_config(
    page_title="Smart Content Studio - Ultimate Pro Suite v11",
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
        padding-left: 2rem;
        padding-right: 2rem;
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
        width: 100%;
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

    /* ميديا كويري لتحسين التنسيق على الموبايل والشاشات الصغيرة */
    @media (max-width: 768px) {
        div.block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.3rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
        .stButton>button {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم الفوري
# ==========================================
HISTORY_FILE = "content_studio_ultimate_v11_history.json"
FAV_FILE = "content_studio_ultimate_v11_favorites.json"

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

if "history" not in str_lit.session_state:
    str_lit.session_state["history"] = load_data(HISTORY_FILE)

if "favorites" not in str_lit.session_state:
    str_lit.session_state["favorites"] = load_data(FAV_FILE)

if "current_result" not in str_lit.session_state:
    str_lit.session_state["current_result"] = None

if "last_lang" not in str_lit.session_state:
    str_lit.session_state["last_lang"] = "العربية"

default_states = {
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
# 2. القاموس الشامل (عربي / إنجليزي)
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
        "main_title": "🎙️ استوديو المحتوى التجاري المدمج",
        "main_caption": "منظومة ذكاء اصطناعي متوافقة مع الموبايل والـ PC مع دعم التبديل التام للغة",
        
        "tabs": [
            "1️⃣ 💡 الأفكار والسكريبتات",
            "2️⃣ 🎵 الأغاني والصوت",
            "3️⃣ 🎨 تصميم الصور",
            "4️⃣ 🗣️ تحريك الفيديو",
            "5️⃣ 📊 التسويق"
        ],
        
        "extra_features_label": "✨ إضافات الذكاء الاصطناعي المتقدمة:",
        "extra_options": [
            "توليد عناوين فيروسية جذابة (Viral Titles)",
            "استخراج هاشتاغات تريند مخصصة (Smart Hashtags)",
            "تحليل النبرة العاطفية ونسبة النجاح (Sentiment & Success Analysis)",
            "اقتراح أفكار صور مصغرة CTR Thumbnails",
            "ترجمة ملخصة لأهم النقاط للإنجليزية",
            "إعادة صياغة ذكية لتويتر/لينكد إن"
        ],

        "t1_header": "🎬 صانع الأفكار والسكريبتات الاحترافية",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو بالتفصيل أو استخدم المايك...",
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
        "t1_btn": "🔥 توليد السكريبت والإضافات الذكية",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ معالجة وتوليد السكريبت الشامل...",

        "t2_header": "🎵 صناعة الأغاني والهندسة الصوتية",
        "t2_input_label": "💡 فكرة الأغنية أو موضوع الكلمات:",
        "t2_input_placeholder": "اكتب موضوع الأغنية أو استخدم المايك...",
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
        "t2_btn": "✨ توليد الكلمات وتجهيز القالب الصوتي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات والهندسة الصوتية...",

        "t3_header": "🎨 مهندس برومبتات الصور",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه بدقة:",
        "t3_input_placeholder": "صف تفاصيل الصورة أو استخدم المايك...",
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
        "t3_btn": "🎨 توليد الأوامر البرمجية للصورة",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة أولاً!",
        "t3_spin": "⚡ جارٍ هندسة البرومبت وتجهيز المقاسات...",

        "t4_header": "🗣️ محرك تحريك الفيديو والأفاتار",
        "t4_input_label": "📜 النص الإلقائي أو وصف الحركة البصرية:",
        "t4_input_placeholder": "اكتب تفاصيل حركة الكاميرا أو استخدم المايك...",
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
        "t4_spin": "⚡ جارٍ إعداد سيناريو الحركة...",

        "t5_header": "📊 استوديو التسويق والخطط الاستراتيجية",
        "t5_input_label": "🎯 موضوع المحتوى أو المنتج المراد تسويقه:",
        "t5_input_placeholder": "اكتب تفاصيل المشروع أو استخدم المايك...",
        "t5_plat": "📱 المنصة المستهدفة:",
        "t5_plat_opts": [
            "TikTok (تريندات وفيديوهات قصيرة)", "Instagram Reels & Stories (براند وبصريات)", "YouTube Shorts & Long (تعليمي وترفيهي)", 
            "LinkedIn (تسويق احترافي وبزنس B2B)", "Facebook Community (تفاعل جماهيري واسع)", "X / Twitter (حملات تويتات ونقاشات)", 
            "Snapchat Spotlight (إعلانات جيل صاعد)", "Pinterest Boards (أفكار وتسوق بصري)", "WhatsApp Business (رسائل تسويقية مباشرة)", "Podcast Networks (منصات البودكاست)"
        ],
        "t5_goal": "🎯 هدف الحملة:",
        "t5_goal_opts": [
            "زيادة المبيعات والتحويلات (Sales Conversion)", "بناء الوعي بالعلامة التجارية (Brand Awareness)", "زيادة التفاعل والمشاركات (Engagement & Shares)", 
            "جذب زيارات للموقع أو القناة (Traffic Generation)", "جمع ليدز وتسجيلات عملاء (Lead Generation)", "إطلاق منتج جديد في السوق (Product Launch)", 
            "إعادة استهداف العملاء القدامى (Retargeting)", "تحسين السمعة وبناء الثقة (Trust & PR)", "زيادة تحميل التطبيقات (App Installs)", "بناء مجتمع ولاء دائم (Community Loyalty)"
        ],
        "t5_budget": "💰 الميزانية التقريبية المقترحة ($):",
        "t5_btn": "🚀 تنفيذ الخطة الاستراتيجية والإعلانية",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل المنتج أو المحتوى أولاً!",
        "t5_spin": "⚡ جارٍ تحليل السوق واستخراج الخطة...",

        "result_label": "🚀 النتيجة الاحترافية المنفذة:",
        "copy_btn": "📋 نسخ النص للحافظة",
        "download_txt": "📥 تحميل كملف نصي (.txt)"
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
        "main_title": "🎙️ Integrated Commercial Content Studio",
        "main_caption": "Mobile & PC responsive AI suite with dynamic language switching",
        
        "tabs": [
            "1️⃣ 💡 Ideas & Scripts",
            "2️⃣ 🎵 Music Studio",
            "3️⃣ 🎨 Pro Image Prompts",
            "4️⃣ 🗣️ Video & Avatar Motion",
            "5️⃣ 📊 Marketing Strategies"
        ],
        
        "extra_features_label": "✨ Advanced AI Add-ons:",
        "extra_options": [
            "Viral Catchy Titles",
            "Smart Trend Hashtags",
            "Sentiment & Success Analysis",
            "CTR Thumbnail Ideas",
            "English Executive Summary",
            "LinkedIn / Twitter Repurposing"
        ],

        "t1_header": "🎬 Professional Script & Viral Hooks Generator",
        "t1_input_label": "📽️ Video Title or Core Idea:",
        "t1_input_placeholder": "Enter video idea or use mic...",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_dur_opts": [
            "10 Seconds (Ultra Short)", "15 Seconds (Shorts/Reels)", "30 Seconds (Standard Promo)", 
            "60 Seconds (TikTok/Reels Full)", "90 Seconds (Deep Hook)", "3 Minutes (YouTube Standard)", 
            "5 Minutes (Mini Documentary)", "10 Minutes (Full Tutorial)", "15+ Minutes (Masterclass)", "Full Podcast Episode (30+ Min)"
        ],
        "t1_style": "🎨 Visual Style & Tone:",
        "t1_style_opts": [
            "Cinematic Realism", "Documentary & Suspense", "Sarcastic / Comedy", "Educational & Interactive", 
            "Motivational & High-Energy", "Mystery & Curiosity", "Storytelling & Drama", "Tech & Professional", "Vlog Style", "Direct Response Sales"
        ],
        "t1_target": "🎯 Target Audience:",
        "t1_target_opts": [
            "Gen Z & Youth", "Entrepreneurs & Professionals", "Techies & Coders", "General Entertainment", 
            "Family & Kids Friendly", "Self-Improvement & Finance Seekers", "Gamers & Esports", "Health & Fitness Enthusiasts", "Investors & Capital Owners", "Content Creators & Influencers"
        ],
        "t1_btn": "🔥 Generate Script & Smart Add-ons",
        "t1_warn": "⚠️ Please enter the video idea first!",
        "t1_spin": "⚡ Generating professional script...",

        "t2_header": "🎵 Music Production & Sound Engineering",
        "t2_input_label": "💡 Song Idea or Theme:",
        "t2_input_placeholder": "Enter song theme or use mic...",
        "t2_dialect": "🗣️ Dialect / Cultural Flavor:",
        "t2_dialect_opts": [
            "Modern Egyptian Slang", "Classical Arabic (Fusha)", "Khaleeji Traditional", "North African / Fast Moroccan", 
            "Lebanese / Levantine Smooth", "Iraqi Sad Romantic", "Modern Khaleeji Pop", "US Pop English", "UK Rap English", "Arabic/English Fusion"
        ],
        "t2_style": "🎼 Music Genre:",
        "t2_style_opts": [
            "Fast Mahraganat / Street", "Underground Rap / Hip-Hop", "Romantic Arabic Pop", "Acoustic Guitar", 
            "EDM / Dance", "Lo-Fi Beats", "Techno / Trance", "Classic Rock", "Cafe Jazz", "Orchestral Opera"
        ],
        "t2_vocal": "🎙️ Vocal Performance:",
        "t2_vocal_opts": [
            "Deep Baritone Male", "Energetic Tenor", "Warm Female Soprano", "Auto-Tune / Robotic", 
            "Group Choir / Harmonies", "Pure Kids Vocals", "Fast Sharp Rap Delivery", "Emotional Whisper", "Vocoder / Electronic Voice", "Traditional Tarab Vocal"
        ],
        "t2_btn": "✨ Generate Full Song & Sound Layout",
        "t2_warn": "⚠️ Please enter the song idea first!",
        "t2_spin": "⚡ Crafting lyrics...",

        "t3_header": "🎨 Pro Image Prompt Engineer",
        "t3_input_label": "🖼️ Describe your scene precisely:",
        "t3_input_placeholder": "Describe details or use mic...",
        "t3_engine": "🎯 AI Image Engine:",
        "t3_engine_opts": [
            "Midjourney v6 (Highest Cinematic Quality)", "Flux.1 (Stunning Realism & Details)", "DALL-E 3 (Deep Prompt Understanding)", 
            "Stable Diffusion XL (Full Control)", "Adobe Firefly v3 (Commercial Pro)", "Leonardo AI (Lighting & Fantasy)", 
            "Ideogram 2.0 (Best Text Integration)", "BlueWillow (Variety & Speed)", "Kandinsky 3.0 (Artistic & Painting)", "DeepAI Classic"
        ],
        "t3_aspect": "📐 Platform Resolution & Aspect Ratio:",
        "t3_aspect_opts": [
            "9:16 (TikTok / YouTube Shorts / Reels)", "16:9 (YouTube Videos / Desktop)", "1:1 (Instagram / Facebook Post)", 
            "4:5 (Portrait Feed / Carousel)", "21:9 (Ultra-Wide Cinematic Banner)", "3:2 (Photography Standard)", 
            "2:3 (Pinterest Pin)", "4:3 (Classic TV / Presentation)", "5:4 (Art Print)", "Custom Pro Grid"
        ],
        "t3_light": "💡 Lighting Style:",
        "t3_light_opts": [
            "Cinematic Studio Lighting", "Cyberpunk Neon Glow", "Golden Hour Natural Sunlight", "Dark Moody Atmosphere", 
            "Vibrant & Pop Art", "Moonlight Glow", "Museum Spotlight", "Retro Vintage", "High Key Bright", "Dark Luxury"
        ],
        "t3_btn": "🎨 Generate Pro Image Prompts",
        "t3_warn": "⚠️ Please enter image description first!",
        "t3_spin": "⚡ Engineering visual prompts...",

        "t4_header": "🗣️ Video Engine, Avatar & Motion Prompts",
        "t4_input_label": "📜 Voiceover Text or Motion Description:",
        "t4_input_placeholder": "Enter text or use mic...",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_tool_opts": [
            "Runway Gen-3 Alpha (Realistic Cinematic)", "Luma Dream Machine (Dynamic Motion)", "HeyGen Avatar (Professional Speaker)", 
            "Pika Labs 2.0 (VFX & Motion Graphics)", "Sora OpenAI (Absolute Realism)", "Kling AI (Complex Physics)", 
            "Minimax Video (Smooth & Fast)", "Stable Video Diffusion (SVD)", "AnimateDiff (Advanced Animation)", "D-ID Studio (Talking Faces)"
        ],
        "t4_cam": "🎥 Camera Movement:",
        "t4_cam_opts": [
            "Slow Zoom In", "Dramatic Zoom Out", "Pan Right/Left", "Dynamic Tracking Shot", 
            "Static with Ambient Motion", "Orbit 360 Degree", "Drone FPV Flyover", "Handheld Cam Shake", "Fast Whip Pan", "Crane Down"
        ],
        "t4_btn": "⚡ Generate Motion Prompts",
        "t4_warn": "⚠️ Please enter text or motion description first!",
        "t4_spin": "⚡ Preparing motion commands...",

        "t5_header": "📊 Marketing Studio & Strategic Planning",
        "t5_input_label": "🎯 Content Topic or Product to Market:",
        "t5_input_placeholder": "Enter product details or use mic...",
        "t5_plat": "📱 Target Publishing Platform:",
        "t5_plat_opts": [
            "TikTok (Trends & Short Videos)", "Instagram Reels & Stories (Brand Building)", "YouTube Shorts & Long (Educational & Ent.)", 
            "LinkedIn (Professional B2B)", "Facebook Community (Mass Audience)", "X / Twitter (Discussions & Threads)", 
            "Snapchat Spotlight", "Pinterest Boards (Visual Commerce)", "WhatsApp Business (Direct Messaging)", "Podcast Networks"
        ],
        "t5_goal": "🎯 Campaign Goal:",
        "t5_goal_opts": [
            "Sales Conversion", "Brand Awareness", "Engagement & Shares", "Traffic Generation", 
            "Lead Generation", "Product Launch", "Retargeting", "Trust & PR Improvement", "App Installs", "Community Loyalty"
        ],
        "t5_budget": "💰 Estimated Ad Budget ($):",
        "t5_btn": "🚀 Execute Strategic Plan",
        "t5_warn": "⚠️ Please enter content topic first!",
        "t5_spin": "⚡ Analyzing market strategy...",

        "result_label": "🚀 Professional Execution Result:",
        "copy_btn": "📋 Copy to Clipboard",
        "download_txt": "📥 Download as Text (.txt)"
    }
}

# ==========================================
# 3. دالة الترجمة الفورية للنتائج
# ==========================================
def translate_text(text, target_language):
    if not API_KEY or not text:
        return text
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    target_lang_name = "Arabic" if target_language == "العربية" else "English"
    payload = {"contents": [{"parts": [{"text": f"Translate the following professional content accurately into {target_lang_name}. Keep all markdown formatting intact:\n\n{text}"}]}]}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except:
        pass
    return text

# ==========================================
# 4. دالة الإدخال الصوتي المتطورة المتوافقة مع الموبايل
# ==========================================
def floating_voice_textarea(label, session_key, placeholder):
    val = str_lit.text_area(label, value=str_lit.session_state.get(session_key, ""), key=session_key, height=120, placeholder=placeholder)
    
    js_code = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const textAreas = doc.querySelectorAll('textarea');
        
        textAreas.forEach((ta) => {{
            if (ta.getAttribute('aria-label') === '{label}' || ta.placeholder === '{placeholder}') {{
                const wrapper = ta.closest('.stTextArea') || ta.parentElement;
                
                if (wrapper && !wrapper.querySelector('.floating-mic-container_{session_key}')) {{
                    const micDiv = doc.createElement('div');
                    micDiv.className = 'floating-mic-container_{session_key}';
                    micDiv.style.cssText = "position: absolute; bottom: 10px; right: 10px; display: flex; align-items: center; gap: 6px; z-index: 999;";
                    
                    micDiv.innerHTML = `
                        <div id="waves_{session_key}" style="display: none; align-items: center; gap: 2px; height: 14px; background: rgba(0,0,0,0.8); padding: 2px 6px; border-radius: 10px;">
                            <div style="width: 2px; background: #6366f1; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out;"></div>
                            <div style="width: 2px; background: #6366f1; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.15s;"></div>
                            <div style="width: 2px; background: #6366f1; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.3s;"></div>
                        </div>
                        <button type="button" id="mic_btn_{session_key}" title="Mic" style="background: #1e293b; border: 1px solid #6366f1; color: #818cf8; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                            🎙️
                        </button>
                        <button type="button" id="stop_btn_{session_key}" title="Stop" style="background: #1e293b; border: 1px solid #f85149; color: #f85149; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; display: none; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                            ⏹️
                        </button>
                    `;
                    
                    if (!doc.getElementById('wave-style-global')) {{
                        const style = doc.createElement('style');
                        style.id = 'wave-style-global';
                        style.innerHTML = '@keyframes waveA {{ 0%, 100% {{ height: 4px; }} 50% {{ height: 14px; }} }}';
                        doc.head.appendChild(style);
                    }}

                    wrapper.style.position = 'relative';
                    wrapper.appendChild(micDiv);

                    let recognition = null;
                    let isRec = false;
                    const btn = micDiv.querySelector('#mic_btn_{session_key}');
                    const stopBtn = micDiv.querySelector('#stop_btn_{session_key}');
                    const waves = micDiv.querySelector('#waves_{session_key}');

                    function startRecording() {{
                        const SpeechRecognition = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
                        if (!SpeechRecognition) {{
                            alert("Speech recognition is not supported in this browser.");
                            return;
                        }}

                        recognition = new SpeechRecognition();
                        recognition.lang = 'ar-EG';
                        recognition.interimResults = true;
                        recognition.continuous = true;

                        recognition.onstart = function() {{
                            isRec = true;
                            btn.style.background = '#f85149';
                            btn.style.color = '#fff';
                            stopBtn.style.display = 'flex';
                            waves.style.display = 'flex';
                        }};

                        let finalTranscript = ta.value ? ta.value + ' ' : '';

                        recognition.onresult = function(e) {{
                            let interim = '';
                            for (let i = e.resultIndex; i < e.results.length; ++i) {{
                                if (e.results[i].isFinal) {{
                                    finalTranscript += e.results[i][0].transcript + ' ';
                                }} else {{
                                    interim += e.results[i][0].transcript;
                                }}
                            }}
                            const fullText = finalTranscript + interim;
                            const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, "value").set;
                            setter.call(ta, fullText);
                            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }};

                        recognition.onerror = function() {{ stopRecordingProcess(); }};
                        recognition.onend = function() {{
                            if (isRec) {{
                                try {{ recognition.start(); }} catch(err) {{}}
                            }}
                        }};

                        try {{ recognition.start(); }} catch(err) {{}}
                    }}

                    function stopRecordingProcess() {{
                        isRec = false;
                        if (recognition) {{
                            try {{ recognition.stop(); }} catch(e) {{}}
                        }}
                        btn.style.background = '#1e293b';
                        btn.style.color = '#818cf8';
                        stopBtn.style.display = 'none';
                        waves.style.display = 'none';
                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}

                    btn.onclick = function() {{
                        if (!isRec) {{ startRecording(); }} else {{ stopRecordingProcess(); }}
                    }};
                    stopBtn.onclick = function() {{ stopRecordingProcess(); }};
                }}
            }}
        }});
    }})();
    </script>
    """
    str_lit.components.v1.html(js_code, height=0, width=0)
    return str_lit.session_state.get(session_key, "")

# ==========================================
# 5. دالة التنفيذ والتخزين
# ==========================================
def execute_ai_action(prompt_text, category_name="General", user_topic="", tab_index=0, lang_choice="العربية"):
    if not API_KEY:
        str_lit.error("❌ GEMINI_API_KEY is missing in Secrets!")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    output_lang_instr = " Write the response in Arabic." if lang_choice == "العربية" else " Write the response in English."
    payload = {"contents": [{"parts": [{"text": prompt_text + output_lang_instr}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200:
            output_text = res_data['candidates'][0]['content']['parts'][0]['text']
            
            item = {
                "id": len(str_lit.session_state["history"]) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "category": category_name,
                "topic": user_topic if user_topic else "New Request",
                "prompt": prompt_text,
                "result": output_text,
                "tab_index": tab_index,
                "rating": 5
            }
            
            str_lit.session_state["history"].insert(0, item)
            save_data(HISTORY_FILE, str_lit.session_state["history"])
            return output_text
        else:
            str_lit.error(f"❌ Error from Gemini API: {res_data.get('error', {}).get('message', 'Unknown error')}")
            return None
    except Exception as e:
        str_lit.error(f"❌ Connection Error: {e}")
        return None

# ==========================================
# 6. لوحة التحكم الجانبية (Sidebar)
# ==========================================
with str_lit.sidebar:
    lang_options = ["العربية", "English"]
    selected_lang = str_lit.selectbox("🌐 لغة واجهة المستخدم / Interface Language", lang_options, index=0 if str_lit.session_state["last_lang"] == "العربية" else 1)
    
    if selected_lang != str_lit.session_state["last_lang"]:
        str_lit.session_state["last_lang"] = selected_lang
        if str_lit.session_state["current_result"]:
            str_lit.session_state["current_result"] = translate_text(str_lit.session_state["current_result"], selected_lang)
        str_lit.rerun()

    T = TEXTS[selected_lang]
    
    str_lit.markdown(f"### {T['sidebar_title']}")
    str_lit.markdown(f"### {T['stats_title']}")
    total_tasks = len(str_lit.session_state["history"])
    str_lit.metric(label=T["stat_total"], value=total_tasks)
    
    str_lit.markdown("---")
    search_query = str_lit.text_input(T["search_label"], "")
    
    str_lit.markdown(f"### {T['fav_title']}")
    favs = str_lit.session_state["favorites"]
    if favs:
        for fav in favs:
            if str_lit.button(f"⭐ {fav.get('topic', 'Fav')[:20]}", key=f"fav_{fav.get('id', 0)}"):
                str_lit.session_state["current_result"] = fav["result"]
    else:
        str_lit.info(T["fav_empty"])
        
    str_lit.markdown("---")
    str_lit.markdown(f"### {T['history_title']}")
    history = str_lit.session_state["history"]
    
    if history:
        if str_lit.button(T["clear_history"]):
            str_lit.session_state["history"] = []
            save_data(HISTORY_FILE, [])
            str_lit.rerun()
            
        for item in history[:10]:
            if search_query.lower() in item['topic'].lower() or search_query.lower() in item['category'].lower():
                if str_lit.button(f"📌 [{item['category']}] {item['topic'][:18]}...", key=f"hist_{item['id']}"):
                    str_lit.session_state["current_result"] = item["result"]
    else:
        str_lit.info(T["history_empty"])

# ==========================================
# 7. الواجهة الرئيسية والتنقل بين التبويبات
# ==========================================
T = TEXTS[str_lit.session_state["last_lang"]]

str_lit.title(T["main_title"])
str_lit.caption(T["main_caption"])

tabs = str_lit.tabs(T["tabs"])

# --- التبويب الأول: الأفكار والسكريبتات ---
with tabs[0]:
    str_lit.header(T["t1_header"])
    t1_topic = floating_voice_textarea(T["t1_input_label"], "t1_val", T["t1_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t1_dur = str_lit.selectbox(T["t1_dur"], T["t1_dur_opts"], key="t1_dur_idx")
    with col2:
        t1_style = str_lit.selectbox(T["t1_style"], T["t1_style_opts"], key="t1_style_idx")
    with col3:
        t1_target = str_lit.selectbox(T["t1_target"], T["t1_target_opts"], key="t1_target_idx")
        
    t1_extra = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t1_extra_opts")
    
    if str_lit.button(T["t1_btn"], key="t1_submit"):
        if not t1_topic.strip():
            str_lit.warning(T["t1_warn"])
        else:
            with str_lit.spinner(T["t1_spin"]):
                prompt = f"""
                Act as an elite YouTube Director and Professional Scriptwriter.
                Create a comprehensive video script and breakdown based on the following details:
                - Video Topic/Idea: {t1_topic}
                - Duration: {t1_dur}
                - Visual Style: {t1_style}
                - Target Audience: {t1_target}
                - Extra Features Requested: {', '.join(t1_extra) if t1_extra else 'None'}
                
                Provide structured sections: Hook, Intro, Main Content Body with visual cues, Outro/CTA, plus any requested extra features.
                """
                res = execute_ai_action(prompt, category_name="Scripts", user_topic=t1_topic, tab_index=0, lang_choice=str_lit.session_state["last_lang"])
                if res:
                    str_lit.session_state["current_result"] = res

# --- التبويب الثاني: الأغاني والصوت ---
with tabs[1]:
    str_lit.header(T["t2_header"])
    t2_topic = floating_voice_textarea(T["t2_input_label"], "t2_val", T["t2_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t2_dialect = str_lit.selectbox(T["t2_dialect"], T["t2_dialect_opts"], key="t2_dial_idx")
    with col2:
        t2_style = str_lit.selectbox(T["t2_style"], T["t2_style_opts"], key="t2_sty_idx")
    with col3:
        t2_vocal = str_lit.selectbox(T["t2_vocal"], T["t2_vocal_opts"], key="t2_voc_idx")
        
    t2_extra = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t2_extra_opts")
    
    if str_lit.button(T["t2_btn"], key="t2_submit"):
        if not t2_topic.strip():
            str_lit.warning(T["t2_warn"])
        else:
            with str_lit.spinner(T["t2_spin"]):
                prompt = f"""
                Act as a professional Music Producer and Hit Songwriter.
                Create professional song lyrics and sound design layout based on:
                - Theme/Idea: {t2_topic}
                - Dialect/Flavor: {t2_dialect}
                - Genre: {t2_style}
                - Vocal Style: {t2_vocal}
                - Extra Add-ons: {', '.join(t2_extra) if t2_extra else 'None'}
                """
                res = execute_ai_action(prompt, category_name="Music", user_topic=t2_topic, tab_index=1, lang_choice=str_lit.session_state["last_lang"])
                if res:
                    str_lit.session_state["current_result"] = res

# --- التبويب الثالث: تصميم الصور ---
with tabs[2]:
    str_lit.header(T["t3_header"])
    t3_topic = floating_voice_textarea(T["t3_input_label"], "t3_val", T["t3_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t3_engine = str_lit.selectbox(T["t3_engine"], T["t3_engine_opts"], key="t3_eng_idx")
    with col2:
        t3_aspect = str_lit.selectbox(T["t3_aspect"], T["t3_aspect_opts"], key="t3_asp_idx")
    with col3:
        t3_light = str_lit.selectbox(T["t3_light"], T["t3_light_opts"], key="t3_lgt_idx")
        
    t3_extra = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t3_extra_opts")
    
    if str_lit.button(T["t3_btn"], key="t3_submit"):
        if not t3_topic.strip():
            str_lit.warning(T["t3_warn"])
        else:
            with str_lit.spinner(T["t3_spin"]):
                prompt = f"""
                Act as an expert AI Image Prompt Engineer.
                Create optimized, high-end visual prompts based on:
                - Scene Description: {t3_topic}
                - AI Engine: {t3_engine}
                - Aspect Ratio: {t3_aspect}
                - Lighting: {t3_light}
                - Extra Features: {', '.join(t3_extra) if t3_extra else 'None'}
                """
                res = execute_ai_action(prompt, category_name="Images", user_topic=t3_topic, tab_index=2, lang_choice=str_lit.session_state["last_lang"])
                if res:
                    str_lit.session_state["current_result"] = res

# --- التبويب الرابع: تحريك الفيديو ---
with tabs[3]:
    str_lit.header(T["t4_header"])
    t4_topic = floating_voice_textarea(T["t4_input_label"], "t4_val", T["t4_input_placeholder"])
    
    col1, col2 = str_lit.columns(2)
    with col1:
        t4_tool = str_lit.selectbox(T["t4_tool"], T["t4_tool_opts"], key="t4_tool_idx")
    with col2:
        t4_cam = str_lit.selectbox(T["t4_cam"], T["t4_cam_opts"], key="t4_cam_idx")
        
    t4_extra = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t4_extra_opts")
    
    if str_lit.button(T["t4_btn"], key="t4_submit"):
        if not t4_topic.strip():
            str_lit.warning(T["t4_warn"])
        else:
            with str_lit.spinner(T["t4_spin"]):
                prompt = f"""
                Act as a professional Video Director and Motion Prompt Specialist.
                Create detailed animation and motion sequence prompts for:
                - Text / Motion Desc: {t4_topic}
                - Target Tool: {t4_tool}
                - Camera Movement: {t4_cam}
                - Extra Features: {', '.join(t4_extra) if t4_extra else 'None'}
                """
                res = execute_ai_action(prompt, category_name="Motion", user_topic=t4_topic, tab_index=3, lang_choice=str_lit.session_state["last_lang"])
                if res:
                    str_lit.session_state["current_result"] = res

# --- التبويب الخامس: استراتيجيات التسويق ---
with tabs[4]:
    str_lit.header(T["t5_header"])
    t5_topic = floating_voice_textarea(T["t5_input_label"], "t5_val", T["t5_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t5_plat = str_lit.selectbox(T["t5_plat"], T["t5_plat_opts"], key="t5_plat_idx")
    with col2:
        t5_goal = str_lit.selectbox(T["t5_goal"], T["t5_goal_opts"], key="t5_goal_idx")
    with col3:
        t5_budget = str_lit.number_input(T["t5_budget"], min_value=100, max_value=100000, value=1000, step=100, key="t5_bud_val")
        
    t5_extra = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t5_extra_opts")
    
    if str_lit.button(T["t5_btn"], key="t5_submit"):
        if not t5_topic.strip():
            str_lit.warning(T["t5_warn"])
        else:
            with str_lit.spinner(T["t5_spin"]):
                prompt = f"""
                Act as a Chief Marketing Officer (CMO) and Growth Strategist.
                Create a comprehensive marketing and campaign strategy for:
                - Product/Topic: {t5_topic}
                - Platform: {t5_plat}
                - Goal: {t5_goal}
                - Budget: ${t5_budget}
                - Extra Features: {', '.join(t5_extra) if t5_extra else 'None'}
                """
                res = execute_ai_action(prompt, category_name="Marketing", user_topic=t5_topic, tab_index=4, lang_choice=str_lit.session_state["last_lang"])
                if res:
                    str_lit.session_state["current_result"] = res

# ==========================================
# 8. عرض النتيجة النهائية وأزرار التحكم
# ==========================================
if str_lit.session_state["current_result"]:
    str_lit.markdown("---")
    str_lit.subheader(T["result_label"])
    str_lit.markdown(str_lit.session_state["current_result"])
    
    col_c1, col_c2 = str_lit.columns(2)
    with col_c1:
        if str_lit.button(T["copy_btn"]):
            str_lit.toast("تم نسخ النص بنجاح!", icon="📋")
    with col_c2:
        str_lit.download_button(
            label=T["download_txt"],
            data=str_lit.session_state["current_result"],
            file_name=f"content_studio_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
