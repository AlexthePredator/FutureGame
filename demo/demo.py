import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Per eseguire:
# streamlit run FutureGame/demo/demo.py

# Carica il modello addestrato
model = joblib.load("FutureGame/addestramentoModello/Modello/rf_model_future_game.pkl")

# Lista di tutte le feature usate dal modello
FEATURES = [
    'required_age', 'achievements', 'platform_count', 'is_free', 'price_log', 'trimester',
    'genre_top1_freq', 'genre_top2_freq', 'genre_Indie', 'genre_Action', 'genre_Adventure',
    'genre_Casual', 'genre_Free To Play', 'genre_RPG', 'genre_Strategy', 'genre_Simulation',
    'genre_Early Access', 'genre_Massively Multiplayer', 'genre_Sports', 'genre_Racing',
    'cat_Captions available', 'cat_Co-op', 'cat_Cross-Platform Multiplayer',
    'cat_Family Sharing', 'cat_Full controller support', 'cat_In-App Purchases',
    'cat_Includes Source SDK', 'cat_Includes level editor', 'cat_LAN Co-op', 'cat_LAN PvP',
    'cat_MMO', 'cat_Multi-player', 'cat_Online Co-op', 'cat_Online PvP', 'cat_PvP',
    'cat_Shared/Split Screen', 'cat_Shared/Split Screen Co-op', 'cat_Shared/Split Screen PvP',
    'cat_Single-player', 'cat_Steam Trading Cards',
    'publishers_freq', 'developer_freq',
    'pub_top_Big Fish Games', 'pub_top_Conglomerate 5', 'pub_top_Daedalic Entertainment',
    'pub_top_Devolver Digital', 'pub_top_DigiPen Institute of Technology', 'pub_top_Electronic Arts',
    'pub_top_GrabTheGames', 'pub_top_KOEI TECMO GAMES CO., LTD.', 'pub_top_Kagura Games',
    'pub_top_Nacon', 'pub_top_PLAYISM', 'pub_top_SA Industry', 'pub_top_SEGA',
    'pub_top_Sekai Project', 'pub_top_Square Enix', 'pub_top_THQ Nordic', 'pub_top_Ubisoft',
    'pub_top_Volens Nolens Games', 'pub_top_other', 'pub_top_tinyBuild',
    'dev_top_Arc System Works', 'dev_top_Boogygames Studios', 'dev_top_CAPCOM Co., Ltd.',
    'dev_top_Creobit', 'dev_top_Do Games Limited', 'dev_top_EnsenaSoft', 'dev_top_FIVE-BN GAMES',
    'dev_top_KOEI TECMO GAMES CO., LTD.', 'dev_top_Laush Dmitriy Sergeevich',
    'dev_top_MAGIX Software GmbH', 'dev_top_Milestone S.r.l.', 'dev_top_Nihon Falcom',
    'dev_top_Quiet River', 'dev_top_RewindApp', 'dev_top_Ripknot Systems',
    'dev_top_Square Enix', 'dev_top_TigerQiuQiu', 'dev_top_Warfare Studios',
    'dev_top_Winged Cloud', 'dev_top_other'
]

st.title(" Predizione Successo Videogioco (Demo)")

# Input base
title = st.text_input("Titolo del gioco (solo per visualizzazione)")
required_age = st.number_input("Età minima richiesta", min_value=0, max_value=21, step=1)
achievements = st.number_input("Numero achievements", min_value=0, step=1)
platform_count = st.slider("Numero piattaforme supportate", 1, 3, 1)
price = st.number_input("Prezzo (€)", min_value=0.0, max_value=200.0, step=0.1)
if price == 0.0:
    is_free = st.checkbox("Free-to-Play", value=True)
else:
    is_free = False
trimester = st.selectbox("Trimestre di uscita (1=Dic,Gen,Feb) (2=Mar,Apr,Mag) (3=Giu,Lug,Ago) (4=Set,Ott,Nov)", [1, 2, 3, 4])

# Variabili numeriche da frequenze
publishers_freq = st.number_input("Publisher frequency (conteggio giochi dello stesso publisher)", min_value=0, step=1)
developer_freq = st.number_input("Developer frequency (conteggio giochi dello stesso developer)", min_value=0, step=1)
genre_top1_freq = st.number_input("Frequenza globale del genere top1", min_value=0, step=1)
genre_top2_freq = st.number_input("Frequenza globale del genere top2", min_value=0, step=1)

# Sezioni multi-selezione per generi e categorie
top_genres = [g for g in FEATURES if g.startswith("genre_")]
selected_genres = st.multiselect("Generi principali", top_genres)
top_cats = [c for c in FEATURES if c.startswith("cat_")]
selected_cats = st.multiselect("Categorie", top_cats)

# Publisher e developer top
top_publishers = [p for p in FEATURES if p.startswith("pub_top_")]
selected_pub = st.selectbox("Publisher principale", top_publishers)
top_devs = [d for d in FEATURES if d.startswith("dev_top_")]
selected_dev = st.selectbox("Developer principale", top_devs)

# Button
if st.button("Predici successo"):
    # Trasforma input in dict di feature
    row = {col: 0 for col in FEATURES}

    # Variabili base
    row["required_age"] = required_age
    row["achievements"] = achievements
    row["platform_count"] = platform_count
    row["is_free"] = int(is_free)
    row["price_log"] = np.log1p(price)
    row["trimester"] = trimester
    row["publishers_freq"] = publishers_freq
    row["developer_freq"] = developer_freq
    row["genre_top1_freq"] = genre_top1_freq
    row["genre_top2_freq"] = genre_top2_freq

    # Generi e categorie -> 1 se selezionati
    for g in selected_genres:
        row[g] = 1
    for c in selected_cats:
        row[c] = 1

    # Publisher e developer selezionati
    if selected_pub:
        row[selected_pub] = 1
    if selected_dev:
        row[selected_dev] = 1

    # Crea DataFrame
    X_new = pd.DataFrame([row])

    # Predizione
    y_pred = model.predict(X_new)[0]
    labels = ["insuccesso", "basso_successo", "medio_successo", "alto_successo"]

    st.success(f" Risultato per '{title}': **{labels[y_pred]}**")

