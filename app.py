import streamlit as st
import requests
import json
import os
from datetime import datetime

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="استوديو المحتوى الذكي - Floating Mic Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = st.secrets.get("GEMINI_API_KEY")

# ==========================================
# نظام الحفظ الدائم
# ==========================================
HISTORY_FILE = "content_studio_float_history.json"
FAV_FILE = "content_studio_float_favorites.json"

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
        "fav_title": "⭐ المفضلة",
        "fav_empty": "لا توجد عناصر مفضلة",
        "history_title": "📜 سجل العمليات (حفظ دائم)",
        "history_empty": "السجل فارغ",
        "clear_history": "🗑️ مسح السجل بالكامل",
        "stats_title": "📊 لوحة الإحصائيات",
        "stat_total": "إجمالي الأعمال المُنجزة:",
        "main_title": "🎙️ استوديو المحتوى الذكي (Floating Voice Pro)",
        "main_caption": "المنظومة الاحترافية المزودة بزر المايك والترددات المدمجة داخل خانة النص",
        
        "tabs": [
            "1️⃣ 💡 فكرة وسكريبت والخطافات",
            "2️⃣ 🎵 أستديو الأغاني والصوت",
            "3️⃣ 🎨 مهندس الصور الاحترافي",
            "4️⃣ 🗣️ تحريك الفيديو والأفاتار",
            "5️⃣ 📊 التسويق والتريندات"
        ],
        
        "t1_title": "🎬 صانع الفكرة، السكريبت التفصيلي، والـ Hook Generator",
        "t1_input": "📽️ عنوان أو فكرة الفيديو الأساسية (استخدم مايك اليمين للتحدث):",
        "t1_dur": "⏱️ مدة الفيديو التقديرية:",
        "t1_style": "🎨 النمط البصري:",
        "t1_btn": "🔥 تنفيذ وتوليد السكريبت والخطافات",
        "t1_warn": "⚠️ يرجى إدخال عنوان أو فكرة الفيديو أولاً!",
        "t1_spin": "⚡ جارٍ توليد السكريبت بواسطة Gemini 3.6 Flash...",

        "t2_title": "🎵 صناعة الأغاني، الهندسة الصوتية، ومكتبة القوافي",
        "t2_idea": "💡 فكرة الأغنية أو الموضوع الرئيسي:",
        "t2_dialect": "🗣️ اللهجة أو الطابع الثقافي:",
        "t2_style": "🎼 النمط الموسيقي:",
        "t2_btn": "✨ تنفيذ وتوليد الأغنية الكاملة والقوافي",
        "t2_warn": "⚠️ يرجى إدخال فكرة الأغنية أولاً!",
        "t2_spin": "⚡ جارٍ صياغة الكلمات وهندسة المكس...",

        "t3_title": "🎨 مهندس برومبتات الصور الاحترافية",
        "t3_desc": "🖼️ وصف الصورة الخيالية بدقة:",
        "t3_engine": "🎯 محرك الذكاء الاصطناعي للصور:",
        "t3_aspect": "📐 أبعاد ومقاسات الصورة:",
        "t3_btn": "🎨 تنفيذ وتوليد برومبتات الصور",
        "t3_warn": "⚠️ يرجى إدخال وصف الصورة المطلوب!",
        "t3_spin": "⚡ جارٍ هندسة الأوامر البصرية...",

        "t4_title": "🗣️ محرك الفيديو، الأفاتار، وتحويل الصور لحركة",
        "t4_script": "📜 النص الإلقائي أو أوامر الحركة الأساسية:",
        "t4_tool": "🤖 أداة التحريك والأفاتار المستهدفة:",
        "t4_btn": "⚡ تنفيذ برومبتات التحريك",
        "t4_warn": "⚠️ يرجى إدخال النص أولاً!",
        "t4_spin": "⚡ جارٍ إعداد أوامر الـ Animation...",

        "t5_title": "📊 استوديو التسويق، خطط المحتوى، والتريندات",
        "t5_topic": "🎯 موضوع المحتوى أو المنتج المراد تسويقه:",
        "t5_platform": "📱 المنصة المستهدفة للنشر:",
        "t5_btn": "🚀 تنفيذ الخطة التسويقية والتريند",
        "t5_warn": "⚠️ يرجى إدخال موضوع المحتوى!",
        "t5_spin": "⚡ جارٍ تحليل السوق واستخراج الهاشتاجات...",
        
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
        "main_title": "🎙️ Smart Content Studio (Floating Voice Pro)",
        "main_caption": "Professional system with built-in mic and waveforms inside the text box",
        
        "tabs": [
            "1️⃣ 💡 Idea, Script & Hooks",
            "2️⃣ 🎵 Suno Music & Audio",
            "3️⃣ 🎨 Image Prompt Engineer",
            "4️⃣ 🗣️ Video & Avatar Animation",
            "5️⃣ 📊 Marketing & Trends"
        ],
        
        "t1_title": "🎬 Idea Generator, Script, & Viral Hooks",
        "t1_input": "📽️ Video Title or Core Idea (Use right mic to speak):",
        "t1_dur": "⏱️ Estimated Duration:",
        "t1_style": "🎨 Visual Style:",
        "t1_btn": "🔥 Execute Script & Hooks",
        "t1_warn": "⚠️ Please enter video title!",
        "t1_spin": "⚡ Generating professional script...",

        "t2_title": "🎵 Music Production & Sound Engineering",
        "t2_idea": "💡 Song Idea or Theme:",
        "t2_dialect": "🗣️ Dialect:",
        "t2_style": "🎼 Main Music Style:",
        "t2_btn": "✨ Execute Full Song",
        "t2_warn": "⚠️ Please enter the song idea!",
        "t2_spin": "⚡ Crafting lyrics...",

        "t3_title": "🎨 Professional Image Prompt Engineer",
        "t3_desc": "🖼️ Describe your imagined image:",
        "t3_engine": "🎯 AI Image Engine:",
        "t3_aspect": "📐 Aspect Ratio:",
        "t3_btn": "🎨 Execute Pro Prompts",
        "t3_warn": "⚠️ Please enter image description!",
        "t3_spin": "⚡ Engineering visual prompts...",

        "t4_title": "Video Engine & Avatar Animation",
        "t4_script": "📜 Voiceover Text or Motion Commands:",
        "t4_tool": "🤖 Target Animation Tool:",
        "t4_btn": "⚡ Execute Motion Prompts",
        "t4_warn": "⚠️ Please enter text first!",
        "t4_spin": "⚡ Preparing motion prompts...",

        "t5_title": "📊 Marketing & Content Plans",
        "t5_topic": "🎯 Content Topic:",
        "t5_platform": "📱 Target Platform:",
        "t5_btn": "🚀 Execute Marketing Plan",
        "t5_warn": "⚠️ Please enter content topic!",
        "t5_spin": "⚡ Analyzing market strategy...",
        
        "result_label": "🚀 Executed Result:",
        "copy_btn": "📋 Copy Text",
        "download_txt": "📥 Download (.txt)",
        "rating_label": "⭐ Rate Result:"
    }
}

# ==========================================
# 3. دالة خانة النص المدمجة مع المايك العائم
# ==========================================
def floating_voice_textarea(label, session_key, placeholder="اكتب فكرتك أو اضغط مايك اليمين..."):
    # خانة النص العادية من Streamlit
    val = st.text_area(label, value=st.session_state.get(session_key, ""), key=session_key, height=120, placeholder=placeholder)
    
    # حقن كود جافاسكريبت و CSS لتثبيت زر المايك والترددات في الزاوية اليمنى السفلى داخل حقل النص مباشرة
    components_code = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const textAreas = doc.querySelectorAll('textarea');
        
        textAreas.forEach((ta) => {{
            if (ta.getAttribute('aria-label') === `{label}` || ta.placeholder === `{placeholder}`) {{
                const wrapper = ta.closest('.stTextArea') || ta.parentElement;
                
                if (wrapper && !wrapper.querySelector('.floating-mic-container_{session_key}')) {{
                    // إنشاء الحاوية العائمة في اليمين تحت
                    const micDiv = doc.createElement('div');
                    micDiv.className = 'floating-mic-container_{session_key}';
                    micDiv.style.cssText = "position: absolute; bottom: 12px; right: 12px; display: flex; align-items: center; gap: 8px; z-index: 999;";
                    
                    micDiv.innerHTML = `
                        <div id="waves_{session_key}" style="display: none; align-items: center; gap: 3px; height: 16px; background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 10px;">
                            <div style="width: 3px; background: #ea4335; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out;"></div>
                            <div style="width: 3px; background: #ea4335; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.15s;"></div>
                            <div style="width: 3px; background: #ea4335; border-radius: 2px; animation: waveA 0.6s infinite ease-in-out 0.3s;"></div>
                        </div>
                        <button type="button" id="mic_btn_{session_key}" title="تحدث بالصوت" style="background: #2b2d31; border: 1px solid #5f6368; color: #8ab4f8; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); transition: 0.2s;">
                            🎙️
                        </button>
                    `;
                    
                    // إضافة أسلوب الحركة للترددات
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
                    const waves = micDiv.querySelector('#waves_{session_key}');

                    btn.onclick = function() {{
                        const SpeechRecognition = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
                        if (!SpeechRecognition) {{
                            alert("متصفحك لا يدعم التعرف الصوتي. يرجى استخدام Google Chrome.");
                            return;
                        }}

                        if (!isRec) {{
                            recognition = new SpeechRecognition();
                            recognition.lang = 'ar-EG';
                            recognition.interimResults = true;
                            recognition.continuous = true;

                            recognition.onstart = function() {{
                                isRec = true;
                                btn.style.background = '#ea4335';
                                btn.style.color = '#fff';
                                btn.style.borderColor = '#ff8580';
                                btn.style.transform = 'scale(1.1)';
                                waves.style.display = 'flex';
                            }};

                            recognition.onresult = function(e) {{
                                let transcript = '';
                                for (let i = e.resultIndex; i < e.results.length; ++i) {{
                                    transcript += e.results[i][0].transcript;
                                }}
                                ta.value = (ta.value ? ta.value + ' ' : '') + transcript;
                                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }};

                            recognition.onerror = function() {{ stopRec(); }};
                            recognition.onend = function() {{ stopRec(); }};

                            try {{ recognition.start(); }} catch(err) {{ console.log(err); }}
                        }} else {{
                            if (recognition) recognition.stop();
                            stopRec();
                        }}
                    }};

                    function stopRec() {{
                        isRec = false;
                        btn.style.background = '#2b2d31';
                        btn.style.color = '#8ab4f8';
                        btn.style.borderColor = '#5f6368';
                        btn.style.transform = 'scale(1.0)';
                        waves.style.display = 'none';
                    }}
                }}
            }
        }});
    }})();
    </script>
    """
    st.components.v1.html(components_code, height=0, width=0)
    return val

# ==========================================
# 4. دالة الاتصال بنموذج Gemini 3.6 Flash
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
                        st.toast("تمت الإضافة للمفضلة!")

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
# 1️⃣ فكرة وسكريبت والخطافات
# ----------------------------------------------------
if st.session_state["selected_tab"] == 0:
    st.markdown(f"### {T['t1_title']}")
    
    # استدعاء خانة النص مع المايك العائم على اليمين تحت
    v_title = floating_voice_textarea(T['t1_input'], "t1_val", "اكتب أو اضغط مايك اليمين للتحدث...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_duration = st.selectbox(T["t1_dur"], ["30 ثانية", "60 ثانية", "3 دقائق"])
    with col_b:
        v_style = st.selectbox(T["t1_style"], ["سينمائي واقعي", "وثائقي", "كوميدي ساخر"])
    
    if st.button(T["t1_btn"], type="primary", key="action_btn_1"):
        if not v_title.strip():
            st.warning(T["t1_warn"])
        else:
            with st.spinner(T["t1_spin"]):
                prompt = f"Create a professional script for '{v_title}', duration {v_duration}, style {v_style}, with viral hooks for the first 3 seconds."
                execute_ai_action(prompt, category_name="Script", user_topic=v_title[:25], tab_index=0)
                st.rerun()

    render_active_result(0)

# ----------------------------------------------------
# 2️⃣ أستديو الأغاني والصوت
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 1:
    st.markdown(f"### {T['t2_title']}")
    
    song_idea = floating_voice_textarea(T['t2_idea'], "t2_val", "اكتب فكرة الأغنية أو تحدث بالمايك...")
    
    c1, c2 = st.columns(2)
    with c1:
        lyrics_dialect = st.selectbox(T["t2_dialect"], ["عامية مصرية", "فصحى", "خليجي"])
    with c2:
        song_style = st.selectbox(T["t2_style"], ["Rap", "Pop", "Acoustic", "EDM"])

    if st.button(T["t2_btn"], type="primary", key="action_btn_2"):
        if not song_idea.strip():
            st.warning(T["t2_warn"])
        else:
            with st.spinner(T["t2_spin"]):
                prompt = f"Create song lyrics and rhyme dictionary for theme: '{song_idea}', dialect: {lyrics_dialect}, style: {song_style}."
                execute_ai_action(prompt, category_name="Music", user_topic=song_idea[:25], tab_index=1)
                st.rerun()

    render_active_result(1)

# ----------------------------------------------------
# 3️⃣ مهندس الصور الاحترافي
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 2:
    st.markdown(f"### {T['t3_title']}")
    
    img_desc = floating_voice_textarea(T['t3_desc'], "t3_val", "صف صورتك بالتفصيل كتابةً أو بالمايك...")
    
    c1, c2 = st.columns(2)
    with c1:
        img_engine = st.selectbox(T["t3_engine"], ["Midjourney v6", "Flux.1", "DALL-E 3"])
    with c2:
        img_aspect = st.selectbox(T["t3_aspect"], ["16:9 عريض", "9:16 موبايل", "1:1 مربع"])
    
    if st.button(T["t3_btn"], type="primary", key="action_btn_3"):
        if not img_desc.strip():
            st.warning(T["t3_warn"])
        else:
            with st.spinner(T["t3_spin"]):
                prompt = f"Generate 3 pro image prompts for {img_engine} based on: '{img_desc}', aspect ratio {img_aspect}."
                execute_ai_action(prompt, category_name="Image", user_topic=img_desc[:25], tab_index=2)
                st.rerun()

    render_active_result(2)

# ----------------------------------------------------
# 4️⃣ تحريك الفيديو والأفاتار
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 3:
    st.markdown(f"### {T['t4_title']}")
    
    a_script = floating_voice_textarea(T['t4_script'], "t4_val", "أدخل النص أو أملِهِ بالمايك العائم...")
    a_ai_tool = st.selectbox(T["t4_tool"], ["Runway Gen-3", "Luma Dream Machine", "HeyGen Avatar"])
    
    if st.button(T["t4_btn"], type="primary", key="action_btn_4"):
        if not a_script.strip():
            st.warning(T["t4_warn"])
        else:
            with st.spinner(T["t4_spin"]):
                prompt = f"Motion and animation prompts for {a_ai_tool} based on script: '{a_script}'."
                execute_ai_action(prompt, category_name="Animation", user_topic=a_script[:25], tab_index=3)
                st.rerun()

    render_active_result(3)

# ----------------------------------------------------
# 5️⃣ التسويق والتريندات
# ----------------------------------------------------
elif st.session_state["selected_tab"] == 4:
    st.markdown(f"### {T['t5_title']}")
    
    m_topic = floating_voice_textarea(T['t5_topic'], "t5_val", "اكتب أو تحدث بموضوع الحملة التسويقية...")
    m_platform = st.selectbox(T["t5_platform"], ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn"])
    
    if st.button(T["t5_btn"], type="primary", key="action_btn_5"):
        if not m_topic.strip():
            st.warning(T["t5_warn"])
        else:
            with st.spinner(T["t5_spin"]):
                prompt = f"Create a marketing strategy and viral hashtags for '{m_topic}' on platform '{m_platform}'."
                execute_ai_action(prompt, category_name="Marketing", user_topic=m_topic[:25], tab_index=4)
                st.rerun()

    render_active_result(4)
