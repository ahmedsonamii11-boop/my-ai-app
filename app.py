import streamlit as st
import google.generativeai as genai
import json
import random

# ==================== 1. إعدادات الصفحة والتصميم الاحترافي ====================
st.set_page_config(
    page_title="Ultimate AI Content Studio Pro 50-in-1",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للواجهة والتصميم السينمائي الجذاب
st.markdown("""
<style>
    /* خلفيات وتنسيق عام */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* العناوين والبطاقات */
    .main-title {
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }
    
    /* بطاقات الميزات */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* أزرار مخصصة */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# إدارة الحالة الخفية (Session State)
if "history" not in st.session_state:
    st.session_state["history"] = []
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []
if "selected_item" not in st.session_state:
    st.session_state["selected_item"] = None
if "zen_mode" not in st.session_state:
    st.session_state["zen_mode"] = False

# ==================== 2. القائمة الجانبية (السجل، المفضلة، والإعدادات) ====================
with st.sidebar:
    st.title("⚙️ الإعدادات والسجل")
    
    lang = st.radio("🌐 لغة الواجهة:", ["العربية", "English"])
    is_ar = (lang == "العربية")
    
    st.divider()
    
    # قراءة المفتاح تلقائياً من Secrets بدون إظهار أي خانة للمستخدم
    api_key = st.secrets.get("GEMINI_API_KEY") or st.session_state.get("saved_api_key")

    if api_key:
        genai.configure(api_key=api_key)
    
    # وضع التركيز (Zen Mode)
    st.session_state["zen_mode"] = st.checkbox("🧘 وضع التركيز (Zen Mode)" if is_ar else "🧘 Zen Mode")
    
    st.divider()
    
    # البحث في السجل
    search_query = st.text_input("🔍 بحث في السجل:" if is_ar else "🔍 Search History:")
    
    # قسم المفضلة
    st.subheader("⭐ المفضلة (Favorites)" if is_ar else "⭐ Favorites")
    if st.session_state.get("favorites"):
        for idx, fav in enumerate(st.session_state["favorites"]):
            if st.button(f"⭐ {fav['title']}", key=f"fav_{idx}", use_container_width=True):
                st.session_state["selected_item"] = fav
    else:
        st.caption("لا توجد عناصر مضافة للمفضلة" if is_ar else "No favorites yet")
        
    st.divider()
    
    # قسم السجل الكامل
    st.subheader("📜 السجل الكامل (History)" if is_ar else "📜 Full History")
    if st.session_state.get("history"):
        if st.button("🗑️ مسح السجل بالكامل" if is_ar else "🗑️ Clear All History", use_container_width=True):
            st.session_state["history"] = []
            st.session_state["selected_item"] = None
            st.rerun()
            
        filtered_history = st.session_state["history"]
        if search_query:
            filtered_history = [h for h in filtered_history if search_query.lower() in h['title'].lower() or search_query.lower() in h['content'].lower()]
            
        for idx, item in enumerate(reversed(filtered_history)):
            icon = "🎵" if item["type"] == "song" else ("🎨" if item["type"] == "image" else ("🎥" if item["type"] == "video" else "🎬"))
            if st.button(f"{icon} {item['title']}", key=f"hist_{idx}", use_container_width=True):
                st.session_state["selected_item"] = item
    else:
        st.caption("السجل فارغ حتى الآن" if is_ar else "History is empty")
# ==================== 3. محرك الذكاء الاصطناعي والدوال المساعدة ====================
def call_gemini(prompt_text):
    api_key = st.session_state.get("saved_api_key", "")
    if not api_key:
        return None, "NO_KEY"
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text
        )
        if response and response.text:
            return response.text, "SUCCESS"
        return None, "EMPTY"
    except Exception as e:
        return None, str(e)

def save_to_history(item_type, title, content):
    data = {"type": item_type, "title": title, "content": content}
    st.session_state["history"].append(data)

# ==================== 4. الواجهة الرئيسية والتبويبات ====================
if not st.session_state["zen_mode"]:
    st.markdown('<div class="main-title">🎬 استوديو المحتوى الذكي الشامل (50 ميزة)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">منظومة احترافية متكاملة لصناعة الأغاني، الصور، الفيديوهات، والـ Storyboards</div>', unsafe_allow_html=True)

# عرض العنصر المحدد من السجل
if st.session_state["selected_item"]:
    item = st.session_state["selected_item"]
    st.info(f"📌 **عرض العمل المحفوظ من السجل:** {item['title']}")
    st.markdown(item["content"])
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⭐ إضافة للمفضلة"):
            if item not in st.session_state["favorites"]:
                st.session_state["favorites"].append(item)
                st.success("تمت الإضافة للمفضلة!")
    with c2:
        if st.button("❌ إغلاق العرض والعودة"):
            st.session_state["selected_item"] = None
            st.rerun()
    st.divider()

# زر الأفكار العشوائية (Surprise Me)
col_top1, col_top2 = st.columns([4, 1])
with col_top2:
    if st.button("🎲 فاجئني بفكرة! (Surprise Me)", use_container_width=True):
        ideas = [
            "أغنية راب حماسية عن شخص يبني مستقبله في مجال الذكاء الاصطناعي",
            "صورة سينمائية لفارس يقف على قمة جبل وقت الغروب بأسلوب Unreal Engine 5",
            "فيديو كليب أنيميشن لسيارة رياضية تنطلق في شوارع طوكيو بالليل"
        ]
        st.toast(random.choice(ideas), icon="💡")

tabs = st.tabs([
    "🎵 استوديو الأغاني وSuno",
    "🎨 استوديو الصور والجراديانت",
    "🎥 تحريك الفيديو والعدسات",
    "🎬 سكريبت الفيديو والـ Storyboard",
    "📱 تسويق المحتوى والتريند"
])

# -------------------- 1. استوديو الأغاني وSuno --------------------
with tabs[0]:
    st.markdown("### 🎵 صناعة الأغاني، الهندسة الصوتية، والقوافي (Suno Pro Studio)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        song_idea = st.text_area("فكرة الأغنية أو موضوعها:", placeholder="مثال: أغنية حماسية عن التحدي والمثابرة...", height=100)
        song_structure = st.multiselect(
            "أجزاء الأغنية المطلوبة (Structure Builder):",
            ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Guitar Solo]", "[Drop]", "[Outro]"],
            default=["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"]
        )
        lyrics_dialect = st.selectbox("اللهجة/الطابع الثقافي:", ["عامية مصرية", "فصحى سينمائية", "خليجي احترافي", "شامي حماسي", "English Hip-Hop"])
        
    with col2:
        song_style = st.selectbox("النمط الموسيقي الرئيسي:", ["Egyptian Rap / راب مصري", "Pop / مبهج", "Acoustic / هادئ", "Rock / حماسي", "EDM / رقص وإيقاع", "Trap / تراب"])
        vocal_type = st.selectbox("نوع وتكتيك الغناء (Vocalist Selector):", ["صوت رجالي مبحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال حماسي", "Duet (ثنائي)"])
        audio_mixing = st.multiselect("مؤثرات الهندسة الصوتية (Mixing Tools):", ["Reverb", "Heavy 808 Bass", "Stereo Width", "Echo Drops", "Lo-Fi Filter"], default=["Heavy 808 Bass"])
        song_mood = st.select_slider("طابع الأداء والصوت:", options=["حزين", "درامي", "متوازن", "حماسي جداً", "صاخب"])

    if st.button("✨ توليد الأغنية، البرومبت، وقاموس القوافي", type="primary", key="btn_song"):
        if song_idea:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            with st.spinner("جاري صياغة الكلمات، حساب الـ BPM، وتنظيم الهندسة الصوتية..."):
                prompt = f"""You are an elite Music Producer and Songwriter.
Create a complete song package based on:
- Idea: '{song_idea}'
- Genre: '{song_style}'
- Structure: {', '.join(song_structure)}
- Dialect: '{lyrics_dialect}'
- Vocalist Style: '{vocal_type}'
- Audio Effects: {', '.join(audio_mixing)}
- Mood: '{song_mood}'

Provide:
1. Full Lyrics with structural tags and proper rhyming.
2. Suno AI Style Prompt in English (<120 characters) specifying BPM, instruments, and mixing.
3. Estimated Duration & BPM Recommendation.
4. 3 Catchy Song Titles.
5. Album Art Cover Prompt for Midjourney."""
                
                res, status = call_gemini(prompt)
                if status == "SUCCESS":
                    st.success("تم توليد حزمة الأغنية بنجاح!")
                    st.markdown(res)
                    title_str = f"أغنية: {song_idea[:15]}..."
                    save_to_history("song", title_str, res)
                    
                    st.download_button("📥 تحميل الكلمات والحزمة كملف TXT", res, file_name="song_package.txt")
                else:
                    st.error("تعذر الاتصال بالذكاء الاصطناعي. تأكد من إدخال API Key.")
            st.link_button("🚀 الانتقال المباشر إلى Suno AI", "https://suno.com", use_container_width=True)
        else:
            st.warning("يرجى إدخال فكرة الأغنية أولاً!")

# -------------------- 2. استوديو الصور والجراديانت --------------------
with tabs[1]:
    st.markdown("### 🎨 مهندس البرومبتات البصرية والإضاءة (Visual Studio Pro)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        img_idea = st.text_area("وصف الصورة أو المشهد الأساسي:", placeholder="مثال: رائد فضاء يكتشف جرفاً مليئاً بالبلورات المضيئة...", height=100)
        aspect_ratio = st.radio("أبعاد الصورة (Aspect Ratio):", ["16:9 (سينمائي)", "9:16 (ستوري/تيك توك)", "1:1 (مربع انستغرام)"], horizontal=True)
        negative_prompt = st.text_input("عناصر ممنوع ظهورها (Negative Prompt):", value="blurry, low quality, distorted, extra limbs, bad anatomy")
        
    with col2:
        art_engine = st.selectbox("المحرك والنمط الفني:", ["Unreal Engine 5 Render", "Midjourney V6 Photorealistic", "Anime / Cyberpunk Concept", "3D Pixar Render", "Dark Fantasy Oil Painting"])
        lighting_style = st.selectbox("نوع الإضاءة وتوزيع الألوان:", ["Volumetric Cinematic Lighting", "Golden Hour Sunset", "Neon Night Glow", "Studio Softbox Lighting", "Dramatic Rim Light"])
        director_style = st.selectbox("أسلوب الإخراج والعدسات:", ["Christopher Nolan Style", "35mm Vintage Camera", "Wide-Angle GoPro", "Macro Close-Up Lens"])

    if st.button("✨ توليد البرومبت المعزز المتقدم", type="primary", key="btn_img"):
        if img_idea:
            with st.spinner("جاري صياغة البرومبت التفصيلي..."):
                ar_code = "--ar 16:9" if "16:9" in aspect_ratio else ("--ar 9:16" if "9:16" in aspect_ratio else "--ar 1:1")
                prompt = f"""Act as a master Midjourney & Google Flow Prompt Engineer.
Idea: '{img_idea}'
Engine/Style: '{art_engine}'
Lighting: '{lighting_style}'
Director Style: '{director_style}'
Aspect Ratio: '{ar_code}'
Negative Prompt: '{negative_prompt}'

Generate:
1. Master English Prompt with rich photographic details, resolution, lighting, and camera parameters.
2. Short Prompt version for Bing Image Creator.
3. Visual Color Palette suggestions (Hex Codes / Vibe)."""
                
                res, status = call_gemini(prompt)
                if status == "SUCCESS":
                    st.success("تم تجهيز البرومبت السينمائي بنجاح!")
                    st.markdown(res)
                    title_str = f"صورة: {img_idea[:15]}..."
                    save_to_history("image", title_str, res)
                    st.download_button("📥 تحميل البرومبت كملف TXT", res, file_name="image_prompt.txt")
                else:
                    st.error("حدث خطأ في التوليد.")
            st.link_button("🚀 فتح Bing Image Creator", "https://www.bing.com/create", use_container_width=True)
        else:
            st.warning("يرجى إضافة وصف الصورة!")

# -------------------- 3. تحريك الفيديو والعدسات --------------------
with tabs[2]:
    st.markdown("### 🎥 مسارات حركة الكاميرا والـ VFX (Luma & Runway Studio)")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        vid_idea = st.text_area("وصف حركة المشهد المراد تحريكه:", placeholder="مثال: تنين يرفرف بأجنحته أعلى قلعة قديمة في وسط عاصفة...", height=100)
    with col2:
        cam_motion = st.selectbox("حركة المسار (Camera Dynamics):", [
            "Dolly Zoom (إحساس سينمائي)", 
            "Orbit Around Subject (دوران حول العنصر)", 
            "FPV Speed Tracking (تتبع سريع)", 
            "Drone Overhead Flyover (لقطة جوية)",
            "Pan Left to Right + Zoom In (حركة مركبة)"
        ])
        vfx_effects = st.multiselect("المؤثرات البصرية الخاصة (VFX):", ["CGI Smoke & Fire", "Slow-Mo Explosion", "Rain Reflections", "Cyberpunk Particle Drift"], default=["Rain Reflections"])
        fps_quality = st.select_slider("سلاسة الحركة والجودة:", options=["30fps Standard", "60fps Cinematic", "Slow Motion 120fps"])

    if st.button("✨ توليد أمر تحريك الفيديو والـ Sequence", type="primary", key="btn_vid"):
        if vid_idea:
            with st.spinner("جاري إعداد سكريبت تحريك المشهد..."):
                prompt = f"""Act as a Video FX & Motion Prompt Generator for Luma Dream Machine & Runway Gen-2.
Scene: '{vid_idea}'
Camera Movement: '{cam_motion}'
VFX: {', '.join(vfx_effects)}
Quality: '{fps_quality}'

Provide:
1. Exact English Motion Prompt ready for pasting.
2. Timeline Sequence breakdown (First 2 sec, Next 3 sec)."""
                
                res, status = call_gemini(prompt)
                if status == "SUCCESS":
                    st.success("أمر تحريك الفيديو جاهز!")
                    st.markdown(res)
                    title_str = f"فيديو: {vid_idea[:15]}..."
                    save_to_history("video", title_str, res)
                else:
                    st.error("تعذر التوليد.")
            st.link_button("🚀 فتح Luma Dream Machine", "https://lumalabs.ai/dream-machine", use_container_width=True)
        else:
            st.warning("يرجى كتابة وصف المشهد!")

# -------------------- 4. سكريبت الفيديو والـ Storyboard --------------------
with tabs[3]:
    st.markdown("### 🎬 تحويل النصوص والأغاني إلى Storyboard فيديو كليب")
    
    script_input = st.text_area("أدخل كلمات الأغنية أو السكريبت الكامل هنا:", placeholder="الصق كلمات الأغنية أو السكريبت هنا...", height=150)
    
    if st.button("✨ إنشاء الـ Storyboard والمشاهد المصورة", type="primary"):
        if script_input:
            with st.spinner("جاري تحليل النص وتقسيمه لمشاهد مصورة..."):
                prompt = f"""Convert the following script/lyrics into a highly detailed Music Video Storyboard:
Script: '{script_input}'

For each section/scene:
1. Scene Title & Shot Type (Wide Shot, Close-up, Drone Shot).
2. Detailed Visual Description.
3. Lighting & Color Palette.
4. Ready-to-use Image Prompt for generating that exact scene background."""
                
                res, status = call_gemini(prompt)
                if status == "SUCCESS":
                    st.success("تم توليد الـ Storyboard بنجاح!")
                    st.markdown(res)
                    save_to_history("storyboard", "Storyboard فيديو كليب", res)
                else:
                    st.error("تعذر التوليد.")
        else:
            st.warning("أدخل السكريبت أولاً!")

# -------------------- 5. تسويق المحتوى والتريند --------------------
with tabs[4]:
    st.markdown("### 📱 صانع محتوى المنصات والعناوين التريند (Social Copywriter)")
    
    col1, col2 = st.columns(2)
    with col1:
        project_desc = st.text_area("وصف مشروعك/الأغنية/الصورة المراد تسويقها:", placeholder="مثال: أغنية راب جديدة عن النجاح والتطوير الذاتي...", height=100)
    with col2:
        target_platform = st.multiselect("المنصات المستهدفة:", ["TikTok", "YouTube Shorts", "Instagram Reels", "LinkedIn", "Facebook"], default=["TikTok", "YouTube Shorts"])

    if st.button("✨ توليد العناوين، منشورات التواصل، والهاشتاجات", type="primary"):
        if project_desc:
            with st.spinner("جاري كتابة المحتوى التسويقي الجاذب..."):
                prompt = f"""Act as a Viral Social Media Marketing Expert.
Project: '{project_desc}'
Target Platforms: {', '.join(target_platform)}

Provide:
1. 5 High-CTR Viral Headlines / Hook Titles (أول 3 ثوانٍ).
2. Complete Engaging Social Media Caption with Emojis for Instagram/TikTok.
3. 15 High-Performing Hashtags.
4. Strong Call to Action (CTA) to boost shares and comments."""
                
                res, status = call_gemini(prompt)
                if status == "SUCCESS":
                    st.success("تم تجهيز الخطة التسويقية بالكامل!")
                    st.markdown(res)
                    save_to_history("marketing", "خطة تسويق منشور", res)
                else:
                    st.error("حدث خطأ في التوليد.")
        else:
            st.warning("أدخل وصف المشروع!")
