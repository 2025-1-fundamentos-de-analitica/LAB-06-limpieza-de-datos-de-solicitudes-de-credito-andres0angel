import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    main(
        input_file="files/input/solicitudes_de_credito.csv",
        output_file="files/output"
    )


def load_data(input_file):
    datos = pd.read_csv(input_file, sep=";", index_col=0)
    return datos


def text_normalization(df, col):
    df[col] = (
        df[col]
        .str.lower()
        .str.strip()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    return df


def main(input_file, output_file):
    columnas_objetivo = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "monto_del_credito",
        "línea_credito",
    ]

    datos_crudos = load_data(input_file)

    for col in columnas_objetivo:
        datos_crudos = text_normalization(datos_crudos, col)

    datos_crudos["barrio"] = (
        datos_crudos["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    datos_crudos["comuna_ciudadano"] = datos_crudos["comuna_ciudadano"].astype(int)
    datos_crudos["monto_del_credito"] = datos_crudos["monto_del_credito"].astype(float)

    fechas_1 = pd.to_datetime(datos_crudos["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fechas_2 = pd.to_datetime(datos_crudos["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    datos_crudos["fecha_de_beneficio"] = fechas_1.combine_first(fechas_2)

    datos_limpios = datos_crudos.drop_duplicates().dropna()

    save_output(datos_limpios, "solicitudes_de_credito", output_file)


def save_output(df_final, nombre_archivo, ruta_salida="files/output"):
    os.makedirs(ruta_salida, exist_ok=True)
    df_final.to_csv(
        os.path.join(ruta_salida, f"{nombre_archivo}.csv"),
        sep=";",
        index=False
    )


if __name__ == "__main__":
    pregunta_01()
