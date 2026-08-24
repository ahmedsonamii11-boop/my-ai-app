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

# قائمة التبويبات بالترتيب المنطقي الصحيح
TAB_OPTIONS = [
    "1️⃣ 💡 الفكرة والسكريبت",
    "2️⃣ 🎵 استوديو الأغاني والصوت",
    "3️⃣ 🎨 استوديو الصور والمؤثرات",
    "4️⃣ 🗣️ تحريك الصور والفيديو",
    "5️⃣ 📊 تسويق المحتوى والتريند"
]

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = TAB_OPTIONS[0]

if "current_result" not in st.session_state:
    st.session_state["current_result"] = None

# ==========================================
# 2. دالة الاتصال والحفظ
# ==========================================
def generate_ai_response(prompt_text, category_name="عام", user_topic="", tab_name=""):
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
                "tab_name": tab_name
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
# 3. القائمة الجانبية (Sidebar)
# ==========================================
with st.sidebar:
    st.title("⚙️ الإعدادات والسجل")
    
    lang = st.radio("🌐 لغة الواجهة:", ["العربية", "English"])
    is_ar = (lang == "العربية")
    
    st.divider()
    search_query = st.text_input("🔍 بحث في السجل:" if is_ar else "🔍 Search History:")
    
    # ⭐ المفضلة
    st.subheader("⭐ المفضلة (Favorites)" if is_ar else "⭐ Favorites")
    if not st.session_state["favorites"]:
        st.caption("لا توجد عناصر مضافة للمفضلة" if is_ar else "No favorites added yet")
    else:
        for fav in st.session_state["favorites"]:
            with st.expander(f"⭐ {fav['topic']} ({fav['category']})"):
                st.markdown(fav["result"])
    
    st.divider()
    
    # 📜 السجل الكامل التفاعلي
    st.subheader("📜 السجل الكامل (History)" if is_ar else "📜 Full History")
    
    if not st.session_state["history"]:
        st.caption("السجل فارغ حتى الآن" if is_ar else "History is empty")
    else:
        filtered = [
            item for item in st.session_state["history"]
            if search_query.lower() in item["topic"].lower() or search_query.lower() in item["category"].lower() or search_query.lower() in item["result"].lower()
        ] if search_query else st.session_state["history"]

        for item in filtered:
            col_item1, col_item2 = st.columns([3, 1])
            with col_item1:
                # عند الضغط ينقلك فوراً للتبويب الخاص بها
                if st.button(f"📌 {item['topic']} ({item['timestamp']})", key=f"hist_{item['id']}"):
                    st.session_state["current_result"] = item
                    st.session_state["selected_tab"] = item["tab_name"]
                    st.rerun()
            with col_item2:
                if st.button("⭐", key=f"fav_btn_{item['id']}"):
                    if item not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item)
                        st.toast("تمت الإضافة للمفضلة!")

# ==========================================
# 4. الواجهة الرئيسية والتنقل بين مراحل الإنتاج
# ==========================================
st.title("🎬 استوديو المحتوى الذكي الشامل")
st.caption("منظومة احترافية مرتبة حسب مراحل صناعة المحتوى")

# شريط التنقل الرئيسي التفاعلي (راديو أفقي محاكي للتبويبات)
selected = st.radio(
    "اختر مرحلة العمل:",
    TAB_OPTIONS,
    index=TAB_OPTIONS.index(st.session_state["selected_tab"]),
    horizontal=True,
    key="nav_radio"
)
st.session_state["selected_tab"] = selected

st.divider()

# ----------------------------------------------------
# 1️⃣ الفكرة والسكريبت
# ----------------------------------------------------
if selected == TAB_OPTIONS[0]:
    st.markdown("### 🎬 صانع الفكرة، السكريبت التفصيلي، والـ Storyboard")
    
    v_title = st.text_input("📽️ عنوان أو فكرة الفيديو:")
    v_duration = st.select_slider("⏱️ مدة الفيديو التقديرية:", options=["15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق"])
    v_style = st.selectbox("🎨 النمط البصري:", ["سينمائي واقعي (Cinematic)", "3D Animation", "Dark Fantasy", "Cyberpunk", "Documentary"])
    
    if st.button("🎬 توليد السكريبت والـ Storyboard", type="primary", key="btn_script"):
        if not v_title:
            st.warning("⚠️ يرجى إدخال عنوان الفيديو!")
        else:
            with st.spinner("...جارٍ كتابة السكريبت"):
                prompt = f"Create a script for {v_title}, duration {v_duration}, style {v_style}."
                generate_ai_response(prompt, category_name="سكريبت فيديو", user_topic=v_title[:20], tab_name=TAB_OPTIONS[0])
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_name"] == TAB_OPTIONS[0]:
        st.success(f"📌 النتيجة المعروضة: {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 2️⃣ استوديو الأغاني والصوت (Suno Pro Studio)
# ----------------------------------------------------
elif selected == TAB_OPTIONS[1]:
    st.markdown("### 🎵 صناعة الأغاني، الهندسة الصوتية، والقوافي (Suno Pro Studio)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        song_idea = st.text_area("💡 فكرة الأغنية أو موضوعها:", placeholder="مثال: حرب / حب / خوف...", height=100)
        song_structure = st.multiselect(
            "🏗️ أجزاء الأغنية المطلوبة:",
            ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Guitar Solo]", "[Drop]", "[Outro]"],
            default=["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"]
        )
        lyrics_dialect = st.selectbox("🗣️ اللهجة/الطابع الثقافي:", ["عامية مصرية", "فصحى سينمائية", "خليجي احترافي", "شامي حماسي", "English Hip-Hop"])
        
    with col2:
        song_style = st.selectbox("🎼 النمط الموسيقي الرئيسي:", ["Egyptian Rap / راب مصري", "Pop / مبهج", "Acoustic / هادئ", "Rock / حماسي", "EDM / هيب وإيقاع"])
        vocal_type = st.selectbox("🎤 نوع وتكنيك الغناء:", ["صوت رجالي بحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال حماسي"])
        audio_mixing = st.multiselect("🎛️ مؤثرات الهندسة الصوتية:", ["Heavy 808 Bass", "Reverb", "Stereo Width", "Echo Drops", "Lo-Fi Filter"])
        song_mood = st.select_slider("🎚️ طابع الأداء والصوت:", options=["حزين", "درامي", "متوازن", "حماسي جداً", "صاخب"])

    if st.button("✨ توليد الأغنية، البرومبت، وقاموس القوافي", type="primary", key="btn_song"):
        if not song_idea:
            st.warning("⚠️ يرجى إدخال فكرة الأغنية أولاً!")
        else:
            with st.spinner("...جارٍ صياغة الكلمات وهندسة البرومبت"):
                prompt = f"Create a song based on idea: {song_idea}, dialect: {lyrics_dialect}, style: {song_style}."
                generate_ai_response(prompt, category_name="أغاني Suno", user_topic=song_idea[:20], tab_name=TAB_OPTIONS[1])
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_name"] == TAB_OPTIONS[1]:
        st.success(f"📌 النتيجة المعروضة: {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 3️⃣ استوديو الصور والمؤثرات
# ----------------------------------------------------
elif selected == TAB_OPTIONS[2]:
    st.markdown("### 🎨 مهندس برومبتات الصور الاحترافية (Midjourney & Flux)")
    
    img_desc = st.text_input("🖼️ وصف الصورة التي تتخيلها:")
    img_engine = st.selectbox("🎯 محرك الصور:", ["Midjourney v6", "Flux.1", "Leonardo AI", "DALL-E 3"])
    img_aspect = st.selectbox("أبعاد الصورة:", ["16:9", "9:16", "1:1", "4:5"])
    
    if st.button("🎨 توليد البرومبتات الاحترافية", type="primary", key="btn_img"):
        if not img_desc:
            st.warning("⚠️ يرجى إدخال وصف الصورة!")
        else:
            with st.spinner("...جارٍ كتابة برومبت الهندسة البصرية"):
                prompt = f"Generate 3 image prompts for {img_engine} based on {img_desc} with aspect ratio {img_aspect}."
                generate_ai_response(prompt, category_name="برومبت صور", user_topic=img_desc[:20], tab_name=TAB_OPTIONS[2])
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_name"] == TAB_OPTIONS[2]:
        st.success(f"📌 النتيجة المعروضة: {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 4️⃣ تحريك الصور والفيديو
# ----------------------------------------------------
elif selected == TAB_OPTIONS[3]:
    st.markdown("### 🗣️ محرك الفيديو، الأفاتار، وتحويل الصور إلى فيديو")
    
    a_script = st.text_area("📜 النص أو أوامر التحريك المطلوب تنفيذها:", height=100)
    a_voice = st.selectbox("🎙️ نبرة الصوت المفضل:", ["صوتي وثائقي فخم", "سريع وحماسي", "ودود وإخباري", "درامي عميق"])
    a_ai_tool = st.selectbox("🤖 أداة التحريك المستهدفة:", ["Runway Gen-2 / Gen-3", "Luma Dream Machine", "HeyGen / D-ID", "Pika Labs"])
    
    if st.button("⚡ توليد برومبتات التحريك والصوت", type="primary", key="btn_anim"):
        if not a_script:
            st.warning("⚠️ يرجى إدخال النص أولاً!")
        else:
            with st.spinner("...جارٍ إعداد أوامر التحريك"):
                prompt = f"Animation prompts for {a_ai_tool} with script: {a_script}."
                generate_ai_response(prompt, category_name="تحريك فيديو", user_topic=a_script[:20], tab_name=TAB_OPTIONS[3])
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_name"] == TAB_OPTIONS[3]:
        st.success(f"📌 النتيجة المعروضة: {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])

# ----------------------------------------------------
# 5️⃣ تسويق المحتوى والتريند
# ----------------------------------------------------
elif selected == TAB_OPTIONS[4]:
    st.markdown("### 📊 استوديو التسويق، الهاشتاجات، والتريندات")
    
    m_topic = st.text_input("🎯 موضوع المحتوى أو المنتج:")
    m_platform = st.selectbox("📱 المنصة المستهدفة:", ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook", "X (Twitter)"])
    m_goal = st.selectbox("📌 الهدف من المحتوى:", ["زيادة التفاعل (Engagement)", "زيادة المبيعات (Sales)", "زيادة المتابعين (Awareness)"])
    
    if st.button("🚀 توليد الخطة التسويقية والتريند", type="primary", key="btn_mkt"):
        if not m_topic:
            st.warning("⚠️ يرجى إدخال موضوع المحتوى!")
        else:
            with st.spinner("...جارٍ تحليل التريندات وكتابة الاستراتيجية"):
                prompt = f"Marketing plan for {m_topic} on {m_platform} for {m_goal}."
                generate_ai_response(prompt, category_name="تسويق وتريند", user_topic=m_topic[:20], tab_name=TAB_OPTIONS[4])
                st.rerun()

    if st.session_state["current_result"] and st.session_state["current_result"]["tab_name"] == TAB_OPTIONS[4]:
        st.success(f"📌 النتيجة المعروضة: {st.session_state['current_result']['topic']}")
        st.markdown(st.session_state["current_result"]["result"])
