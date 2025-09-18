import streamlit as st

# Configuration
st.set_page_config(page_title="Wordle en Streamlit", layout="centered")

# Initialisation de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "target_word" not in st.session_state:
    st.session_state.target_word = ""
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Définir ton mot de passe ici
APP_PASSWORD = "openai123"

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

    # --- Zone pour choisir le mot (admin / créateur du jeu) ---
    with st.expander("Choisir le mot à deviner (ne pas montrer aux joueurs 😉)"):
        word_input = st.text_input("Mot secret", type="password", max_chars=5)
        if st.button("Définir le mot"):
            if len(word_input) == 5 and word_input.isalpha():
                st.session_state.target_word = word_input.upper()
                st.session_state.guesses = []
                st.session_state.game_over = False
                st.success("Mot défini !")
            else:
                st.error("Le mot doit contenir exactement 5 lettres.")

    # --- Zone de jeu ---
    if st.session_state.target_word:
        guess = st.text_input("Votre proposition (5 lettres)", max_chars=5).upper()

        if st.button("Valider"):
            if len(guess) != 5 or not guess.isalpha():
                st.warning("Votre mot doit contenir 5 lettres.")
            elif st.session_state.game_over:
                st.info("La partie est terminée, définissez un nouveau mot.")
            else:
                st.session_state.guesses.append(guess)
                if guess == st.session_state.target_word:
                    st.success(f"🎉 Bravo ! Vous avez trouvé {st.session_state.target_word}")
                    st.session_state.game_over = True
                elif len(st.session_state.guesses) >= 6:
                    st.error(f"😢 Perdu ! Le mot était {st.session_state.target_word}")
                    st.session_state.game_over = True

        # Affichage des tentatives
        for g in st.session_state.guesses:
            result = []
            for i, c in enumerate(g):
                if c == st.session_state.target_word[i]:
                    result.append(f"🟩 {c}")
                elif c in st.session_state.target_word:
                    result.append(f"🟨 {c}")
                else:
                    result.append(f"⬛ {c}")
            st.write(" ".join(result))
