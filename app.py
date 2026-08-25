save_data(HISTORY_FILE, str_lit.session_state["history"])
            return output_text
        else:
            str_lit.error(f"API Error: {res_data}")
    except Exception as e:
        str_lit.error(f"Connection Error: {e}")
    return None

# ==========================================
# 6. الشريط الجانبي (Sidebar & Control Center)
# ==========================================
with str_lit.sidebar:
    lang_choice = str_lit.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English"])
    
    # تحديث لغة الواجهة والنتائج عند التبديل الفوري
    if lang_choice != str_lit.session_state["last_lang"]:
        if str_lit.session_state["current_result"]:
            str_lit.session_state["current_result"] = translate_text(str_lit.session_state["current_result"], lang_choice)
        str_lit.session_state["last_lang"] = lang_choice
        str_lit.rerun()

    T = TEXTS[lang_choice]

    str_lit.markdown(f"### {T['sidebar_title']}")
    
    # مؤشرات الأداء والإحصائيات
    str_lit.markdown(f"### {T['stats_title']}")
    total_tasks = len(str_lit.session_state["history"])
    str_lit.info(f"{T['stat_total']} **{total_tasks}**")
    
    str_lit.markdown("---")
    
    # بحث متقدم في السجل
    search_query = str_lit.text_input(T["search_label"], "")
    
    # العناصر المفضلة
    str_lit.markdown(f"### {T['fav_title']}")
    favs = str_lit.session_state["favorites"]
    if favs:
        for idx, fav in enumerate(favs):
            with str_lit.expander(f"⭐ {fav.get('topic', 'Favorite')[:30]}..."):
                str_lit.write(fav.get("result", ""))
                if str_lit.button(f"🗑️ Remove #{idx}", key=f"rm_fav_{idx}"):
                    str_lit.session_state["favorites"].pop(idx)
                    save_data(FAV_FILE, str_lit.session_state["favorites"])
                    str_lit.rerun()
    else:
        str_lit.caption(T["fav_empty"])

    str_lit.markdown("---")

    # الأرشيف والسجل الكامل
    str_lit.markdown(f"### {T['history_title']}")
    history_items = str_lit.session_state["history"]
    
    if history_items:
        if str_lit.button(T["clear_history"]):
            str_lit.session_state["history"] = []
            save_data(HISTORY_FILE, [])
            str_lit.rerun()
            
        for item in history_items:
            if search_query and search_query.lower() not in item['topic'].lower() and search_query.lower() not in item['result'].lower():
                continue
            with str_lit.expander(f"[{item['category']}] {item['topic'][:25]}... ({item['timestamp']})"):
                str_lit.write(item['result'])
                col_h1, col_h2 = str_lit.columns(2)
                with col_h1:
                    if str_lit.button("📂 Load", key=f"load_{item['id']}"):
                        str_lit.session_state["current_result"] = item['result']
                        str_lit.rerun()
                with col_h2:
                    if str_lit.button("⭐ Save Fav", key=f"fav_{item['id']}"):
                        if item not in str_lit.session_state["favorites"]:
                            str_lit.session_state["favorites"].append(item)
                            save_data(FAV_FILE, str_lit.session_state["favorites"])
                            str_lit.success("Saved!")
                            str_lit.rerun()
    else:
        str_lit.caption(T["history_empty"])

# ==========================================
# 7. الواجهة الرئيسية (Main Studio Application)
# ==========================================
str_lit.title(T["main_title"])
str_lit.caption(T["main_caption"])
str_lit.markdown("---")

tabs = str_lit.tabs(T["tabs"])

# --- التاب الأول: الأفكار والسكريبتات الاحترافية ---
with tabs[0]:
    str_lit.subheader(T["t1_header"])
    t1_input = floating_voice_textarea(T["t1_input_label"], "t1_val", T["t1_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t1_dur = str_lit.selectbox(T["t1_dur"], T["t1_dur_opts"], key="t1_dur_idx")
    with col2:
        t1_style = str_lit.selectbox(T["t1_style"], T["t1_style_opts"], key="t1_style_idx")
    with col3:
        t1_target = str_lit.selectbox(T["t1_target"], T["t1_target_opts"], key="t1_target_idx")
        
    t1_extras = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t1_extra_sel")
    
    if str_lit.button(T["t1_btn"], key="btn_t1"):
        if not t1_input.strip():
            str_lit.warning(T["t1_warn"])
        else:
            with str_lit.spinner(T["t1_spin"]):
                full_prompt = f"""
                Act as an elite YouTube & Social Media Content Director and Senior Scriptwriter.
                Create a professional, highly engaging video script based on the following details:
                - Core Idea / Title: {t1_input}
                - Duration: {t1_dur}
                - Visual Style & Tone: {t1_style}
                - Target Audience: {t1_target}
                - Include Advanced Add-ons: {', '.join(t1_extras) if t1_extras else 'Standard Pro Package'}

                Structure the response cleanly with Markdown headings, hooks, timestamps, B-roll cues, and voiceover lines.
                """
                res = execute_ai_action(full_prompt, category_name="Scripts", user_topic=t1_input, tab_index=0, lang_choice=lang_choice)
                if res:
                    str_lit.session_state["current_result"] = res
                    str_lit.rerun()

# --- التاب الثاني: الأغاني والصوت ---
with tabs[1]:
    str_lit.subheader(T["t2_header"])
    t2_input = floating_voice_textarea(T["t2_input_label"], "t2_val", T["t2_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t2_dialect = str_lit.selectbox(T["t2_dialect"], T["t2_dialect_opts"], key="t2_dialect_idx")
    with col2:
        t2_style = str_lit.selectbox(T["t2_style"], T["t2_style_opts"], key="t2_style_idx")
    with col3:
        t2_vocal = str_lit.selectbox(T["t2_vocal"], T["t2_vocal_opts"], key="t2_vocal_idx")
        
    t2_extras = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t2_extra_sel")

    if str_lit.button(T["t2_btn"], key="btn_t2"):
        if not t2_input.strip():
            str_lit.warning(T["t2_warn"])
        else:
            with str_lit.spinner(T["t2_spin"]):
                full_prompt = f"""
                Act as a professional Music Producer, Lyricist, and Audio Engineer.
                Create professional song lyrics and structured musical composition guidelines for platforms like Suno/Udio based on:
                - Song Theme: {t2_input}
                - Dialect / Cultural Flavor: {t2_dialect}
                - Music Genre: {t2_style}
                - Vocal Performance: {t2_vocal}
                - Additional Elements: {', '.join(t2_extras) if t2_extras else 'None'}

                Include verse/chorus breakdowns, song tags for AI generators, and vocal delivery directions.
                """
                res = execute_ai_action(full_prompt, category_name="Music", user_topic=t2_input, tab_index=1, lang_choice=lang_choice)
                if res:
                    str_lit.session_state["current_result"] = res
                    str_lit.rerun()

# --- التاب الثالث: تصميم الصور ---
with tabs[2]:
    str_lit.subheader(T["t3_header"])
    t3_input = floating_voice_textarea(T["t3_input_label"], "t3_val", T["t3_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t3_engine = str_lit.selectbox(T["t3_engine"], T["t3_engine_opts"], key="t3_engine_idx")
    with col2:
        t3_aspect = str_lit.selectbox(T["t3_aspect"], T["t3_aspect_opts"], key="t3_aspect_idx")
    with col3:
        t3_light = str_lit.selectbox(T["t3_light"], T["t3_light_opts"], key="t3_light_idx")
        
    t3_extras = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t3_extra_sel")

    if str_lit.button(T["t3_btn"], key="btn_t3"):
        if not t3_input.strip():
            str_lit.warning(T["t3_warn"])
        else:
            with str_lit.spinner(T["t3_spin"]):
                full_prompt = f"""
                Act as an Expert AI Prompt Engineer and Commercial Art Director.
                Generate highly detailed, optimized image generation prompts based on:
                - Scene Description: {t3_input}
                - Target AI Engine: {t3_engine}
                - Resolution / Aspect Ratio: {t3_aspect}
                - Lighting Style: {t3_light}
                - Extra Features: {', '.join(t3_extras) if t3_extras else 'None'}

                Provide ready-to-copy prompts in English (optimized for Midjourney/Flux) along with camera settings and style tokens.
                """
                res = execute_ai_action(full_prompt, category_name="Images", user_topic=t3_input, tab_index=2, lang_choice=lang_choice)
                if res:
                    str_lit.session_state["current_result"] = res
                    str_lit.rerun()

# --- التاب الرابع: تحريك الفيديو والأفاتار ---
with tabs[3]:
    str_lit.subheader(T["t4_header"])
    t4_input = floating_voice_textarea(T["t4_input_label"], "t4_val", T["t4_input_placeholder"])
    
    col1, col2 = str_lit.columns(2)
    with col1:
        t4_tool = str_lit.selectbox(T["t4_tool"], T["t4_tool_opts"], key="t4_tool_idx")
    with col2:
        t4_cam = str_lit.selectbox(T["t4_cam"], T["t4_cam_opts"], key="t4_cam_idx")
        
    t4_extras = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t4_extra_sel")

    if str_lit.button(T["t4_btn"], key="btn_t4"):
        if not t4_input.strip():
            str_lit.warning(T["t4_warn"])
        else:
            with str_lit.spinner(T["t4_spin"]):
                full_prompt = f"""
                Act as a Senior VFX Supervisor and AI Video Motion Director.
                Create precise animation prompts and movement descriptions based on:
                - Text / Motion Description: {t4_input}
                - Target Tool: {t4_tool}
                - Camera Movement: {t4_cam}
                - Extra Features: {', '.join(t4_extras) if t4_extras else 'None'}

                Provide exact text inputs for Runway/Luma/HeyGen, frame rates, physics parameters, and pacing cues.
                """
                res = execute_ai_action(full_prompt, category_name="Video Motion", user_topic=t4_input, tab_index=3, lang_choice=lang_choice)
                if res:
                    str_lit.session_state["current_result"] = res
                    str_lit.rerun()

# --- التاب الخامس: التسويق والخطط الاستراتيجية ---
with tabs[4]:
    str_lit.subheader(T["t5_header"])
    t5_input = floating_voice_textarea(T["t5_input_label"], "t5_val", T["t5_input_placeholder"])
    
    col1, col2, col3 = str_lit.columns(3)
    with col1:
        t5_plat = str_lit.selectbox(T["t5_plat"], T["t5_plat_opts"], key="t5_plat_idx")
    with col2:
        t5_goal = str_lit.selectbox(T["t5_goal"], T["t5_goal_opts"], key="t5_goal_idx")
    with col3:
        t5_budget = str_lit.number_input(T["t5_budget"], min_value=50, max_value=100000, value=1000, step=50, key="t5_budget_val")
        
    t5_extras = str_lit.multiselect(T["extra_features_label"], T["extra_options"], key="t5_extra_sel")

    if str_lit.button(T["t5_btn"], key="btn_t5"):
        if not t5_input.strip():
            str_lit.warning(T["t5_warn"])
        else:
            with str_lit.spinner(T["t5_spin"]):
                full_prompt = f"""
                Act as a Chief Marketing Officer (CMO) and Growth Strategist.
                Design a comprehensive, data-driven marketing strategy and ad campaign layout based on:
                - Product / Content Topic: {t5_input}
                - Target Platform: {t5_plat}
                - Campaign Goal: {t5_goal}
                - Estimated Ad Budget: ${t5_budget}
                - Extra Features: {', '.join(t5_extras) if t5_extras else 'None'}

                Include target audience profiling, ad copy angles, budget allocation percentages, KPIs, and scheduling recommendations.
                """
                res = execute_ai_action(full_prompt, category_name="Marketing", user_topic=t5_input, tab_index=4, lang_choice=lang_choice)
                if res:
                    str_lit.session_state["current_result"] = res
                    str_lit.rerun()

# ==========================================
# 8. عرض النتيجة النهائية مع أدوات التفاعل
# ==========================================
if str_lit.session_state["current_result"]:
    str_lit.markdown("---")
    str_lit.subheader(T["result_label"])
    
    # صندوق عرض النتيجة القابل للنسخ والقراءة
    str_lit.markdown(f"""
    <div style="background-color: rgba(15, 23, 42, 0.85); border: 1px solid rgba(99, 102, 241, 0.3); padding: 20px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); max-height: 600px; overflow-y: auto;">
        {str_lit.session_state["current_result"]}
    </div>
    """, unsafe_allow_html=True)
    
    str_lit.markdown("<br>", unsafe_allow_html=True)
    
    col_res1, col_res2, col_res3 = str_lit.columns([1, 1, 2])
    
    with col_res1:
        if str_lit.button(T["copy_btn"]):
            str_lit.code(str_lit.session_state["current_result"], language="markdown")
            str_lit.success("Ready for copy!")
            
    with col_res2:
        str_lit.download_button(
            label=T["download_txt"],
            data=str_lit.session_state["current_result"],
            file_name=f"Smart_Content_Result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
    with col_res3:
        rating = str_lit.slider(T["rating_label"], 1, 5, 5, key="result_rating_slider")
