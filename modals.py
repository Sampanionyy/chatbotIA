import streamlit as st
from config import MODELS, SYSTEM_PROMPTS


@st.dialog("Parametres")
def settings_modal():
    st.selectbox(
        "Modele",
        list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.selected_model),
        key="_modal_model",
    )
    st.selectbox(
        "Persona RH",
        list(SYSTEM_PROMPTS.keys()),
        index=list(SYSTEM_PROMPTS.keys()).index(st.session_state.selected_persona),
        key="_modal_persona",
    )
    temp = st.slider(
        "Temperature",
        min_value=0.0, max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="0 = deterministe   0.5 = equilibre   1.0 = creatif",
        key="_modal_temp",
    )
    captions = {
        (0.0, 0.0): "Mode deterministe - reponses precises et reproductibles.",
        (0.1, 0.4): "Mode factuel - reponses stables et fiables.",
        (0.5, 0.7): "Mode equilibre - bon compromis precision et fluidite.",
        (0.8, 1.0): "Mode creatif - reponses variees et originales.",
    }
    for (lo, hi), caption in captions.items():
        if lo <= temp <= hi:
            st.caption(caption)
            break

    st.divider()
    col_save, col_cancel = st.columns(2)
    if col_save.button("Enregistrer", use_container_width=True, type="primary"):
        st.session_state.selected_model   = st.session_state._modal_model
        st.session_state.selected_persona = st.session_state._modal_persona
        st.session_state.temperature      = st.session_state._modal_temp
        st.rerun()
    if col_cancel.button("Annuler", use_container_width=True):
        st.rerun()


@st.dialog("Metriques")
def metrics_modal():
    m = st.session_state.metrics
    times = m["response_times"]

    col1, col2 = st.columns(2)
    col1.metric("Questions posees", m["total_questions"])
    col2.metric("Erreurs", m["total_errors"])

    if times:
        col3, col4 = st.columns(2)
        col3.metric("Temps moyen", f"{sum(times)/len(times):.2f}s")
        col4.metric("Temps max", f"{max(times):.2f}s")

    if m["model_usage"]:
        st.markdown("**Modeles utilises**")
        max_usage = max(m["model_usage"].values())
        for model, count in m["model_usage"].items():
            short = model.split("-")[-1].strip()
            st.progress(count / max_usage, text=f"{short}: {count}")

    votes = m["satisfaction_votes"]
    total_votes = votes["good"] + votes["bad"]
    if total_votes:
        score = votes["good"] / total_votes * 100
        st.metric("Satisfaction", f"{score:.0f}%", f"{total_votes} votes")
    else:
        st.caption("Aucun vote de satisfaction pour l'instant.")

    st.divider()
    if st.button("Fermer", use_container_width=True):
        st.rerun()
