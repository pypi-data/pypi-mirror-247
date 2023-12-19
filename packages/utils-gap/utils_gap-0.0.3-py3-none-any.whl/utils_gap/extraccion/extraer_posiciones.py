import pandas as pd
from datetime import timedelta
from src.utils_gap.utils.fechas import from_pd_date

def extraer_posiciones(data_path, first_day, last_pos_path=""):
    df = extraccion(data_path)
    print(f"Largo df: {len(df)}")

    if not first_day:
        df_last_pos = extraer_historicos(last_pos_path)
        df = pd.concat([df, df_last_pos], ignore_index=True)
        print(f"Largo nuevas posiciones df: {len(df)}")

    return parse_features(df)

def extraer_historicos(data_path):
    df = pd.read_csv(data_path, parse_dates=["msgdate"])
    df["msgdate"] = df["msgdate"].apply(from_pd_date)
    df["mmsi"] = df["mmsi"].apply(lambda x: str(int(x)))

    return df

def extraccion(data_path):
    df = pd.read_parquet(data_path, engine='pyarrow')
    df = df.reset_index(drop=True)

    df = df.dropna(subset=["MMSI"]).reset_index(drop=True)
    df["MMSI"] = df["MMSI"].apply(lambda x: str(int(x)))

    df.rename(columns={"msgTime": "msgdate"}, inplace=True)
    df.columns = [c.lower() for c in df.columns]

    df = df.drop(["_id", "type", "truemmsi", "mmsitype"], axis=1)
    df["msgdate"] = df["msgdate"].apply(from_pd_date)

    return df

def parse_features(df):
    df = df.sort_values(by="msgdate").reset_index(drop=True)
    df = df.reset_index().rename(columns={"index": "idx"})

    df["next_msgdate"] = (df.groupby('mmsi')['msgdate'].shift(-1) - df['msgdate']).fillna(timedelta(hours=0))
    df["next_idx"] = df.groupby('mmsi')['idx'].shift(-1).fillna(0).astype(int)

    return df