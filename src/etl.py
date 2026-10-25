import pandas as pd
import glob
from pathlib import Path

def extract(raw_dir: str) -> pd.DataFrame:
    """Extrae y combina todos los archivos JSON de Audio en un solo DataFrame."""
    # Leemos solo los archivos de Audio para enfocarnos en la música
    files = glob.glob(f"{raw_dir}/Streaming_History_Audio_*.json")
    
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos de audio en {raw_dir}")
        
    dfs = [pd.read_json(f) for f in files]
    df_raw = pd.concat(dfs, ignore_index=True)
    print(f"Extraídos {len(df_raw)} registros en total.")
    return df_raw

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpieza, filtrado y normalización de tipos."""
    # 1. Copia para no modificar el original
    df_clean = df.copy()
    
    # 2. Filtrar solo música (descartar nulos en track_name)
    df_clean = df_clean.dropna(subset=['master_metadata_track_name'])
    
    # 3. Filtrar reproducciones menores a 30 segundos
    df_clean = df_clean[df_clean['ms_played'] >= 30000]
    
    # 4. Normalizar el timestamp (ts) a tipo datetime
    df_clean['ts'] = pd.to_datetime(df_clean['ts'])
    
    # 5. Seleccionar y renombrar columnas útiles
    columnas_utiles = {
        'ts': 'played_at',
        'ms_played': 'ms_played',
        'master_metadata_track_name': 'track_name',
        'master_metadata_album_artist_name': 'artist_name',
        'master_metadata_album_album_name': 'album_name',
        'spotify_track_uri': 'track_uri',
        'reason_start': 'reason_start',
        'reason_end': 'reason_end',
        'shuffle': 'shuffle',
        'skipped': 'skipped'
    }
    
    df_clean = df_clean[list(columnas_utiles.keys())].rename(columns=columnas_utiles)
    
    print(f"Tras la limpieza, quedan {len(df_clean)} registros válidos de música.")
    return df_clean

def load(df: pd.DataFrame, output_dir: str):
    """Guarda el DataFrame limpio en formato Parquet."""
    output_path = f"{output_dir}/spotify_clean.parquet"
    # Guardamos en Parquet usando el motor pyarrow
    df.to_parquet(output_path, engine='pyarrow', index=False)
    print(f"Datos guardados exitosamente en: {output_path}")

if __name__ == "__main__":
    # Configuración de rutas
    RAW_DIR = "data/raw"
    PROCESSED_DIR = "data/processed"
    
    # Ejecución de la pipeline ETL
    df_raw = extract(RAW_DIR)
    df_transformed = transform(df_raw)
    load(df_transformed, PROCESSED_DIR)
