# -*- coding: utf-8 -*-

import sys
import argparse
import BINARIES.module2_goslimproche as module2_goslimproche


if 'module_main' in sys.argv[0] :#Lancement sur windows python module_main.py **************
    sys.argv.remove(sys.argv[0])
print (sys.argv)

#sys.argv=['liste1GO.txt','outPut.csv','-fileGOSLIM=MesGOSlim.csv', '-r=all' , '-comment=True', '-formatInput=Acc&GO']

"""
EXEMPLE
Lancement sous windows :
python module_main.py C:/Users/tombo/Desktop/go/liste1GO.txt outPut.csv -fileGOSLIM=C:/Users/tombo/Desktop/go/MesGOSlim.txt -r=all -comment=True -formatInput=ACCandGO

L outil PARSER permet de parametrer les arguments du programme.
ADD ARGUMENT est utilise pour ajouter un argument avec son aide.
PARSER génère automatiquement l aide du programme.
"""

parser = argparse.ArgumentParser(prog='Gene clustering par GoSlim',description='Menu')
parser.add_argument('fileGO', action="store",
                    help='File with gene and GO : <ACC>/t<GOID>')
parser.add_argument('fileOUT', action="store",
                    help='Output file')
parser.add_argument('-fileGOSLIM', action="store",
                    help='File with GOSLIM ID'
                    'like the file MesGOSlim.csv')
parser.add_argument('-r', action="store", default='ia',
                    help='relation type \n'
                    'by default ia'
                    'ia ==> Relation is_a \n'
                    'po ==> Relation part_of \n'
                    'reg ==> Relation regulates \n'
                    'pr ==> Relation positively_regulates \n'
                    'nr ==> Relation negatively_regulates \n'
                    'all ==> ALL Relation \n')
parser.add_argument('-comment', action="store",
                    help='add commentary \n'
                    'True ==> add commentary for mains Logs \n'
                    'False ==> Doesnt add commentary for mains Logs \n')
parser.add_argument('-formatInput', action="store",
                    help='choose format of your input data \n'
                    'ACCandGO ==> data with two columns : first column is for the AccessionNumber of your Gene and the second is for the GeneOntholgyNumber \n'
                    '\n'
                    '|    ACC    |    GO    |\n'
                    '-----------------------\n'
                    '|    ATG15441|   GO:0025489     |\n'
                    '|      ...      |      ...      |\n'
                    '\n'
                    'GO ==> Only one column with your  GeneOntholgyNumber \n')

"""
Si l'utilisateur saisi les arguments obligatoires, la fonction ci-dessous envoie les informations au module2 qui réalise les calculs.
"""

argParser = parser.parse_args(sys.argv)
dico_arg = dict(argParser._get_kwargs())

if 'fileGO' in dico_arg :
    module2_goslimproche.GiveGOSlim(dico_arg['fileGO'],
                                             dico_arg['fileOUT'],
                                             dico_arg['fileGOSLIM'],
                                             dico_arg['r'],
                                             dico_arg['comment'],
                                             dico_arg['formatInput'])