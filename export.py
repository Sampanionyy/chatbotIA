import os
import csv
from datetime import datetime
import streamlit as st


def export_conversation_csv() -> str:
    filename = f"conversation_{st.session_state.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tour", "Role", "Message", "Timestamp"])
        for i, msg in enumerate(st.session_state.messages):
            writer.writerow([i + 1, msg["role"], msg["content"], msg.get("ts", "")])
    return filepath
