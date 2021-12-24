#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import random
import math
import numpy as np
import os


# In[2]:


'''
Ce code permet d'étudier toute la base d'enquête. Puis, il procède à la jointure des tables ménage, personne et déplacement.
Il fait ensuite le mapping X,Y ; les départements ; les communes en fonction des codes INSEE comme clé de mapping. 
Ces mappings permettront de faire le filtre des périmètres d'étude (hauts-de-France et Nord-Pas-de-Calais). 
Le code prend en entrée les données issues du code dataHdF_preparing.ipynb stockés dans le dossier input_hdf et du 
traitement sur QGis qui a permis d'avoir pour chaque communes de la France ses coorodnnées X,Y, les codes des départements 
et de communes. Ce code renvoie dans output_hdf les données nécessaires à la génération de la demande de transport.
'''


# In[14]:


print('=======> Read survey concatenated from dataHdF_preparing code and XY commune file from QGIS')
# Ces fonctions permettent d'indiquer les chemins des fichiers input
path_france_xy = "input_hdf/communesFranceXY.csv"
path_menage = "input_hdf/menage_hdf.csv"
path_person = "input_hdf/person_hdf.csv"
path_deplacement ="input_hdf/deplacement_hdf.csv"
path_trajet = "input_hdf/trajet_hdf.csv"
# chargement base donnée revenus disponibles (feuille Ensemble)
path_filosofi = "input_hdf/FILO_DISP_COM.xls"


# In[15]:


# Cette fonction permet de lire données dans un fichier
#Elle prend en entrée le chemin du fichier
def read_file(file_path):
    df = pd.read_csv(file_path, sep=";",encoding='utf8')
    return df


# In[16]:


#Cette fonction permet de sauvegarder des données dans un fichier
#Elle prend en entrée les données et le chemin du fichier de sortie

def save_file(df, output_path):
    df.to_csv(output_path,index=None, sep=',',encoding='utf8')


# # Input

# In[17]:


menage_hdf = pd.read_csv(path_menage, sep=";", dtype=str)
person_hdf  = pd.read_csv(path_person, sep=";", dtype=str)
deplacement_hdf = pd.read_csv(path_deplacement, sep=";", dtype=str)
trajet_hdf = pd.read_csv(path_menage, sep=";", dtype=str)
data_france_xy = pd.read_csv(path_france_xy, sep=",", dtype=str)
filosofi = pd.read_excel(path_filosofi, sheet_name = "ENSEMBLE", skiprows = 5, encoding='utf8', dtype=str)


# In[18]:


#Compte le nombre de ménages, de personnes et de déplacements en Hauts de France de l'échantillon
nbrTotalMen_hdf=menage_hdf.ECH.count()
nbrTotalPers_hdf=person_hdf.PECH.count()
nbrTotalDepl_hdf=deplacement_hdf.DECH.count()


# In[19]:


#Affiche le nombre de ménages, de personnes et de déplacements en Hauts de France de l'échantillon
print("-------> Found %d househols from menage.txt" % nbrTotalMen_hdf)
print("-------> Found %d persons from person.txt" % nbrTotalPers_hdf)
print("-------> Found %d trips from deplacement.txt" % nbrTotalDepl_hdf)


# # REVENU DES MENAGE EN HDF

# In[22]:


print("-------> Affectation de revenu à chaque ménage")
filosofi


# In[46]:


'''Cette fonction permet d'affecter à chaque ménage de résidence MP2 en codes INSEE, des revenus
    Elle renvoie en sortie les nouvelle données avec les revnus
    Elle prend comme entrées: menage, data_income et output_file
        data est les données avec les code INSEE (menage.csv),
        filosofi les données de correspondance code CODGEO et (revenus),
        output_file est le chemin complet du fichier de sortie
'''
# Remplacement des codes INSEE par leur correspondance
def mapping_codeINSEE_income(data, filosofi):
    #select columns
    filosofi.columns =["CODGEO","LIBGEO","NBMEN15","NBPERS15","NBUC15","Q115","Q215","Q315","Q3_Q1","D115","D215","D315",
                      "D415","D615","D715","D815","D915","RD","S80S2015","GI15","PACT15","PCHO15","PTSA15","PBEN15",
                      "PPEN15","PPAT15","PPSOC15","PPFAM15","PPMINI15","PPLOGT15","PIMPOT15"]

# mapping
    # mapping code INSEE avec LIBGEO
    map_LIBGEO = dict(zip(filosofi.CODGEO, filosofi.LIBGEO))
    # mapping code INSEE avec NBMEN15
    map_NBMEN15 = dict(zip(filosofi.CODGEO, filosofi.NBMEN15))
    # mapping code INSEE avec NBPERS15
    map_NBPERS15 = dict(zip(filosofi.CODGEO, filosofi.NBPERS15))
    # mapping code INSEE avec NBUC15
    map_NBUC15 = dict(zip(filosofi.CODGEO, filosofi.NBUC15))
    # mapping code INSEE avec Q115
    map_Q115 = dict(zip(filosofi.CODGEO, filosofi.Q115))
    # mapping code INSEE avec Q215
    map_Q215 = dict(zip(filosofi.CODGEO, filosofi.Q215))
    # mapping code INSEE avec Q315
    map_Q315 = dict(zip(filosofi.CODGEO, filosofi.Q315))
    # mapping code INSEE avec Q3_Q1
    map_Q3_Q1 = dict(zip(filosofi.CODGEO, filosofi.Q3_Q1))
    # mapping code INSEE avec D115
    map_D115 = dict(zip(filosofi.CODGEO, filosofi.D115))
    # mapping code INSEE avec D215
    map_D215 = dict(zip(filosofi.CODGEO, filosofi.D215))
    # mapping code INSEE avec D315
    map_D315 = dict(zip(filosofi.CODGEO, filosofi.D315))
    # mapping code INSEE avec D415
    map_D415 = dict(zip(filosofi.CODGEO, filosofi.D415))
    # mapping code INSEE avec D615
    map_D615 = dict(zip(filosofi.CODGEO, filosofi.D615))
    # mapping code INSEE avec D715
    map_D715 = dict(zip(filosofi.CODGEO, filosofi.D715))
    # mapping code INSEE avec D815
    map_D815 = dict(zip(filosofi.CODGEO, filosofi.D815))
    # mapping code INSEE avec D915
    map_D915 = dict(zip(filosofi.CODGEO, filosofi.D915))
    # mapping code INSEE avec RD
    map_RD = dict(zip(filosofi.CODGEO, filosofi.RD))
    # mapping code INSEE avec S80S2015
    map_S80S2015 = dict(zip(filosofi.CODGEO, filosofi.S80S2015))
    # mapping code INSEE avec GI15
    map_GI15 = dict(zip(filosofi.CODGEO, filosofi.GI15))
    # mapping code INSEE avec PACT15
    map_PACT15 = dict(zip(filosofi.CODGEO, filosofi.PACT15))
    # mapping code INSEE avec PCHO15
    map_PCHO15 = dict(zip(filosofi.CODGEO, filosofi.PCHO15))
    # mapping code INSEE avec PTSA15
    map_PTSA15 = dict(zip(filosofi.CODGEO, filosofi.PTSA15))
    # mapping code INSEE avec PBEN15
    map_PBEN15 = dict(zip(filosofi.CODGEO, filosofi.PBEN15))
    # mapping code INSEE avec PPEN15
    map_PPEN15 = dict(zip(filosofi.CODGEO, filosofi.PPEN15))
    # mapping code INSEE avec PPAT15
    map_PPAT15 = dict(zip(filosofi.CODGEO, filosofi.PPAT15))
    # mapping code INSEE avec PPSOC15
    map_PPSOC15 = dict(zip(filosofi.CODGEO, filosofi.PPSOC15))
    # mapping code INSEE avec PPFAM15
    map_PPFAM15 = dict(zip(filosofi.CODGEO, filosofi.PPFAM15))
    # mapping code INSEE avec PPMINI15
    map_PPMINI15 = dict(zip(filosofi.CODGEO, filosofi.PPMINI15))
    # mapping code INSEE avec PPLOGT15
    map_PPLOGT15 = dict(zip(filosofi.CODGEO, filosofi.PPLOGT15))
    # mapping code INSEE avec PIMPOT15
    map_PIMPOT15 = dict(zip(filosofi.CODGEO, filosofi.PIMPOT15))
    
# création des colonnes
    #Créer des colonnes pour les revenus des résidences des ménages
    data["LIBGEO"]=data["MP2"]
    data["NBMEN15"]=data["MP2"]
    data["NBPERS15"]=data["MP2"]
    data["NBUC15"]=data["MP2"]
    data["Q115"]=data["MP2"]
    data["Q215"]=data["MP2"]
    data["Q315"]=data["MP2"]
    data["Q3_Q1"]=data["MP2"]
    data["D115"]=data["MP2"]
    data["D215"]=data["MP2"]
    data["D315"]=data["MP2"]
    data["D415"]=data["MP2"]
    data["D615"]=data["MP2"]
    data["D715"]=data["MP2"]
    data["D815"]=data["MP2"]
    data["D915"]=data["MP2"]
    data["RD"]=data["MP2"]
    data["S80S2015"]=data["MP2"]
    data["GI15"]=data["MP2"]
    data["PACT15"]=data["MP2"]
    data["PCHO15"]=data["MP2"]
    data["PTSA15"]=data["MP2"]
    data["PBEN15"]=data["MP2"]
    data["PPEN15"]=data["MP2"]
    data["PPAT15"]=data["MP2"]
    data["PPSOC15"]=data["MP2"]
    data["PPFAM15"]=data["MP2"]
    data["PPMINI15"]=data["MP2"]
    data["PPLOGT15"]=data["MP2"]
    data["PIMPOT15"]=data["MP2"]
# remplacement 
    # remplacer les codes INSEE par les revenus
    data[["LIBGEO"]] = data[["LIBGEO"]].applymap(map_LIBGEO.get)
    data[["NBMEN15"]] = data[["NBMEN15"]].applymap(map_NBMEN15.get)
    data[["NBPERS15"]] = data[["NBPERS15"]].applymap(map_NBPERS15.get)
    data[["NBUC15"]] = data[["NBUC15"]].applymap(map_NBUC15.get)
    data[["Q115"]] = data[["Q115"]].applymap(map_Q115.get)
    data[["Q215"]] = data[["Q215"]].applymap(map_Q215.get)
    data[["Q315"]] = data[["Q315"]].applymap(map_Q315.get)
    data[["Q3_Q1"]] = data[["Q3_Q1"]].applymap(map_Q3_Q1.get)
    data[["D115"]] = data[["D115"]].applymap(map_D115.get)
    data[["D215"]] = data[["D215"]].applymap(map_D215.get)
    data[["D315"]] = data[["D315"]].applymap(map_D315.get)
    data[["D415"]] = data[["D415"]].applymap(map_D415.get)
    data[["D615"]] = data[["D615"]].applymap(map_D615.get)
    data[["D715"]] = data[["D715"]].applymap(map_D715.get)
    data[["D815"]] = data[["D815"]].applymap(map_D815.get)
    data[["D915"]] = data[["D915"]].applymap(map_D915.get)
    data[["RD"]] = data[["RD"]].applymap(map_RD.get)
    data[["S80S2015"]] = data[["S80S2015"]].applymap(map_S80S2015.get)
    data[["GI15"]] = data[["GI15"]].applymap(map_GI15.get)
    data[["PACT15"]] = data[["PACT15"]].applymap(map_PACT15.get)
    data[["PCHO15"]] = data[["PCHO15"]].applymap(map_PCHO15.get)
    data[["PTSA15"]] = data[["PTSA15"]].applymap(map_PTSA15.get)
    data[["PBEN15"]] = data[["PBEN15"]].applymap(map_PBEN15.get)
    data[["PPEN15"]] = data[["PPEN15"]].applymap(map_PPEN15.get)
    data[["PPAT15"]] = data[["PPAT15"]].applymap(map_PPAT15.get)
    data[["PPSOC15"]] = data[["PPSOC15"]].applymap(map_PPSOC15.get)
    data[["PPFAM15"]] = data[["PPFAM15"]].applymap(map_PPFAM15.get)
    data[["PPMINI15"]] = data[["PPMINI15"]].applymap(map_PPMINI15.get)
    data[["PPLOGT15"]] = data[["PPLOGT15"]].applymap(map_PPLOGT15.get)
    data[["PIMPOT15"]] = data[["PIMPOT15"]].applymap(map_PIMPOT15.get)
    
# suppression des données dont les ménages ne sont pas dans les HdF ==> menage_income    
    data = data.dropna(subset=["Q215"])
    return data


# In[47]:


# Application de la fonction de mapping MP2 avec les revenus : 
# 119 ménages n'ont pas de revenus et devront prendre les valeurs des ménages plus proches
menage_income = mapping_codeINSEE_income(menage_hdf, filosofi)


# In[48]:


NbrCommSansRevMedian = len(menage_hdf) - len(menage_income)
print('-------> Nombre de ménages sans revenu médian =')
print(NbrCommSansRevMedian)


# In[49]:


menage_hdf


# # DEPLACEMENT DES PERSONNES EN HdF

# In[50]:


print('=======> Merge menage and person')
# Quels sont les ménages des personnes
menage_person_hdf = pd.merge(person_hdf, menage_hdf, how='left',on ="ECH")


# In[51]:


print('--------> menage_person_hdf')
menage_person_hdf


# In[52]:


menage_person_hdf.to_csv("output_hdf/fusion/menage_person_hdf.csv", index=None, sep=";")


# In[53]:


print('=======> Merge menage, person and deplacement')


# In[54]:


# Quels sont les déplacements des personnes : 
deplacement_menage_person_hdf = pd.merge(deplacement_hdf, menage_person_hdf, how='left',on ="PECH")


# In[55]:


# Trier selon DECH
trips=deplacement_menage_person_hdf.sort_values(by = 'DECH')


# In[56]:


trips.to_csv("output_hdf/fusion/trips.csv", index=None, sep=";")


# In[57]:


print('--------> deplacement_menage_person_hdf')
trips


# # Jointure des données pour récuperer les coordonnées X et Y

# In[58]:


print('=========> Merge trips with cordonates XY')
print('---------> Base XY centroid of municiplities of France')
data_france_xy


# In[59]:


'''Cette fonction permet de remplacer les codes INSEE par les coordonnées (X et Y), les départements
    Elle renvoie en sortie les nouvelle données avec les coordonnées X et Y, les codes départementaux 
    Elle prend comme entrées: data, data_france_xy et output_file
        data est les données avec les code INSEE (déplacement.txt),
        data_france_xy les données de correspondance code INSEE et (X, Y) des communes françaises,
        output_file est le chemin complet du fichier de sortie
'''

# Remplacement des codes INSEE par leur correspondance
def mapping_codeINSEE_xyFrance(data, data_france_xy):
    #select columns
    data_france_xy.columns =["ID_GEOFLA","CODE_COM","INSEE_CODE","NOM_COM","STATUT","X_CHF_LIEU","Y_CHF_LIEU","X_CENTROID",
                             "Y_CENTROID","Z_MOYEN","SUPERFICIE","POPULATION","CODE_CANT","CODE_ARR","CODE_DEPT","NOM_DEPT",
                             "CODE_REG","NOM_REG","Xcord","Ycord"]
# mapping

    # mapping code INSEE et coordonnées (nécessaire pour la localisation des activités : pour les variables D3 et D7)
    map_x = dict(zip(data_france_xy.INSEE_CODE, data_france_xy.Xcord))
    map_y = dict(zip(data_france_xy.INSEE_CODE, data_france_xy.Ycord))
   
    # mapping code INSEE avec superficie (nécessaire pour la distribution des agents de la même commune : pour D3 et D7)
    map_sup = dict(zip(data_france_xy.INSEE_CODE, data_france_xy.SUPERFICIE))
    
    # mapping code INSEE avec département (nécssaire pour l'anayse des flux : pour les variables PP2, DP2, D3 et D7)
    map_dept = dict(zip(data_france_xy.INSEE_CODE, data_france_xy.CODE_DEPT))
    
    # mapping code INSEE avec région (nécssaire pour l'anayse des flux : pour les variables PP2, DP2, D3 et D7)
    map_reg = dict(zip(data_france_xy.INSEE_CODE, data_france_xy.CODE_REG))

    
# création de colonnes

    #Créer des colonnes pour X et Y
    data["D3X"] = data["D3"]
    data["D3Y"] = data["D3"]
    data["D7X"] = data["D7"]
    data["D7Y"] = data["D7"]
    
    # Créer des colonnes pour Superficie
    data["SUP_D3"]=data["D3"]
    data["SUP_D7"]=data["D7"]
    
    # créer des colonnes pour CODE_DEPT
    data["CODEDEPT_D3"]=data["D3"]
    data["CODEDEPT_D7"]=data["D7"]
    data["CODEDEPT_PP2"]=data["PP2"]
    data["CODEDEPT_DP2"]=data["DP2"]
    
    # créer des colonnes pour CODE_REG
    data["CODEREG_D3"]=data["D3"]
    data["CODEREG_D7"]=data["D7"]
    data["CODEREG_PP2"]=data["PP2"]
    data["CODEREG_DP2"]=data["DP2"]

        
# remplacement    

    # remplacer les codes INSEE par les coordonnées
    data[["D3X","D7X"]] = data[["D3X","D7X"]].applymap(map_x.get)
    data[["D3Y","D7Y"]] = data[["D3Y","D7Y"]].applymap(map_y.get)
    
    # remplacer les codes INSEE par les superficies
    data[["SUP_D3"]] = data[["SUP_D3"]].applymap(map_sup.get)
    data[["SUP_D7"]] = data[["SUP_D7"]].applymap(map_sup.get)
    
    # remplacer les codes INSEE par les départements
    data[["CODEDEPT_D3"]] = data[["CODEDEPT_D3"]].applymap(map_dept.get)
    data[["CODEDEPT_D7"]] = data[["CODEDEPT_D7"]].applymap(map_dept.get)
    data[["CODEDEPT_PP2"]] = data[["CODEDEPT_PP2"]].applymap(map_dept.get)
    data[["CODEDEPT_DP2"]] = data[["CODEDEPT_DP2"]].applymap(map_dept.get)

    # remplacer les codes INSEE par les régions
    data[["CODEREG_D3"]] = data[["CODEREG_D3"]].applymap(map_reg.get)
    data[["CODEREG_D7"]] = data[["CODEREG_D7"]].applymap(map_reg.get)
    data[["CODEREG_PP2"]] = data[["CODEREG_PP2"]].applymap(map_reg.get)
    data[["CODEREG_DP2"]] = data[["CODEREG_DP2"]].applymap(map_reg.get)

    
    # suppression des données dont les coordonnées X,Y ne figurent pas dans la base ComunesXY.csv ==> travelDiary_hdf
    data = data.dropna(subset=["D3X","D3Y", "D7X","D7Y"])
    
    #data[cols].to_csv(output_file,index=None, sep=";")
    
    return data


# In[60]:


# Application de la fonction de mapping à partir des XY de la france
print('---------> Application of mapping XY function')
deplacement_xy_france = mapping_codeINSEE_xyFrance(trips, data_france_xy)


# In[61]:


print('---------> deplacement_xy_france mapped')
deplacement_xy_france # 5310 déplacements sans X ou Y de la base HdF


# In[62]:


print('---------> deplacement_xy_france mapped with origin or destination not in France')
trips 


# In[63]:


trips_outside = len(trips) - len(deplacement_xy_france)
print("-------> Found %d trips for which the origin or the destination is out of France" % trips_outside)


# In[77]:


print("========> Extraction of relevant variables for MATSim")
# Extraction des variables pertinentes pour l'étude : données qui n'ont pas de correspondance X,Y sont enlevées
travelDiary_hdf = deplacement_xy_france[["DECH","PECH","COEQ","DP2","D4A","D4B","D3","D3X","D3Y","D2AA","D8A","D8B",
                                         "D7","D7X","D7Y","D5AA","MODP","NDEP","SUP_D3","SUP_D7","CODEDEPT_D3","CODEREG_D3",
                                         "CODEDEPT_D7","CODEREG_D7","MTDQ","PTDQ","P4","P2","P5","P10","M5","DOIB","DIST",
                                         "D8C","D9","M6A","M6B","M6C","M6D","CODEDEPT_PP2","CODEREG_PP2","CODEDEPT_DP2",
                                         "CODEREG_DP2","Q115","Q215","Q315","Q3_Q1","D115","D215","D315","D415","D615",
                                         "D715","D815","D915","ECH_x"]]


# In[78]:


travelDiary_hdf


# In[79]:


travelDiary_hdf.to_csv("output_hdf/travelDiaries/travelDiary_hdf.csv", index=None, sep=";")


# # Application du filtre pour le Nord pas de Calais

# In[82]:


## Déplacements pour le Nord-Pas-de-calais en tant qu'origine ou destination de flux de la région
## travelDiary_hdf est utilisé car constitue la base où les X,Y des communes sont connus 
print("========> Filter trips in studied area : Departments of Nord-Pas-de-Calais has been taked as spatial zone")
is_deplNpdcXY = (travelDiary_hdf["CODEDEPT_D3"] == '59') | (travelDiary_hdf["CODEDEPT_D7"]=='62') | (travelDiary_hdf["CODEDEPT_D7"] == '59') | (travelDiary_hdf["CODEDEPT_D3"]=='62')

travelDiary_npdcXY = travelDiary_hdf[is_deplNpdcXY]

travelDiary_npdcXY.to_csv("output_hdf/travelDiaries/travelDiaryDeciles_npdcXY.csv", index=None, sep=";")


# In[83]:


travelDiary_npdcXY


# In[ ]:





# # Evaluation de la population dans la zone d'étude

# In[50]:


# Déplacement des personnes en NPdC en tant qu'origine ou destination (intra-NPdC & origine ou destination HdF)
PECH_personsXY = travelDiary_npdcXY['PECH'].astype(str)


# In[51]:


j=0
for PECH in list(set(PECH_personsXY)):
    j=j+1
print('-------> Nbr persons qui se déplacent en NPdC avec soit une origine ou une destination en HdF : used for demand')
print(j)


# In[52]:


print('=======> Verify occurency from data ID')
occurencePECH = travelDiary_npdcXY.PECH.value_counts()


# In[53]:


occurencePECH


# # Fin du code

