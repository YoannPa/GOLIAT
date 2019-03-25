dict_accTOgo={}

def addGO (nomfichierentree='liste1.txt', nomfichiersorti='liste1GO.txt'):#Fonction qui est spécifique du fichier liste1.txt et qui creee un fichier au format "ACC&GO"
    fileIN = open(nomfichierentree, "r")
    fileOUT=open(nomfichiersorti, "w")
    getDict()
    for line in fileIN :
        acc=line.rstrip()
        if acc in dict_accTOgo :
            fileOUT.write(acc+"\t"+dict_accTOgo[acc]+"\n")
        else :
            print("EXCEPTION :",acc)

def getDict(nomfichierentree='TAIR_annotations_GO_liste.txt'):#Fonction qui est spécifique du fichier TAIR_annotations_GO_liste.txt et qui creee un dictionnaire pour la fonction addGO
    fileIN = open(nomfichierentree, "r")
    for line in fileIN :
        tmp=line.split("\t")
        dict_accTOgo[tmp[0]]=tmp[1]
        
addGO()