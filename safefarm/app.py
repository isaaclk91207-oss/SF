"""SafeFarm Myanmar - Flood Damage Assessment"""

import streamlit as st
from config import get_string, REGIONS, CROPS, GROWTH_STAGES, CLASS_COLORS

# Page config
st.set_page_config(
    page_title="SafeFarm Myanmar",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key):
    """Helper to get translated string."""
    return get_string(key, st.session_state.lang)

def render_header():
    """Render app header with language toggle."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"🌾 {t('app_title')}")
        st.caption(f"{t('team_name')} | {t('tagline')}")
    
    with col2:
        lang = st.radio(
            t("language"),
            [t("lang_en"), t("lang_my")],
            horizontal=True,
            label_visibility="collapsed",
            index=1 if st.session_state.lang == "my" else 0
        )
        st.session_state.lang = "my" if lang == t("lang_my") else "en"

def render_form():
    """Render assessment form."""
    st.subheader(f"📋 {t('form_title')}")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            region = st.selectbox(t("region"), REGIONS)
            township = st.text_input(t("township"))
            village = st.text_input(t("village"))
            farm_location = st.text_input(t("farm_location"))
        
        with col2:
            crop_type = st.selectbox(t("crop_type"), CROPS[st.session_state.lang])
            farm_area = st.number_input(t("farm_area"), min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
            flood_days = st.number_input(t("flood_days"), min_value=1, max_value=90, value=7, step=1)
            growth_stage = st.selectbox(t("growth_stage"), GROWTH_STAGES[st.session_state.lang])
        
        urgent_support = st.checkbox(t("urgent_support"))
        uploaded_image = st.file_uploader(t("upload_photo"), type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button(t("assess_button"), use_container_width=True)
    
    return {
        "region": region,
        "township": township,
        "village": village,
        "farm_location": farm_location,
        "crop_type": crop_type,
        "farm_area": farm_area,
        "flood_days": flood_days,
        "growth_stage": growth_stage,
        "urgent_support": urgent_support,
        "uploaded_image": uploaded_image,
        "submitted": submitted
    }

def render_result_placeholder():
    """Render result area placeholder."""
    st.subheader(f"📊 {t('result_title')}")
    st.info(t("model_demo"))

def render_disclaimer():
    """Render disclaimer footer."""
    st.divider()
    st.caption(f"⚠️ {t('disclaimer')}")
    st.caption(t("footer_text"))

def main():
    """Main app entry point."""
    render_header()
    
    col_form, col_result = st.columns([1, 1])
    
    with col_form:
        form_data = render_form()
    
    with col_result:
        render_result_placeholder()
    
    render_disclaimer()

if __name__ == "__main__":
    main()
