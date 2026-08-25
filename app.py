import streamlit as str_lit
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات المنصة المؤسسية
# ==========================================
str_lit.set_page_config(
    page_title="إبداع بريميوم | Enterprise AI Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

str_lit.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0f172a 50%, #1e1b4b 100%);
        font-family: 'Cairo', sans-serif;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(20px);
    }
    
    div.block-container { 
        padding-top: 1.5rem; 
        max-width: 1400px;
    }

    .stButton>button {
        border-radius: 14px; 
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        color: white; 
        border: none; 
        padding: 0.7rem 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.8);
        background: linear-gradient(135deg, #818cf8 0%, #4f46e5 100%);
    }

    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 14px !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        background-color: rgba(30, 41, 59, 0.6) !important;
        color: #f1f5f9 !important;
        padding: 12px !important;
        backdrop-filter: blur(10px);
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }
    
    .feature-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 20px;
        border-radius: 14px;
        margin-top: 15px;
    }
    
    .enterprise-header {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.3rem;
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
# 3. القاموس الثنائي الشامل لكل تفاصيل الموقع
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
        "main_caption": "النظام السيبراني المتكامل لإنتاج المحتوى، الخطط الاستراتيجية، وحملات الملايين بالذكاء الاصطناعي",
        
        "tabs": [
            "📊 لوحة القيادة",
            "0️⃣ التخطيط الاستراتيجي",
            "1️⃣ السكريبتات والفيديو",
            "2️⃣ الأغاني والصوت",
            "3️⃣ هندسة الصور",
            "4️⃣ تحريك الموشن",
            "5️⃣ الحملات الإعلانية"
        ],
        
        "d_title": "مرحباً بك في لوحة تحكم الجيل القادم",
        "d_sub": "تتيح لك هذه المنصة التحكم الكامل في جميع أذرع التسويق والإنتاج الفني بجودة تضاهي أكبر الوكالات العالمية.",
        
        # تفاصيل لوحة القيادة الجديدة
        "d_desc_title": "💡 ما هي منصة 'إبداع بريميوم' وكيف تحدث ثورة في عملك؟",
        "d_desc_text": "تعتبر هذه المنصة نظاماً برمجياً متكاملاً مصمماً خصيصاً للشركات الكبرى، وكالات التسويق، وصناع المحتوى المحترفين الذين يستهدفون جودة استثنائية وعوائد استثمارية ضخمة. نحن ندمج أحدث نماذج الذكاء الاصطناعي (مثل Gemini 1.5) لنقدم لك:",
        "d_feat_1": "🎯 **التخطيط الاستراتيجي المتقدم:** بناء نماذج العمل، دراسات جدوى، وخرائط طريق للشركات الناشئة.",
        "d_feat_2": "🎬 **استوديو السكريبتات الفيروسية:** توليد محتوى منصات التواصل الاجتماعي (تيك توك، ريلز، يوتيوب) بنبرات صوت وخطاب دقيقة.",
        "d_feat_3": "🎵 **الإنتاج الصوتي والموسيقي:** صياغة كلمات الأغاني والهويات الصوتية بلهجات وطابع احترافي.",
        "d_feat_4": "🎨 **هندسة الهوية البصرية:** كتابة أوامر مخصصة لأقوى محركات الصور (Midjourney, Flux) بأبعادات وتأثيرات سينمائية.",
        "d_feat_5": "📊 **إدارة الحملات الإعلانية:** هيكلة ميزانيات ضخمة واستهدافات دقيقة لتحقيق أعلى معدلات تحويل (Conversions).",
        
        "btn_gen": "⚡ تنفيذ عملية الإنتاج الذكي",
        "warn": "⚠️ يرجى إدخال البيانات المطلوبة أولاً!",
        "spin": "⚡ جارٍ معالجة البيانات عبر شبكات النماذج الكبرى...",
        "res_title": "🚀 مخرجات الذكاء الاصطناعي المعتمدة:",
        "download": "📥 تصدير التقرير الاحترافي (.txt)",
        "rate": "⭐ تقييم جودة المخرج:",

        # تفاصيل التبويب 0
        "t0_head": "🗺️ المرحلة الأولى: التخطيط الاستراتيجي المتقدم",
        "t0_label": "🎯 املأ فكرة المشروع أو الشركة الناشئة:",
        "t0_ph": "اكتب تفاصيل المشروع الاستثماري...",
        "t0_goal": "🎯 الهدف الاستراتيجي:",
        "t0_goal_opts": ["إطلاق شركة ناشئة (Startup)", "حملة تسويقية رقمية كبرى", "منصة تعليمية أو بودكاست", "إعادة هيكلة براند", "توسيع مبيعات التجارة الإلكترونية"],
        "t0_meth": "📈 منهجية العمل:",
        "t0_meth_opts": ["Business Model Canvas", "Lean Startup", "SWOT & Competitor Analysis", "OKRs Growth Plan"],
        "t0_market": "🌍 النطاق الجغرافي / السوق:",
        "t0_market_opts": ["مصر والشمال الإفريقي", "دول الخليج العربي", "الشرق الأوسط وشمال إفريقيا (MENA)", "السوق العالمي (Global - English)"],

        # تفاصيل التبويب 1
        "t1_head": "🎬 المرحلة الثانية: صانع الأفكار والسكريبتات الاحترافية",
        "t1_label": "📽️ فكرة الفيديو أو الموضوع الأساسي:",
        "t1_ph": "اكتب فكرة الفيديو باختصار...",
        "t1_dur": "⏱️ مدة الفيديو:",
        "t1_dur_opts": ["15 ثانية (Reels/Shorts)", "30 ثانية (Fast Hook)", "60 ثانية (TikTok Pro)", "3 دقائق (YouTube Deep)", "10 دقائق (Masterclass)"],
        "t1_style": "🎨 النمط البصري والسينمائي:",
        "t1_style_opts": ["سينمائي واقعي (Cinematic)", "وثائقي تحقيقي (Documentary)", "تعليمي تفاعلي (Edutainment)", "كوميدي خفيف", "درامي مؤثر", "تقني تكنولوجي"],
        "t1_tone": "🎙️ نبرة الإلقاء (Tone):",
        "t1_tone_opts": ["حماسي ومتحفز", "هادئ وموثوق", "غموض وتشويق", "تحفيزي ملهم", "ساخر وذكاء ترفيهي"],
        "t1_target": "🎯 الفئة المستهدفة:",
        "t1_target_opts": ["الجيل الناشئ (Gen Z)", "رواد الأعمال والمستثمرون", "المهنيون والموظفون", "الأسرة وربات البيوت", "المهتمون بالتكنولوجيا والتقنية"],

        # تفاصيل التبويب 2
        "t2_head": "🎵 المرحلة الثالثة: استوديو الأغاني والموسيقى المتطور",
        "t2_label": "💡 موضوع الأغنية أو الرسالة المراد توصيلها:",
        "t2_ph": "اكتب موضوع الكلمات أو القصة...",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_dialect_opts": ["عامية مصرية عصرية", "فصحى فخمة", "خليجي طربي", "لبناني/شامي دافئ", "إنجليزي بوب عالمي"],
        "t2_genre": "🎼 النمط الموسيقي:",
        "t2_genre_opts": ["مهرجانات وشعبي حديث", "راب وسريع (Hip Hop/Trap)", "بوب هادئ (Chill Pop)", "روك درامي", "موسيقى تصويرية ملحمية"],
        "t2_vocal": "🎙️ نوع الأداء الصوتي:",
        "t2_vocal_opts": ["رجالي عميق (Bass/Baritone)", "شبابي حماسي عالي", "نسائي دافئ وناعم", "كورال جماعي", "مؤثرات أوتوتيون حديثة"],
        "t2_inst": "🎸 الآلات البارزة:",
        "t2_inst_opts": ["بيتات إلكترونية وثقيلة", "جيتار آكوستيك هادئ", "عود شرقي وإيقاعات", "بيانو كلاسيكي درامي"],

        # تفاصيل التبويب 3
        "t3_head": "🎨 المرحلة الرابعة: هندسة الصور والهوية البصرية",
        "t3_label": "🖼️ وصف المشهد المراد تصميمه بدقة:",
        "t3_ph": "صف العناصر، الألوان، والخلفية...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي المستهدف:",
        "t3_engine_opts": ["Midjourney v6.0", "Flux.1 Dev/Pro", "DALL-E 3 Ultra", "Adobe Firefly v3", "Stable Diffusion XL"],
        "t3_aspect": "📐 أبعاد الصورة (Aspect Ratio):",
        "t3_aspect_opts": ["9:16 (Stories / Reels / TikTok)", "16:9 (YouTube Cinematic)", "1:1 (Instagram Square)", "4:5 (Instagram Portrait)", "21:9 (Ultra Wide Cinema)"],
        "t3_light": "💡 الإضاءة والتأثيرات:",
        "t3_light_opts": ["سينمائية استوديو (Studio Lighting)", "سايبربانك نيون مظلم", "ساعة ذهبية (Golden Hour)", "إضاءة خافتة درامية (Moody)", "إضاءة إعلانية تجارية نظيفة"],
        "t3_shot": "📷 زاوية الكاميرا:",
        "t3_shot_opts": ["لقطة مقربة جداً (Macro/Close-up)", "عين الطائر (Bird's Eye View)", "لقطة من أسفل لتعظيم الشخصية", "بورتريه احترافي عريض"],

        # تفاصيل التبويب 4
        "t4_head": "🗣️ المرحلة الخامسة: سينما تحريك الفيديو والموشن",
        "t4_label": "📜 وصف الحركة المطلوبة أو تحريك الصورة:",
        "t4_ph": "صف كيف تتحرك الكاميرا أو العناصر...",
        "t4_tool": "🤖 أداة التحريك الذكية:",
        "t4_tool_opts": ["Runway Gen-3 Alpha", "Luma Dream Machine", "OpenAI Sora Prompts", "Pika Labs v2.2", "HeyGen AI Avatar"],
        "t4_cam": "🎥 حركة الكاميرا الاحترافية:",
        "t4_cam_opts": ["زوم إن بطيء ودرامي (Slow Zoom In)", "زوم أوت للكشف عن المشهد", "بانوراما أفقية سريعة (Pan)", "تتبع حركي متقدم (Tracking Shot)", "لقطة دوران 360 درجة"],
        "t4_speed": "⚡ سرعة وتيرة الحركة:",
        "t4_speed_opts": ["بطيء جداً وسينمائي (Cinematic Slow-mo)", "سرعة عادية متوازنة", "حركة سريعة وخاطفة (Dynamic Fast)"],

        # تفاصيل التبويب 5
        "t5_head": "📊 المرحلة السادسة: الإعلانات والتسويق الرقمي",
        "t5_label": "🎯 المنتج أو الخدمة المراد تسويقها:",
        "t5_ph": "اكتب تفاصيل المنتج والجمهور المستهدف...",
        "t5_plat": "📱 المنصة الإعلانية المستهدفة:",
        "t5_plat_opts": ["TikTok Ads Manager", "Meta Ads (Instagram/Facebook)", "YouTube Video Ads", "LinkedIn B2B Ads", "Google Search Ads"],
        "t5_goal": "🎯 الهدف التسويقي (Campaign Objective):",
        "t5_goal_opts": ["مبيعات مباشرة وإيرادات (Conversions)", "وعي عالي بالعلامة التجارية (Awareness)", "توليد عملاء محتملين (Lead Generation)", "زيارات وزيارات للموقع (Traffic)"],
        "t5_strategy": "💡 استراتيجية المحتوى الإعلاني:",
        "t5_strategy_opts": ["قصة العميل (UGC Style)", "إثبات اجتماعي ومراجعات", "عرض خصم لفترة محدودة", "مقارنة تنافسية مباشرة"],
        "t5_budget": "💰 الميزانية الشهرية المقترحة ($):"
    },
    "English": {
        "sidebar_title": "💎 Enterprise Control",
        "search_label": "🔍 Search Archive:",
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
            "0️⃣ Strategy",
            "1️⃣ Scripts & Video",
            "2️⃣ Music & Audio",
            "3️⃣ Visual Engineering",
            "4️⃣ Motion Cinema",
            "5️⃣ Mega Campaigns"
        ],
        
        "d_title": "Welcome to Next-Gen Command Center",
        "d_sub": "Empowering global agencies and enterprises with state-of-the-art AI content generation workflows.",
        
        # English Command Center Guide
        "d_desc_title": "💡 What is 'Ibda3 Enterprise' and How Does it Revolutionize Your Business?",
        "d_desc_text": "This platform is an all-in-one software ecosystem custom-built for major corporations, marketing agencies, and professional content creators targeting exceptional quality and massive ROI. We integrate state-of-the-art AI models (like Gemini 1.5) to deliver:",
        "d_feat_1": "🎯 **Advanced Strategic Planning:** Business model canvases, feasibility studies, and startup roadmaps.",
        "d_feat_2": "🎬 **Viral Scripts Studio:** Social media content generation (TikTok, Reels, YouTube) with precise tonal control.",
        "d_feat_3": "🎵 **Music & Audio Production:** Song lyrics and sonic branding crafted with professional cultural nuances.",
        "d_feat_4": "🎨 **Visual Engineering:** Tailored prompts for top image engines (Midjourney, Flux) with cinematic framing.",
        "d_feat_5": "📊 **Mega Ad Campaigns:** Structuring massive budgets and precise targeting for peak conversions.",
        
        "btn_gen": "⚡ Execute Intelligent Production",
        "warn": "⚠️ Please enter required details first!",
        "spin": "⚡ Processing via Advanced LLM Cluster...",
        "res_title": "🚀 Verified AI Output:",
        "download": "📥 Export Professional Report (.txt)",
        "rate": "⭐ Rate Output Quality:",

        # Tab 0 En
        "t0_head": "Phase 1: Advanced Strategy",
        "t0_label": "Core Project/Startup Idea:",
        "t0_ph": "Enter investment project details...",
        "t0_goal": "Strategic Goal:",
        "t0_goal_opts": ["Startup Launch", "Major Campaign", "EdTech / Podcast", "Brand Rebranding", "E-commerce Scale"],
        "t0_meth": "Methodology:",
        "t0_meth_opts": ["Business Model Canvas", "Lean Startup", "SWOT & Competitor Analysis", "OKRs Growth Plan"],
        "t0_market": "Target Market:",
        "t0_market_opts": ["Egypt & North Africa", "GCC Countries", "MENA Region", "Global (English)"],

        # Tab 1 En
        "t1_head": "Phase 2: Professional Scripts Studio",
        "t1_label": "Video Idea or Core Topic:",
        "t1_ph": "Enter video concept briefly...",
        "t1_dur": "Video Duration:",
        "t1_dur_opts": ["15s (Reels/Shorts)", "30s (Fast Hook)", "60s (TikTok Pro)", "3m (YouTube Deep)", "10m (Masterclass)"],
        "t1_style": "Visual Style:",
        "t1_style_opts": ["Cinematic Realistic", "Investigative Documentary", "Edutainment", "Light Comedy", "Emotional Drama", "Tech Geek"],
        "t1_tone": "Vocal Tone:",
        "t1_tone_opts": ["Energetic & Motivated", "Calm & Trustworthy", "Mystery & Suspense", "Inspirational", "Sarcastic & Witty"],
        "t1_target": "Target Audience:",
        "t1_target_opts": ["Gen Z", "Entrepreneurs & Investors", "Professionals & Employees", "Families & Homemakers", "Tech Enthusiasts"],

        # Tab 2 En
        "t2_head": "Phase 3: Advanced Music Studio",
        "t2_label": "Song Theme or Core Message:",
        "t2_ph": "Enter lyrics theme or story...",
        "t2_dialect": "Cultural Flavor / Dialect:",
        "t2_dialect_opts": ["Modern Egyptian Slang", "Formal Classical Arabic", "Gulf Tarab", "Warm Levantine", "Global Pop English"],
        "t2_genre": "Music Genre:",
        "t2_genre_opts": ["Modern Mahraganat", "Hip Hop / Trap", "Chill Pop", "Dramatic Rock", "Epic Soundtrack"],
        "t2_vocal": "Vocal Style:",
        "t2_vocal_opts": ["Deep Bass / Baritone", "High Energy Youth", "Warm & Soft Female", "Group Choir", "Modern Autotune"],
        "t2_inst": "Prominent Instruments:",
        "t2_inst_opts": ["Heavy Electronic Beats", "Acoustic Guitar", "Oriental Oud & Percussion", "Dramatic Classical Piano"],

        # Tab 3 En
        "t3_head": "Phase 4: Visual Identity & Image Engineering",
        "t3_label": "Precise Scene Description:",
        "t3_ph": "Describe elements, colors, and background...",
        "t3_engine": "Target AI Engine:",
        "t3_engine_opts": ["Midjourney v6.0", "Flux.1 Dev/Pro", "DALL-E 3 Ultra", "Adobe Firefly v3", "Stable Diffusion XL"],
        "t3_aspect": "Aspect Ratio:",
        "t3_aspect_opts": ["9:16 (Stories / Reels / TikTok)", "16:9 (YouTube Cinematic)", "1:1 (Instagram Square)", "4:5 (Instagram Portrait)", "21:9 (Ultra Wide Cinema)"],
        "t3_light": "Lighting & Effects:",
        "t3_light_opts": ["Studio Lighting", "Dark Cyberpunk Neon", "Golden Hour", "Moody Dramatic", "Clean Commercial Lighting"],
        "t3_shot": "Camera Shot:",
        "t3_shot_opts": ["Macro / Close-up", "Bird's Eye View", "Low Angle Power Shot", "Wide Professional Portrait"],

        # Tab 4 En
        "t4_head": "Phase 5: Video Motion Cinema",
        "t4_label": "Required Motion & Animation Description:",
        "t4_ph": "Describe camera or element movement...",
        "t4_tool": "Smart Motion Tool:",
        "t4_tool_opts": ["Runway Gen-3 Alpha", "Luma Dream Machine", "OpenAI Sora Prompts", "Pika Labs v2.2", "HeyGen AI Avatar"],
        "t4_cam": "Professional Camera Movement:",
        "t4_cam_opts": ["Slow Zoom In", "Zoom Out Reveal", "Fast Pan", "Advanced Tracking Shot", "360 Degree Rotation"],
        "t4_speed": "Motion Speed:",
        "t4_speed_opts": ["Cinematic Slow-mo", "Balanced Normal Speed", "Dynamic Fast Motion"],

        # Tab 5 En
        "t5_head": "Phase 6: Advanced Mega Marketing Campaigns",
        "t5_label": "Product or Service to Market:",
        "t5_ph": "Enter product details and target audience...",
        "t5_plat": "Target Ad Platform:",
        "t5_plat_opts": ["TikTok Ads Manager", "Meta Ads (Instagram/Facebook)", "YouTube Video Ads", "LinkedIn B2B Ads", "Google Search Ads"],
        "t5_goal": "Campaign Objective:",
        "t5_goal_opts": ["Conversions", "Brand Awareness", "Lead Generation", "Traffic"],
        "t5_strategy": "Ad Strategy:",
        "t5_strategy_opts": ["UGC Style", "Social Proof & Reviews", "Limited Time Offer", "Direct Competitor Comparison"],
        "t5_budget": "Suggested Monthly Budget ($):"
    }
}

# ==========================================
# 4. محرك استدعاء الذكاء الاصطناعي المؤسسي
# ==========================================
def call_gemini_enterprise(prompt, lang_choice):
    if not API_KEY:
        return "❌ الخطأ: مفتاح API غير موجود في إعدادات المنصة (Streamlit Secrets)."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    sys_inst = f"You are an elite enterprise AI Architect for 'Ibda3 Enterprise Suite', producing world-class, exhaustive, highly professional business and creative assets. Language: {lang_choice}."
    payload = {"contents": [{"role": "user", "parts": [{"text": sys_inst + "\n\n" + prompt}]}]}
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"❌ خطأ في الاتصال: {r.status_code}"
    except Exception as e:
        return f"❌ خطأ تقني: {str(e)}"

# ==========================================
# 5. الشريط الجانبي وتغيير اللغة الفوري
# ==========================================
with str_lit.sidebar:
    selected_lang = str_lit.radio("🌐 Language / اللغة:", ["العربية", "English"], horizontal=True)
    t = TEXTS[selected_lang]
    
    str_lit.markdown(f"### {t['sidebar_title']}")
    str_lit.markdown("---")
    
    str_lit.markdown(f"#### {t['stats_title']}")
    str_lit.metric(label=t["stat_total"], value=len(str_lit.session_state["history"]))
    str_lit.markdown("---")
    
    search_query = str_lit.text_input(t["search_label"], "")
    
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
# 6. الواجهة الرئيسية والتبويبات الكاملة بالتفاصيل
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
# تبويب 0: لوحة القيادة (Command Center) - مع الشرح التفصيلي العملاق
# ------------------------------------------
with tabs[0]:
    str_lit.markdown(f"""
    <div class="metric-card">
        <h2>{t['d_title']}</h2>
        <p style="font-size: 1.1rem; color: #94a3b8; margin-bottom: 20px;">{t['d_sub']}</p>
        
        <div class="feature-box">
            <h3 style="color: #818cf8; margin-bottom: 10px;">{t['d_desc_title']}</h3>
            <p style="line-height: 1.7; color: #cbd5e1;">{t['d_desc_text']}</p>
            <ul style="line-height: 1.8; color: #e2e8f0; margin-top: 10px; list-style-type: none; padding: 0;">
                <li>{t['d_feat_1']}</li>
                <li>{t['d_feat_2']}</li>
                <li>{t['d_feat_3']}</li>
                <li>{t['d_feat_4']}</li>
                <li>{t['d_feat_5']}</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = str_lit.columns(3)
    col1.metric("العمليات الناجحة / Operations", len(str_lit.session_state["history"]), "+100%")
    col2.metric("العناصر المفضلة / Favorites", len(str_lit.session_state["favorites"]), "Secure")
    col3.metric("الذكاء الاصطناعي / AI Status", "Active", "Gemini 1.5 Cluster")

# ------------------------------------------
# تبويب 1: التخطيط الاستراتيجي
# ------------------------------------------
with tabs[1]:
    str_lit.subheader(t["t0_head"])
    str_lit.session_state["t0_v"] = str_lit.text_area(t["t0_label"], value=str_lit.session_state["t0_v"], placeholder=t["t0_ph"])
    c1, c2, c3 = str_lit.columns(3)
    goal_0 = c1.selectbox(t["t0_goal"], t["t0_goal_opts"])
    meth_0 = c2.selectbox(t["t0_meth"], t["t0_meth_opts"])
    market_0 = c3.selectbox(t["t0_market"], t["t0_market_opts"])
    
    if str_lit.button(t["btn_gen"], key="b0"):
        if not str_lit.session_state["t0_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Advanced Strategic plan for project: '{str_lit.session_state['t0_v']}'. Goal: {goal_0}, Methodology: {meth_0}, Market: {market_0}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Strategic Planning", str_lit.session_state["t0_v"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 2: السكريبتات والفيديو
# ------------------------------------------
with tabs[2]:
    str_lit.subheader(t["t1_head"])
    str_lit.session_state["t1_v"] = str_lit.text_area(t["t1_label"], value=str_lit.session_state["t1_v"], placeholder=t["t1_ph"])
    c1, c2, c3, c4 = str_lit.columns(4)
    dur = c1.selectbox(t["t1_dur"], t["t1_dur_opts"])
    style = c2.selectbox(t["t1_style"], t["t1_style_opts"])
    tone = c3.selectbox(t["t1_tone"], t["t1_tone_opts"])
    target = c4.selectbox(t["t1_target"], t["t1_target_opts"])
    
    if str_lit.button(t["btn_gen"], key="b1"):
        if not str_lit.session_state["t1_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Pro Video Script for: '{str_lit.session_state['t1_v']}', Duration: {dur}, Style: {style}, Tone: {tone}, Target: {target}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Scripts Studio", str_lit.session_state["t1_v"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 3: الأغاني والصوت المتطور
# ------------------------------------------
with tabs[3]:
    str_lit.subheader(t["t2_head"])
    str_lit.session_state["t2_v"] = str_lit.text_area(t["t2_label"], value=str_lit.session_state["t2_v"], placeholder=t["t2_ph"])
    c1, c2, c3, c4 = str_lit.columns(4)
    dialect = c1.selectbox(t["t2_dialect"], t["t2_dialect_opts"])
    genre = c2.selectbox(t["t2_genre"], t["t2_genre_opts"])
    vocal = c3.selectbox(t["t2_vocal"], t["t2_vocal_opts"])
    inst = c4.selectbox(t["t2_inst"], t["t2_inst_opts"])
    
    if str_lit.button(t["btn_gen"], key="b2"):
        if not str_lit.session_state["t2_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Pro Song Lyrics and Music Production Guide for: '{str_lit.session_state['t2_v']}', Dialect: {dialect}, Genre: {genre}, Vocal: {vocal}, Instruments: {inst}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Music Studio", str_lit.session_state["t2_v"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 4: هندسة الصور والهوية
# ------------------------------------------
with tabs[4]:
    str_lit.subheader(t["t3_head"])
    str_lit.session_state["t3_v"] = str_lit.text_area(t["t3_label"], value=str_lit.session_state["t3_v"], placeholder=t["t3_ph"])
    c1, c2, c3, c4 = str_lit.columns(4)
    engine = c1.selectbox(t["t3_engine"], t["t3_engine_opts"])
    aspect = c2.selectbox(t["t3_aspect"], t["t3_aspect_opts"])
    light = c3.selectbox(t["t3_light"], t["t3_light_opts"])
    shot = c4.selectbox(t["t3_shot"], t["t3_shot_opts"])
    
    if str_lit.button(t["btn_gen"], key="b3"):
        if not str_lit.session_state["t3_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Advanced Image Generation Prompts for: '{str_lit.session_state['t3_v']}', Engine: {engine}, Aspect Ratio: {aspect}, Lighting: {light}, Shot: {shot}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Visual Engineering", str_lit.session_state["t3_v"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 5: تحريك الموشن والفيديو
# ------------------------------------------
with tabs[5]:
    str_lit.subheader(t["t4_head"])
    str_lit.session_state["t4_v"] = str_lit.text_area(t["t4_label"], value=str_lit.session_state["t4_v"], placeholder=t["t4_ph"])
    c1, c2, c3 = str_lit.columns(3)
    tool = c1.selectbox(t["t4_tool"], t["t4_tool_opts"])
    cam = c2.selectbox(t["t4_cam"], t["t4_cam_opts"])
    speed = c3.selectbox(t["t4_speed"], t["t4_speed_opts"])
    
    if str_lit.button(t["btn_gen"], key="b4"):
        if not str_lit.session_state["t4_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Pro Video Motion Prompts for: '{str_lit.session_state['t4_v']}', Tool: {tool}, Camera: {cam}, Speed: {speed}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Motion Cinema", str_lit.session_state["t4_v"], res)
                str_lit.success("تم بنجاح!")

# ------------------------------------------
# تبويب 6: الإعلانات والتسويق
# ------------------------------------------
with tabs[6]:
    str_lit.subheader(t["t5_head"])
    str_lit.session_state["t5_v"] = str_lit.text_area(t["t5_label"], value=str_lit.session_state["t5_v"], placeholder=t["t5_ph"])
    c1, c2, c3, c4 = str_lit.columns(4)
    plat = c1.selectbox(t["t5_plat"], t["t5_plat_opts"])
    goal = c2.selectbox(t["t5_goal"], t["t5_goal_opts"])
    strategy = c3.selectbox(t["t5_strategy"], t["t5_strategy_opts"])
    budget = c4.number_input(t["t5_budget"], min_value=50, max_value=500000, value=2500, step=100)
    
    if str_lit.button(t["btn_gen"], key="b5"):
        if not str_lit.session_state["t5_v"].strip(): str_lit.warning(t["warn"])
        else:
            with str_lit.spinner(t["spin"]):
                prompt = f"Mega Ad Campaign for: '{str_lit.session_state['t5_v']}', Platform: {plat}, Objective: {goal}, Strategy: {strategy}, Budget: ${budget}."
                res = call_gemini_enterprise(prompt, selected_lang)
                log_and_store("Mega Campaigns", str_lit.session_state["t5_v"], res)
                str_lit.success("تم بنجاح!")

# ==========================================
# 7. قسم النتائج والتصدير
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
