import ast
import pandas as pd

# Parser robusto: assicura che ogni cella diventi una LISTA di generi
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