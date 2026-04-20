# ChatBot RH

Assistant conversationnel RH developpe avec Streamlit et des LLM via API Groq.

---

## Structure du projet

```
.
├── app.py            # Point d'entree, orchestration generale
├── chat_ui.py        # Rendu des messages et boutons de feedback
├── config.py         # Modeles, personas, constantes de configuration
├── export.py         # Export de la conversation en CSV
├── llm.py            # Appel API (Groq via compatibilite OpenAI), metriques
├── modals.py         # Fenetres parametres et metriques (st.dialog)
├── rate_limiter.py   # Limitation du nombre de requetes par fenetre de temps
├── session.py        # Initialisation de l'etat de session Streamlit
├── styles.py         # CSS personnalise (police Nunito, badges quota)
├── .env              # Cles API (non versionnees)
└── chatbot_rh.log    # Fichier de logs genere a l'execution
```

---

## Ce qui fonctionne

**Qualite des reponses — temperature**
- Parametre temperature expose dans l'interface (0.0 a 1.0, pas de 0.1)
- Trois regimes documentes : deterministe (0), equilibre (0.5), creatif (1.0)
- Caption explicatif dynamique selon la valeur choisie

**Rate limiting**
- Fenetre glissante de 60 secondes, maximum 10 requetes par fenetre
- Delai minimum de 1 seconde entre deux requetes (sleep automatique)
- Badge de quota color (vert / orange / rouge) affiche en temps reel
- Message d'erreur utilisateur avec temps d'attente restant si limite atteinte

**Gestion des erreurs**
- `RateLimitError` : message d'attente clair
- `APITimeoutError` : timeout fixe a 30 secondes, message explicite
- `APIConnectionError` : message de connectivite
- `APIError` generique : code HTTP et detail affiches
- Reponse vide du modele : erreur capturee et signalee
- Message trop court (< 3 caracteres) ou trop long (> 2000 caracteres) : validation cote client

**Monitoring et metriques**
- Techniques : nombre de questions, nombre d'erreurs, temps de reponse moyen et maximum, usage par modele
- Business : votes de satisfaction 👍 / 👎, score de satisfaction en pourcentage, nombre de sessions
- Accessible via le bouton "Logs" (modale st.dialog)
- Logs structures dans `chatbot_rh.log` : user_id, modele, temperature, temps de reponse, tokens consommes

**UX et fonctionnalites complementaires**
- Historique de conversation complet dans la session
- Bouton "Reset" pour demarrer une nouvelle conversation
- Choix dynamique du modele (Groq Llama 3.1 8B ou 3.3 70B)
- Choix du persona RH (assistant generaliste, coach carriere, expert droit du travail)
- Export de la conversation en CSV (bouton telechargement)
- Gestion multi-utilisateurs basique via `user_id` genere a la session (`user_XXXX`)
- Interface centree, police Nunito, style epure

---

## Choix techniques

**Temperature**
Valeur par defaut de 0.7 (mode equilibre). En contexte RH, une temperature trop elevee risque de produire des reponses imprecises sur des sujets sensibles (droit du travail, paie). La valeur 0.7 offre un bon compromis entre fluidite et fiabilite.

**Rate limiting par fenetre glissante**
Plutot qu'un compteur par minute calendaire, la fenetre glissante est plus juste pour l'utilisateur : elle expire progressivement et evite les blocages de 60 secondes en debut de fenetre.

**Separation des modules**
Chaque responsabilite est isolee dans un fichier dedie (session, rate limiter, LLM, export, UI). Cela facilite la maintenance et les tests unitaires futurs.

**Compatibilite OpenAI pour Groq**
Groq expose une API compatible OpenAI. Le client `openai.OpenAI` est reutilise en changeant uniquement `base_url` et `api_key`. Ajouter un nouveau fournisseur ne necessite que d'etendre le dictionnaire `MODELS` dans `config.py`.

---

## Limites du travail

- Pas de persistance des donnees : l'historique, les metriques et les votes de satisfaction sont perdus au rechargement de la page (stockage uniquement en `st.session_state`)
- Pas d'authentification reelle : le `user_id` est genere aleatoirement et ne correspond a aucun compte
- Pas de classification des questions : le type de question (conges, paie, recrutement) n'est pas detecte automatiquement
- Un seul fournisseur actif (Groq) : l'integration OpenAI est prevue dans la structure mais non activee faute de cle
- Pas de tests automatises (unitaires ou d'integration)
- L'export CSV est genere dans `/tmp` sans nettoyage automatique des anciens fichiers

---

## Pistes d'amelioration

- Persister les conversations et metriques dans une base de donnees (SQLite ou PostgreSQL)
- Ajouter une authentification utilisateur (OAuth ou formulaire simple)
- Classifier automatiquement les questions pour des metriques business plus fines
- Integrer OpenAI GPT-4o comme fournisseur alternatif
- Ajouter des tests unitaires (pytest) sur le rate limiter et le parsing des reponses
- Implementer un systeme de RAG (Retrieval-Augmented Generation) pour ancrer les reponses dans les documents RH internes de l'entreprise
- Nettoyer periodiquement les fichiers CSV d'export dans `/tmp`

---

## Exemple de log

```
2025-01-15 14:32:10 | INFO | user=user_4821 | model=llama-3.1-8b-instant | T=0.7 | time=1.43s | tokens=312
2025-01-15 14:32:55 | WARNING | user=user_4821 | rate limit atteint
2025-01-15 14:33:01 | INFO | user=user_4821 | reset
2025-01-15 14:35:22 | ERROR | user=user_4821 | error: Le serveur n'a pas repondu a temps (timeout 30s). Reessayez.
```

---

## Installation et lancement

```bash
pip install streamlit openai python-dotenv
```

Creer un fichier `.env` :

```
GROQ_API_KEY=votre_cle_groq
```

Lancer l'application :

```bash
streamlit run app.py
```