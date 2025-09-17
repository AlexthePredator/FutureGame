import pandas as pd
import numpy as np
import joblib
import streamlit as st

# Per eseguire:
# streamlit run demo/demo.py
# Da eseguire dalla directory FutureGame: cd .\FutureGame\

# Carico il modello addestrato
model = joblib.load("addestramentoModello/Modello/rf_model_future_game.pkl")
#model = joblib.load("addestramentoModello/Modello/rf_model_future_game_1.pkl")
# Carico le mappe di frequenza salvate
freq_map_pub = joblib.load("addestramentoModello/map/freq_map_pub.pkl")
freq_map_dev = joblib.load("addestramentoModello/map/freq_map_dev.pkl")
freq_map_genre = joblib.load("addestramentoModello/map/freq_map_genre.pkl")

# Lista di tutte le variabili usate dal modello
FEATURES = [
    'required_age', 'achievements', 'platform_count', 'is_free', 'price_log', 'trimester',
    'top1_genre_freq', 'top2_genre_freq', 'genre_Indie', 'genre_Action', 'genre_Adventure',
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

st.title(" Predizione Successo Videogioco")

# Path immagine Logo
image_path = "img/logoFutureGame.png"

# Mostra immagine Logo Progetto
st.image(image_path, caption="Future Game", width='content')

# Input utente semplici
title = st.text_input("Titolo del gioco:")
required_age = st.number_input("Età minima richiesta:", min_value=0, max_value=21, step=1)
achievements = st.number_input("Numero achievements Steam:", min_value=0, step=1)
platform_count = st.slider("Numero piattaforme supportate:", 1, 3, 1)
price = st.number_input("Prezzo (€):", min_value=0.0, max_value=200.0, step=0.1)
if price == 0.0:
    is_free = st.checkbox("Free-to-Play", value=True)
else:
    is_free = False
trimester = st.selectbox("Trimestre di uscita: (1=Dic,Gen,Feb) (2=Mar,Apr,Mag) (3=Giu,Lug,Ago) (4=Set,Ott,Nov)", [1, 2, 3, 4])

# Generi
## selezione multipla per generi
genres = st.multiselect("Seleziona i generi del gioco", options=list(freq_map_genre.keys()))
### Calcolo dei top1 e top2 (ordine)
if genres:
    ordered = sorted(genres, key=lambda g: -freq_map_genre.get(g, 0))
    top1 = ordered[0]
    top2 = ordered[1] if len(ordered) > 1 else None
else:
    top1 = 0
    top2 = 0
# calcolo le frequenze del top1  e top2
top1_freq = freq_map_genre.get(top1, 0) # uso per riempire riga
top2_freq = freq_map_genre.get(top2, 0) if top2 else 0 # uso per riempire riga
st.write("Genere top 1: -", top1, " - freq: ", top1_freq)
st.write("Genere top 2: -", top2, "  - freq: ", top2_freq)

# Categorie: selezione multipla per Categorie
top_cats = [c for c in FEATURES if c.startswith("cat_")]
selected_cats = st.multiselect("Categorie:", top_cats)

# Developer
developer = st.selectbox("Developer principale:", options=list(freq_map_dev.keys()))
# Frequenze calcolate come nel preprocessing:
developer_freq = freq_map_dev.get(developer, 0)
st.write("Developer freq:", developer_freq) # stampa per l'utente
top_devs = [d for d in FEATURES if d.startswith("dev_top_")]
selected_dev = st.selectbox("Tutti i Developers - (selezionare se presente)", top_devs)

# Publisher
publisher = st.selectbox("Publisher principale", options=list(freq_map_pub.keys()))
# Frequenze calcolate come nel preprocessing:
publishers_freq = freq_map_pub.get(publisher, 0)
st.write("Publisher freq:", publishers_freq) # stampa per l'utente
top_publishers = [p for p in FEATURES if p.startswith("pub_top_")]
selected_pub = st.selectbox("Tutti i Publishers - (selezionare se presente)", top_publishers)


# Button
if st.button("Predici successo"):
    # Trasforma input in dict di feature
    row = {col: 0 for col in FEATURES}

    # Caricamento variabili
    row["required_age"] = required_age
    row["achievements"] = achievements
    row["platform_count"] = platform_count
    row["is_free"] = int(is_free)
    row["price_log"] = np.log1p(price)
    row["trimester"] = trimester
    row["publishers_freq"] = publishers_freq
    row["developer_freq"] = developer_freq

    # Caricamento top1 e top2
    if genres:
        row["top1_genre_freq"] = top1_freq
        row["top2_genre_freq"] = top2_freq
    else:
        row["top1_genre_freq"] = 0
        row["top2_genre_freq"] = 0

    # Generi e categorie -> 1 se selezionati
    ## i generi hanno bisogno di aggiungere prefisso per essere come dataset
    for g in genres:
        row[f"genre_{g}"] = 1 if g in genres else 0
    # categorie già come le vaariabili del ds
    for c in selected_cats:
        row[c] = 1

    # Publisher e developer selezionati
    if selected_pub:
        row[selected_pub] = 1
    if selected_dev:
        row[selected_dev] = 1

    # Crea DataFrame
    X_demo = pd.DataFrame([row])

    # Predizione
    y_pred = model.predict(X_demo)[0]
    labels = ["insuccesso", "basso successo", "medio successo", "alto successo"]

    st.success(f" Risultato per il gioco '{title}':  **{labels[y_pred]}**")

    # Probabilità associate a tutte le classi
    y_proba = model.predict_proba(X_demo)[0]  # restituisce array con le % per ogni classe

    # Mostra tutte le probabilità
    st.write("### Probabilità per ogni classe:")
    for i, p in enumerate(y_proba):
        st.write(f"Classe {i}: {p:.2%}")

