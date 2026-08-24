import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتهيئة الأساسية
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي الشامل",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = st.secrets.get("GEMINI_API_KEY")

if "history" not in st.session_state:
    st.session_state["history"] = []

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = 0

if "current_result" not in st.session_state:
    st.session_state["current_result"] = None

# ==========================================
# 2. القاموس الثنائي (عربي / English)
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚙️ الإعدادات والسجل",
        "lang_label": "🌐 لغة الواجهة:",
        "search_label": "🔍 بحث في السجل:",
        "fav_title": "⭐ المفضلة (Favorites)",
        "fav_empty": "لا توجد عناصر مضافة للمفضلة",
        "history_title": "📜 السجل الكامل (History)",
        "history_empty": "السجل فارغ حتى الآن",
        "main_title": "🎬 استوديو المحتوى الذكي الشامل",
        "main_caption": "منظومة احترافية مرتبة حسب مراحل صناعة المحتوى",
        
        # التبويبات
        "tabs": [
            "1️⃣ 💡 الفكرة والسكريبت",
            "2️⃣ 🎵 استوديو الأغاني والصوت",
            "3️⃣ 🎨 استوديو الصور والمؤثرات",
            "4️⃣ 🗣️ تحريك الصور والفيديو",
            "5️⃣ 📊 تسويق المحتوى والتريند"
        ],
        
        # التبويب 1
        "t1_title": "🎬 صانع الفكرة، السكريبت التفصيلي، والـ Storyboard",
        "t1_input": "📽️ عنوان أو فكرة الفيديو:",
        "t1_dur": "⏱️ مدة الفيديو التقديرية:",
        "t1_style": "🎨 النمط البصري:",
        "t1_btn": "🎬 توليد السكريبت والـ Storyboard",
        "t1_warn": "⚠️ يرجى إدخال عنوان الفيديو!",
        "t1_spin": "...جارٍ كتابة السكريبت",

        # التبويب 2
        "t2_title": "🎵 صناعة الأغاني، الهندسة الصوتية، والقوافي (Suno Pro Studio)",
        "t2_idea": "💡 فكرة الأغنية أو موضوعها:",
        "t2_struct": "🏗️ أجزاء الأغنية المطلوبة:",
        "t2_dialect": "🗣️ اللهجة/الطابع الثقافي:",
        "t2_style": "🎼 النمط الموسيقي الرئيسي:",
        "t2_vocal": "🎤 نوع وتكنيك الغناء:",
        "t2_mix": "🎛️ مؤثرات الهندسة الصوتية:",
        "t2_mood": "🎚️ طابع الأداء والصوت:",
        "t2_btn": "✨ توليد الأغنية، البرومبت، وقاموس القوافي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "...جارٍ صياغة الكلمات وهندسة البرومبت",

        # التبويب 3
        "t3_title": "🎨 مهندس برومبتات الصور الاحترافية (Midjourney & Flux)",
        "t3_desc": "🖼️ وصف الصورة التي تتخيلها:",
        "t3_engine": "🎯 محرك الصور:",
        "t3_aspect": "أبعاد الصورة:",
        "t3_btn": "🎨 توليد البرومبتات الاحترافية",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة!",
        "t3_spin": "...جارٍ كتابة برومبت الهندسة البصرية",

        # التبويب 4
        "t4_title": "🗣️ محرك الفيديو، الأفاتار، وتحويل الصور إلى فيديو",
        "t4_script": "📜 النص أو أوامر التحريك المطلوب تنفيذها:",
        "t4_voice": "🎙️ نبرة الصوت المفضل:",
        "t4_tool": "🤖 أداة التحريك المستهدفة:",
        "t4_btn": "⚡ توليد برومبتات التحريك والصوت",
        "t4_warn": "⚠️ يرجى إدخال النص أولاً!",
        "t4_spin": "...جارٍ إعداد أوامر التحريك",

        # التبويب 5
        "t5_title": "📊 استوديو التسويق، الهاشتاجات، والتريندات",
        "t5_topic": "🎯 موضوع المحتوى أو المنتج:",
        "t5_platform": "📱 المنصة المستهدفة:",
        "t5_goal": "📌 الهدف من المحتوى:",
        "t5_btn": "🚀 توليد الخطة التسويقية والتريند",
        "t5_warn": "⚠️ يرجى إدخال موضوع المحتوى!",
        "t5_spin": "...جارٍ تحليل التريندات وكتابة الاستراتيجية",
        
        "result_label": "📌 النتيجة المعروضة:"
    },
    "English": {
        "sidebar_title": "⚙️ Settings & History",
        "lang_label": "🌐 Interface Language:",
        "search_label": "🔍 Search History:",
        "fav_title": "⭐ Favorites",
        "fav_empty": "No favorites added yet",
        "history_title": "📜 Full History",
        "history_empty": "History is empty",
        "main_title": "🎬 All-in-One Smart Content Studio",
        "main_caption": "A professional system ordered by content creation stages",
        
        "tabs": [
            "1️⃣ 💡 Idea & Script",
            "2️⃣ 🎵 Suno Music Studio",
            "3️⃣ 🎨 Image & Effects Studio",
            "4️⃣ 🗣️ Video & Avatar Animation",
            "5️⃣ 📊 Marketing & Trends"
        ],
        
        "t1_title": "🎬 Idea Generator, Script, & Storyboard",
        "t1_input": "📽️ Video Title or Idea:",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_style": "🎨 Visual Style:",
        "t1_btn": "🎬 Generate Script & Storyboard",
        "t1_warn": "⚠️ Please enter a video title!",
        "t1_spin": "...Writing script",

        "t2_title": "🎵 Music Production, Sound Engineering, & Rhymes (Suno)",
        "t2_idea": "💡 Song Idea or Theme:",
        "t2_struct": "🏗️ Song Structure:",
        "t2_dialect": "🗣️ Dialect / Cultural Tone:",
        "t2_style": "🎼 Main Music Style:",
        "t2_vocal": "🎤 Vocalist Type & Technique:",
        "t2_mix": "🎛️ Audio Mixing Effects:",
        "t2_mood": "🎚️ Performance Mood:",
        "t2_btn": "✨ Generate Song, Prompt, & Rhymes",
        "t2_warn": "⚠️ Please enter the song idea first!",
        "t2_spin": "...Crafting lyrics and prompts",

        "t3_title": "🎨 Professional Image Prompt Engineer (Midjourney & Flux)",
        "t3_desc": "🖼️ Describe the image you imagine:",
        "t3_engine": "🎯 Image Engine:",
        "t3_aspect": "Aspect Ratio:",
        "t3_btn": "🎨 Generate Pro Prompts",
        "t3_warn": "⚠️ Please enter image description!",
        "t3_spin": "...Writing visual engineering prompt",

        "t4_title": "🗣️ Video Engine, Avatar, & Image-to-Video",
        "t4_script": "📜 Text or Motion Prompts:",
        "t4_voice": "🎙️ Preferred Voice Tone:",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_btn": "⚡ Generate Animation & Voice Prompts",
        "t4_warn": "⚠️ Please enter text first!",
        "t4_spin": "...Preparing motion commands",

        "t5_title": "📊 Marketing, Hashtags, & Trends Studio",
        "t5_topic": "🎯 Content or Product Topic:",
        "t5_platform": "📱 Target Platform:",
        "t5_goal": "📌 Content Goal:",
        "t5_btn": "🚀 Generate Marketing Plan & Trend",
        "t5_warn": "⚠️ Please enter content topic!",
        "t5_spin": "...Analyzing trends and strategy",
        
        "result_label": "📌 Displayed Result:"
    }
}

# ==========================================
# 3. دالة الاتصال والحفظ
# ==========================================
def generate_ai_response(prompt_text, category_name="عام", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ لم يتم العثور على GEMINI_API_KEY في Streamlit Secrets!")
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
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "category": category_name,
                "topic": user_topic if user_topic else "طلب جديد",
                "prompt": prompt_text,
                "result": output_text,
                "tab_index": tab_index
            }
            st.session_state["history"].insert(0, item)
            st.session_state["current_result"] = item
            return output_text
        else:
            error_msg = res_data.get('error', {}).get('message', 'خطأ غير معروف')
            st.error(f"❌ خطأ من API ({response.status_code}): {error_msg}")
            return None
    except Exception as e:
        st.error(f"❌ حدث خطأ في الاتصال: {str(e)}")
        return None

# ==========================================
# 4. القائمة الجانبية (Sidebar)
# ==========================================
with st.sidebar:
    # اختيار اللغة أولاً لتطبيق الترجمة على القائمة بالكامل
    lang = st.radio("🌐 لغة الواجهة / Interface Language:", ["العربية", "English"])
    T = TEXTS[lang]
    
    st.title(T["sidebar_title"])
    st.divider()
    
    search_query = st.text_input(T["search_label"])
    
    # ⭐ المفضلة
    st.subheader(T["fav_title"])
    if not st.session_state["favorites"]:
        st.caption(T["fav_empty"])
    else:
        for fav in st.session_state["favorites"]:
            with st.expander(f"⭐ {fav['topic']} ({fav['category']})"):
                st.markdown(fav["result"])
    
    st.divider()
    
    # 📜 السجل الكامل
    st.subheader(T["history_title"])
    if not st.session_state["history"]:
        st.caption(T["history_empty"])
    else:
        filtered = [
            item for item in st.session_state["history"]
            if search_query.lower() in item["topic"].lower() or search_query.lower() in item["category"].lower() or search_query.lower() in item["result"].lower()
        ] if search_query else st.session_state["history"]

        for item in filtered:
            col_item1, col_item2 = st.columns([3, 1])
            with col_item1:
                if st.button(f"📌 {item['topic']} ({item['timestamp']})", key=f"hist_{item['id']}" ):
                    st.session_state["current_result"] = item
                    st.session_state["selected_tab"] = item["tab_index"]
                    st.rerun()
            with col_item2:
                if st.button("⭐", key=f"fav_btn_{item['id']}"):
                    if item not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item)
                        st.toast("Done!" if lang == "English" else "تمت الإضافة للمفضلة!")

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
st.title(T["main_title"])
st.caption(T["main_caption"])

# شريط التنقل الرئيسي المتجانس مع اللغة
selected_tab_name = st.radio(
    "Navigation" if lang == "English" else "اختر مرحلة العمل:",
    T["tabs"],
    index=st.session_state["selected_tab"],
    horizontal=True,
    key="nav_radio"
)
st.session_state["selected_tab"] = T["tabs"].index(selected_tab_name)

st.divider()

# ----------------------------------------------------
# 1️⃣ الفكرة والسكريبت
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_title']}")
    v_title = st.text_input(T["t1_input"])
    v_duration = st.select_slider(T["t1_dur"], options=["15s", "30s", "60s", "3m"] if lang == "English" else ["15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق"])
    v_style = st.selectbox(T["t1_style"], ["Cinematic", "3D Animation", "Dark Fantasy", "Cyberpunk", "Documentary"] if lang == "English" else ["سينمائي واقعي (Cinematic)", "3D Animation", "Dark Fantasy", "Cyberpunk", "Documentary"])
    
    if st.button(T["t1_btn"], type="primary", key="btn_script"):
        if not v_title:
            st.warning(T["t1_warn"])
        else:
            with st.spinner(T["t1_spin"]):
                prompt = f"Create a script for {v_title}, duration {v_duration}, style {v_style}."
                generate_ai_response(prompt, category_name="Script" if lang=="English" else "سكريبت فيديو", user_topic=v_title[:20], tab_index=0)
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_index"] == 0:
        st.success(f"{T['result_label']} {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 2️⃣ استوديو الأغاني والصوت (Suno Pro Studio)
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 1:
    st.markdown(f"### {T['t2_title']}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        song_idea = st.text_area(T["t2_idea"], placeholder="Example: war / love / fear..." if lang=="English" else "مثال: حرب / حب / خوف...", height=100)
        song_structure = st.multiselect(
            T["t2_struct"],
            ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Guitar Solo]", "[Drop]", "[Outro]"],
            default=["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"]
        )
        lyrics_dialect = st.selectbox(T["t2_dialect"], ["Egyptian Colloquial", "Cinematic Formal", "Khaleeji", "Shami", "English Hip-Hop"] if lang=="English" else ["عامية مصرية", "فصحى سينمائية", "خليجي احترافي", "شامي حماسي", "English Hip-Hop"])
        
    with col2:
        song_style = st.selectbox(T["t2_style"], ["Egyptian Rap", "Pop", "Acoustic", "Rock", "EDM"] if lang=="English" else ["Egyptian Rap / راب مصري", "Pop / مبهج", "Acoustic / هادئ", "Rock / حماسي", "EDM / هيب وإيقاع"])
        vocal_type = st.selectbox(T["t2_vocal"], ["Deep Male Voice", "Powerful Female Voice", "Auto-tune Rap Flow", "Hype Choir"] if lang=="English" else ["صوت رجالي بحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال حماسي"])
        audio_mixing = st.multiselect(T["t2_mix"], ["Heavy 808 Bass", "Reverb", "Stereo Width", "Echo Drops", "Lo-Fi Filter"])
        song_mood = st.select_slider(T["t2_mood"], options=["Sad", "Dramatic", "Balanced", "Very Hype", "Loud"] if lang=="English" else ["حزين", "درامي", "متوازن", "حماسي جداً", "صاخب"])

    if st.button(T["t2_btn"], type="primary", key="btn_song"):
        if not song_idea:
            st.warning(T["t2_warn"])
        else:
            with st.spinner(T["t2_spin"]):
                prompt = f"Create a song based on idea: {song_idea}, dialect: {lyrics_dialect}, style: {song_style}."
                generate_ai_response(prompt, category_name="Suno Music" if lang=="English" else "أغاني Suno", user_topic=song_idea[:20], tab_index=1)
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_index"] == 1:
        st.success(f"{T['result_label']} {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 3️⃣ استوديو الصور والمؤثرات
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown(f"### {T['t3_title']}")
    
    img_desc = st.text_input(T["t3_desc"])
    img_engine = st.selectbox(T["t3_engine"], ["Midjourney v6", "Flux.1", "Leonardo AI", "DALL-E 3"])
    img_aspect = st.selectbox(T["t3_aspect"], ["16:9", "9:16", "1:1", "4:5"])
    
    if st.button(T["t3_btn"], type="primary", key="btn_img"):
        if not img_desc:
            st.warning(T["t3_warn"])
        else:
            with st.spinner(T["t3_spin"]):
                prompt = f"Generate 3 image prompts for {img_engine} based on {img_desc} with aspect ratio {img_aspect}."
                generate_ai_response(prompt, category_name="Image Prompts" if lang=="English" else "برومبت صور", user_topic=img_desc[:20], tab_index=2)
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_index"] == 2:
        st.success(f"{T['result_label']} {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 4️⃣ تحريك الصور والفيديو
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown(f"### {T['t4_title']}")
    
    a_script = st.text_area(T["t4_script"], height=100)
    a_voice = st.selectbox(T["t4_voice"], ["Epic Documentary", "Fast & Hype", "Friendly News", "Deep Dramatic"] if lang=="English" else ["صوتي وثائقي فخم", "سريع وحماسي", "ودود وإخباري", "درامي عميق"])
    a_ai_tool = st.selectbox(T["t4_tool"], ["Runway Gen-2 / Gen-3", "Luma Dream Machine", "HeyGen / D-ID", "Pika Labs"])
    
    if st.button(T["t4_btn"], type="primary", key="btn_anim"):
        if not a_script:
            st.warning(T["t4_warn"])
        else:
            with st.spinner(T["t4_spin"]):
                prompt = f"Animation prompts for {a_ai_tool} with script: {a_script}."
                generate_ai_response(prompt, category_name="Animation" if lang=="English" else "تحريك فيديو", user_topic=a_script[:20], tab_index=3)
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_index"] == 3:
        st.success(f"{T['result_label']} {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 5️⃣ تسويق المحتوى والتريند
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown(f"### {T['t5_title']}")
    
    m_topic = st.text_input(T["t5_topic"])
    m_platform = st.selectbox(T["t5_platform"], ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook", "X (Twitter)"])
    m_goal = st.selectbox(T["t5_goal"], ["Engagement", "Sales", "Awareness"] if lang=="English" else ["زيادة التفاعل (Engagement)", "زيادة المبيعات (Sales)", "زيادة المتابعين (Awareness)"])
    
    if st.button(T["t5_btn"], type="primary", key="btn_mkt"):
        if not m_topic:
            st.warning(T["t5_warn"])
        else:
            with st.spinner(T["t5_spin"]):
                prompt = f"Marketing plan for {m_topic} on {m_platform} for {m_goal}."
                generate_ai_response(prompt, category_name="Marketing" if lang=="English" else "تسويق وتريند", user_topic=m_topic[:20], tab_index=4)
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_index"] == 4:
        st.success(f"{T['result_label']} {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])
