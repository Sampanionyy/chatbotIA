CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, h1, h2, h3,
button, input, textarea, select, label, .stSelectbox, .stSlider {
    font-family: 'Nunito', sans-serif !important;
}

.quota-badge {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}
.quota-ok   { background: #e6f9ee; color: #1a7a40; }
.quota-warn { background: #fff8e1; color: #a06000; }
.quota-crit { background: #fdecea; color: #b71c1c; }

div[data-testid="stButton"] button {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}

[data-testid="stChatMessage"] {
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
}
</style>
"""