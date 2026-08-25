import streamlit as st
import requests

st.set_page_config(page_title="استوديو التوليد الفوري", page_icon="🚀", layout="centered")

API_KEY = st.secrets.get("GEMINI_API_KEY")

st.title("🚀 استوديو الأكشن الفوري (Direct Action Mode)")
st.caption("اكتب طلبك أو فكرتك، واضغط إنتر أو زر التوليد عشان تشوف النتيجة قدامك حالاً بدون أي أعطال.")

# خانة إدخال مباشرة وواضحة جداً بعيدة عن أي تعقيد جافاسكريبت
user_prompt = st.text_area("✍️ اكتب هنا فكرة الفيديو، الأغنية، أو المحتوى المراد تنفيذه:", height=120)

col1, col2 = st.columns(2)
with col1:
    action_type = st.selectbox("🎯 حدد نوع العملية المطلوبة:", [
        "توليد سكريبت فيديو مع خطافات", 
        "تأليف كلمات أغنية وقوافي", 
        "كتابة برومبتات صور احترافية", 
        "خطة تسويق وتريندات"
    ])
with col2:
    creativity = st.slider("🎚️ درجة الإبداع:", 0.1, 1.0, 0.7)

# زر التوليد الصريح الذي يقود للأكشن الفوري
if st.button("🔥 تنفيذ الأكشن وتوليد النتيجة فوراً", type="primary", use_container_width=True):
    if not user_prompt.strip():
        st.warning("⚠️ يرجى كتابة النص أو الفكرة أولاً ليتم تنفيذ الأكشن!")
    else:
        if not API_KEY:
            st.error("❌ مفتاح GEMINI_API_KEY غير موجود في إعدادات Secrets.")
        else:
            with st.spinner("⚡ جارٍ الاتصال بالخادم وتنفيذ الأكشن المطلوب..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                full_query = f"Act as an expert creator. Task: {action_type}. Details: {user_prompt}"
                payload = {"contents": [{"parts": [{"text": full_query}]}]}
                
                try:
                    response = requests.post(url, json=payload, headers=headers)
                    res_data = response.json()
                    
                    if response.status_code == 200:
                        output_result = res_data['candidates'][0]['content']['parts'][0]['text']
                        st.success("✅ تم تنفيذ الأكشن بنجاح وإليك النتيجة:")
                        st.markdown("---")
                        st.markdown(output_result)
                        st.markdown("---")
                        st.download_button("📥 تحميل النتيجة كملف نصي", output_result, file_name="action_result.txt", mime="text/plain")
                    else:
                        error_msg = res_data.get('error', {}).get('message', 'خطأ غير معروف')
                        st.error(f"❌ حدث خطأ من الخادم: {error_msg}")
                except Exception as e:
                    st.error(f"❌ حدث خطأ في الاتصال: {str(e)}")
