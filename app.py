import streamlit as st
import requests
import json
import os
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي الشامل - Pro Max",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم
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

for key in ["t1_input_val", "t2_input_val", "t3_input_val", "t4_input_val", "t5_input_val"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ==========================================
# 2. القاموس (عربي / English)
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
        "main_caption": "المنظومة الاحترافية مع خانة الإدخال الصوتية المدمجة كقطعة واحدة",
        
        "tabs": [
            "1️⃣ 💡 فكرة وسكريبت والخطافات",
            "2️⃣ 🎵 أستديو الأغاني والصوت",
            "3️⃣ 🎨 مهندس الصور الاحترافي",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار",
            "5️⃣ 📊 التسويق والتريندات"
        ],
        
        "t1_title": "🎬 صانع الفكرة، السكريبت التفصيلي، والـ Hook Generator",
        "t1_input": "📽️ عنوان أو فكرة الفيديو الأساسية:",
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
        "t4_script": "📜 النص الإلقائي أو أوامر الحركة الأساسية:",
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
        "main_caption": "Professional system with unified voice input box",
        
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

        "t4_title": "Video Engine & Avatar Animation",
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

# ==========================================
# 3. صندوق الإدخال الموحد (Gemini Style Box)
# ==========================================
def unified_voice_textarea(label_text, session_key, placeholder="اكتب فكرتك أو اضغط على المิاك وتحدث..."):
    current_val = st.session_state.get(session_key, "")
    
    # سنقوم بإنشاء عنصر مرئي متكامل يحتوي على الليبل، المربع الأسود الكبير، أزرار المايك بالأسفل تماماً بداخل نفس الإطار
    html_code = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                background-color: transparent;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .field-label {{
                font-weight: 600;
                color: #e2e8f0;
                font-size: 1.05rem;
                margin-bottom: 8px;
                display: block;
            }}
            .gemini-box-container {{
                display: flex;
                flex-direction: column;
                background-color: #1e1f22;
                border: 2px solid #444746;
                border-radius: 16px;
                padding: 12px 16px;
                gap: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
                transition: border-color 0.3s;
            }}
            .gemini-box-container:focus-within {{
                border-color: #8ab4f8;
            }}
            .gemini-textarea {{
                background: transparent;
                border: none;
                color: #e3e3e3;
                width: 100%;
                outline: none;
                font-size: 1.1rem;
                resize: vertical;
                min-height: 100px;
                font-family: inherit;
                line-height: 1.5;
            }}
            .toolbar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-top: 1px solid #333538;
                padding-top: 8px;
            }}
            .tools-left {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .icon-btn {{
                background: transparent;
                border: none;
                color: #c4c7c5;
                cursor: pointer;
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 6px 14px;
                border-radius: 20px;
                transition: background 0.2s, color 0.2s;
                gap: 6px;
            }}
            .icon-btn:hover {{
                background: rgba(255, 255, 255, 0.12);
                color: #ffffff;
            }}
            .mic-btn {{
                color: #8ab4f8;
                background: rgba(138, 180, 248, 0.1);
            }}
            .stop-btn {{
                color: #ea4335;
                display: none;
                background: rgba(234, 67, 53, 0.15);
            }}
            .waveform {{
                display: none;
                align-items: center;
                gap: 3px;
                height: 18px;
                padding: 0 8px;
            }}
            .wave-bar {{
                width: 3px;
                background-color: #ea4335;
                border-radius: 2px;
                animation: waveAnim 1s infinite ease-in-out;
            }}
            .wave-bar:nth-child(2) {{ animation-delay: 0.2s; }}
            .wave-bar:nth-child(3) {{ animation-delay: 0.4s; }}
            .wave-bar:nth-child(4) {{ animation-delay: 0.1s; }}
            .wave-bar:nth-child(5) {{ animation-delay: 0.3s; }}

            @keyframes waveAnim {{
                0%, 100% {{ height: 4px; }}
                50% {{ height: 18px; }}
            }}
        </style>
    </head>
    <body>
        <div class="field-label">{label_text}</div>
        <div class="gemini-box-container">
            <textarea class="gemini-textarea" id="mainTextArea" placeholder="{placeholder}" oninput="syncVal(this.value)">{current_val}</textarea>
            
            <div class="toolbar">
                <div class="tools-left">
                    <button type="button" class="icon-btn mic-btn" id="micBtn" onclick="startRecording()">
                        🎤 <span>تحدث بصوتك</span>
                    </button>
                    
                    <button type="button" class="icon-btn stop-btn" id="stopBtn" onclick="stopRecording()">
                        ⏹️ <span>إيقاف المايك</span>
                    </button>

                    <div class="waveform" id="waveContainer">
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                    </div>
                </div>
            </div>
        </div>

        <script>
        let recognition = null;
        let isRecording = false;

        function syncVal(val) {{
            const hiddenBox = window.parent.document.querySelector('textarea[data-baseweb="textarea"][aria-label*="{session_key}"]') || 
                              window.parent.document.getElementById('hidden_{session_key}');
            if (hiddenBox) {{
                hiddenBox.value = val;
                hiddenBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
                hiddenBox.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}

        function startRecording() {{
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                alert("متصفحك لا يدعم الإدخال الصوتي، يرجى استخدام متصفح Google Chrome.");
                return;
            }}
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'ar-EG';
            recognition.interimResults = false;
            recognition.continuous = true;
            
            const micBtn = document.getElementById('micBtn');
            const stopBtn = document.getElementById('stopBtn');
            const waveContainer = document.getElementById('waveContainer');
            const mainTextArea = document.getElementById('mainTextArea');
            
            recognition.onstart = function() {{
                isRecording = true;
                micBtn.style.display = 'none';
                stopBtn.style.display = 'flex';
                waveContainer.style.display = 'flex';
                mainTextArea.placeholder = "جاري الاستماع... تحدث براحتك 🎙️";
            }};
            
            recognition.onresult = function(event) {{
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    if (event.results[i].isFinal) {{
                        finalTranscript += event.results[i][0].transcript + ' ';
                    }}
                }}
                if (finalTranscript.trim() !== '') {{
                    let currentText = mainTextArea.value;
                    if (currentText.length > 0 && !currentText.endsWith(' ')) {{
                        currentText += ' ';
                    }}
                    mainTextArea.value = currentText + finalTranscript;
                    syncVal(mainTextArea.value);
                }}
            }};
            
            recognition.onerror = function() {{
                stopRecording();
            }};
            
            recognition.onend = function() {{
                if (isRecording) {{
                    try {{ recognition.start(); }} catch(e) {{}}
                }}
            }};
            
            recognition.start();
        }}

        function stopRecording() {{
            isRecording = false;
            if (recognition) {{
                recognition.stop();
            }}
            
            const micBtn = document.getElementById('micBtn');
            const stopBtn = document.getElementById('stopBtn');
            const waveContainer = document.getElementById('waveContainer');
            const mainTextArea = document.getElementById('mainTextArea');
            
            micBtn.style.display = 'flex';
            stopBtn.style.display = 'none';
            waveContainer.style.display = 'none';
            mainTextArea.placeholder = "{placeholder}";
        }}
        </script>
    </body>
    </html>
    """
    # عرض الحاوية المدمجة
    components.html(html_code, height=170)
    
    # حقل مخفي لربط القيمة بـ Streamlit Session State بدقة تامة
    hidden_val = st.text_area("", value=current_val, key=f"hidden_{session_key}", label_visibility="collapsed")
    if hidden_val != current_val:
        st.session_state[session_key] = hidden_val
    return st.session_state[session_key]

# ==========================================
# 4. دالة الـ API
# ==========================================
def generate_ai_response(prompt_text, category_name="عام", user_topic="", tab_index=0):
    if not API_KEY:
        st.error("❌ لم يتم العثور على GEMINI_API_KEY في إعدادات Streamlit Secrets!")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
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
# 6. الواجهة الرئيسية
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
# 1️⃣ فكرة وسكريبت والخطافات
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_title']}")
    
    # الصندوق الموحد للفكرة (جواه مربع الكتابة + زرار المايك في الأسفل كقطعة واحدة)
    v_title = unified_voice_textarea(T['t1_input'], "t1_input_val", "اكتب فكرتك هنا أو اضغط 'تحدث بصوتك' لتتحول لكتابة تلقائياً...")
    
    # المدة والنمط تحتها
    v_duration = st.select_slider(T["t1_dur"], options=["15 ثانية", "30 ثانية", "60 ثانية", "3 دقائق", "بودكاست"])
    v_style = st.selectbox(T["t1_style"], ["سينمائي واقعي", "3D Animation", "Dark Fantasy", "Cyberpunk", "وثائقي"])
    v_hook_enabled = st.checkbox(T["t1_hook"], value=True)
    
    if st.button(T["t1_btn"], type="primary", key="btn_s1"):
        if not v_title.strip():
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
    
    song_idea = unified_voice_textarea(T['t2_idea'], "t2_input_val", "اكتب فكرة الأغنية أو اضغط زر المايك للتحدث...")
    
    col1, col2 = st.columns(2)
    with col1:
        song_structure = st.multiselect(T["t2_struct"], ["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Outro]"], default=["[Intro]", "[Verse 1]", "[Chorus]", "[Outro]"])
        lyrics_dialect = st.selectbox(T["t2_dialect"], ["عامية مصرية", "فصحى سينمائية", "خليجي", "شامي"])
        
    with col2:
        song_style = st.selectbox(T["t2_style"], ["Egyptian Rap", "Melodic Rap", "Pop", "Acoustic", "EDM"])
        vocal_type = st.selectbox(T["t2_vocal"], ["صوت رجالي بحوح", "صوت أنثوي قوي", "Auto-tune Rap Flow", "كورال"])
        audio_mixing = st.multiselect(T["t2_mix"], ["Heavy 808 Bass", "Reverb", "Stereo Width", "Delay"])
        song_mood = st.select_slider(T["t2_mood"], options=["حزين", "درامي", "متوازن", "حماسي", "صاخب"])

    if st.button(T["t2_btn"], type="primary", key="btn_s2"):
        if not song_idea.strip():
            st.warning(T["t2_warn"])
        else:
            with st.spinner(T["t2_spin"]):
                prompt = f"Create song lyrics and rhyme dictionary for theme: '{song_idea}', dialect: {lyrics_dialect}, style: {song_style} with mixing notes."
                generate_ai_response(prompt, category_name="Music" if lang=="English" else "أغاني", user_topic=song_idea[:25], tab_index=1)
                st.rerun()

    render_result_section(1)

# ----------------------------------------------------
# 3️⃣ مهندس الصور الاحترافي
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown(f"### {T['t3_title']}")
    
    img_desc = unified_voice_textarea(T['t3_desc'], "t3_input_val", "صف صورتك بالتفصيل أو استخدم زر المايك للإملاء الصوتي...")
    
    img_engine = st.selectbox(T["t3_engine"], ["Midjourney v6", "Flux.1", "Leonardo AI", "DALL-E 3"])
    img_aspect = st.selectbox(T["t3_aspect"], ["16:9 عريض", "9:16 موبايل", "1:1 مربع", "4:5 إنستجرام"])
    
    if st.button(T["t3_btn"], type="primary", key="btn_s3"):
        if not img_desc.strip():
            st.warning(T["t3_warn"])
        else:
            with st.spinner(T["t3_spin"]):
                prompt = f"Generate 3 pro image prompts for {img_engine} based on: '{img_desc}', aspect {img_aspect}."
                generate_ai_response(prompt, category_name="Image" if lang=="English" else "صور", user_topic=img_desc[:25], tab_index=2)
                st.rerun()

    render_result_section(2)

# ----------------------------------------------------
# 4️⃣ تحريك الفيديو والأفاتار
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown(f"### {T['t4_title']}")
    
    a_script = unified_voice_textarea(T['t4_script'], "t4_input_val", "اكتب النص أو تحدث عبر المايك مباشرة...")
    
    a_voice = st.selectbox(T["t4_voice"], ["صوت وثائقي فخم", "سريع وحماسي", "ودود وإخباري", "درامي مؤثر"])
    a_ai_tool = st.selectbox(T["t4_tool"], ["Runway Gen-3", "Luma Dream Machine", "HeyGen Avatar", "Pika Labs"])
    
    if st.button(T["t4_btn"], type="primary", key="btn_s4"):
        if not a_script.strip():
            st.warning(T["t4_warn"])
        else:
            with st.spinner(T["t4_spin"]):
                prompt = f"Motion prompts for {a_ai_tool} and voiceover tone '{a_voice}' for script: '{a_script}'."
                generate_ai_response(prompt, category_name="Animation" if lang=="English" else "تحريك", user_topic=a_script[:25], tab_index=3)
                st.rerun()

    render_result_section(3)

# ----------------------------------------------------
# 5️⃣ التسويق والتريندات
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown(f"### {T['t5_title']}")
    
    m_topic = unified_voice_textarea(T['t5_topic'], "t5_input_val", "اكتب موضوع المحتوى أو استخدم المايك...")
    
    m_platform = st.selectbox(T["t5_platform"], ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook", "LinkedIn"])
    m_goal = st.selectbox(T["t5_goal"], ["التفاعل وبناء الجمهور", "المبيعات والتحويل", "نشر الوعي بالعلامة التجارية"])
    
    if st.button(T["t5_btn"], type="primary", key="btn_s5"):
        if not m_topic.strip():
            st.warning(T["t5_warn"])
        else:
            with st.spinner(T["t5_spin"]):
                prompt = f"Marketing strategy and viral hashtags for '{m_topic}' on '{m_platform}' targeting '{m_goal}'."
                generate_ai_response(prompt, category_name="Marketing" if lang=="English" else "تسويق", user_topic=m_topic[:25], tab_index=4)
                st.rerun()

    render_result_section(4)
