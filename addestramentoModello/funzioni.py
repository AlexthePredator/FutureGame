import ast
import pandas as pd
import re
import string

# Parser : ogni cella diventi una lista di generi 
# (da stringa ottenuta dal dataset a lista)
def parse_fromString_toList(x):
    if isinstance(x, list):
        return [str(s).strip() for s in x if str(s).strip() != ""]
    if pd.isna(x):
        return []
    if isinstance(x, str):
        s = x.strip()
        # stringa che rappresenta una lista Python
        if s.startswith('[') and s.endswith(']'):
            try:
                v = ast.literal_eval(s)
                if isinstance(v, list):
                    return [str(t).strip() for t in v if str(t).strip() != ""]
            except Exception:
                pass
        # fallback: separo per virgola oppure tengo il token singolo
        if ',' in s:
            parts = [p.strip().strip("'").strip('"') for p in s.split(',')]
            return [p for p in parts if p]
        return [s.strip("'").strip('"')]
    # qualunque altro tipo sconosciuto
    return []

# estrae primo valore dalla cella (tipo lista)
def estrai_primo(val):
    # caso missing
    if pd.isna(val):
        return None
    # caso stringa che rappresenta lista
    if isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed[0]   # primo elemento
            else:
                return None        # lista vuota
        except Exception:
            return val  # fallback: magari era già stringa semplice
    # caso lista già vera
    if isinstance(val, list):
        return val[0] if len(val) > 0 else None
    # fallback generico
    return None

def formatta_testo(text):
    # Sostituisci tutti gli spazi (anche multipli) con "_"
    text = re.sub(r'\s+', '_', text)
    # Rimuovi la punteggiatura
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Rimuovi i numeri
    #text = re.sub(r'\d+', '', text)
    # Rimuovi i caratteri speciali e simboli (ma lascia gli "_")
    text = re.sub(r'[^a-zA-Z_]', '', text)
    return text