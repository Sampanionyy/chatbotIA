import time
import streamlit as st
from config import DEFAULT_SESSION
import copy


def init_session():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = f"user_{int(time.time() % 10000):04d}"
    for k, v in DEFAULT_SESSION.items():
        if k not in st.session_state:
            st.session_state[k] = copy.deepcopy(v)
