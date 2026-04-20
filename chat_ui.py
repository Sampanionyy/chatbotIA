import streamlit as st


def render_chat():
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                meta = [v for k in ("ts", "elapsed") if (v := str(msg[k]) if msg.get(k) else None)]
                if msg.get("elapsed"):
                    meta = [msg["ts"], f"{msg['elapsed']}s"] if msg.get("ts") else [f"{msg['elapsed']}s"]
                elif msg.get("ts"):
                    meta = [msg["ts"]]
                if meta:
                    st.caption(" · ".join(meta))
                fb1, fb2, _ = st.columns([1, 1, 8])
                if fb1.button("👍", key=f"up_{i}"):
                    st.session_state.metrics["satisfaction_votes"]["good"] += 1
                    st.toast("Merci pour votre retour !")
                if fb2.button("👎", key=f"down_{i}"):
                    st.session_state.metrics["satisfaction_votes"]["bad"] += 1
                    st.toast("Merci, nous en prenons note.")
