import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة والتصميم الاحترافي (Pro Dark Suite)
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي - Ultimate Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { color: #e0e0e0; }
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(138, 180, 248, 0.3);
    }
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #111418;
        border-right: 1px solid #21262d;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم الفوري
# ==========================================
HISTORY_FILE = "content_studio_ultimate_history.json"
FAV_FILE = "content_studio_ultimate_favorites.json"

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
# 2. القاموس (عربي / English)
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
        "main_caption": "منظومة إبداعية احترافية موسعة بالكامل مع تحكم صوتي متطور وخيارات غير محدودة",
        
        "tabs": [
            "1️⃣ 💡 الفكرة والسكريبت والخطافات",
            "2️⃣ 🎵 أستديو الأغاني والصوت الاحترافي",
            "3️⃣ 🎨 مهندس الصور والريزوليوشن القياسي",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار المتقدم",
            "5️⃣ 📊 التسويق وخطط المحتوى الاستراتيجية"
        ],
        
        "result_label": "🚀 النتيجة الفورية المنجزة:",
        "copy_btn": "📋 نسخ النص للحافظة",
        "download_txt": "📥 تحميل كملف نصي (.txt)",
        "rating_label": "⭐ تقييم جودة النتيجة:"
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
        "main_caption": "Expanded professional AI suite with voice control & rich custom options",
        
        "tabs": [
            "1️⃣ 💡 Ideas, Scripts & Hooks",
            "2️⃣ 🎵 Pro Suno Music & Audio",
            "3️⃣ 🎨 Image Prompts & Resolutions",
            "4️⃣ 🗣️ Advanced Video & Avatar",
            "5️⃣ 📊 Marketing & Strategies"
        ],
        
        "result_label": "🚀 Executed Result:",
        "copy_btn": "📋 Copy Text",
        "download_txt": "📥 Download (.txt)",
        "rating_label": "⭐ Rate Result:"
    }
}

# ==========================================
# 3. دالة الإدخال الصوتي المتطورة
# ==========================================
def floating_voice_textarea(label, session_key, placeholder="اكتب فكرتك أو اضغط مايك للتسجيل المستمر..."):
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
                        <button type="button" id="mic_btn_{session_key}" title="بدء التسجيل المستمر" style="background: #21262d; border: 1px solid #30363d; color: #58a6ff; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s;">
                            🎙️
                        </button>
                        <button type="button" id="stop_btn_{session_key}" title="إيقاف التسجيل" style="background: #21262d; border: 1px solid #f85149; color: #f85149; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; display: none; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s;">
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
                            alert("متصفحك لا يدعم التعرف الصوتي. يرجى استخدام Google Chrome.");
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
                        btn.style.background = '#21262d';
                        btn.style.color = '#58a6ff';
                        btn.style.borderColor = '#30363d';
                        btn.style.transform = 'scale(1.0)';
                        stopBtn.style.display = 'none';
                        waves.style.display = 'none';

                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        ta.blur();
                        ta.focus();
                    }}

                    btn.onclick = function() {{
                        if (!isRec) {{
                            startRecording();
                        }} else {{
                            stopRecordingProcess();
                        }}
                    }};

                    stopBtn.onclick = function() {{
                        stopRecordingProcess();
                    }};
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
def execute_ai_action(prompt_text, category_name="عام", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ لم يتم العثور على مفتاح GEMINI_API_KEY في ملف الـ Secrets!")
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
# 5. القائمة الجانبية
# ==========================================
with st.sidebar:
    lang = st.selectbox("🌐 اللغة / Language:", ["العربية", "English"])
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
                        st.toast("تمت الإضافة للمفضلة بنجاح!")

# ==========================================
# 6. الواجهة الرئيسية والتبويبات الموسعة
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
        st.info(f"📊 إحصائيات الناتج: {word_count} كلمة | {char_count} حرف")
        
        c_b1, c_b2, c_b3 = st.columns(3)
        with c_b1:
            if st.button(T["copy_btn"], key=f"cp_{res['id']}_{tab_idx}"):
                st.toast("تم النسخ بنجاح!")
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
# 1️⃣ فكرة وسكريبت والخطافات (موسع)
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown("### 🎬 صانع الفكرة، السكريبت التفصيلي، والـ Hook Generator الاحترافي")
    v_title = floating_voice_textarea("📽️ عنوان أو فكرة الفيديو الأساسية:", "t1_val", "اكتب فكرة الفيديو أو املِها بالمايك...")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        v_duration = st.selectbox("⏱️ مدة الفيديو التقديرية:", ["15 ثانية (Shorts/Reels)", "30 ثانية", "60 ثانية (TikTok/Reels)", "3 دقائق (YouTube Standard)", "10+ دقائق (Documentary/Long)"])
    with col_b:
        v_style = st.selectbox("🎨 النمط البصري والإلقائي:", ["سينمائي واقعي (Cinematic)", "وثائقي تشويقي (Documentary)", "كوميدي ساخر (Sarcastic/Comedy)", "تعليمي تفاعلي (Educational)", "حماسي تحفيزي (Motivational)"])
    with col_c:
        v_target = st.selectbox("🎯 الجمهور المستهدف:", ["الشباب والمراهقين (Gen Z)", "رواد الأعمال والمهنيين", "العامة والمهتمين بالترفيه", "الأطفال والعائلات"])
    
    if st.button("🔥 تنفيذ وتوليد السكريبت والخطافات", type="primary", key="action_btn_1"):
        if not v_title.strip():
            st.warning("⚠️ يرجى إدخال عنوان أو فكرة الفيديو أولاً!")
        else:
            with st.spinner("⚡ جارٍ توليد سكريبت احترافي وخطافات فيرال..."):
                prompt = f"Create a pro video script for '{v_title}', duration: {v_duration}, style: {v_style}, target audience: {v_target}, with viral hooks for the first 3 seconds, scene descriptions, and call-to-action."
                execute_ai_action(prompt, category_name="Script", user_topic=v_title[:25], tab_index=0)
                st.rerun()

    render_active_result(0)

# ----------------------------------------------------
# 2️⃣ أستديو الأغاني والصوت الاحترافي (موسع بالكامل)
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 1:
    st.markdown("### 🎵 صناعة الأغاني، الهندسة الصوتية، ومكتبة القوافي المتقدمة")
    song_idea = floating_voice_textarea("💡 فكرة الأغنية أو الموضوع الرئيسي:", "t2_val", "اكتب موضوع الأغنية أو تفاصيل الكلمات المطلوبة...")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        lyrics_dialect = st.selectbox("🗣️ اللهجة أو الطابع الثقافي:", ["عامية مصرية عصرية", "فصحى بلاغية", "خليجي طربي", "مغربي / شمال إفريقي", "إنجليزي غربي (English)"])
    with c2:
        song_style = st.selectbox("🎼 النمط الموسيقي (Music Genre):", ["مهرجانات / شعبي سريع (Mahraganat)", "راب / هيب هوب أندرجراوند (Rap/Hip-Hop)", "بوب عربي رومانسي (Pop)", "أكوستيك هادئ جيتار (Acoustic)", "إي دي إم إلكتروني راقص (EDM/Dance)", "لوفي تشิล هادئ (Lo-Fi Beats)"])
    with c3:
        vocal_type = st.selectbox("🎙️ صوت المغني والأداء (Vocal Profile):", ["صوت رجالي قوي وعميق (Deep Baritone)", "صوت شبابي حماسي ومرن (Energetic Tenor)", "صوت نسائي ناعم ودافئ (Warm Soprano)", "صوت روبوتي مدمج أوتوتيون (Auto-Tune / Robotic)", "جوقة جماعية حماسية (Choir/Harmonies)"])

    if st.button("✨ تنفيذ وتوليد الأغنية الكاملة والقوافي", type="primary", key="action_btn_2"):
        if not song_idea.strip():
            st.warning("⚠️ يرجى إدخال فكرة الأغنية أولاً!")
        else:
            with st.spinner("⚡ جارٍ صياغة الكلمات، هندسة المكس، وتحديد البرومبتات الصوتية..."):
                prompt = f"Create full song lyrics with structure (Verse, Chorus, Bridge, Outro), dialect: {lyrics_dialect}, music style: {song_style}, vocal profile: {vocal_type}, for theme: '{song_idea}'. Include Suno AI prompt tags and rhyme dictionary."
                execute_ai_action(prompt, category_name="Music", user_topic=song_idea[:25], tab_index=1)
                st.rerun()

    render_active_result(1)

# ----------------------------------------------------
# 3️⃣ مهندس الصور والريزوليوشن القياسي (موسع بالكامل)
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown("### 🎨 مهندس برومبتات الصور الاحترافية مع تحديد المقاسات والمنصات")
    img_desc = floating_voice_textarea("🖼️ وصف الصورة الخيالية أو المشهد بدقة:", "t3_val", "صف تفاصيل الصورة والألوان والإضاءة بدقة...")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        img_engine = st.selectbox("🎯 محرك الذكاء الاصطناعي للصور:", ["Midjourney v6 (أعلى جودة وسينمائية)", "Flux.1 (واقعية مذهلة وتفاصيل دقيقة)", "DALL-E 3 (فهم عميق للنصوص)", "Stable Diffusion XL (تحكم حر كامل)"])
    with c2:
        img_aspect = st.selectbox("📐 الأبعاد والريزوليوشن المناسب للمنصة:", [
            "9:16 (مناسب لـ TikTok / YouTube Shorts / Instagram Reels)", 
            "16:9 (مناسب لـ YouTube Videos / Desktop Wallpaper)", 
            "1:1 (مناسب لـ Instagram / Facebook Post)", 
            "4:5 (مناسب لـ Portrait Feed / IG Carousel)", 
            "21:9 (مناسب لـ Ultra-Wide Cinematic Banners)"
        ])
    with c3:
        img_lighting = st.selectbox("💡 نمط الإضاءة والجودة:", [
            "إضاءة استوديو سينمائية (Cinematic Studio Lighting)", 
            "إضاءة نيون سايبربانك (Cyberpunk Neon Glow)", 
            "إضاءة شمس طبيعية ساحرة (Golden Hour Natural)", 
            "مظلم درامي غامض (Dark Moody Atmosphere)", 
            "ألوان زاهية نابضة بالحياة (Vibrant & Pop Art)"
        ])

    if st.button("🎨 تنفيذ وتوليد برومبتات الصور الاحترافية", type="primary", key="action_btn_3"):
        if not img_desc.strip():
            st.warning("⚠️ يرجى إدخال وصف الصورة المطلوب!")
        else:
            with st.spinner("⚡ جارٍ هندسة الأوامر وتجهيز المقاسات المخصصة..."):
                prompt = f"Generate 3 pro image generation prompts for engine: {img_engine}, based on description: '{img_desc}', aspect ratio: {img_aspect}, lighting/mood: {img_lighting}. Provide English prompts ready to copy."
                execute_ai_action(prompt, category_name="Image", user_topic=img_desc[:25], tab_index=2)
                st.rerun()

    render_active_result(2)

# ----------------------------------------------------
# 4️⃣ تحريك الفيديو والأفاتار المتقدم (موسع)
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown("### 🗣️ محرك الفيديو، الأفاتار، وتحويل الصور لحركة (Motion Prompts)")
    a_script = floating_voice_textarea("📜 النص الإلقائي أو وصف الحركة البصرية:", "t4_val", "اكتب النص أو تفاصيل الحركة المطلوبة للكاميرا والأفاتار...")
    
    c1, c2 = st.columns(2)
    with c1:
        a_ai_tool = st.selectbox("🤖 أداة التحريك والأفاتار المستهدفة:", ["Runway Gen-3 (حركة سينمائية واقعية)", "Luma Dream Machine (حركات ديناميكية سريعة)", "HeyGen Avatar (أفاتار ناطق احترافي)", "Pika Labs (تأثيرات بصرية وموشن جرافيك)"])
    with c2:
        camera_motion = st.selectbox("🎥 حركة الكاميرا (Camera Movement):", ["زوم إن بطيء (Slow Zoom In)", "حركة بانورامية جانبية (Pan Right/Left)", "تتبع الحركة (Dynamic Tracking Shot)", "لقطة ثابتة مع تفاصيل حية (Static with Ambient Motion)"])

    if st.button("⚡ تنفيذ برومبتات التحريك", type="primary", key="action_btn_4"):
        if not a_script.strip():
            st.warning("⚠️ يرجى إدخال النص أو الحركة أولاً!")
        else:
            with st.spinner("⚡ جارٍ إعداد أوامر الحركة المتقدمة..."):
                prompt = f"Generate advanced motion and animation prompts for tool: {a_ai_tool}, camera movement: {camera_motion}, based on input script/desc: '{a_script}'."
                execute_ai_action(prompt, category_name="Animation", user_topic=a_script[:25], tab_index=3)
                st.rerun()

    render_active_result(3)

# ----------------------------------------------------
# 5️⃣ التسويق وخطط المحتوى الاستراتيجية (موسع)
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown("### 📊 استوديو التسويق، خطط المحتوى، والتريندات الاستراتيجية")
    m_topic = floating_voice_textarea("🎯 موضوع المحتوى أو المنتج المراد تسويقه:", "t5_val", "اكتب تفاصيل المنتج أو المشروع المراد وضع خطة له...")
    
    c1, c2 = st.columns(2)
    with c1:
        m_platform = st.selectbox("📱 المنصة المستهدفة للنشر:", ["TikTok (تريندات وفيديوهات قصيرة سريعة)", "Instagram Reels & Stories (بناء براند وبصريات)", "YouTube Shorts & Long (محتوى تعليمي وترفيهي متكامل)", "LinkedIn (تسويق احترافي وبزنس)", "Facebook Community (تفاعل جماهيري واسع)"])
    with c2:
        m_goal = st.selectbox("🎯 هدف الحملة التسويقية:", ["زيادة المبيعات والتحويلات (Sales Conversion)", "بناء الوعي بالعلامة التجارية (Brand Awareness)", "زيادة التفاعل والمشاركات (Engagement & Shares)", "جذب زيارات للموقع أو القناة (Traffic Generation)"])

    if st.button("🚀 تنفيذ الخطة التسويقية والتريند", type="primary", key="action_btn_5"):
        if not m_topic.strip():
            st.warning("⚠️ يرجى إدخال موضوع المحتوى أولاً!")
        else:
            with st.spinner("⚡ جارٍ تحليل السوق، وضع استراتيجية النشر واستخراج الهاشتاجات..."):
                prompt = f"Create a comprehensive marketing strategy, content calendar outline, viral hashtags, and growth tactics for topic/product: '{m_topic}', target platform: {m_platform}, main goal: {m_goal}."
                execute_ai_action(prompt, category_name="Marketing", user_topic=m_topic[:25], tab_index=4)
                st.rerun()

    render_active_result(4)
