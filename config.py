from collections import defaultdict

MODELS = {
    "Groq - Llama 3.1 8B (rapide)": {
        "id": "llama-3.1-8b-instant",
        "provider": "groq",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
    },
    "Groq - Llama 3.3 70B": {
        "id": "llama-3.3-70b-versatile",
        "provider": "groq",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
    }
}

SYSTEM_PROMPTS = {
    "Assistant RH generaliste": (
        "Tu es un assistant RH expert. Tu reponds aux questions sur les conges, "
        "la paie, le recrutement, le droit du travail francais et la gestion des talents. "
        "Sois precis, bienveillant et professionnel."
    ),
    "Coach carriere": (
        "Tu es un coach carriere experimente. Tu aides les employes a developper "
        "leurs competences, preparer des entretiens et planifier leur evolution professionnelle."
    ),
    "Expert droit du travail": (
        "Tu es un expert en droit du travail francais. Tu fournis des informations "
        "precises sur la legislation, les conventions collectives et les procedures RH. "
        "Rappelle toujours de consulter un juriste pour des cas specifiques."
    ),
}

MAX_REQUESTS_PER_WINDOW = 10
RATE_WINDOW_SECONDS = 60
MIN_DELAY_BETWEEN_REQUESTS = 1

DEFAULT_SESSION = {
    "messages": [],
    "request_timestamps": [],
    "last_request_time": 0.0,
    "metrics": {
        "total_questions": 0,
        "total_errors": 0,
        "response_times": [],
        "model_usage": defaultdict(int),
        "satisfaction_votes": {"good": 0, "bad": 0},
        "sessions": 1,
    },
    "temperature": 0.7,
    "selected_model": list(MODELS.keys())[0],
    "selected_persona": list(SYSTEM_PROMPTS.keys())[0],
}
