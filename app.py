import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم الجذاب المطور
# ==========================================
st.set_page_config(
    page_title="Smart Content Studio - Ultimate Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* خلفية متدرجة وجذابة للتطبيق بالكامل */
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #0f172a 100%);
        color: #f1f5f9;
    }
    
    /* القائمة الجانبية بتدرج وتصميم فخم */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
    }

    /* تحسين الأزرار الرئيسية لتكون نابضة بالحياة */
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
        box-shadow: 0 6px 20px rgba(96, 165, 250, 0.6);
    }

    /* حقول الإدخال والـ Textarea بتصميم أزرق خفيف وواضح */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #f8fafc !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5) !important;
    }

    /* عناوين التبويبات والمكونات */
    h1, h2, h3 {
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم الفوري
# ==========================================
HISTORY_FILE = "content_studio_ultimate_v3_history.json"
FAV_FILE = "content_studio_ultimate_v3_favorites.json"

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

for k in ["t1_val", "t2_val", "t3_val", "t4_val", "t5_val"]:
    if k not in st.session_state:
        st.session_state[k] = ""

# ==========================================
# 2. القاموس الشامل للغتين (Arabic & English)
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚙️ الإدارة والتحكم الشامل",
        "search_label": "🔍 بحث في السجل:",
        "fav_title": "⭐ المفضلة المحفوظة",
        "fav_empty": "لا توجد عناصر مفضلة",
        "history_title": "📜 سجل العمليات (حفظ دائم)",
        "history_empty": "السجل فارغ حالياً",
        "clear_history": "🗑️ مسح السجل بالكامل",
        "stats_title": "📊 لوحة الإحصائيات",
        "stat_total": "إجمالي الأعمال المُنجزة:",
        "main_title": "🎙️ استوديو المحتوى الذكي (Ultimate Pro Suite)",
        "main_caption": "منظومة إبداعية احترافية بالكامل مع تعريب وترجمة كل العناصر فورياً",
        
        "tabs": [
            "1️⃣ 💡 الفكرة والسكريبت والخطافات",
            "2️⃣ 🎵 أستديو الأغاني والصوت الاحترافي",
            "3️⃣ 🎨 مهندس الصور والريزوليوشن القياسي",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار المتقدم",
            "5️⃣ 📊 التسويق وخطط المحتوى الاستراتيجية"
        ],
        
        # Tab 1
        "t1_header": "🎬 صانع الفكرة، السكريبت التفصيلي، والـ Hook Generator الاحترافي",
        "t1_input_label": "📽️ عنوان أو فكرة الفيديو الأساسية:",
        "t1_input_placeholder": "اكتب فكرة الفيديو أو املِها بالمايك...",
        "t1_dur": "⏱️ مدة الفيديو التقديرية:",
        "t1_dur_opts": ["15 ثانية (Shorts/Reels)", "30 ثانية", "60 ثانية (TikTok/Reels)", "3 دقائق (YouTube Standard)", "10+ دقائق (Documentary/Long)"],
        "t1_style": "🎨 النمط البصري والإلقائي:",
        "t1_style_opts": ["سينمائي واقعي (Cinematic)", "وثائقي تشويقي (Documentary)", "كوميدي ساخر (Sarcastic/Comedy)", "تعليمي تفاعلي (Educational)", "حماسي تحفيزي (Motivational)"],
        "t1_target": "🎯 الجمهور المستهدف:",
        "t1_target_opts": ["الشباب والمراهقين (Gen Z)", "رواد الأعمال والمهنيين", "العامة والمهتمين بالترفيه", "الأطفال والعائلات"],
        "t1_btn": "🔥 تنفيذ وتوليد السكريبت والخطافات",
        "t1_warn": "⚠️ يرجى إدخال عنوان أو فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ توليد سكريبت احترافي وخطافات فيرال...",

        # Tab 2
        "t2_header": "🎵 صناعة الأغاني، الهندسة الصوتية، ومكتبة القوافي المتقدمة",
        "t2_input_label": "💡 فكرة الأغنية أو الموضوع الرئيسي:",
        "t2_input_placeholder": "اكتب موضوع الأغنية أو تفاصيل الكلمات المطلوبة...",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_dialect_opts": ["عامية مصرية عصرية", "فصحى بلاغية", "خليجي طربي", "مغربي / شمال إفريقي", "إنجليزي غربي (English)"],
        "t2_style": "🎼 النمط الموسيقي (Music Genre):",
        "t2_style_opts": ["مهرجانات / شعبي سريع (Mahraganat)", "راب / هيب هوب أندرجراوند (Rap/Hip-Hop)", "بوب عربي رومانسي (Pop)", "أكوستيك هادئ جيتار (Acoustic)", "إي دي إم إلكتروني راقص (EDM/Dance)", "لوفي تشิล هادئ (Lo-Fi Beats)"],
        "t2_vocal": "🎙️ صوت المغني والأداء (Vocal Profile):",
        "t2_vocal_opts": ["صوت رجالي قوي وعميق (Deep Baritone)", "صوت شبابي حماسي ومرن (Energetic Tenor)", "صوت نسائي ناعم ودافئ (Warm Soprano)", "صوت روبوتي مدمج أوتوتيون (Auto-Tune / Robotic)", "جوقة جماعية حماسية (Choir/Harmonies)"],
        "t2_btn": "✨ تنفيذ وتوليد الأغنية الكاملة والقوافي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات، هندسة المكس، وتحديد البرومبتات الصوتية...",

        # Tab 3
        "t3_header": "🎨 مهندس برومبتات الصور الاحترافية مع تحديد المقاسات والمنصات",
        "t3_input_label": "🖼️ وصف الصورة الخيالية أو المشهد بدقة:",
        "t3_input_placeholder": "صف تفاصيل الصورة والألوان والإضاءة بدقة...",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي للصور:",
        "t3_engine_opts": ["Midjourney v6 (أعلى جودة وسينمائية)", "Flux.1 (واقعية مذهلة وتفاصيل دقيقة)", "DALL-E 3 (فهم عميق للنصوص)", "Stable Diffusion XL (تحكم حر كامل)"],
        "t3_aspect": "📐 الأبعاد والريزوليوشن المناسب للمنصة:",
        "t3_aspect_opts": [
            "9:16 (مناسب لـ TikTok / YouTube Shorts / Instagram Reels)", 
            "16:9 (مناسب لـ YouTube Videos / Desktop Wallpaper)", 
            "1:1 (مناسب لـ Instagram / Facebook Post)", 
            "4:5 (مناسب لـ Portrait Feed / IG Carousel)", 
            "21:9 (مناسب لـ Ultra-Wide Cinematic Banners)"
        ],
        "t3_light": "💡 نمط الإضاءة والجودة:",
        "t3_light_opts": [
            "إضاءة استوديو سينمائية (Cinematic Studio Lighting)", 
            "إضاءة نيون سايبربانك (Cyberpunk Neon Glow)", 
            "إضاءة شمس طبيعية ساحرة (Golden Hour Natural)", 
            "مظلم درامي غامض (Dark Moody Atmosphere)", 
            "ألوان زاهية نابضة بالحياة (Vibrant & Pop Art)"
        ],
        "t3_btn": "🎨 تنفيذ وتوليد برومبتات الصور الاحترافية",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة المطلوب!",
        "t3_spin": "⚡ جارٍ هندسة الأوامر وتجهيز المقاسات المخصصة...",

        # Tab 4
        "t4_header": "🗣️ محرك الفيديو، الأفاتار، وتحويل الصور لحركة (Motion Prompts)",
        "t4_input_label": "📜 النص الإلقائي أو وصف الحركة البصرية:",
        "t4_input_placeholder": "اكتب النص أو تفاصيل الحركة المطلوبة للكاميرا والأفاتار...",
        "t4_tool": "🤖 أداة التحريك والأفاتار المستهدفة:",
        "t4_tool_opts": ["Runway Gen-3 (حركة سينمائية واقعية)", "Luma Dream Machine (حركات ديناميكية سريعة)", "HeyGen Avatar (أفاتار ناطق احترافي)", "Pika Labs (تأثيرات بصرية وموشن جرافيك)"],
        "t4_cam": "🎥 حركة الكاميرا (Camera Movement):",
        "t4_cam_opts": ["زوم إن بطيء (Slow Zoom In)", "حركة بانورامية جانبية (Pan Right/Left)", "تتبع الحركة (Dynamic Tracking Shot)", "لقطة ثابتة مع تفاصيل حية (Static with Ambient Motion)"],
        "t4_btn": "⚡ تنفيذ برومبتات التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أو الحركة أولاً!",
        "t4_spin": "⚡ جارٍ إعداد أوامر الحركة المتقدمة...",

        # Tab 5
        "t5_header": "📊 استوديو التسويق، خطط المحتوى، والتريندات الاستراتيجية",
        "t5_input_label": "🎯 موضوع المحتوى أو المنتج المراد تسويقه:",
        "t5_input_placeholder": "اكتب تفاصيل المنتج أو المشروع المراد وضع خطة له...",
        "t5_plat": "📱 المنصة المستهدفة للنشر:",
        "t5_plat_opts": ["TikTok (تريندات وفيديوهات قصيرة سريعة)", "Instagram Reels & Stories (بناء براند وبصريات)", "YouTube Shorts & Long (محتوى تعليمي وترفيهي متكامل)", "LinkedIn (تسويق احترافي وبزنس)", "Facebook Community (تفاعل جماهيري واسع)"],
        "t5_goal": "🎯 هدف الحملة التسويقية:",
        "t5_goal_opts": ["زيادة المبيعات والتحويلات (Sales Conversion)", "بناء الوعي بالعلامة التجارية (Brand Awareness)", "زيادة التفاعل والمشاركات (Engagement & Shares)", "جذب زيارات للموقع أو القناة (Traffic Generation)"],
        "t5_btn": "🚀 تنفيذ الخطة التسويقية والتريند",
        "t5_warn": "⚠️ يرجى إدخال موضوع المحتوى أولاً!",
        "t5_spin": "⚡ جارٍ تحليل السوق، وضع استراتيجية النشر واستخراج الهاشتاجات...",

        # General Result UI
        "result_label": "🚀 النتيجة الفورية المنجزة:",
        "copy_btn": "📋 نسخ النص للحافظة",
        "download_txt": "📥 تحميل كملف نصي (.txt)",
        "rating_label": "⭐ تقييم جودة النتيجة:",
        "stats_res": "📊 إحصائيات الناتج:"
    },
    "English": {
        "sidebar_title": "⚙️ Control Panel",
        "search_label": "🔍 Search History:",
        "fav_title": "⭐ Favorites",
        "fav_empty": "No favorites added yet",
        "history_title": "📜 History Log",
        "history_empty": "History is empty",
        "clear_history": "🗑️ Clear History",
        "stats_title": "📊 Live Metrics",
        "stat_total": "Total Executions:",
        "main_title": "🎙️ Smart Content Studio (Ultimate Pro Suite)",
        "main_caption": "Expanded professional AI suite with full bilingual localization & rich custom options",
        
        "tabs": [
            "1️⃣ 💡 Ideas, Scripts & Hooks",
            "2️⃣ 🎵 Pro Suno Music & Audio",
            "3️⃣ 🎨 Image Prompts & Resolutions",
            "4️⃣ 🗣️ Advanced Video & Avatar",
            "5️⃣ 📊 Marketing & Strategies"
        ],
        
        # Tab 1
        "t1_header": "🎬 Idea Generator, Script, & Viral Hooks",
        "t1_input_label": "📽️ Video Title or Core Idea:",
        "t1_input_placeholder": "Enter video idea or use continuous mic...",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_dur_opts": ["15 Seconds (Shorts/Reels)", "30 Seconds", "60 Seconds (TikTok/Reels)", "3 Minutes (YouTube Standard)", "10+ Minutes (Documentary/Long)"],
        "t1_style": "🎨 Visual & Delivery Style:",
        "t1_style_opts": ["Cinematic Realism", "Documentary & Suspense", "Sarcastic / Comedy", "Educational & Interactive", "Motivational & High-Energy"],
        "t1_target": "🎯 Target Audience:",
        "t1_target_opts": ["Gen Z & Youth", "Entrepreneurs & Professionals", "General Entertainment", "Families & Kids"],
        "t1_btn": "🔥 Execute Script & Hooks",
        "t1_warn": "⚠️ Please enter video title or idea first!",
        "t1_spin": "⚡ Generating professional script & viral hooks...",

        # Tab 2
        "t2_header": "🎵 Music Production & Advanced Sound Engineering",
        "t2_input_label": "💡 Song Idea or Main Theme:",
        "t2_input_placeholder": "Enter song theme or lyrics details...",
        "t2_dialect": "🗣️ Dialect / Cultural Flavor:",
        "t2_dialect_opts": ["Modern Egyptian Slang", "Classical Arabic (Fusha)", "Khaleeji Traditional", "North African / Moroccan", "Western English"],
        "t2_style": "🎼 Music Genre:",
        "t2_style_opts": ["Fast Mahraganat / Street", "Underground Rap / Hip-Hop", "Romantic Arabic Pop", "Acoustic Guitar", "EDM / Dance", "Lo-Fi Beats"],
        "t2_vocal": "🎙️ Vocal Profile & Performance:",
        "t2_vocal_opts": ["Deep Baritone Male", "Energetic Tenor", "Warm Female Soprano", "Auto-Tune / Robotic", "Group Choir / Harmonies"],
        "t2_btn": "✨ Execute Full Song & Rhymes",
        "t2_warn": "⚠️ Please enter the song idea first!",
        "t2_spin": "⚡ Crafting lyrics, mix layout, and audio prompt tags...",

        # Tab 3
        "t3_header": "🎨 Pro Image Prompt Engineer with Resolutions & Platforms",
        "t3_input_label": "🖼️ Describe your imagined image or scene:",
        "t3_input_placeholder": "Describe precise details, colors, and lighting...",
        "t3_engine": "🎯 AI Image Engine:",
        "t3_engine_opts": ["Midjourney v6 (Highest Cinematic Quality)", "Flux.1 (Stunning Realism & Details)", "DALL-E 3 (Deep Prompt Understanding)", "Stable Diffusion XL (Full Control)"],
        "t3_aspect": "📐 Aspect Ratio & Platform Resolution:",
        "t3_aspect_opts": [
            "9:16 (Best for TikTok / YouTube Shorts / Instagram Reels)", 
            "16:9 (Best for YouTube Videos / Desktop Wallpaper)", 
            "1:1 (Best for Instagram / Facebook Post)", 
            "4:5 (Best for Portrait Feed / IG Carousel)", 
            "21:9 (Best for Ultra-Wide Cinematic Banners)"
        ],
        "t3_light": "💡 Lighting & Atmosphere:",
        "t3_light_opts": [
            "Cinematic Studio Lighting", 
            "Cyberpunk Neon Glow", 
            "Golden Hour Natural Sunlight", 
            "Dark Moody Atmosphere", 
            "Vibrant & Pop Art"
        ],
        "t3_btn": "🎨 Execute Pro Image Prompts",
        "t3_warn": "⚠️ Please enter image description first!",
        "t3_spin": "⚡ Engineering visual prompts & custom resolutions...",

        # Tab 4
        "t4_header": "🗣️ Video Engine, Avatar & Motion Prompts",
        "t4_input_label": "📜 Voiceover Text or Visual Motion Description:",
        "t4_input_placeholder": "Enter text or specific camera/avatar motion details...",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_tool_opts": ["Runway Gen-3 (Cinematic Motion)", "Luma Dream Machine (Dynamic Motion)", "HeyGen Avatar (Speaking Professional Avatar)", "Pika Labs (VFX & Motion Graphics)"],
        "t4_cam": "🎥 Camera Movement:",
        "t4_cam_opts": ["Slow Zoom In", "Pan Right/Left", "Dynamic Tracking Shot", "Static with Ambient Motion"],
        "t4_btn": "⚡ Execute Motion Prompts",
        "t4_warn": "⚠️ Please enter text or motion description first!",
        "t4_spin": "⚡ Preparing advanced motion commands...",

        # Tab 5
        "t5_header": "📊 Marketing Studio, Content Plans & Strategies",
        "t5_input_label": "🎯 Content Topic or Product to Market:",
        "t5_input_placeholder": "Enter product details or project marketing scope...",
        "t5_plat": "📱 Target Publishing Platform:",
        "t5_plat_opts": ["TikTok (Trends & Short Videos)", "Instagram Reels & Stories (Brand Building)", "YouTube Shorts & Long (Educational & Entertainment)", "LinkedIn (Professional Business)", "Facebook Community (Mass Audience Engagement)"],
        "t5_goal": "🎯 Marketing Campaign Goal:",
        "t5_goal_opts": ["Sales Conversion", "Brand Awareness", "Engagement & Shares", "Traffic Generation"],
        "t5_btn": "🚀 Execute Marketing Plan & Trend",
        "t5_warn": "⚠️ Please enter content topic first!",
        "t5_spin": "⚡ Analyzing market strategy, content calendar, and hashtags...",

        # General Result UI
        "result_label": "🚀 Executed Result:",
        "copy_btn": "📋 Copy Text",
        "download_txt": "📥 Download (.txt)",
        "rating_label": "⭐ Rate Result:",
        "stats_res": "📊 Output Stats:"
    }
}

# ==========================================
# 3. دالة الإدخال الصوتي المتطورة
# ==========================================
def floating_voice_textarea(label, session_key, placeholder):
    val = st.text_area(label, value=st.session_state.get(session_key, ""), key=session_key, height=120, placeholder=placeholder)
    
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
                    micDiv.style.cssText = "position: absolute; bottom: 12px; right: 12px; display: flex; align-items: center; gap: 8px; z-index: 999;";
                    
                    micDiv.innerHTML = `
                        <div id="waves_{session_key}" style="display: none; align-items: center; gap: 3px; height: 16px; background: rgba(0,0,0,0.7); padding: 2px 8px; border-radius: 12px;">
                            <div style="width: 3px; background: #ff4b4b; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out;"></div>
                            <div style="width: 3px; background: #ff4b4b; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.15s;"></div>
                            <div style="width: 3px; background: #ff4b4b; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.3s;"></div>
                        </div>
                        <button type="button" id="mic_btn_{session_key}" title="Mic" style="background: #1e293b; border: 1px solid #3b82f6; color: #60a5fa; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s;">
                            🎙️
                        </button>
                        <button type="button" id="stop_btn_{session_key}" title="Stop" style="background: #1e293b; border: 1px solid #f85149; color: #f85149; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; display: none; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s;">
                            ⏹️
                        </button>
                    `;
                    
                    if (!doc.getElementById('wave-style-global')) {{
                        const style = doc.createElement('style');
                        style.id = 'wave-style-global';
                        style.innerHTML = '@keyframes waveA {{ 0%, 100% {{ height: 4px; }} 50% {{ height: 16px; }} }}';
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
                            btn.style.borderColor = '#ff7b72';
                            btn.style.transform = 'scale(1.1)';
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

                        try {{ recognition.start(); }} catch(err) {{ console.log(err); }}
                    }}

                    function stopRecordingProcess() {{
                        isRec = false;
                        if (recognition) {{
                            try {{ recognition.stop(); }} catch(e) {{}}
                        }}
                        btn.style.background = '#1e293b';
                        btn.style.color = '#60a5fa';
                        btn.style.borderColor = '#3b82f6';
                        btn.style.transform = 'scale(1.0)';
                        stopBtn.style.display = 'none';
                        waves.style.display = 'none';

                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        ta.blur();
                        ta.focus();
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
    st.components.v1.html(js_code, height=0, width=0)
    return st.session_state.get(session_key, "")

# ==========================================
# 4. دالة تنفيذ وتخزين العمليات الفورية
# ==========================================
def execute_ai_action(prompt_text, category_name="General", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ GEMINI_API_KEY is missing in Secrets!")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
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
                "prompt": prompt_text,
                "result": output_text,
                "tab_index": tab_index,
                "rating": 5
            }
            
            st.session_state["history"].insert(0, item)
            save_data(HISTORY_FILE, st.session_state["history"])
            st.session_state["current_result"] = item
            return output_text
        else:
            error_msg = res_data.get('error', {}).get('message', 'Unknown error')
            st.error(f"❌ Server Error: {error_msg}")
            return None
    except Exception as e:
        st.error(f"❌ Connection Error: {str(e)}")
        return None

# ==========================================
# 5. القائمة الجانبية (Sidebar)
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

    if not st.session_state["history"]:
        st.caption(T["history_empty"])
    else:
        filtered = [
            item for item in st.session_state["history"]
            if search_query.lower() in item["topic"].lower() or search_query.lower() in item["category"].lower() or search_query.lower() in item["result"].lower()
        ] if search_query else st.session_state["history"]

        for item in filtered:
            c1, c2 = st.columns([3, 1])
            with c1:
                if st.button(f"📌 {item['topic'][:18]}", key=f"hist_{item['id']}"):
                    st.session_state["current_result"] = item
                    st.session_state["selected_tab"] = item["tab_index"]
                    st.rerun()
            with c2:
                if st.button("⭐", key=f"fav_btn_{item['id']}"):
                    if item not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item)
                        save_data(FAV_FILE, st.session_state["favorites"])
                        st.toast("Saved to Favorites!" if lang == "English" else "تمت الإضافة للمفضلة!")

# ==========================================
# 6. الواجهة الرئيسية والتبويبات
# ==========================================
st.title(T["main_title"])
st.caption(T["main_caption"])
st.divider()

selected_tab_name = st.radio(
    "Navigation" if lang == "English" else "اختر مرحلة العمل الإبداعي:",
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
        
        word_count = len(res["result"].split())
        char_count = len(res["result"])
        st.info(f"{T['stats_res']} {word_count} words | {char_count} chars")
        
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            if st.button(T["copy_btn"], key=f"cp_{res['id']}_{tab_idx}"):
                st.toast("Copied successfully!" if lang == "English" else "تم النسخ بنجاح!")
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

# ----------------------------------------------------
# 1️⃣ Ideas, Scripts & Hooks
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_header']}")
    v_title = floating_voice_textarea(T['t1_input_label'], "t1_val", T['t1_input_placeholder'])
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        v_duration = st.selectbox(T['t1_dur'], T['t1_dur_opts'])
    with col_b:
        v_style = st.selectbox(T['t1_style'], T['t1_style_opts'])
    with col_c:
        v_target = st.selectbox(T['t1_target'], T['t1_target_opts'])
    
    if st.button(T['t1_btn'], type="primary", key="action_btn_1"):
        if not v_title.strip():
            st.warning(T['t1_warn'])
        else:
            with st.spinner(T['t1_spin']):
                prompt = f"Create a professional script for '{v_title}', duration {v_duration}, style {v_style}, target audience {v_target}, with viral hooks for the first 3 seconds."
                execute_ai_action(prompt, category_name="Script", user_topic=v_title[:25], tab_index=0)
                st.rerun()

    render_active_result(0)

# ----------------------------------------------------
# 2️⃣ Pro Suno Music & Audio
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 1:
    st.markdown(f"### {T['t2_header']}")
    song_idea = floating_voice_textarea(T['t2_input_label'], "t2_val", T['t2_input_placeholder'])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        lyrics_dialect = st.selectbox(T['t2_dialect'], T['t2_dialect_opts'])
    with c2:
        song_style = st.selectbox(T['t2_style'], T['t2_style_opts'])
    with c3:
        vocal_type = st.selectbox(T['t2_vocal'], T['t2_vocal_opts'])

    if st.button(T['t2_btn'], type="primary", key="action_btn_2"):
        if not song_idea.strip():
            st.warning(T['t2_warn'])
        else:
            with st.spinner(T['t2_spin']):
                prompt = f"Create full song lyrics and structure, dialect: {lyrics_dialect}, style: {song_style}, vocal: {vocal_type}, for theme: '{song_idea}'. Include Suno tags."
                execute_ai_action(prompt, category_name="Music", user_topic=song_idea[:25], tab_index=1)
                st.rerun()

    render_active_result(1)

# ----------------------------------------------------
# 3️⃣ Image Prompts & Resolutions
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown(f"### {T['t3_header']}")
    img_desc = floating_voice_textarea(T['t3_input_label'], "t3_val", T['t3_input_placeholder'])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        img_engine = st.selectbox(T['t3_engine'], T['t3_engine_opts'])
    with c2:
        img_aspect = st.selectbox(T['t3_aspect'], T['t3_aspect_opts'])
    with c3:
        img_lighting = st.selectbox(T['t3_light'], T['t3_light_opts'])

    if st.button(T['t3_btn'], type="primary", key="action_btn_3"):
        if not img_desc.strip():
            st.warning(T['t3_warn'])
        else:
            with st.spinner(T['t3_spin']):
                prompt = f"Generate 3 pro image prompts for engine: {img_engine}, description: '{img_desc}', aspect ratio: {img_aspect}, lighting: {img_lighting}."
                execute_ai_action(prompt, category_name="Image", user_topic=img_desc[:25], tab_index=2)
                st.rerun()

    render_active_result(2)

# ----------------------------------------------------
# 4️⃣ Advanced Video & Avatar
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown(f"### {T['t4_header']}")
    a_script = floating_voice_textarea(T['t4_input_label'], "t4_val", T['t4_input_placeholder'])
    
    c1, c2 = st.columns(2)
    with c1:
        a_ai_tool = st.selectbox(T['t4_tool'], T['t4_tool_opts'])
    with c2:
        camera_motion = st.selectbox(T['t4_cam'], T['t4_cam_opts'])

    if st.button(T['t4_btn'], type="primary", key="action_btn_4"):
        if not a_script.strip():
            st.warning(T['t4_warn'])
        else:
            with st.spinner(T['t4_spin']):
                prompt = f"Motion prompts for tool: {a_ai_tool}, camera movement: {camera_motion}, based on: '{a_script}'."
                execute_ai_action(prompt, category_name="Animation", user_topic=a_script[:25], tab_index=3)
                st.rerun()

    render_active_result(3)

# ----------------------------------------------------
# 5️⃣ Marketing & Strategies
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown(f"### {T['t5_header']}")
    m_topic = floating_voice_textarea(T['t5_input_label'], "t5_val", T['t5_input_placeholder'])
    
    c1, c2 = st.columns(2)
    with c1:
        m_platform = st.selectbox(T['t5_plat'], T['t5_plat_opts'])
    with c2:
        m_goal = st.selectbox(T['t5_goal'], T['t5_goal_opts'])

    if st.button(T['t5_btn'], type="primary", key="action_btn_5"):
        if not m_topic.strip():
            st.warning(T['t5_warn'])
        else:
            with st.spinner(T['t5_spin']):
                prompt = f"Marketing strategy, content plan and viral hashtags for '{m_topic}' on platform '{m_platform}' with goal '{m_goal}'."
                execute_ai_action(prompt, category_name="Marketing", user_topic=m_topic[:25], tab_index=4)
                st.rerun()

    render_active_result(4)
