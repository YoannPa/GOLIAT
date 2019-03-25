#!/usr/bin/python

import BINARIES.module1 as module1
import os
import re
import shutil



def CallLog(tabAllAcc,compteurAccTraite,nomfichiersorti,dico_go,compteurGoslim_user,path,relation,commentaire):#Fonction qui ouvre le fichier OutPut et qui creee un tableau pour les differents Logs.
    Tableau_file=[]
    Tableau_GoSlim=[]
    File = open(nomfichiersorti, "r")
    File.readline()
    for line in File :
        line=line.rstrip()
        tmp=line.split(";")
        Tableau_file.append(line)
        Tableau_GoSlim.append(tmp[2])
    Tableau_GoSlim=set(Tableau_GoSlim)    
    File.close()
    MakeLog(Tableau_file, Tableau_GoSlim, tabAllAcc, compteurAccTraite,compteurGoslim_user,path,relation,commentaire)#Fonction qui creee une matrice du fichier Logs.csv
    MakeLog_matrix(Tableau_file,path,relation)
    MakeLog_OntologyByGoSlim(Tableau_file,dico_go,compteurAccTraite,path,relation,commentaire)
    MakeLog_OntologyByACC(Tableau_file,dico_go,path,relation)

def MakeLog (Tableau_file,Tableau_GoSlim,tabAllAcc,compteurAccTraite,compteurGoslim_user,path,relation,commentaire):
    nameFile="Logs_"+relation+".csv"
    FileLogs=open(nameFile, "w")
    if commentaire=="True" :
        FileLogs.write("Initial Number Gene:"+";"+str(len(tabAllAcc))+"\n")
        FileLogs.write("Compute Number Gene:"+";"+str(compteurAccTraite)+"\n")
        FileLogs.write("Number of you own GOSlims:"+";"+str(compteurGoslim_user)+"\n")
        FileLogs.write("Number of unique close GOSlim:"+";"+str(len(Tableau_GoSlim))+"\n\n")
    FileLogs.write("GOSlim"+";"+"List_gene_present"+";"+"List_gene_unpresent"+"\n")
    tabAllGoSlim=[] 
    for ligne in Tableau_file :
        tmp=ligne.split(";")
        if re.search("choose one of this GO :",tmp[4]) is None :
            tabAllGoSlim+=(tmp[4].split(" "))
    tabAllGoSlim=set(tabAllGoSlim)
    for GoSlim in tabAllGoSlim :
        tabGenePresentTmp=[]
        tabGeneUnpresentTmp=[]
        for ligne in Tableau_file :
            tmp=ligne.split(";")
            acc=tmp[0]
            if re.search(GoSlim,tmp[4]) is not None and re.search("choose one of this GO :",tmp[4]) is None:    
                tabGenePresentTmp.append(acc)
            elif  re.search(GoSlim,tmp[4]) is None and re.search("choose one of this GO :",tmp[4]) is None:
                tabGeneUnpresentTmp.append(acc)
        FileLogs.write(str(GoSlim)+";"+str(" ".join(tabGenePresentTmp))+";"+str(" ".join(tabGeneUnpresentTmp))+"\n")
    FileLogs.write("\n\n")
    FileLogs.close()
    shutil.move(nameFile, path+"/"+nameFile)#Deplace le fichier dans le dossier Sorties
    print("Fini creation log.")

def MakeLog_matrix (Tableau_file,path,relation):#Fonction qui creee une matrice du fichier Logs.csv
    nameFile="Logs_matrix_"+relation+".csv"
    FileLogs=open(nameFile, "w")
    FileLogs.write("GOSlim"+";")
    for ligne in Tableau_file :
        tmp=ligne.split(";")
        acc=tmp[0]
        FileLogs.write(acc+";")
    FileLogs.write("\n")
    tabAllGoSlim=[]
    for ligne in Tableau_file :
        tmp=ligne.split(";")
        if re.search("choose one of this GO :",tmp[4]) is None :
            tabAllGoSlim+=(tmp[4].split(" "))
    tabAllGoSlim=set(tabAllGoSlim)
    for GoSlim in tabAllGoSlim :
        line=[]
        for ligne in Tableau_file :
            tmp=ligne.split(";")
            acc=tmp[0]
            if re.search(GoSlim,tmp[4]) is not None and re.search("choose one of this GO :",tmp[4]) is None:
                line.append("1")
            elif  re.search(GoSlim,tmp[4]) is None and re.search("choose one of this GO :",tmp[4]) is None:
                line.append("0")
        FileLogs.write(str(GoSlim)+";".join(line)+"\n") 
    FileLogs.write("\n\n")
    FileLogs.close()
    shutil.move(nameFile, path+"/"+nameFile)#Deplace le fichier dans le dossier Sorties
    print("Fini creation log_matrix.")
    
def MakeLog_OntologyByGoSlim (Tableau_file,dico_go,compteurAccTraite,path,relation,commentaire):
    nameFile="Logs_Ontology_By_GoSlim_"+relation+".csv"
    FileLogs=open(nameFile, "w")
    if commentaire=="True" :
        compteur_MF=0
        compteur_BP=0
        compteur_CC=0
        for ligne in Tableau_file :
            tmp=ligne.split(";")
            val=dico_go.getOntology(tmp[2])
            if val=="molecular_function":
                compteur_MF+=1
            if val=="biological_process":
                compteur_BP+=1
            if val=="cellular_component":
                compteur_CC+=1
        FileLogs.write("Number of Gene with a close MF GOSlim"+";"+str(compteur_MF)+"\n")
        FileLogs.write("Number of Gene with a close BP GOSlim"+";"+str(compteur_BP)+"\n")
        FileLogs.write("Number of Gene with a close CC GOSlim"+";"+str(compteur_CC)+"\n")
        FileLogs.write("Compute Number Gene :"+";"+str(compteurAccTraite)+"\n\n\n")
    FileLogs.write("GOSlim"+";"+"Ontology"+";"+"count of gene"+"\n")
    tabAllGoSlim=[]
    for ligne in Tableau_file :
        tmp=ligne.split(";")
        if re.search("choose one of this GO :",tmp[4]) is None :
            tabAllGoSlim+=(tmp[4].split(" "))
    tabAllGoSlim=set(tabAllGoSlim)
    for GoSlim in tabAllGoSlim :
        nbAcc=0
        for ligne in Tableau_file :
            tmp=ligne.split(";")
            acc=tmp[0]
            if re.search(GoSlim,tmp[4]) is not None and re.search("choose one of this GO :",tmp[4]) is None:    
                nbAcc+=1
        FileLogs.write(str(GoSlim)+";"+str(dico_go.getOntology(GoSlim))+";"+str(nbAcc)+"\n") 
    FileLogs.write("\n\n")
    FileLogs.close()
    shutil.move(nameFile, path+"/"+nameFile)#Deplace le fichier dans le dossier Sorties
    print("Fini creation log_ontology.")
    
def MakeLog_OntologyByACC (Tableau_file,dico_go,path,relation):
    nameFile="Logs_Ontology_By_ACC_"+relation+".csv"
    FileLogs=open(nameFile, "w")
    FileLogs.write("Accession Number"+";"+"Ontology"+";"+"GOSlims"+"\n")
    for ligne in Tableau_file :
        tmp=ligne.split(";")
        if re.search("choose one of this GO :",tmp[4]) is None :
            FileLogs.write(tmp[0]+";"+dico_go.getOntology(tmp[2])+";"+tmp[4]+"\n")
    FileLogs.write("\n\n")
    FileLogs.close()
    shutil.move(nameFile, path+"/"+nameFile)#Deplace le fichier dans le dossier Sorties
    print("Fini creation log_ontology_acc.")
    