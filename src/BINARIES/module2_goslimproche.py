#!/usr/bin/python

import BINARIES.module1 as module1
import BINARIES.module4_Logs as module4_Logs
import re
import os.path
import shutil
import time

"""
La fonction "AjoutFileGOSlim" prend un fichier de GO number et le parcours puis ajoute chaque GO dans l'objet DICO_GO en tant que GOSLIM
"""

def AjoutFileGOSlim(dico_go,nomfichier):#Fonction qui ajoute des GOslims personnels dans un dico
    File = open(nomfichier,"r")
    tab_newGoSlim=[]
    for line in File :#Boucle qui lit le fichier
        line=line.rstrip()
        tmp=line.split(";")
        tab_newGoSlim.append(tmp[0])
    compteurGoslim_user=dico_go.addTabGoslim(tab_newGoSlim)#Fonction qui ajoute des GOslims personnels
    return(compteurGoslim_user)#Renvoie le nombre de Goslims ajoutes 

"""
DOC
La fonction "GiveGOSlim" prend en entree un fichier avec les genes et GO ou seulement les GO.
Pour chaque GO la fonction recherche les GOslims proches et tous les GOslims parmi les parents du GO.
La fonction genere un fichier de sortie puis lance le module4 qui genere les logs.
"""
    
def GiveGOSlim (nomfichierentree, nomfichiersorti, nomfichierGoSlim, relation, commentaire,formatInput, nomfichierOBO='DATA/go.obo'):#Fonction principale du programme
    print("formatData : ",formatInput)
    print("relation :",relation)
    tab_acc=[]
    path="./Sorties_"+time.strftime('%Y-%m-%d-%HH-%Mmin')
    if not os.path.exists(path):    #remplace le chemin relatif par le chemin absolu
        os.mkdir(path)#Creation du dossier de sortie
    compteurAccTraite=0
    dico_go=module1.Dico_go()
    dico_go.remplirDico(nomfichierOBO)#Fonction qui remplit les dictionnaires de relations en fonction du fichier "go.obo"
    compteurGoslim_user=0
    dico=dico_go.GetRelationP(relation)#Fonction qui renvoie le dictionnaire utile de la relation
    if(nomfichierGoSlim is not None):#Condition si l'utilisateur veux rentrer un fichier de GOSlim personnel
        compteurGoslim_user=AjoutFileGOSlim(dico_go,nomfichierGoSlim)
    File = open(nomfichierentree,"r")
    tmp=nomfichiersorti.split(".")
    nomfichiersorti=tmp[0]+"_"+relation+"."+tmp[1] # LE FICHIER NE DOIT PAS AVOIR DE POINTS "." DANS SON NOM A PART POUR L EXTENSION.
    FileSortir=open(nomfichiersorti, "w")
    if formatInput=="ACCandGO":
        FileSortir.write("Accession Number"+";"+"GO"+";"+"close GOSlim"+";"+"close GOSlim name"+";"+"path GOSlims"+"\n")
    if formatInput=="GO":
        FileSortir.write("GO"+";"+"close GOSlim"+";"+"close GOSlim name"+";"+"path GOSlims"+"\n")
    for line in File :
        line=line.rstrip()
        tmp=line.split("\t")
        if formatInput=="ACCandGO":
            if re.search("GO:",tmp[1])is None: #On enleve l'en-tete
                continue
        if re.search("GO:",tmp[0])is None and formatInput=="GO": #On enleve l'en-tete
            continue
        if len(tmp)<2 and formatInput=="ACCandGO":
            print("EXCEPTION:",line)
            continue
        if len(tmp)<1 and formatInput=="GO":
            print("EXCEPTION:",line)
            continue
        if formatInput=="ACCandGO":
            acc=tmp[0]
            tab_acc.append(acc)
            go=tmp[1]
        if formatInput=="GO":
            go=tmp[0]
        (goslim_proche, goslim_chemin)=dico_go.chemin(go,dico,relation)#Fonction qui renvoie le chemin parentale d'un GO
        goslim_proche_name=dico_go.getName(goslim_proche)#Fonction qui renvoie le nom d'un GO
        if goslim_proche_name != "no_name":#On compte les genes traites par le programme
            compteurAccTraite+=1
        if formatInput=="ACCandGO":
            FileSortir.write(acc+";"+go+";"+goslim_proche+";"+goslim_proche_name+";"+" ".join(goslim_chemin)+"\n")
        if formatInput=="GO":
            FileSortir.write(go+";"+goslim_proche+";"+goslim_proche_name+";"+" ".join(goslim_chemin)+"\n")
    File.close()
    FileSortir.close()
    shutil.move(nomfichiersorti, path+"/"+nomfichiersorti)#Deplace le fichier dans le dossier Sorties
    print("Fini parcours acc.")
    if formatInput=="ACCandGO":
        module4_Logs.CallLog(tab_acc,compteurAccTraite,path+"/"+nomfichiersorti,dico_go,compteurGoslim_user,path,relation,commentaire)#Fonction qui creee les fichiers logs
        print("Fini Logs.")