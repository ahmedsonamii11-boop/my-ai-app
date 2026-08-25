import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم المتجاوب (Responsive)
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي الشامل - Pro Max",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# كود CSS لتنسيق الواجهة وإزالة أي رموز غريبة وتظبيط المظهر الاحترافي
st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @media only screen and (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h3 { font-size: 1.2rem !important; }
        .stButton button { width: 100% !important; }
        [data-testid="column"] { width: 100% !important; flex: 100% !important; min-width: 100% !important; }
    }
    .voice-hint {
        font-size: 0.85rem;
        color: #ef4444;
        font-weight: 600;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم (Persistent Storage - JSON)
# ==========================================
HISTORY_FILE = "content_studio_history_pro.json"
FAV_FILE = "content_studio_favorites_pro.json"

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

# تهيئة المتغيرات النصية المرتبطة بالصوت لضمان عدم حدوث أخطاء
for key in ["t1_input_val", "t2_idea_val", "t3_desc_val", "t4_script_val", "t5_topic_val"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ==========================================
# 2. القاموس الثنائي الشامل (عربي / English)
# ==========================================
TEXTS = {
    "العربية": {
        "sidebar_title": "⚙️ الإدارة والتحكم الشامل",
        "search_label": "🔍 بحث متقدم في السجل:",
        "fav_title": "⭐ المفضلة والمشاريع المثبتة",
        "fav_empty": "لا توجد عناصر مضافة للمفضلة بعد",
        "history_title": "📜 السجل الكامل (حفظ دائم)",
        "history_empty": "السجل فارغ حتى الآن",
        "clear_history": "🗑️ مسح السجل بالكامل",
        "export_all": "📥 تصدير قاعدة البيانات (JSON)",
        "stats_title": "📊 لوحة إحصائيات الأداء الحية",
        "stat_total": "إجمالي الأعمال المُنجزة:",
        "main_title": "🎬 استوديو المحتوى الذكي الشامل (Pro Max)",
        "main_caption": "المنظومة الاحترافية المتكاملة مع إمكانية الإدخال الصوتي المباشر للأفكار والتريندات",
        
        "tabs": [
            "1️⃣ 💡 فكرة وسكريبت والخطافات",
            "2️⃣ 🎵 أستديو الأغاني والصوت",
            "3️⃣ 🎨 مهندس الصور الاحترافي",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار",
            "5️⃣ 📊 التسويق والتريندات"
        ],
        
        "t1_title": "🎬 صانع الفكرة، السكريبت التفصيلي، والـ Hook Generator",
        "t1_input": "📽️ عنوان أو فكرة الفيديو:",
        "t1_dur": "⏱️ مدة الفيديو التقديرية:",
        "t1_style": "🎨 النمط البصري المتقدم:",
        "t1_hook": "🎯 تفعيل صانع الخطافات (أول 3 ثوانٍ):",
        "t1_btn": "🎬 توليد السكريبت والخطافات",
        "t1_warn": "⚠️ يرجى إدخال عنوان أو فكرة الفيديو!",
        "t1_spin": "...جارٍ توليد السكريبت الاحترافي",

        "t2_title": "🎵 صناعة الأغاني، الهندسة الصوتية، ومكتبة القوافي",
        "t2_idea": "💡 فكرة الأغنية أو الموضوع الرئيسي:",
        "t2_struct": "🏗️ أجزاء الأغنية والترتيب:",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_style": "🎼 النمط الموسيقي وسرعة الإيقاع (BPM):",
        "t2_vocal": "🎤 نوع وتكنيك الغناء والهارموني:",
        "t2_mix": "🎛️ مؤثرات الهندسة الصوتية والماسترنج:",
        "t2_mood": "🎚️ طابع الأداء والشعور:",
        "t2_btn": "✨ توليد الأغنية الكاملة وقاموس القوافي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "...جارٍ صياغة الكلمات وهندسة المكس",

        "t3_title": "🎨 مهندس برومبتات الصور الاحترافية",
        "t3_desc": "🖼️ وصف الصورة الخيالية بدقة:",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي للصور:",
        "t3_aspect": "📐 أبعاد ومقاسات الصورة:",
        "t3_btn": "🎨 توليد برومبتات الصور الاحترافية",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة المطلوب!",
        "t3_spin": "...جارٍ هندسة الأوامر البصرية",

        "t4_title": "🗣️ محرك الفيديو، الأفاتار، وتحويل الصور لحركة",
        "t4_script": "📜 النص الإلقائي أو أوامر الحركة:",
        "t4_voice": "🎙️ نبرة الصوت وتكنيك الأداء:",
        "t4_tool": "🤖 أداة التحريك والأفاتار المستهدفة:",
        "t4_btn": "⚡ توليد برومبتات التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أولاً!",
        "t4_spin": "...جارٍ إعداد أوامر الـ Animation",

        "t5_title": "📊 استوديو التسويق، خطط المحتوى، والتريندات",
        "t5_topic": "🎯 موضوع المحتوى أو المنتج المراد تسويقه:",
        "t5_platform": "📱 المنصة المستهدفة للنشر:",
        "t5_goal": "📌 الهدف التسويقي الأساسي:",
        "t5_btn": "🚀 توليد الخطة التسويقية والتريند",
        "t5_warn": "⚠️ يرجى إدخال موضوع المحتوى!",
        "t5_spin": "...جارٍ تحليل السوق واستخراج الهاشتاجات",
        
        "result_label": "📌 النتيجة المعروضة:",
        "copy_btn": "📋 نسخ النص للحافظة",
        "download_txt": "📥 تحميل كملف نصي (.txt)",
        "rating_label": "⭐ تقييم جودة النتيجة:"
    },
    "English": {
        "sidebar_title": "⚙️ Control & Pro Management",
        "search_label": "🔍 Advanced History Search:",
        "fav_title": "⭐ Favorites & Pinned",
        "fav_empty": "No favorites added yet",
        "history_title": "📜 Full History (Auto-Saved)",
        "history_empty": "History is empty",
        "clear_history": "🗑️ Clear All History",
        "export_all": "📥 Export Database (JSON)",
        "stats_title": "📊 Live Metrics",
        "stat_total": "Total Completed Works:",
        "main_title": "🎬 All-in-One Smart Content Studio (Pro Max)",
        "main_caption": "Professional system with voice input support for ideas and trends",
        
        "tabs": [
            "1️⃣ 💡 Idea, Script & Hooks",
            "2️⃣ 🎵 Suno Music & Audio",
            "3️⃣ 🎨 Image Prompt Engineer",
            "4️⃣ 🗣️ Video & Avatar Animation",
            "5️⃣ 📊 Marketing & Trends"
        ],
        
        "t1_title": "🎬 Idea Generator, Script, & Viral Hooks",
        "t1_input": "📽️ Video Title or Core Idea:",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_style": "🎨 Visual Style:",
        "t1_hook": "🎯 Enable Viral Hooks:",
        "t1_btn": "🎬 Generate Script & Hooks",
        "t1_warn": "⚠️ Please enter video title!",
        "t1_spin": "...Generating professional script",

        "t2_title": "🎵 Music Production & Sound Engineering",
        "t2_idea": "💡 Song Idea or Theme:",
        "t2_struct": "🏗️ Song Structure:",
        "t2_dialect": "🗣️ Dialect / Cultural Tone:",
        "t2_style": "🎼 Main Music Style:",
        "t2_vocal": "🎤 Vocal Type:",
        "t2_mix": "🎛️ Audio Mixing Effects:",
        "t2_mood": "🎚️ Performance Mood:",
        "t2_btn": "✨ Generate Full Song & Rhymes",
        "t2_warn": "⚠️ Please enter the song idea first!",
        "t2_spin": "...Crafting lyrics and mix notes",

        "t3_title": "🎨 Professional Image Prompt Engineer",
        "t3_desc": "🖼️ Describe your imagined image:",
        "t3_engine": "🎯 AI Image Engine:",
        "t3_aspect": "📐 Aspect Ratio:",
        "t3_btn": "🎨 Generate Pro Prompts",
        "t3_warn": "⚠️ Please enter image description!",
        "t3_spin": "...Engineering visual prompts",

        "t4_title": "🗣️ Video Engine & Avatar Animation",
        "t4_script": "📜 Voiceover Text or Motion Commands:",
        "t4_voice": "🎙️ Voice Tone:",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_btn": "⚡ Generate Motion Prompts",
        "t4_warn": "⚠️ Please enter text first!",
        "t4_spin": "...Preparing motion prompts",

        "t5_title": "📊 Marketing & Content Plans",
        "t5_topic": "🎯 Content Topic:",
        "t5_platform": "📱 Target Platform:",
        "t5_goal": "📌 Core Marketing Goal:",
        "t5_btn": "🚀 Generate Marketing Plan",
        "t5_warn": "⚠️ Please enter content topic!",
        "t5_spin": "...Analyzing market strategy",
        
        "result_label": "📌 Displayed Result:",
        "copy_btn": "📋 Copy Text",
        "download_txt": "📥 Download (.txt)",
        "rating_label": "⭐ Rate Result:"
    }
}

# دالة الجافاسكريبت للمايك المباشر (تضغط الزرار، تتكلم، وتتنسخ الفكرة أوتوماتيك للحافظة عشان تلصقها بضغطة زر)
def render_inline_mic_helper(input_id_name):
    st.markdown(f"""
        <div style="margin-bottom: 8px;">
            <span class="voice-hint">🎙️ بدل الكتابة، اضغط للحديث الصوتي:</span><br>
            <button onclick="recordVoice_{input_id_name}()" style="background-color:#ef4444; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer; font-size:0.85rem; font-weight:bold;">
                🔴 اضغط وتحدث بصوتك
            </button>
            <span id="status_{input_id_name}" style="font-size:0.8rem; color:#555; margin-left:8px;"></span>
        </div>
        <script>
        function recordVoice_{input_id_name}() {{
            if (window.hasOwnProperty('webkitSpeechRecognition')) {{
                var recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = "ar-EG";
                recognition.start();
                
                document.getElementById('status_{input_id_name}').innerText = "جاري الاستماع... تتحدث الآن 🎙️";
                
                recognition.onresult = function(e) {{
                    var text = e.results[0][0].transcript;
                    document.getElementById('status_{input_id_name}').innerText = "تم التقاط الصوت بنجاح! ✅";
                    navigator.clipboard.writeText(text);
                    alert("تم نسخ كلامك الصوتي: (" + text + ")\\nالآن اضغط لصق (Paste) في خانة الكتابة أدناه.");
                    recognition.stop();
                };
                
                recognition.onerror = function(e) {{
                    document.getElementById('status_{input_id_name}').innerText = "حدث خطأ في التسجيل.";
                    recognition.stop();
                }}
            }} else {{
                alert("متصفحك لا يدعم الإدخال الصوتي، يرجى استخدام Google Chrome.");
            }}
        }}
        </script>
    """, unsafe_allow_html=True)

# ==========================================
# 3. دالة الاتصال الذكي بالـ API
# ==========================================
def generate_ai_response(prompt_text, category_name="عام", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ لم يتم العثور على GEMINI_API_KEY في إعدادات Streamlit Secrets!")
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
                "topic": user_topic if user_topic else "طلب جديد",
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
            error_msg = res_data.get('error', {}).get('message', 'خطأ غير معروف')
            st.error(f"❌ خطأ من الخادم: {error_msg}")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {str(e)}")
        return None

# ==========================================
# 4. القائمة الجانبية المتجاوبة
# ==========================================
with st.sidebar:
    lang = st.radio("🌐 اللغة / Language:", ["العربية", "English"])
    T = TEXTS[lang]
    
    st.title(T["sidebar_title"])
    st.divider()
    
    st.subheader(T["stats_title"])
    st.metric(label=T["stat_total"], value=len(st.session_state["history"]))
    
    st.divider()
    search_query = st.text_input(T["search_label"])
    
    if st.button(T["export_all"], key="export_db"):
        db_json = json.dumps(st.session_state["history"], ensure_ascii=False, indent=4)
        st.download_button("💾 تحميل JSON", db_json, "studio_backup.json", "application/json")
    
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
        if st.button(T["clear_history"], key="clear_hist"):
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
            col_item1, col_item2 = st.columns([3, 1])
            with col_item1:
                if st.button(f"📌 {item['topic']}", key=f"hist_{item['id']}"):
                    st.session_state["current_result"] = item
                    st.session_state["selected_tab"] = item["tab_index"]
                    st.rerun()
            with col_item2:
                if st.button("⭐", key=f"fav_btn_{item['id']}"):
                    if item not in st.session_state["favorites"]:
                        st.session_state["favorites"].append(item)
                        save_data(FAV_FILE, st.session_state["favorites"])
                        st.toast("تمت الإضافة للمفضلة!")

# ==========================================
# 5. الواجهة الرئيسية والتنقل بين الأقسام
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

def render_result_section(tab_idx):
    res = st.session_state["current_result"]
    if res and res["tab_index"] == tab_idx:
        st.success(f"{T['result_label']} {res['topic']}")
        st.markdown(res["result"])
        
        word_count = len(res["result"].split())
        char_count = len(res["result"])
        st.info(f"📊 إحصائيات الناتج: {word_count} كلمة | {char_count} حرف")
        
        c_btn1, c_btn2, c_btn3 = st.columns([1, 1, 1])
        with c_btn1:
            if st.button(T["copy_btn"], key=f"copy_{res['id']}_{tab_idx}"):
                st.toast("تم النسخ بنجاح!")
        with c_btn2:
            st.download_button(
                label=T["download_txt"],
                data=res["result"],
                file_name=f"content_{res['id']}.txt",
                mime="text/plain",
                key=f"download_{res['id']}_{tab_idx}"
            )
        with c_btn3:
            res["rating"] = st.slider(T["rating_label"], 1, 5, res.get("rating", 5), key=f"rate_{res['id']}")

# ----------------------------------------------------
# 1️⃣ الفكرة والسكريبت والخطافات
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_title']}")
    
    render_inline_mic_helper("tab1_input")
    v_title = st.text_input(T["t1_input"], key="t1_field")
    
    v_duration = st.select_slider(T["t1_dur"], options=["15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق", "بودكاست"])
    v_style = st.selectbox(T["t1_style"], ["سينمائي واقعي", "3D Animation", "Dark Fantasy", "Cyberpunk", "وثائقي"])
    v_hook_enabled = st.checkbox(T["t1_hook"], value=True)
    
    if st.button(T["t1_btn"], type="primary", key="btn_s1"):
        if not v_title:
            st.warning(T["t1_warn"])
        else:
            with st.spinner(T["t1_spin"]):
                prompt = f"Create a professional script for '{v_title}', duration {v_duration}, style {v_style}, with viral hooks for the first 3 seconds."
                generate_ai_response(prompt, category_name="Script" if lang=="English" else "سكريبت", user_topic=v_title[:25], tab_index=0)
                st.rerun()

    render_result_section(0)

# ----------------------------------------------------
# 2️⃣ أستديو الأغاني والصوت
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 1:
    st.markdown(f"### {T['t2_title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        render_inline_mic_helper("tab2_input")
        song_idea = st.text_area(T["t2_idea"], height=100, key="t2_field")
        song_structure = st.multiselect(T["t2_struct"], ["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"], default=["[Intro]", "[Verse 1]", "[Chorus]", "[Outro]"])
        lyrics_dialect = st.selectbox(T["t2_dialect"], ["عامية مصرية", "فصحى سينمائية", "خليجي", "شامي"])
        
    with col2:
        song_style = st.selectbox(T["t2_style"], ["Egyptian Rap", "Melodic Rap", "Pop", "Acoustic", "EDM"])
        vocal_type = st.selectbox(T["t2_vocal"], ["صوت رجالي بحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال"])
        audio_mixing = st.multiselect(T["t2_mix"], ["Heavy 808 Bass", "Reverb", "Stereo Width", "Delay"])
        song_mood = st.select_slider(T["t2_mood"], options=["حزين", "درامي", "متوازن", "حماسي", "صاخب"])

    if st.button(T["t2_btn"], type="primary", key="btn_s2"):
        if not song_idea:
            st.warning(T["t2_warn"])
        else:
            with st.spinner(T["t2_spin"]):
                prompt = f"Create song lyrics for theme: '{song_idea}', dialect: {lyrics_dialect}, style: {song_style} with mixing notes."
                generate_ai_response(prompt, category_name="Music" if lang=="English" else "أغاني", user_topic=song_idea[:25], tab_index=1)
                st.rerun()

    render_result_section(1)

# ----------------------------------------------------
# 3️⃣ مهندس الصور
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown(f"### {T['t3_title']}")
    
    render_inline_mic_helper("tab3_input")
    img_desc = st.text_input(T["t3_desc"], key="t3_field")
    
    img_engine = st.selectbox(T["t3_engine"], ["Midjourney v6", "Flux.1", "Leonardo AI", "DALL-E 3"])
    img_aspect = st.selectbox(T["t3_aspect"], ["16:9 عريض", "9:16 موبايل", "1:1 مربع", "4:5 إنستجرام"])
    
    if st.button(T["t3_btn"], type="primary", key="btn_s3"):
        if not img_desc:
            st.warning(T["t3_warn"])
        else:
            with st.spinner(T["t3_spin"]):
                prompt = f"Generate 3 pro image prompts for {img_engine} based on: '{img_desc}', aspect {img_aspect}."
                generate_ai_response(prompt, category_name="Image" if lang=="English" else "صور", user_topic=img_desc[:25], tab_index=2)
                st.rerun()

    render_result_section(2)

# ----------------------------------------------------
# 4️⃣ تحريك الفيديو
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown(f"### {T['t4_title']}")
    
    render_inline_mic_helper("tab4_input")
    a_script = st.text_area(T["t4_script"], height=100, key="t4_field")
    
    a_voice = st.selectbox(T["t4_voice"], ["صوت وثائقي فخم", "سريع وحماسي", "ودود وإخباري", "درامي مؤثر"])
    a_ai_tool = st.selectbox(T["t4_tool"], ["Runway Gen-3", "Luma Dream Machine", "HeyGen Avatar", "Pika Labs"])
    
    if st.button(T["t4_btn"], type="primary", key="btn_s4"):
        if not a_script:
            st.warning(T["t4_warn"])
        else:
            with st.spinner(T["t4_spin"]):
                prompt = f"Motion prompts for {a_ai_tool} and voiceover tone '{a_voice}' for script: '{a_script}'."
                generate_ai_response(prompt, category_name="Animation" if lang=="English" else "تحريك", user_topic=a_script[:25], tab_index=3)
                st.rerun()

    render_result_section(3)

# ----------------------------------------------------
# 5️⃣ التسويق والتريند
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown(f"### {T['t5_title']}")
    
    render_inline_mic_helper("tab5_input")
    m_topic = st.text_input(T["t5_topic"], key="t5_field")
    
    m_platform = st.selectbox(T["t5_platform"], ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook", "LinkedIn"])
    m_goal = st.selectbox(T["t5_goal"], ["التفاعل وبناء الجمهور", "المبيعات والتحويل", "نشر الوعي بالعلامة التجارية"])
    
    if st.button(T["t5_btn"], type="primary", key="btn_s5"):
        if not m_topic:
            st.warning(T["t5_warn"])
        else:
            with st.spinner(T["t5_spin"]):
                prompt = f"Marketing strategy and viral hashtags for '{m_topic}' on '{m_platform}' targeting '{m_goal}'."
                generate_ai_response(prompt, category_name="Marketing" if lang=="English" else "تسويق", user_topic=m_topic[:25], tab_index=4)
                st.rerun()

    render_result_section(4)
