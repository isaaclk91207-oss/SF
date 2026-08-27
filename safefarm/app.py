"""SafeFarm Myanmar - Flood Damage Assessment"""

import streamlit as st
from PIL import Image
from config import get_string, REGIONS, CROPS, GROWTH_STAGES, CLASS_COLORS
from utils.image import validate_image, preprocess_image, get_image_info
from model.inference import get_classifier, predict_image
from utils.priority import calculate_priority, get_priority_label, get_recommendations
from utils.priority import calculate_priority, get_priority_label, get_recommendations

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
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "gradcam_image" not in st.session_state:
    st.session_state.gradcam_image = None
if "priority_score" not in st.session_state:
    st.session_state.priority_score = None
if "priority_score" not in st.session_state:
    st.session_state.priority_score = None

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


def render_model_status():
    """Show model status in sidebar."""
    classifier = get_classifier()
    info = classifier.get_model_info()
    with st.sidebar:
        st.markdown("### Model Status")
        if info["status"] == "demo":
            st.warning(f"⚠️ {t('model_demo')}")
        else:
            st.success(f"✅ Model: {info['name']}")
            st.info(f"Device: {info['device']}")


def render_image_upload():
    """Render image upload section."""
    st.subheader(f"📷 {t('upload_photo')}")

    uploaded_file = st.file_uploader(
        t("upload_photo"),
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        # Validate image
        validation = validate_image(uploaded_file)

        if not validation["valid"]:
            st.error(f"❌ {validation['error']}")
            return None

        # Show warning if any
        if validation["warning"]:
            st.warning(f"⚠️ {validation['warning']}")

        # Open and display image
        image = Image.open(uploaded_file)
        st.session_state.uploaded_image = image

        # Get image info
        info = get_image_info(image)

        # Display image and info
        col_img, col_info = st.columns([2, 1])

        with col_img:
            st.image(image, caption=uploaded_file.name, use_container_width=True)

        with col_info:
            st.markdown("**Image Info:**")
            st.text(f"Size: {info['width']}x{info['height']}")
            st.text(f"Mode: {info['mode']}")
            st.text(f"Format: {info['format']}")

        # Preprocess preview
        processed = preprocess_image(image)
        st.session_state.processed_image = processed

        with st.expander("🔍 Preprocessed Image (224x224)"):
            st.image(processed, caption="Model Input", width=200)

        return image

    return None


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
        "submitted": submitted
    }


def render_result_card(prediction, form_data=None):
    """Render result card with prediction and priority score."""
    st.subheader(f"📊 {t('result_title')}")

    if prediction is None:
        st.info("Upload an image and click 'Assess Damage' to see results")
        return

    damage_class = prediction["class"]
    confidence = prediction["confidence"]
    color = CLASS_COLORS.get(damage_class, "#9E9E9E")

    if prediction.get("is_demo", False):
        st.warning(f"⚠️ {t('model_demo')}")

    # Main result card
    st.markdown(f"""
    <div style="
        border: 2px solid {color};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: {color}15;
    ">
        <h3 style="color: {color}; margin: 0;">
            {t('damage_level')}: {t(damage_class)}
        </h3>
        <p style="font-size: 24px; margin: 10px 0;">
            {t('confidence')}: {confidence:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Probability breakdown
    st.markdown("**Probability Breakdown:**")
    probs = prediction["probabilities"]
    cols = st.columns(4)
    for i, (cls, prob) in enumerate(probs.items()):
        with cols[i]:
            st.metric(label=t(cls), value=f"{prob:.1%}")

    # Priority Score
    if form_data is not None:
        st.markdown("---")
        st.subheader(f"🎯 {t('priority_score')}")

        score = calculate_priority(
            damage_level=damage_class,
            farm_area=form_data["farm_area"],
            flood_days=form_data["flood_days"],
            growth_stage=form_data["growth_stage"],
            urgent_support=form_data["urgent_support"]
        )
        st.session_state.priority_score = score
        priority_label = get_priority_label(score)

        label_color = {"high": "#F44336", "medium": "#FF9800", "low": "#4CAF50"}
        pcolor = label_color.get(priority_label, "#9E9E9E")

        st.markdown(f"""
        <div style="
            border: 2px solid {pcolor};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            background-color: {pcolor}15;
        ">
            <p style="font-size: 36px; margin: 0; color: {pcolor};">
                {score}
            </p>
            <p style="margin: 5px 0;">
                {t('priority_' + priority_label)}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Recommendations
        recs = get_recommendations(damage_class, score, form_data["urgent_support"])
        st.markdown("**Recommended Actions:**")
        for rec_key in recs:
            st.markdown(f"- {t(rec_key)}")

    # Grad-CAM
    st.markdown("---")
    st.subheader("🔍 Visual Evidence (Grad-CAM)")

    if prediction.get("has_gradcam", False) and prediction.get("gradcam_image") is not None:
        col_orig, col_cam = st.columns(2)
        with col_orig:
            st.markdown("**Original Image:**")
            st.image(st.session_state.uploaded_image, use_container_width=True)
        with col_cam:
            st.markdown("**Grad-CAM Heat Map:**")
            st.image(prediction["gradcam_image"], use_container_width=True)
        st.markdown("""
        **Legend:**
        - 🔴 **Red** = Model focused here (high attention)
        - 🟡 **Yellow** = Medium attention
        - 🟢 **Green/Blue** = Model ignored here (low attention)
        """)
    else:
        st.info("⚠️ Grad-CAM not available in demo mode")
        st.caption("Grad-CAM requires a trained model to show which image regions influenced the prediction.")


def render_disclaimer():
    """Render disclaimer footer."""
    st.divider()
    st.caption(f"⚠️ {t('disclaimer')}")
    st.caption(t("footer_text"))


def main():
    """Main app entry point."""
    render_header()
    render_model_status()

    col_upload, col_result = st.columns([1, 1])

    with col_upload:
        image = render_image_upload()
        form_data = render_form()

        # Handle form submission
        if form_data["submitted"] and image is not None:
            with st.spinner("Analyzing image..."):
                prediction = predict_image(image)
                st.session_state.prediction = prediction
                st.session_state.gradcam_image = prediction.get("gradcam_image")
                st.rerun()

    with col_result:
        render_result_card(st.session_state.get("prediction", None), form_data)

    render_disclaimer()


if __name__ == "__main__":
    main()
