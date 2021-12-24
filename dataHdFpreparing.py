#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import random
import math
import numpy as np
import os


'''
Ce code fait la concaténation des clés des tables menage (ECH), person (PECH) et deplacement (DECH) avec le numéro et l’année d’enquête pour éviter les doublons. Il prend en entrée les données situées dans le dossier data_hdf fourni par le conseil régional des Hauts-de-France (les variables étant séparées en amont avec un éditeur et stocké dans le dossier cache).
Le code sort les données dans le dossier input_hdf prêt pour le traitement avec le code ermd2016_to_travelDiaries.ipynb
@ AUTHOR : Ngagne Demba DIOP
-- VERSION : mai 2021
'''

# Lire les fichiers d'entrée séparés à partir des données brutes de format particulier
print('=======> Read raw survey files')
menage_hdf = pd.read_csv("/home/ndiop/Documents/phd/scripts/demandCreation/data_hdf/menage.txt", sep=";", dtype=str) # 78251 ménages enquêtés
person_hdf = pd.read_csv("/home/ndiop/Documents/phd/scripts/demandCreation/data_hdf/person.txt", sep=";", dtype=str) # 76751 peronnes enquêtées
deplacement_hdf = pd.read_csv("/home/ndiop/Documents/phd/scripts/demandCreation/data_hdf/deplacement.txt", sep=";", dtype=str) # 301760 déplacements observés
trajet_hdf = pd.read_csv("/home/ndiop/Documents/phd/scripts/demandCreation/data_hdf/trajet.txt", sep=";", dtype=str) # 246242 trajets observés

menage_hdf.head()
person_hdf.head()
deplacement_hdf.head()
trajet_hdf.head()

# Vérification des occurences, ECH est la clé de menage
print('=======> Verify occurency from households ID')
occurenceMenage = menage_hdf.ECH.value_counts()
occurenceMenage
occur_menage = len(menage_hdf) - len(occurenceMenage)
print("-------> Found %d occurences with same household ID" % occur_menage)

# Concaténation des clés
print('=======> Concatenate base IDs with number and year survey')
# base ménage : Concaténation des colonnes MEMD, MANN et ECH pour solutionner les problèmes de doublons sur ECH
menage_hdf["ECH"] = menage_hdf["MEMD"] + menage_hdf["MANN"] + menage_hdf["ECH"]
# base personne : Concaténation des colonnes PEMD, PANN et PECH pour solutionner les problèmes de doublons sur PECH
person_hdf["PECH"] = person_hdf["PEMD"] + person_hdf["PANN"] + person_hdf["PECH"]
# base personne : Concaténation des colonnes PEMD, PANN et ECH pour récupérer les mêmes valeurs de ECH que la base ménage
person_hdf["ECH"] = person_hdf["PEMD"] + person_hdf["PANN"] + person_hdf["ECH"]
# base déplacement : Concaténation des colonnes DEMD, DANN et ECH pour récupérer les mêmes valeurs de ECH que la base ménage
deplacement_hdf["ECH"] = deplacement_hdf["DEMD"] + deplacement_hdf["DANN"] + deplacement_hdf["ECH"]
# base déplacement : Concaténation des colonnes DEMD, DANN et PECH pour récupérer les mêmes valeurs de PECH que la base personne
deplacement_hdf["PECH"] = deplacement_hdf["DEMD"] + deplacement_hdf["DANN"] + deplacement_hdf["PECH"]
# base personne : Concaténation des colonnes DEMD, DANN et DECH pour solutionner les problèmes de doublons sur DECH
deplacement_hdf["DECH"] = deplacement_hdf["DEMD"] + deplacement_hdf["DANN"] + deplacement_hdf["DECH"]
# base trajet : Concaténation des colonnes TEMD, TANN et ECH pour récupérer les mêmes valeurs de ECH que la base ménage
trajet_hdf["ECH"] = trajet_hdf["TEMD"] + trajet_hdf["TANN"] + trajet_hdf["ECH"]
# base trajet : Concaténation des colonnes TEMD, TANN et PECH pour récupérer les mêmes valeurs de PECH que la base personne
trajet_hdf["PECH"] = trajet_hdf["TEMD"] + trajet_hdf["TANN"] + trajet_hdf["PECH"]
# base trajet : Concaténation des colonnes TEMD, TANN et DECH pour récupérer les mêmes valeurs de DECH que la base déplacement
trajet_hdf["DECH"] = trajet_hdf["TEMD"] + trajet_hdf["TANN"] + trajet_hdf["DECH"]

print('-------> menage_hdf')
menage_hdf
print('-------> person_hdf')
person_hdf
print('-------> deplacement_hdf')
deplacement_hdf
print('-------> trajet_hdf')
trajet_hdf

# Revérification des occurences
print('=======> Verify occurency from data ID')
occurenceMenage = menage_hdf.ECH.value_counts()
occurencePerson = person_hdf.PECH.value_counts()
occurenceDeplacement = deplacement_hdf.DECH.value_counts()
occurenceTrajet = trajet_hdf.PECH.value_counts()

occurenceMenage
occurencePerson
occurenceDeplacement

occur_menage = len(menage_hdf) - len(occurenceMenage)
occur_person = len(person_hdf) - len(occurencePerson)
occur_deplacement = len(deplacement_hdf) - len(occurenceDeplacement)
occur_trajet = len(trajet_hdf) - len(occurenceTrajet)

print("-------> Found %d occurences with same ID_menage" % occur_menage)
print("-------> Found %d occurences with same ID_person" % occur_person)
print("-------> Found %d occurences with same ID_deplacement" % occur_deplacement)

# Exporte les bases qui serviront d'input pour le code ermd2016_to_travelDiaries
print('=======> Saving data concatenated to input folder for ermd_to_travelDiaries code')
menage_hdf.to_csv("/home/ndiop/Documents/phd/scripts/demandCreation/input_hdf/menage_hdf.csv", index=None, sep=";")
person_hdf.to_csv("/home/ndiop/Documents/phd/scripts/demandCreation/input_hdf/person_hdf.csv", index=None, sep=";")
deplacement_hdf.to_csv("/home/ndiop/Documents/phd/scripts/demandCreation/input_hdf/deplacement_hdf.csv", index=None, sep=";")
trajet_hdf.to_csv("/home/ndiop/Documents/phd/scripts/demandCreation/input_hdf/trajet_hdf.csv", index=None, sep=";")




