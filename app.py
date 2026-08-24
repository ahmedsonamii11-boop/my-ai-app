import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتهيئة الأساسية
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي الشامل (50 ميزة)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# قراءة المفتاح من الـ Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY")

# تهيئة السجل والمفضلة في session_state لو مش موجودين
if "history" not in st.session_state:
    st.session_state["history"] = []

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# ==========================================
# 2. دالة الاتصال والتسجيل التلقائي
# ==========================================
def generate_ai_response(prompt_text, category_name="عام"):
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
            
            # 💾 حفظ النتيجة تلقائياً في السجل
            history_item = {
                "id": len(st.session_state["history"]) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": category_name,
                "prompt": prompt_text,
                "result": output_text
            }
            st.session_state["history"].insert(0, history_item) # إضافة في البداية لتظهر الأحدث أولاً
            return output_text
        else:
            error_msg = res_data.get('error', {}).get('message', 'خطأ غير معروف')
            st.error(f"❌ خطأ من API ({response.status_code}): {error_msg}")
            return None
    except Exception as e:
        st.error(f"❌ حدث خطأ في الاتصال: {str(e)}")
        return None

# ==========================================
# 3. القائمة الجانبية (Sidebar) وحفظ السجل
# ==========================================
with st.sidebar:
    st.title("⚙️ الإعدادات والسجل")
    
    lang = st.radio("🌐 لغة الواجهة:", ["العربية", "English"])
    is_ar = (lang == "العربية")
    
    st.divider()
    search_query = st.text_input("🔍 بحث في السجل:" if is_ar else "🔍 Search History:")
    
    # 📜 عرض السجل الكامل والتفاعلي
    st.subheader("📜 السجل الكامل (History)")
    
    if not st.session_state["history"]:
        st.caption("السجل فارغ حتى الآن. أي نتيجة تولدها ستظهر هنا أوتوماتيكياً!" if is_ar else "History is empty. Generated results will appear here automatically!")
    else:
        # تصفية السجل بناءً على البحث
        filtered_history = [
            item for item in st.session_state["history"]
            if search_query.lower() in item["category"].lower() or search_query.lower() in item["prompt"].lower()
        ] if search_query else st.session_state["history"]

        for idx, item in enumerate(filtered_history):
            with st.expander(f"📌 [{item['category']}] - {item['timestamp']}"):
                st.markdown(f"**الطلب:** {item['prompt'][:60]}...")
                st.markdown("---")
                st.markdown(item["result"])

# ==========================================
# 4. الواجهة الرئيسية والتبويبات الـ 5 الشاملة
# ==========================================
st.title("🎬 استوديو المحتوى الذكي الشامل (50 ميزة)")
st.caption("منظومة احترافية متكاملة لصناعة الأغاني، الصور، الفيديوهات، والـ Storyboards")

tabs = st.tabs([
    "🎵 Suno استوديو الأغاني", 
    "📊 تسويق المحتوى والتريند", 
    "🎬 سكريبت الفيديو والـ Storyboard", 
    "🗣️ تحريك الفيديو والمنصات", 
    "🎨 استوديو الصور والمؤثرات"
])

# ----------------------------------------------------
# 1️⃣ Suno استوديو الأغاني
# ----------------------------------------------------
with tabs[0]:
    st.markdown("### 🎵 صناعة الأغاني، الهندسة الصوتية، والقوافي (Suno Pro Studio)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        song_idea = st.text_area("💡 فكرة الأغنية أو موضوعها:", placeholder="مثال: أغنية حماسية عن التحدي والمثابرة...", height=100)
        song_structure = st.multiselect(
            "🏗️ أجزاء الأغنية المطلوبة (Structure Builder):",
            ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Guitar Solo]", "[Drop]", "[Outro]"],
            default=["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"]
        )
        lyrics_dialect = st.selectbox("🗣️ اللهجة/الطابع الثقافي:", ["عامية مصرية", "فصحى سينمائية", "خليجي احترافي", "شامي حماسي", "English Hip-Hop"])
        
    with col2:
        song_style = st.selectbox("🎼 النمط الموسيقي الرئيسي:", ["Egyptian Rap / راب مصري", "Pop / مبهج", "Acoustic / هادئ", "Rock / حماسي", "EDM / هيب وإيقاع"])
        vocal_type = st.selectbox("🎤 نوع وتكنيك الغناء (Vocalist Selector):", ["صوت رجالي بحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال حماسي"])
        audio_mixing = st.multiselect("🎛️ مؤثرات الهندسة الصوتية (Mixing Tools):", ["Heavy 808 Bass", "Reverb", "Stereo Width", "Echo Drops", "Lo-Fi Filter"])
        song_mood = st.select_slider("🎚️ طابع الأداء والصوت:", options=["حزين", "درامي", "متوازن", "حماسي جداً", "صاخب"])

    if st.button("✨ توليد الأغنية، البرومبت، وقاموس القوافي", type="primary", key="btn_song"):
        if not song_idea:
            st.warning("⚠️ يرجى إدخال فكرة الأغنية أولاً!")
        else:
            with st.spinner("...جارٍ صياغة الكلمات وهندسة البرومبت"):
                prompt = f"""You are an elite Music Producer and Songwriter.
Create a complete song package based on:
- Idea: '{song_idea}'
- Structure: {', '.join(song_structure)}
- Dialect: {lyrics_dialect}
- Style: {song_style}
- Vocalist: {vocal_type}
- Audio Effects: {', '.join(audio_mixing)}
- Mood: {song_mood}

Provide:
1. Complete Lyrics with structural tags (like [Verse], [Chorus]).
2. Ready-to-use Suno AI Style Prompt.
3. Rhyme Dictionary / Key Vocabulary used.
"""
                result = generate_ai_response(prompt, category_name="أغاني Suno")
                if result:
                    st.success("🎉 تم توليد مشروع الأغنية وحفظه في السجل!")
                    st.markdown(result)

# ----------------------------------------------------
# 2️⃣ تسويق المحتوى والتريند
# ----------------------------------------------------
with tabs[1]:
    st.markdown("### 📊 استوديو التسويق، الهاشتاجات، والتريندات")
    
    m_topic = st.text_input("🎯 موضوع المحتوى أو المنتج:")
    m_platform = st.selectbox("📱 المنصة المستهدفة:", ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook", "X (Twitter)"])
    m_goal = st.selectbox("📌 الهدف من المحتوى:", ["زيادة التفاعل (Engagement)", "زيادة المبيعات (Sales)", "زيادة المتابعين (Awareness)"])
    
    if st.button("🚀 توليد الخطة التسويقية والتريند", type="primary", key="btn_mkt"):
        if not m_topic:
            st.warning("⚠️ يرجى إدخال موضوع المحتوى!")
        else:
            with st.spinner("...جارٍ تحليل التريندات وكتابة الاستراتيجية"):
                prompt = f"""You are a Digital Marketing & Growth Hacking Expert.
Create a marketing plan for:
- Topic: {m_topic}
- Platform: {m_platform}
- Goal: {m_goal}

Provide:
1. 3 Catchy Hooks (العناوين الجاذبة).
2. Content Strategy & Post Description.
3. High-performing Hashtags.
4. Call to Action (CTA).
"""
                result = generate_ai_response(prompt, category_name="تسويق وتريند")
                if result:
                    st.success("🎉 تم توليد الخطة التسويقية وحفظها في السجل!")
                    st.markdown(result)

# ----------------------------------------------------
# 3️⃣ سكريبت الفيديو والـ Storyboard
# ----------------------------------------------------
with tabs[2]:
    st.markdown("### 🎬 صانع السكريبت التفصيلي والـ Storyboard السينمائي")
    
    v_title = st.text_input("📽️ عنوان أو فكرة الفيديو:")
    v_duration = st.select_slider("⏱️ مدة الفيديو التقديرية:", options=["15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق"])
    v_style = st.selectbox("🎨 النمط البصري (Visual Style):", ["سينمائي واقعي (Cinematic)", "3D Animation", "Dark Fantasy", "Cyberpunk", "Documentary"])
    
    if st.button("🎬 توليد السكريبت والـ Storyboard", type="primary", key="btn_script"):
        if not v_title:
            st.warning("⚠️ يرجى إدخال عنوان الفيديو!")
        else:
            with st.spinner("...جارٍ رسم المشاهد وكتابة السكريبت"):
                prompt = f"""You are a Professional Film Director and Scriptwriter.
Create a scene-by-scene Storyboard & Script for:
- Title/Idea: {v_title}
- Duration: {v_duration}
- Visual Style: {v_style}

Format output in a structured table or detailed list:
- Scene Number
- Visual Prompt
- Audio / Voiceover
- Camera Angle & Movement
"""
                result = generate_ai_response(prompt, category_name="سكريبت فيديو")
                if result:
                    st.success("🎉 تم كتابة السكريبت وحفظه في السجل!")
                    st.markdown(result)

# ----------------------------------------------------
# 4️⃣ تحريك الفيديو والمنصات
# ----------------------------------------------------
with tabs[3]:
    st.markdown("### 🗣️ محرك الفيديو، الأفاتار، وتحويل النصوص لأصوات")
    
    a_script = st.text_area("📜 النص المراد تحويله لصوت أو أفاتار:", height=100)
    a_voice = st.selectbox("🎙️ نبرة الصوت المفضل:", ["صوتي وثائقي فخم", "سريع وحماسي (Shorts/TikTok)", "ودود وإخباري", "درامي عميق"])
    a_ai_tool = st.selectbox("🤖 أداة التحريك المستهدفة:", ["Runway Gen-2 / Gen-3", "Luma Dream Machine", "HeyGen / D-ID", "Pika Labs"])
    
    if st.button("⚡ توليد برومبتات التحريك والصوت", type="primary", key="btn_anim"):
        if not a_script:
            st.warning("⚠️ يرجى إدخال النص أولاً!")
        else:
            with st.spinner("...جارٍ إعداد أوامر التحريك والصوت"):
                prompt = f"""You are an AI Video & Avatar Animation Prompt Engineer.
Process this text for video animation using {a_ai_tool}:
Text: '{a_script}'
Desired Voice Tone: {a_voice}

Provide:
1. Exact Motion/Camera Prompts for {a_ai_tool}.
2. Voiceover Delivery Guide.
3. Recommended background music mood.
"""
                result = generate_ai_response(prompt, category_name="تحريك فيديو")
                if result:
                    st.success("🎉 تم تجهيز أوامر التحريك وحفظها في السجل!")
                    st.markdown(result)

# ----------------------------------------------------
# 5️⃣ استوديو الصور والمؤثرات
# ----------------------------------------------------
with tabs[4]:
    st.markdown("### 🎨 مهندس برومبتات الصور الاحترافية (Midjourney & Flux)")
    
    img_desc = st.text_input("🖼️ وصف الصورة التي تتخيلها:")
    img_engine = st.selectbox("🎯 محرك الصور:", ["Midjourney v6", "Flux.1", "Leonardo AI", "DALL-E 3"])
    img_aspect = st.selectbox("أبعاد الصورة (Aspect Ratio):", ["16:9 (فيديو/يوتيوب)", "9:16 (ستوري/ريلز)", "1:1 (مربع)", "4:5 (إنستجرام)"])
    
    if st.button("🎨 توليد البرومبتات الاحترافية", type="primary", key="btn_img"):
        if not img_desc:
            st.warning("⚠️ يرجى إدخال وصف الصورة!")
        else:
            with st.spinner("...جارٍ كتابة برومبت الهندسة البصرية"):
                prompt = f"""You are a Master AI Image Prompt Engineer.
Generate 3 distinct, hyper-detailed image prompts for {img_engine} based on:
- Concept: {img_desc}
- Aspect Ratio: {img_aspect}

Include details on lighting, camera lens, resolution, and style.
"""
                result = generate_ai_response(prompt, category_name="برومبت صور")
                if result:
                    st.success("🎉 تم توليد برومبتات الصور وحفظها في السجل!")
                    st.markdown(result)
