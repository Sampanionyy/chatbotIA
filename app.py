import os
import time
import logging
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from config import MAX_REQUESTS_PER_WINDOW, RATE_WINDOW_SECONDS
from styles import CUSTOM_CSS
from session import init_session
from rate_limiter import check_rate_limit, record_request
from llm import call_llm
from export import export_conversation_csv
from modals import settings_modal, metrics_modal
from chat_ui import render_chat

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("chatbot_rh.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    st.set_page_config(page_title="ChatBot RH", layout="centered", initial_sidebar_state="collapsed")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_session()

    col_title, col_btns = st.columns([3, 2])

    with col_title:
        st.markdown("## ChatBot RH")
        now = time.time()
        recent = [t for t in st.session_state.request_timestamps if now - t < RATE_WINDOW_SECONDS]
        remaining = MAX_REQUESTS_PER_WINDOW - len(recent)
        badge_cls = "quota-ok" if remaining > 5 else "quota-warn" if remaining > 2 else "quota-crit"
        st.markdown(
            f'<span class="quota-badge {badge_cls}">Quota : {remaining}/{MAX_REQUESTS_PER_WINDOW}</span>',
            unsafe_allow_html=True,
        )

    with col_btns:
        b1, b2, b3 = st.columns(3)
        if b1.button(f"Params", use_container_width=True):
            settings_modal()
        if b2.button(f"Logs", use_container_width=True):
            metrics_modal()
        if b3.button(f"Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.metrics["sessions"] += 1
            logger.info("user=%s | reset", st.session_state.user_id)
            st.rerun()

    model_short = st.session_state.selected_model.split("-")[-1].strip()
    persona_short = st.session_state.selected_persona.split()[0]
    st.caption(f"Modèle : {model_short}  ·  Persona : {persona_short}  ·  T° : {st.session_state.temperature}")
    st.divider()

    if st.session_state.messages:
        path = export_conversation_csv()
        with open(path, "rb") as f:
            st.download_button(
                "⬇ Exporter la conversation (CSV)",
                data=f,
                file_name=os.path.basename(path),
                mime="text/csv",
            )

    if not st.session_state.messages:
        st.info(
            "Bienvenue. Je suis votre assistant RH. Posez-moi vos questions "
            "sur les congés, la paie, le recrutement ou le droit du travail."
        )

    render_chat()

    user_input = st.chat_input("Votre question RH...")

    if user_input:
        user_input = user_input.strip()

        if len(user_input) < 3:
            st.warning("Votre message est trop court. Posez une vraie question.")
            st.stop()
        if len(user_input) > 2000:
            st.warning("Message trop long (max 2000 caractères).")
            st.stop()

        ok, rate_msg = check_rate_limit()
        if not ok:
            st.error(rate_msg)
            logger.warning("user=%s | rate limit atteint", st.session_state.user_id)
            st.stop()

        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "ts": datetime.now().strftime("%H:%M"),
        })
        record_request()

        with st.spinner("Réflexion en cours..."):
            try:
                reply, elapsed = call_llm(
                    user_input,
                    st.session_state.selected_model,
                    st.session_state.temperature,
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "ts": datetime.now().strftime("%H:%M"),
                    "elapsed": elapsed,
                })
            except RuntimeError as e:
                st.session_state.metrics["total_errors"] += 1
                logger.error("user=%s | error: %s", st.session_state.user_id, str(e))
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": str(e),
                    "ts": datetime.now().strftime("%H:%M"),
                })

        st.rerun()


if __name__ == "__main__":
    main()