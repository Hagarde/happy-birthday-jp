import streamlit as st

# Configuration
st.set_page_config(page_title="Wordle en Streamlit", layout="centered")

# Initialisation de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Définir ton mot de passe ici
APP_PASSWORD = "garage"

# ⚡ Hardcode du mot secret (toujours en majuscules)
TARGET_WORD = "FUSIL"

st.title("🔐 Wordle en Streamlit")

# --- Authentification ---
if not st.session_state.authenticated:
    pwd = st.text_input("Entrez le mot de passe pour accéder au jeu :", type="password")
    if st.button("Se connecter"):
        if pwd == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("Connexion réussie ✅")
        else:
            st.error("Mot de passe incorrect ❌")

else:
    st.subheader("Bienvenue dans le jeu 🎮")

    # --- Zone de jeu ---
    guess = st.text_input("Votre proposition (5 lettres)", max_chars=5).upper()

    if st.button("Valider"):
        if len(guess) != 5 or not guess.isalpha():
            st.warning("Votre mot doit contenir 5 lettres.")
        elif st.session_state.game_over:
            st.info("La partie est terminée, rechargez la page pour rejouer.")
        else:
            st.session_state.guesses.append(guess)
            if guess == TARGET_WORD:
                st.success(f"🎉 Bravo ! Vous avez trouvé {TARGET_WORD}")
                st.session_state.game_over = True
            elif len(st.session_state.guesses) >= 6:
                st.error(f"😢 Perdu ! Le mot était {TARGET_WORD}")
                st.session_state.game_over = True

    # Affichage des tentatives
    for g in st.session_state.guesses:
        result = []
        for i, c in enumerate(g):
            if c == TARGET_WORD[i]:
                result.append(f"🟩 {c}")
            elif c in TARGET_WORD:
                result.append(f"🟨 {c}")
            else:
                result.append(f"⬛ {c}")
        st.write(" ".join(result))
