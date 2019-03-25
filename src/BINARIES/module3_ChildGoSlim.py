#!/usr/bin/python

import BINARIES.module1 as module1

def GiveGOSlimChild (nomfichierentree, nomfichiersorti, relation):
    File = open(nomfichierentree, "r")
    FileSortir=open(nomfichiersorti, "w")
    dico_go=module1.Dico_go()
    dico_go.remplirDico('DATA/go.obo')
    dico=dico_go.GetRelationP(relation)
    File.readline()
    FileSortir.write("Numero d'accesion"+";"+"Numero GO"+";"+"goslim_chemin_children"+"\n")
    for line in File :
        line=line.rstrip()
        tmp=line.split("\t")
        acc=tmp[0]
        go=tmp[1]
        goslim_chemin_children=module1.cheminChildren(go,dico)
        FileSortir.write(acc+";"+go+";"+" ".join(goslim_chemin_children)+"\n")
    File.close()
    FileSortir.close()
    print("Fini.")
