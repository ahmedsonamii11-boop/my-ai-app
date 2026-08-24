import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. إعدادات الصفحة والتهيئة الأساسية
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي الشامل (50 ميزة)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة المفتاح السري من Streamlit Secrets تلقائياً
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ==========================================
# 2. القائمة الجانبية (اللغة، المفضلة، السجل)
# ==========================================
with st.sidebar:
    st.title("⚙️ الإعدادات والسجل")
    
    lang = st.radio("🌐 لغة الواجهة:", ["العربية", "English"])
    is_ar = (lang == "العربية")
    
    st.divider()
    
    # وضع التركيز (Zen Mode)
    st.session_state["zen_mode"] = st.checkbox("🧘‍♂️ وضع التركيز (Zen Mode)" if is_ar else "🧘‍♂️ Zen Mode")
    
    st.divider()
    
    # البحث في السجل
    search_query = st.text_input("🔍 بحث في السجل:" if is_ar else "🔍 Search History:")
    
    st.subheader("⭐ المفضلة (Favorites)")
    st.caption("لا توجد عناصر مضافة للمفضلة" if is_ar else "No favorites added yet")
    
    st.subheader("📜 السجل الكامل (History)")
    st.caption("السجل فارغ حتى الآن" if is_ar else "History is currently empty")

# ==========================================
# 3. الواجهة الرئيسية واستوديو الأغاني (Suno Studio)
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

# ------------ 1. Suno استوديو الأغاني ------------
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
            if not api_key:
                st.error("❌ لم يتم العثور على API Key في Secrets. يرجى إضافته في إعدادات Streamlit Cloud!")
            else:
                with st.spinner("...جارٍ صياغة الكلمات، حساب الـ BPM وتنظيم الهندسة الصوتية"):
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = f"""You are an elite Music Producer and Songwriter.
Create a complete song package based on:
- Idea: '{song_idea}'
- Structure: {', '.join(song_structure)}
- Dialect/Language: {lyrics_dialect}
- Style: {song_style}
- Vocal Style: {vocal_type}
- Mixing: {', '.join(audio_mixing)}
- Mood: {song_mood}

Provide:
1. Complete Lyrics with structural tags (like [Verse], [Chorus]).
2. Ready-to-use Suno AI Style Prompt.
3. Rhyme Dictionary / Key Vocabulary used.
"""
                        response = model.generate_content(prompt)
                        
                        st.success("🎉 تم توليد مشروع الأغنية بنجاح!")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"❌ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}")
