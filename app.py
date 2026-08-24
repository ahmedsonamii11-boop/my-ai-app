# ==========================================
# 2. دالة الاتصال المباشر الشاملة (Multi-Model Fallback)
# ==========================================
def generate_ai_response(prompt_text):
    if not API_KEY:
        st.error("❌ لم يتم العثور على GEMINI_API_KEY في Streamlit Secrets!")
        return None

    # قائمة بأسماء الموديلات المتاحة على API v1beta
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001",
        "gemini-1.5-pro-latest"
    ]
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    last_error = ""
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        try:
            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()
            
            if response.status_code == 200:
                # نجاح الاتصال وتوليد النص
                return res_data['candidates'][0]['content']['parts'][0]['text']
            else:
                last_error = res_data.get('error', {}).get('message', 'خطأ غير معروف')
        except Exception as e:
            last_error = str(e)
            continue

    st.error(f"❌ خطأ من API: {last_error}")
    return None
