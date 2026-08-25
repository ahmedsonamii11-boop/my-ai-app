import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة وتصميم واجهة المستخدم
# ==========================================
str_lit.set_page_config(
    page_title="إبداع - المنظومة المتكاملة لإنتاج المحتوى",
    page_icon="✨",
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
    .stTextArea textarea, .stTextInput input, .stSelectbox select, .stMultiSelect div {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #f1f5f9 !important;
        padding: 10px !important;
    }
    .guide-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = str_lit.secrets.get("GEMINI_API_KEY")

# ==========================================
# 2. نظام التخزين الدائم الآمن (محمي تماماً)
# ==========================================
HISTORY_FILE = "ibda3_studio_history.json"
FAV_FILE = "ibda3_studio_favorites.json"

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

if "history" not in str_lit.session_state:
    str_lit.session_state["history"] = load_persistent_data(HISTORY_FILE)

if "favorites" not in str_lit.session_state:
    str_lit.session_state["favorites"] = load_persistent_data(FAV_FILE)

if "current_result" not in str_lit.session_state:
    str_lit.session_state["current_result"] = None

for key in ["t0_val", "t1_val", "t2_val", "t3_val", "t4_val", "t5_val"]:
    if key not in str_lit.session_state:
        str_lit.session_state[key] = ""

# ==========================================
# 3. القاموس اللغوي والخيارات المتقدمة
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚡ لوحة التحكم والأرشيف",
        "search_label": "🔍 بحث في الأرشيف:",
        "fav_title": "⭐ العناصر المفضلة المحفوظة",
        "fav_empty": "لا توجد مفضلات مسجلة",
        "history_title": "📜 الأرشيف الدائم",
        "history_empty": "الأرشيف فارغ حالياً",
        "clear_history": "🗑️ تفريغ الأرشيف",
        "stats_title": "📊 المؤشرات",
        "stat_total": "إجمالي العمليات المحفوظة:",
        
        "main_title": "✨ منصة إبداع | Ibda3 Studio Pro",
        "main_caption": "المنظومة الاحترافية المتكاملة لإنتاج المحتوى والخطط الاستراتيجية بالذكاء الاصطناعي",
        
        "tabs": [
            "🏠 دليل الاستخدام",
            "0️⃣ 🗺️ التخطيط الاستراتيجي",
            "1️⃣ 💡 الأفكار والسكريبتات",
            "2️⃣ 🎵 الأغاني والصوت",
            "3️⃣ 🎨 تصميم الصور والهوية",
            "4️⃣ 🗣️ تحريك الفيديو",
            "5️⃣ 📊 التسويق والإعلانات"
        ],
        
        "guide_title": "👋 أهلاً بك في النسخة الاحترافية من منصة إبداع",
        "guide_desc": "تم إثراء المنصة الآن بـ خيارات متقدمة لكل مرحلة تتيح لك تخصيص كل تفصيل بدقة مذهلة:",
        "step_0": "🗺️ التخطيط: اختر أهداف عملك، منهجية الإدارة، ونطاق السوق المستهدف.",
        "step_1": "💡 السكريبتات: حدد مدة الفيديو، النمط البصري، نبرة الصوت، وعقدة البداية (الخطاف).",
        "step_2": "🎵 الأغاني: تحكم في اللهجة، النمط الموسيقي، الآلات المستخدمة، ونوع الأداء الصوتي.",
        "step_3": "🎨 الصور: اختر محركات الذكاء الاصطناعي الكبرى، زوايا التصوير، الأبعاد، والإضاءة الدرامية.",
        "step_4": "🗣️ الفيديو: اختر أدوات التحريك الحركي، مسارات الكاميرا، وسرعة الحركة.",
        "step_5": "📊 التسويق: حدد المنصات الإعلانية، نوع الجمهور، استراتيجية الإنفاق، وهدف الحملة.",

        # خيارات المرحلة 0
        "t0_header": "🗺️ المرحلة الأولى: التخطيط الاستراتيجي المتقدم",
        "t0_input_label": "🎯 ما هو مشروعك أو فكرتك الريادية؟",
        "t0_input_placeholder": "اكتب فكرة المشروع بالتفصيل...",
        "t0_goal": "🎯 الهدف الاستراتيجي:",
        "t0_goal_opts": ["إطلاق شركة ناشئة (Startup)", "حملة تسويقية رقمية كبرى", "منصة تعليمية أو بودكاست", "إعادة هيكلة براند", "توسيع مبيعات التجارة الإلكترونية"],
        "t0_meth": "📈 منهجية العمل:",
        "t0_meth_opts": ["Business Model Canvas", "Lean Startup", "SWOT & Competitor Analysis", "OKRs Growth Plan"],
        "t0_market": "🌍 النطاق الجغرافي / السوق:",
        "t0_market_opts": ["مصر والشمال الإفريقي", "دول الخليج العربي", "الشرق الأوسط وشمال إفريقيا (MENA)", "السوق العالمي (Global - English)"],
        "t0_btn": "🗺️ هندسة الخطة الاستراتيجية الشاملة",
        "t0_warn": "⚠️ يرجى إدخال تفاصيل المشروع أولاً!",
        "t0_spin": "⚡ جارٍ تحليل الأسواق وبناء الاستراتيجية...",

        # خيارات المرحلة 1
        "t1_header": "🎬 المرحلة الثانية: صانع الأفكار والسكريبتات الاحترافية",
        "t1_input_label": "📽️ فكرة الفيديو أو الموضوع الأساسي:",
        "t1_input_placeholder": "اكتب فكرة الفيديو باختصار...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": ["15 ثانية (Reels/Shorts)", "30 ثانية (Fast Hook)", "60 ثانية (TikTok Pro)", "3 دقائق (YouTube Deep)", "10 دقائق (Masterclass)"],
        "t1_style": "🎨 النمط البصري والسينمائي:",
        "t1_style_opts": ["سينمائي واقعي (Cinematic)", "وثائقي تحقيقي (Documentary)", "تعليمي تفاعلي (Edutainment)", "كوميدي خفيف", "درامي مؤثر", "تقني تكنولوجي"],
        "t1_tone": "🎙️ نبرة الإلقاء (Tone):",
        "t1_tone_opts": ["حماسي ومتحفز", "هادئ وموثوق", "غموض وتشويق", "تحفيزي ملهم", "ساخر وذكاء ترفيهي"],
        "t1_target": "🎯 الفئة المستهدفة:",
        "t1_target_opts": ["الجيل الناشئ (Gen Z)", "رواد الأعمال والمستثمرون", "المهنيون والموظفون", "الأسرة وربات البيوت", "المهتمون بالتكنولوجيا والتقنية"],
        "t1_btn": "🔥 توليد السكريبت الاحترافي",
        "t1_warn": "⚠️ يرجى إدخال فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ صياغة الخطاف والسكريبت...",

        # خيارات المرحلة 2
        "t2_header": "🎵 المرحلة الثالثة: استوديو الأغاني والموسيقى المتطور",
        "t2_input_label": "💡 موضوع الأغنية أو الرسالة المراد توصيلها:",
        "t2_input_placeholder": "اكتب موضوع الكلمات أو القصة...",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_dialect_opts": ["عامية مصرية عصرية", "فصحى فخمة", "خليجي طربي", "لبناني/شامي دافئ", "إنجليزي بوب عالمي"],
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_style_opts": ["مهرجانات وشعبي حديث", "راب وسريع (Hip Hop/Trap)", "بوب هادئ (Chill Pop)", "روك درامي", "موسيقى تصويرية ملحمية"],
        "t2_vocal": "🎙️ نوع الأداء الصوتي:",
        "t2_vocal_opts": ["رجالي عميق (Bass/Baritone)", "شبابي حماسي عالي", "نسائي دافئ وناعم", "كورال جماعي", "مؤثرات أوتوتيون حديثة"],
        "t2_inst": "🎸 الآلات البارزة:",
        "t2_inst_opts": ["بيتات إلكترونية وثقيلة", "جيتار آكوستيك هادئ", "عود شرقي وإيقاعات", "بيانو كلاسيكي درامي"],
        "t2_btn": "✨ توليد الكلمات وتوزيع الأغنية",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية!",
        "t2_spin": "⚡ جارٍ تأليف الكلمات والمقاطع...",

        # خيارات المرحلة 3
        "t3_header": "🎨 المرحلة الرابعة: هندسة الصور والهوية البصرية",
        "t3_input_label": "🖼️ وصف المشهد المراد تصميمه بدقة:",
        "t3_input_placeholder": "صف العناصر، الألوان، والخلفية...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي المستهدف:",
        "t3_engine_opts": ["Midjourney v6.0", "Flux.1 Dev/Pro", "DALL-E 3 Ultra", "Adobe Firefly v3", "Stable Diffusion XL"],
        "t3_aspect": "📐 أبعاد الصورة (Aspect Ratio):",
        "t3_aspect_opts": ["9:16 (Stories / Reels / TikTok)", "16:9 (YouTube Cinematic)", "1:1 (Instagram Square)", "4:5 (Instagram Portrait)", "21:9 (Ultra Wide Cinema)"],
        "t3_light": "💡 الإضاءة والتأثيرات:",
        "t3_light_opts": ["سينمائية استوديو (Studio Lighting)", "سايبربانك نيون مظلم", "ساعة ذهبية (Golden Hour)", "إضاءة خافتة درامية (Moody)", "إضاءة إعلانية تجارية نظيفة"],
        "t3_shot": "📷 زاوية الكاميرا:",
        "t3_shot_opts": ["لقطة مقربة جداً (Macro/Close-up)", "عين الطائر (Bird's Eye View)", "لقطة من أسفل لتعظيم الشخصية", "بورتريه احترافي عريض"],
        "t3_btn": "🎨 هندسة أوامر الصور المتقدمة",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة!",
        "t3_spin": "⚡ هندسة الأوامر البرمجية للصور...",

        # خيارات المرحلة 4
        "t4_header": "🗣️ المرحلة الخامسة: سينما تحريك الفيديو والموشن",
        "t4_input_label": "📜 وصف الحركة المطلوبة أو تحريك الصورة:",
        "t4_input_placeholder": "صف كيف تتحرك الكاميرا أو العناصر...",
        "t4_tool": "🤖 أداة التحريك الذكية:",
        "t4_tool_opts": ["Runway Gen-3 Alpha", "Luma Dream Machine", "OpenAI Sora Prompts", "Pika Labs v2.2", "HeyGen AI Avatar"],
        "t4_cam": "🎥 حركة الكاميرا الاحترافية:",
        "t4_cam_opts": ["زوم إن بطيء ودرامي (Slow Zoom In)", "زوم أوت للكشف عن المشهد", "بانوراما أفقية سريعة (Pan)", "تتبع حركي متقدم (Tracking Shot)", "لقطة دوران 360 درجة"],
        "t4_speed": "⚡ سرعة وتيرة الحركة:",
        "t4_speed_opts": ["بطيء جداً وسينمائي (Cinematic Slow-mo)", "سرعة عادية متوازنة", "حركة سريعة وخاطفة (Dynamic Fast)"],
        "t4_btn": "⚡ توليد سيناريو وأوامر التحريك",
        "t4_warn": "⚠️ يرجى إدخال تفاصيل الحركة!",
        "t4_spin": "⚡ إعداد مسار الكاميرا والحركة...",

        # خيارات المرحلة 5
        "t5_header": "📊 المرحلة السادسة: الإعلانات والتسويق الرقمي",
        "t5_input_label": "🎯 المنتج أو الخدمة المراد تسويقها:",
        "t5_input_placeholder": "اكتب تفاصيل المنتج والجمهور المستهدف...",
        "t5_plat": "📱 المنصة الإعلانية المستهدفة:",
        "t5_plat_opts": ["TikTok Ads Manager", "Meta Ads (Instagram/Facebook)", "YouTube Video Ads", "LinkedIn B2B Ads", "Google Search Ads"],
        "t5_goal": "🎯 الهدف التسويقي (Campaign Objective):",
        "t5_goal_opts": ["مبيعات مباشرة وإيرادات (Conversions)", "وعي عالي بالعلامة التجارية (Awareness)", "توليد عملاء محتملين (Lead Generation)", "زيارات وزيارات للموقع (Traffic)"],
        "t5_strategy": "💡 استراتيجية المحتوى الإعلاني:",
        "t5_strategy_opts": ["قصة العميل (UGC Style)", "إثبات اجتماعي ومراجعات", "عرض خصم لفترة محدودة", "مقارنة تنافسية مباشرة"],
        "t5_budget": "💰 الميزانية الشهرية المقترحة ($):",
        "t5_btn": "🚀 تصميم الحملة التسويقية المتكاملة",
        "t5_warn": "⚠️ يرجى إدخال تفاصيل الحملة!",
        "t5_spin": "⚡ تحليل السوق واستهداف الجماهير...",

        "result_label": "🚀 النتيجة الاحترافية المحفوظة:",
        "copy_btn": "📋 نسخ",
        "download_txt": "📥 تحميل ملف (.txt)",
        "rating_label": "⭐ التقييم:"
    },
    "English": {
        "sidebar_title": "⚡ Control Panel & Archive",
        "search_label": "🔍 Search Archive:",
        "fav_title": "⭐ Saved Favorites",
        "fav_empty": "No favorites saved yet",
        "history_title": "📜 Persistent Archive",
        "history_empty": "Archive is empty",
        "clear_history": "🗑️ Clear Archive",
        "stats_title": "📊 Metrics",
        "stat_total": "Total Saved Tasks:",
        "main_title": "✨ Ibda3 Studio | Content & Strategy Platform Pro",
        "main_caption": "Advanced AI-powered end-to-end studio for professional content creation",
        
        "tabs": ["🏠 Guide", "0️⃣ Strategy", "1️⃣ Scripts", "2️⃣ Music", "3️⃣ Images", "4️⃣ Video", "5️⃣ Marketing"],
        
        "guide_title": "👋 Welcome to Ibda3 Studio Pro",
        "guide_desc": "Enhanced with advanced options for each phase to give you absolute professional control:",
        "step_0": "🗺️ Strategy: Choose business models, market scale, and growth objectives.",
        "step_1": "💡 Scripts: Select durations, visual styles, vocal tones, and viral hooks.",
        "step_2": "🎵 Music: Customize dialects, music genres, instruments, and vocal styles.",
        "step_3": "🎨 Images: Pick top AI engines, aspect ratios, lighting, and camera angles.",
        "step_4": "🗣️ Video: Control motion tools, camera tracks, and speed dynamics.",
        "step_5": "📊 Marketing: Target ad platforms, campaign objectives, and bidding strategies.",

        "t0_header": "Phase 1: Advanced Strategy", "t0_input_label": "Core Idea:", "t0_input_placeholder": "Enter idea...",
        "t0_goal": "Goal:", "t0_goal_opts": ["Startup Launch", "Major Campaign", "Podcast/Ed", "Rebranding"], "t0_meth": "Methodology:", "t0_meth_opts": ["Business Model Canvas", "Lean Startup", "SWOT"], "t0_market": "Market:", "t0_market_opts": ["MENA", "GCC", "Global"], "t0_btn": "Build Strategy", "t0_warn": "Enter details!", "t0_spin": "Analyzing...",
        
        "t1_header": "Phase 2: Professional Scripts", "t1_input_label": "Video Idea:", "t1_input_placeholder": "Enter video...",
        "t1_dur": "Duration:", "t1_dur_opts": ["15s", "30s", "60s", "3m"], "t1_style": "Style:", "t1_style_opts": ["Cinematic", "Documentary", "Edutainment"], "t1_tone": "Tone:", "t1_tone_opts": ["Energetic", "Calm", "Suspense"], "t1_target": "Audience:", "t1_target_opts": ["Gen Z", "Entrepreneurs", "Professionals"], "t1_btn": "Generate Script", "t1_warn": "Enter idea!", "t1_spin": "Generating...",
        
        "t2_header": "Phase 3: Music Studio", "t2_input_label": "Song Idea:", "t2_input_placeholder": "Song theme...",
        "t2_dialect": "Flavor:", "t2_dialect_opts": ["Egyptian", "Classical", "Gulf"], "t2_style": "Genre:", "t2_style_opts": ["Mahraganat", "Hip Hop", "Chill Pop"], "t2_vocal": "Vocal:", "t2_vocal_opts": ["Deep Bass", "Energetic", "Warm Female"], "t2_inst": "Instruments:", "t2_inst_opts": ["Electronic Beats", "Acoustic Guitar", "Oriental Oud"], "t2_btn": "Generate Song", "t2_warn": "Enter song!", "t2_spin": "Crafting...",
        
        "t3_header": "Phase 4: Image Engineering", "t3_input_label": "Scene Description:", "t3_input_placeholder": "Describe scene...",
        "t3_engine": "AI Engine:", "t3_engine_opts": ["Midjourney v6", "Flux.1", "DALL-E 3"], "t3_aspect": "Aspect Ratio:", "t3_aspect_opts": ["9:16", "16:9", "1:1"], "t3_light": "Lighting:", "t3_light_opts": ["Studio", "Cyberpunk", "Golden Hour"], "t3_shot": "Camera Shot:", "t3_shot_opts": ["Close-up", "Bird's Eye", "Wide Portrait"], "t3_btn": "Generate Prompts", "t3_warn": "Enter description!", "t3_spin": "Engineering...",
        
        "t4_header": "Phase 5: Video Motion", "t4_input_label": "Motion Text:", "t4_input_placeholder": "Motion details...",
        "t4_tool": "Motion Tool:", "t4_tool_opts": ["Runway Gen-3", "Luma", "Pika"], "t4_cam": "Camera Motion:", "t4_cam_opts": ["Slow Zoom In", "Pan", "Tracking Shot"], "t4_speed": "Speed:", "t4_speed_opts": ["Cinematic Slow-mo", "Balanced", "Fast Dynamic"], "t4_btn": "Generate Motion", "t4_warn": "Enter motion!", "t4_spin": "Preparing...",
        
        "t5_header": "Phase 6: Advanced Marketing", "t5_input_label": "Product:", "t5_input_placeholder": "Campaign details...",
        "t5_plat": "Platform:", "t5_plat_opts": ["TikTok Ads", "Meta Ads", "YouTube Ads"], "t5_goal": "Objective:", "t5_goal_opts": ["Conversions", "Awareness", "Leads"], "t5_strategy": "Ad Strategy:", "t5_strategy_opts": ["UGC Style", "Social Proof", "Limited Offer"], "t5_budget": "Budget ($):", "t5_btn": "Execute Campaign", "t5_warn": "Enter details!", "t5_spin": "Analyzing...",
        
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
    system_instruction = f"You are an elite expert AI Producer for Ibda3 Platform Pro, providing highly professional, comprehensive, and detailed outputs. Language: {lang_choice}."
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
# 5. الشريط الجانبي (محمي بالكامل)
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

# ------------------------------------------
# تبويب 0: دليل الاستخدام والتوجيه
# ------------------------------------------
with tabs[0]:
    str_lit.markdown(f"""
    <div class="guide-box">
        <h2>{t['guide_title']}</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">{t['guide_desc']}</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <ul>
            <li style="margin-bottom: 10px;">{t['step_0']}</li>
            <li style="margin-bottom: 10px;">{t['step_1']}</li>
            <li style="margin-bottom: 10px;">{t['step_2']}</li>
            <li style="margin-bottom: 10px;">{t['step_3']}</li>
            <li style="margin-bottom: 10px;">{t['step_4']}</li>
            <li style="margin-bottom: 10px;">{t['step_5']}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# تبويب 1: التخطيط الاستراتيجي المتقدم
# ------------------------------------------
with tabs[1]:
    str_lit.subheader(t["t0_header"])
    str_lit.session_state["t0_val"] = str_lit.text_area(t["t0_input_label"], value=str_lit.session_state["t0_val"], placeholder=t["t0_input_placeholder"], key="t0_w")
    c1, c2, c3 = str_lit.columns(3)
    goal_0 = c1.selectbox(t["t0_goal"], t["t0_goal_opts"], key="t0_g")
    meth_0 = c2.selectbox(t["t0_meth"], t["t0_meth_opts"], key="t0_m")
    market_0 = c3.selectbox(t["t0_market"], t["t0_market_opts"], key="t0_mk")
    
    if str_lit.button(t["t0_btn"], key="t0_b"):
        if not str_lit.session_state["t0_val"].strip():
            str_lit.warning(t["t0_warn"])
        else:
            with str_lit.spinner(t["t0_spin"]):
                prompt = f"Advanced Strategic plan for project: '{str_lit.session_state['t0_val']}'. Goal: {goal_0}, Methodology: {meth_0}, Market: {market_0}. Provide comprehensive business analysis, KPIs, and roadmap."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Strategic Planning Pro", str_lit.session_state["t0_val"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 2: الأفكار والسكريبتات الاحترافية
# ------------------------------------------
with tabs[2]:
    str_lit.subheader(t["t1_header"])
    str_lit.session_state["t1_val"] = str_lit.text_area(t["t1_input_label"], value=str_lit.session_state["t1_val"], placeholder=t["t1_input_placeholder"], key="t1_w")
    c1, c2, c3, c4 = str_lit.columns(4)
    dur = c1.selectbox(t["t1_dur"], t["t1_dur_opts"], key="t1_d")
    style = c2.selectbox(t["t1_style"], t["t1_style_opts"], key="t1_s")
    tone = c3.selectbox(t["t1_tone"], t["t1_tone_opts"], key="t1_tn")
    target = c4.selectbox(t["t1_target"], t["t1_target_opts"], key="t1_t")
    
    if str_lit.button(t["t1_btn"], key="t1_b"):
        if not str_lit.session_state["t1_val"].strip():
            str_lit.warning(t["t1_warn"])
        else:
            with str_lit.spinner(t["t1_spin"]):
                prompt = f"Pro Video Script for: '{str_lit.session_state['t1_val']}', Duration: {dur}, Visual Style: {style}, Tone: {tone}, Target Audience: {target}. Include strong hook, body scenes, and CTA."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Ideas & Scripts Pro", str_lit.session_state["t1_val"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 3: الأغاني والصوت المتطور
# ------------------------------------------
with tabs[3]:
    str_lit.subheader(t["t2_header"])
    str_lit.session_state["t2_val"] = str_lit.text_area(t["t2_input_label"], value=str_lit.session_state["t2_val"], placeholder=t["t2_input_placeholder"], key="t2_w")
    c1, c2, c3, c4 = str_lit.columns(4)
    dialect = c1.selectbox(t["t2_dialect"], t["t2_dialect_opts"], key="t2_d")
    genre = c2.selectbox(t["t2_style"], t["t2_style_opts"], key="t2_s")
    vocal = c3.selectbox(t["t2_vocal"], t["t2_vocal_opts"], key="t2_v")
    inst = c4.selectbox(t["t2_inst"], t["t2_inst_opts"], key="t2_i")
    
    if str_lit.button(t["t2_btn"], key="t2_b"):
        if not str_lit.session_state["t2_val"].strip():
            str_lit.warning(t["t2_warn"])
        else:
            with str_lit.spinner(t["t2_spin"]):
                prompt = f"Pro Song Lyrics and Music Production Guide for: '{str_lit.session_state['t2_val']}', Dialect: {dialect}, Genre: {genre}, Vocal Style: {vocal}, Instruments: {inst}."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Music & Audio Pro", str_lit.session_state["t2_val"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 4: الصور والهوية البصرية المتقدمة
# ------------------------------------------
with tabs[4]:
    str_lit.subheader(t["t3_header"])
    str_lit.session_state["t3_val"] = str_lit.text_area(t["t3_input_label"], value=str_lit.session_state["t3_val"], placeholder=t["t3_input_placeholder"], key="t3_w")
    c1, c2, c3, c4 = str_lit.columns(4)
    engine = c1.selectbox(t["t3_engine"], t["t3_engine_opts"], key="t3_e")
    aspect = c2.selectbox(t["t3_aspect"], t["t3_aspect_opts"], key="t3_a")
    light = c3.selectbox(t["t3_light"], t["t3_light_opts"], key="t3_l")
    shot = c4.selectbox(t["t3_shot"], t["t3_shot_opts"], key="t3_sh")
    
    if str_lit.button(t["t3_btn"], key="t3_b"):
        if not str_lit.session_state["t3_val"].strip():
            str_lit.warning(t["t3_warn"])
        else:
            with str_lit.spinner(t["t3_spin"]):
                prompt = f"Advanced Image Generation Prompts for: '{str_lit.session_state['t3_val']}', Engine: {engine}, Aspect Ratio: {aspect}, Lighting: {light}, Shot Type: {shot}. Provide ready-to-use professional prompts."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Image Prompts Pro", str_lit.session_state["t3_val"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 5: تحريك الفيديو والموشن
# ------------------------------------------
with tabs[5]:
    str_lit.subheader(t["t4_header"])
    str_lit.session_state["t4_val"] = str_lit.text_area(t["t4_input_label"], value=str_lit.session_state["t4_val"], placeholder=t["t4_input_placeholder"], key="t4_w")
    c1, c2, c3 = str_lit.columns(3)
    tool = c1.selectbox(t["t4_tool"], t["t4_tool_opts"], key="t4_t")
    cam = c2.selectbox(t["t4_cam"], t["t4_cam_opts"], key="t4_c")
    speed = c3.selectbox(t["t4_speed"], t["t4_speed_opts"], key="t4_sp")
    
    if str_lit.button(t["t4_btn"], key="t4_b"):
        if not str_lit.session_state["t4_val"].strip():
            str_lit.warning(t["t4_warn"])
        else:
            with str_lit.spinner(t["t4_spin"]):
                prompt = f"Pro Video Motion Prompts for AI Tools for: '{str_lit.session_state['t4_val']}', Tool: {tool}, Camera Movement: {cam}, Speed: {speed}."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Video Motion Pro", str_lit.session_state["t4_val"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 6: التسويق والإعلانات الرقمية المتقدمة
# ------------------------------------------
with tabs[6]:
    str_lit.subheader(t["t5_header"])
    str_lit.session_state["t5_val"] = str_lit.text_area(t["t5_input_label"], value=str_lit.session_state["t5_val"], placeholder=t["t5_input_placeholder"], key="t5_w")
    c1, c2, c3, c4 = str_lit.columns(4)
    plat = c1.selectbox(t["t5_plat"], t["t5_plat_opts"], key="t5_p")
    goal = c2.selectbox(t["t5_goal"], t["t5_goal_opts"], key="t5_g")
    strategy = c3.selectbox(t["t5_strategy"], t["t5_strategy_opts"], key="t5_st")
    budget = c4.number_input(t["t5_budget"], min_value=50, max_value=500000, value=1500, step=100, key="t5_bgt")
    
    if str_lit.button(t["t5_btn"], key="t5_b"):
        if not str_lit.session_state["t5_val"].strip():
            str_lit.warning(t["t5_warn"])
        else:
            with str_lit.spinner(t["t5_spin"]):
                prompt = f"Advanced Digital Marketing Campaign for: '{str_lit.session_state['t5_val']}', Platform: {plat}, Objective: {goal}, Strategy: {strategy}, Monthly Budget: ${budget}. Include target audience, ad copy angles, and KPIs."
                res = call_gemini(prompt, selected_lang)
                log_and_save("Marketing Strategy Pro", str_lit.session_state["t5_val"], res)
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
            file_name=f"Ibda3_Studio_Pro_Result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    with col_b:
        str_lit.slider(t["rating_label"], 1, 5, 5, key="result_rating")
else:
    str_lit.info("قم بتنفيذ أي خيار بالأعلى لعرض النتيجة الفورية الاحترافية هنا.")
