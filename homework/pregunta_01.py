import pandas as pd
import os

def pregunta_01():
    """
    Limpia el archivo 'files/input/solicitudes_de_credito.csv' aplicando
    transformaciones en texto, conversión de tipos y eliminación de datos
    duplicados o faltantes. El resultado se guarda en 'files/output/solicitudes_de_credito.csv'.
    """
    procesar_solicitudes(
        entrada="files/input/solicitudes_de_credito.csv",
        salida="files/output/solicitudes_de_credito.csv"
    )

def cargar_datos(ruta):
    return pd.read_csv(ruta, sep=";", index_col=0)

def estandarizar_texto(df, campo):
    df[campo] = (
        df[campo]
        .str.lower()
        .str.strip()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.replace("$", "", regex=False)
    )
    return df

def limpiar_datos(df):
    campos_a_normalizar = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "monto_del_credito",
        "línea_credito",
    ]
    
    for campo in campos_a_normalizar:
        df = estandarizar_texto(df, campo)

    df["barrio"] = (
        df["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )
    
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce").astype("Int64")
    df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce")
    
    fechas_1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fechas_2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    df["fecha_de_beneficio"] = fechas_1.combine_first(fechas_2)

    df = df.drop_duplicates()
    df = df.dropna()

    return df

def procesar_solicitudes(entrada, salida):
    df_original = cargar_datos(entrada)
    df_limpio = limpiar_datos(df_original)
    
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    df_limpio.to_csv(salida, sep=";", index=False)

if __name__ == "__main__":
    pregunta_01()
