import logging
import numpy as np
from src.config import FEATURES, TARGET

log = logging.getLogger(__name__)

def filtre_ptid(df):
    df = df.copy()
    nb_avant = len(df)
    df = df[~df["PTID"].str.startswith("381_S_10", na=False)]
    log.info("Lignes supprimées : %s", nb_avant - len(df))
    log.info("Lignes restantes : %s", len(df))

    return df

def remplacer_valeurs_invalides(df):
    nb_nan_avant = df.isnull().sum().sum()
    df = df.replace([-4, -1, 9999], np.nan)
    nb_nan_apres = df.isnull().sum().sum()
    log.info("Valeurs manquantes ajoutées : %s", nb_nan_apres - nb_nan_avant)
    
    return df

def supprimer_doublons(df):
    nb_avant = len(df)
    df = df.drop_duplicates()

    log.info("Doublons supprimés : %s", nb_avant - len(df))
    log.info("Lignes restantes : %s", len(df))

    # Supprimer les lignes où la valeur existe mais l'unité est manquante
    nb_avant = len(df)
    df = df[~((df["VSHEIGHT"].notna()) & (df["VSHTUNIT"].isna()))]
    df = df[~((df["VSWEIGHT"].notna()) & (df["VSWTUNIT"].isna()))]

    log.info("Lignes supprimées (unité manquante) : %s", nb_avant - len(df))

    return df

def convertir_taille_poids(df):
    # Poids : livres → kilogrammes
    df.loc[df["VSWTUNIT"] == 1, "VSWEIGHT"] = (
        df.loc[df["VSWTUNIT"] == 1, "VSWEIGHT"] / 2.20462
    ).round(0)

    log.info("Poids moyen : %s kg", round(df["VSWEIGHT"].mean(), 1))

    # Taille : pouces → centimètres
    df.loc[df["VSHTUNIT"] == 1, "VSHEIGHT"] = (
        df.loc[df["VSHTUNIT"] == 1, "VSHEIGHT"] * 2.54
    ).round(0)

    log.info("Taille moyenne : %s cm", round(df["VSHEIGHT"].mean(), 1))


    return df

def nettoyer_diagnosis(df):   
    # Remplacement des valeurs
    df["DIAGNOSIS"] = df["DIAGNOSIS"].replace({1: 0, 2: 1, 3: 1})
    
    # Affichage de la distribution
    log.info("Distribution de la cible :")
    log.info(df["DIAGNOSIS"].value_counts())
    
    return df



def calculer_indicateurs(df):
    df = df.copy()

    # IMC
    df["IMC"] = df["VSWEIGHT"] / ((df["VSHEIGHT"] / 100) ** 2)
    log.info("IMC moyen : %s", round(df["IMC"].mean(), 1))

    # Ratio tension artérielle
    df["RtensionA"] = df["VSBPSYS"] / df["VSBPDIA"]
    log.info("Ratio tension moyen : %s", round(df["RtensionA"].mean(), 2))

    # Pression pulsée
    df["pressionP"] = df["VSBPSYS"] - df["VSBPDIA"]
    log.info("Pression pulsée moyenne : %s", round(df["pressionP"].mean(), 1))

    return df


def garder_colonnes_finales(df):
    df = df.copy()
    df=df[FEATURES]
    log.info("Colonnes conservées : %s", len(FEATURES) + len([TARGET]))

    return df



  