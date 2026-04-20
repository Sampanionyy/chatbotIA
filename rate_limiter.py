import time
import streamlit as st
from config import MAX_REQUESTS_PER_WINDOW, RATE_WINDOW_SECONDS, MIN_DELAY_BETWEEN_REQUESTS


def check_rate_limit() -> tuple[bool, str]:
    now = time.time()
    st.session_state.request_timestamps = [
        t for t in st.session_state.request_timestamps
        if now - t < RATE_WINDOW_SECONDS
    ]
    if len(st.session_state.request_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        oldest = st.session_state.request_timestamps[0]
        wait = int(RATE_WINDOW_SECONDS - (now - oldest)) + 1
        return False, (
            f"Limite atteinte ({MAX_REQUESTS_PER_WINDOW} requetes/{RATE_WINDOW_SECONDS}s). "
            f"Reessayez dans **{wait} secondes**."
        )
    elapsed = now - st.session_state.last_request_time
    if elapsed < MIN_DELAY_BETWEEN_REQUESTS:
        time.sleep(MIN_DELAY_BETWEEN_REQUESTS - elapsed)
    return True, ""


def record_request():
    now = time.time()
    st.session_state.request_timestamps.append(now)
    st.session_state.last_request_time = now
