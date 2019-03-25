#!/usr/bin/python

"""
Creation de l'objet "Dico_go" :
cet objet a pour fonction de conserver en memoire toutes les informations du fichier "go.obo".
Les relations sont placees dans des hashs distincts avec en cle le GO.
"""

class Dico_go :
    def __init__(self):
        self.dict_GOtoP_is_a = {}
        self.dict_GOtoC_is_a = {}
        self.dict_GOtoP_io = {}
        self.dict_GOtoC_io = {}
        self.dict_GOtoP_r = {}
        self.dict_GOtoC_r = {}
        self.dict_GOtoP_part_of = {}
        self.dict_GOtoC_part_of = {}
        self.dict_GOtoP_occurs_in = {}
        self.dict_GOtoC_occurs_in = {}
        self.dict_GOtoP_regulates = {}
        self.dict_GOtoC_regulates = {}
        self.dict_GOtoP_pr = {}
        self.dict_GOtoC_pr = {}
        self.dict_GOtoP_nr = {}
        self.dict_GOtoC_nr = {}
        self.dict_GOtoGOSLIM = {}
        self.dict_GOtoNAME = {}
        self.dict_Ontology ={}
        self.dict_Consider={}

    """
    La fonction "removeAllGoslim" permet de réinitialiser l'attribut dict_GOtoGOSLIM de l'objet.
    """
    def removeAllGoslim (self):
        self.dict_GOtoGOSLIM = {}
    """
    La fonction prend une liste de GOs pour les ajouter dans l'attribut dict_GOtoGOSLIM.
    """        
    def addTabGoslim (self,tabGoSlim, typeGoSlim='subset_user'):
        nbGoslimAdd=0
        for goSlim in tabGoSlim:
            self.dict_GOtoGOSLIM[goSlim]=typeGoSlim
            nbGoslimAdd+=1
        return(nbGoslimAdd)
        
    """
    La fonction "remplirDico" parcours le fichier "go.obo".
    Pour chaque GO elle recupere toutes les informations et les stocke dans les attributs hash de l'objet.
    namespace est une information sur le terme GO.
    Subset est le GOslim.
    name est une information comme namespace
    consider est un attribut d'un GO s'il est obselète. Alors l'autre GO non-obselète considéré est gardé par le programme. 
    """

    def remplirDico (self, nomfichierOBO):
        oboFile = open(nomfichierOBO, 'r')
        firstTerm=getTerm(oboFile)#on lit le resume du fichier "go.obo"
        firstTerm=None
        while 1:
            term = parseTagValue(getTerm(oboFile))
            
            if len(term) != 0:
                
                termID = term['id'][0]
                if 'is_a' in term :
                    ajoutePC(termID, term['is_a'], self.dict_GOtoP_is_a, self.dict_GOtoC_is_a)
                if 'intersection_of' in term :
                    ajoutePC(termID, term['intersection_of'], self.dict_GOtoP_io,self.dict_GOtoC_io)
                if 'relationship' in term :
                    ajoutePC(termID, term['relationship'], self.dict_GOtoP_r, self.dict_GOtoC_r)
                if 'part_of' in term :
                    ajoutePC(termID, term['part_of'], self.dict_GOtoP_part_of, self.dict_GOtoC_part_of)
                if 'occurs_in' in term :
                    ajoutePC(termID, term['occurs_in'], self.dict_GOtoP_occurs_in, self.dict_GOtoC_occurs_in)
                if 'regulates' in term :
                    ajoutePC(termID, term['regulates'], self.dict_GOtoP_regulates, self.dict_GOtoC_regulates)
                if 'positively_regulates' in term :
                    ajoutePC(termID, term['positively_regulates'], self.dict_GOtoP_pr, self.dict_GOtoC_pr)
                if 'negatively_regulates' in term :
                    ajoutePC(termID, term['negatively_regulates'], self.dict_GOtoP_nr, self.dict_GOtoC_nr)
                
                if 'namespace'in term :
                    goNameSpaceTab=[]
                    for p in term['namespace']:
                        goNameSpaceTab = p
                    self.dict_Ontology[termID] = goNameSpaceTab
                
                if 'subset' in term :
                    goSlimTab=[]
                    for p in term['subset']:
                        tabValeur = p.split()
                        for valeur in tabValeur :
                            if "goslim" in valeur :
                                goSlimTab.append(valeur)
                    self.dict_GOtoGOSLIM[termID] = goSlimTab
                if 'name' in term :
                    goNameTab=[]
                    for p in term['name']:
                        goNameTab = p
                    self.dict_GOtoNAME[termID] = goNameTab
                if 'consider' in term :
                    goConsideTab=[]
                    for p in term['consider']:
                        tabValeur = p.split()
                        for valeur in tabValeur :
                            if "GO:" in valeur :
                                goConsideTab.append(valeur)
                    self.dict_Consider[termID] = goConsideTab
            else:
                break
        oboFile.close()

    """
    Les geter  "getName" et "getOntology" retournent respectivement le nom et l'ontologie pour un go.
    """
    def getName(self,go):
        if go in self.dict_GOtoNAME :
            return (self.dict_GOtoNAME[go])
        return ("no_name")
    
    def getOntology(self,go):
        if go in self.dict_Ontology :
            return (self.dict_Ontology[go])
        return ("no_ontology")
    """
    La fonction "getDico" rend le dictionnaire correspondant a la relation fournie.
    """
        
    def getDico(self,nomDico):
        if nomDico=="dict_GOtoGOSLIM" :
            return self.dict_GOtoGOSLIM
        elif nomDico=="dict_GOtoP_io" :
            return self.dict_GOtoP_io
        elif nomDico=="ia":
            return self.dict_GOtoP_is_a
        elif nomDico=="po":
            return self.dict_GOtoP_part_of
        elif nomDico=="reg":
            list=[self.dict_GOtoP_regulates, self.dict_GOtoP_pr, self.dict_GOtoP_nr, self.dict_GOtoP_part_of]
            dico=fusionListe(list)
            return dico
        elif nomDico=="nr":
            return self.dict_GOtoP_nr
        elif nomDico=="pr":
            return self.dict_GOtoP_pr

        elif nomDico=="dict_GOtoP_occurs_in":
            return self.dict_GOtoP_occurs_in
        elif nomDico=="dict_GOtoP_r":
            return self.dict_GOtoP_r
        elif nomDico=="dict_GOtoP_regulates":
            return self.dict_GOtoP_regulates
        else :
            print ("Exception, not found ",nomDico)
    
    """
    Pour un GO, La fonction "chemin" remonte l'arbre des GOs et elle recupere les GOslim.
    L'attribut "relation" est en option et sera expliqué uyltérieurement. 
    
    1er cas : l'attribut Relation est "none" et DicoUnique est "none" :
    * Avec la fonction getAncestor on recupere tous les GO parents, en utilisant les relations contenues dans DICO.
    * Pour chaque parent, est également recupere le niveau de l'arbre auquel ils sont situés.
    * Ensuite on parcours la liste de parents par niveaux croissant : si le parent est un Goslim il est conservé dans le tableau "res".
    
    2eme cas :l'attribut Relation possède une valeur. Dans ce cas la fonction "chemin" envoie à "getDico" le nom de la relation et recupere le hash contenant les relations et le place dans DicoUnique :
    Comme dans le 1er cas mais avec l'ajout d'une condition.
    On donne à "getAncestor" DicoUnique, puis en retour on recupere une liste. 
    Cette liste contient les informations sour forme de chaines de caractères :
    * un GO
    * un niveau
    * un type
    
    Si type = 2 et GO est un GOslim, alors le GO est conservé dans "res"
    A la fin la fonction retourne "res" sans duplicat. 
    """
    
    def chemin(self,go, dico, relation=None):
        dicoUnique = None
        if relation is not None :
            if relation != 'all' and relation !='ia' :
                dicoUnique=self.getDico(relation)
        if dicoUnique == None :
            parentTab=getAncestors(go, dico)
            niveau=1
            res=[]
            goslimproche=""
            for niveau in range(1,20):
                for GOIDwithNum in parentTab :
                    GOIDnum=GOIDwithNum.split("_")[0]
                    GOID=GOIDwithNum.split("_")[1]
                    if GOIDnum==str(niveau) :
                        if GOID in self.dict_GOtoGOSLIM :
                            if goslimproche=="" :
                                goslimproche = GOID
                            res.append(GOID)
                        if GOID in self.dict_Consider :
                            goslimproche="old GO"
                            res.append("consider="+str(self.dict_Consider[GOID]))
                niveau+=1
            res=list(set(res))
        else :
            parentTab=getAncestors(go, dico, dicoUnique)
            niveau=1
            res=[]
            goslimproche=""
            for niveau in range(1,20):
                for GOIDwithNum in parentTab :
                    tmp=GOIDwithNum.split("_")
                    GOIDnum=int(tmp[0])
                    type=int(tmp[1])
                    GOID=tmp[2]
                    if GOIDnum==niveau and type == 2 :
                        if GOID in self.dict_GOtoGOSLIM :
                            if goslimproche=="" :
                                goslimproche = GOID
                            res.append(GOID)
                        if GOID in self.dict_Consider :
                            goslimproche="old GO"
                            res.append("consider="+str(self.dict_Consider[GOID]))
                niveau+=1
            res=list(set(res))
        return (goslimproche, res)#on renvoie le goslim proche et le chemin
        
    """
    La fonction GetRelationP renvoie le dictionnaire contenant les relations "is a" et les relations choisies.
    """
    
    def GetRelationP(self,relation):
        dico={}
        if relation=="ia" and self.dict_GOtoP_is_a !={}:
            dico=self.dict_GOtoP_is_a
        if relation=="po" and self.dict_GOtoP_part_of !={}:
            dico=fusion(self.dict_GOtoP_part_of, self.dict_GOtoP_is_a)
        if relation=="reg" and self.dict_GOtoP_regulates !={}:
            list=[self.dict_GOtoP_regulates, self.dict_GOtoP_pr, self.dict_GOtoP_nr, self.dict_GOtoP_part_of, self.dict_GOtoP_is_a ]
            dico=fusionListe(list)
        if relation=="pr" and self.dict_GOtoP_pr !={}:
            dico=fusion(self.dict_GOtoP_is_a, self.dict_GOtoP_pr)
        if relation=="nr" and self.dict_GOtoP_nr !={}:
            dico=fusion(self.dict_GOtoP_is_a, self.dict_GOtoP_nr)
        if relation=="all":
            listeDico=[self.dict_GOtoP_is_a,self.dict_GOtoP_part_of,self.dict_GOtoP_regulates,self.dict_GOtoP_pr,self.dict_GOtoP_nr]
            dico=fusionListe(listeDico)
        if relation=="dict_GOtoP_io":
            dico=fusion("dictB", "dictB")
        if relation=="dict_GOtoP_r":
            dico=fusion("dictB", "dictB")
        if relation=="dict_GOtoP_occurs_in" :
            dico=fusion("dictB", "dictB")
        return(dico)
"""
La fonction cheminChildren recherche sur trois niveaux tous les enfants d'un GO pour le dictionnaire de relations fourni.
"""

def cheminChildren(go,dico):
    childrenTab=[]
    if go in dico :
        for child2 in dico[go] :
            childrenTab.append(child2)
            for child3 in dico[go] :
                childrenTab.append(child3)
    return (list(set(childrenTab)))
    
"""
Prend en entree un fichier de type "go.obo".
Parcours le fichier et recupere toutes les informations pour un bloc Term.
"""

def getTerm(stream):
    block = []
    for line in stream:
        if line.strip() == "[Typedef]":
            block = []
            break
        if line.strip() == "[Term]":
            break
        else:
            if line.strip() != "":
                block.append(line.strip())
    return block
"""
La fonction "parseTagValue" parcours un bloc term et met dans un hash les informations.
"""

def parseTagValue(term):
    data = {}
    for line in term:
        tag = line.split(': ', 1)[0]
        value = line.split(': ', 1)[1]
        if 'part_of' in line :
            tag = 'part_of'
        if 'occurs_in' in line :
            tag = 'occurs_in'
        if 'regulates' in line :
            tag = 'regulates'
        if 'positively_regulates' in line :
            tag = 'positively_regulates' 
        if 'negatively_regulates' in line :
            tag = 'negatively_regulates'  
        if tag not in data:
            data[tag] = []
        data[tag].append(value)
    return data
    
"""
La fonction "ajoutePC" prend en entree un GO, ses parents, et les dictionnaires parents et enfants pour une relation.
Elle ajoute les relations GO a parent et GO a enfant dans les dictionnaires respectifs.
"""

def ajoutePC(termID, tab_P, dictP, dictC):
    termParents = []
    for p in tab_P:
        tabValeur = p.split()
        for valeur in tabValeur :
            if "GO:" in valeur :
                termParents.append(valeur)
    if termID not in dictP :
        dictP[termID] = []
    if termID not in dictC :
        dictC[termID] = []
    dictP[termID] += termParents  # append parents of the current term
    for termParent in termParents: # for every parent term, add this current term as children
        if termParent not in dictP :
            dictP[termParent] = []
        if termParent not in dictC :
            dictC[termParent] = []
        dictC[termParent].append(termID)
"""
La fonction "getDescendents" recupere toutes les descendants recursivement.
Son utilisation est impossible si les relations forment des boucles.
"""

def getDescendents(goid, terms, niveau=1):
    return []
    nom=str(niveau)+"_"+goid
    recursiveArray = [nom]
    if goid in terms :
        children = terms[goid]
        if len(children) > 0:
            for child in children:
                recursiveArray.extend(getDescendents(child, terms, niveau+1))
    return set(recursiveArray)
    
"""
La fonction "getAncestor" recupere touts les parents recursivement.
DicoUnique peux etre fourni a la fonction. Dans ce cas, pour chaque GO Parent la fonction verifie si la relation entre GO et GO parent est presente dans DicoUnique.
Dans ce cas type est de valeur 1 par defaut. Sinon type est de valeur 2 si une relation de DicoUnique est utilisee.
De plus, elle ajoute un niveau qui correspond aux nombre de relations déjà franchises et donc au niveau de l'arbre par rapport au niveau de depart.
"""
    
def getAncestors(goid, terms, dicoUnique=None, niveau=1, type=1):
    parentsDicoUnique=[]
    if dicoUnique==None :
        nom=str(niveau)+"_"+goid
        recursiveArray = [nom]
        if goid in terms :
            parents = terms[goid]
            if len(parents) > 0:
                for parent in parents:
                    recursiveArray.extend(getAncestors(parent, terms, dicoUnique, niveau+1))
    else :
        nom=str(niveau)+"_"+str(type)+"_"+goid
        if type == 1 :
            if goid in dicoUnique :
                parentsDicoUnique=dicoUnique[goid]
        recursiveArray = [nom]
        if goid in terms :
            parents = terms[goid]
            if len(parents) > 0:
                for parent in parents:
                    if type == 2 :
                        recursiveArray.extend(getAncestors(parent, terms, dicoUnique, niveau+1, 2))
                    elif parent in parentsDicoUnique :
                        recursiveArray.extend(getAncestors(parent, terms, dicoUnique, niveau+1, 2))
                    else :
                        recursiveArray.extend(getAncestors(parent, terms, dicoUnique, niveau+1, 1))
    return set(recursiveArray)

"""
"fusionliste" et "fusion" prennent des hashs de relations en entree et les fusionnent.
"""
def fusionListe(listeDico):
    z={}
    for dico in listeDico:
        z=fusion(z,dico)
    return (z)

def fusion(dictA,dictB):
    z={}
    for key in dictA :
        if key in dictB :
            z[key]=dictA[key]+dictB[key]
        else :
            z[key]=dictA[key]
    for key in dictB :
        if key in dictA :
            z[key]=dictA[key]+dictB[key]
        else :
            z[key]=dictB[key]
    return (z)
    
"""
BONUS : Ancienne fonction chemin :

def cheminBIS(self,go, dico):
    parentTab=getAncestors(go, dico)
    niveau=1
    res=[]
    goslimproche=""
    for niveau in range(1,20):
        for GOIDwithNum in parentTab :
            GOIDnum=GOIDwithNum.split("_")[0]
            GOID=GOIDwithNum.split("_")[1]
            if GOIDnum==str(niveau) :
                if GOID in self.dict_GOtoGOSLIM :
                    if goslimproche=="" :
                        goslimproche = GOID
                    res.append(GOID)
                if GOID in self.dict_Consider :
                    goslimproche="old GO"
                    res.append("choose one of this GO :"+str(self.dict_Consider[GOID]))
        niveau+=1
    res=list(set(res))
    return (goslimproche, res)#on renvoie le goslim proche et le chemin
    
Ancienne fonction getAncestor

def getAncestorsBIS(goid, terms, niveau=1):
    nom=str(niveau)+"_"+goid
    recursiveArray = [nom]
    if goid in terms :
        parents = terms[goid]
        if len(parents) > 0:
            for parent in parents:
                recursiveArray.extend(getAncestors(parent, terms, niveau+1))
    return set(recursiveArray)
"""