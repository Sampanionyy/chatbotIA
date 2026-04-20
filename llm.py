import os
import time
import logging
import streamlit as st
from openai import OpenAI, APIError, APITimeoutError, RateLimitError, APIConnectionError
from config import MODELS, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)


def get_client(model_name: str) -> OpenAI:
    cfg = MODELS[model_name]
    api_key = os.getenv(cfg["api_key_env"], "")
    if not api_key:
        raise ValueError(f"Cle API manquante : definissez `{cfg['api_key_env']}` dans votre fichier .env.")
    return OpenAI(api_key=api_key, base_url=cfg["base_url"])


def call_llm(user_message: str, model_name: str, temperature: float) -> tuple[str, float]:
    cfg = MODELS[model_name]
    system_content = SYSTEM_PROMPTS[st.session_state.selected_persona]

    messages_payload = [{"role": "system", "content": system_content}]
    for m in st.session_state.messages:
        messages_payload.append({"role": m["role"], "content": m["content"]})
    messages_payload.append({"role": "user", "content": user_message})

    client = get_client(model_name)
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=cfg["id"],
            messages=messages_payload,
            temperature=temperature,
            timeout=30,
        )
    except RateLimitError:
        raise RuntimeError("Limite de l'API atteinte. Patientez quelques instants.")
    except APITimeoutError:
        raise RuntimeError("Le serveur n'a pas repondu a temps (timeout 30s). Reessayez.")
    except APIConnectionError:
        raise RuntimeError("Impossible de joindre l'API. Verifiez votre connexion.")
    except APIError as e:
        raise RuntimeError(f"Erreur API ({e.status_code}) : {e.message}")
    except ValueError as e:
        raise RuntimeError(str(e))
    except Exception as e:
        raise RuntimeError(f"Erreur inattendue : {e}")

    elapsed = round(time.time() - start, 2)
    reply = (response.choices[0].message.content or "").strip()
    if not reply:
        raise RuntimeError("Le modele a retourne une reponse vide. Reformulez votre question.")

    m = st.session_state.metrics
    m["total_questions"] += 1
    m["response_times"].append(elapsed)
    m["model_usage"][model_name] += 1

    logger.info(
        "user=%s | model=%s | T=%.1f | time=%.2fs | tokens=%s",
        st.session_state.user_id, cfg["id"], temperature, elapsed,
        response.usage.total_tokens if response.usage else "?",
    )
    return reply, elapsed
