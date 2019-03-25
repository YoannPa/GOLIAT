# -*- coding: utf-8 -*-

import sys
import argparse
import BINARIES.module6_cytoscape as module6_cytoscape

if 'launch_cytoscape' in sys.argv[0] :
    sys.argv.remove(sys.argv[0])
print (sys.argv)

"""
EXEMPLE
Lancement sous windows :
python launch_cytoscape.py C:/Users/tombo/Desktop/go/PROGRAMME_GOLIAT/Sorties_exemple/outPut_all.csv C:/Users/tombo/Desktop/go/PROGRAMME_GOLIAT/Sorties_exemple/ -r all

L'outil PARSER permet de parametrer les arguments du programme.
ADD ARGUMENT est utilisé pour ajouter un argument avec son aide.
PARSER génère automatiquement l'aide du programme.
"""

parser = argparse.ArgumentParser(prog='Launcher cytoscape',description='Menu')
parser.add_argument('file', action="store",
                    help='Output file generated by module_main')
parser.add_argument('path', action="store",
                    help='Output Directory generated by module_main')
parser.add_argument('-r', action="store", default='ia',
                    help='relation type \n'
                    'by default ia'
                    'ia ==> Relation is_a \n'
                    'po ==> Relation part_of \n'
                    'reg ==> Relation regulates \n'
                    'pr ==> Relation positively_regulates \n'
                    'nr ==> Relation negatively_regulates \n'
                    'all ==> ALL Relation \n')

"""
Si l'utilisateur saisi les arguments obligatoires, la fonction ci-dessous envoie les informations au module2 qui réalise les calculs.
"""


#PARCOURIR LES ARGUMENTS
argParser = parser.parse_args(sys.argv)
dico_arg = dict(argParser._get_kwargs())

if 'file' in dico_arg :#Envoie des arguments au programme 
    module6_cytoscape.CallCytoscape(dico_arg['file'], dico_arg['path'], dico_arg['r'])#Fonction qui crée une visualisation cytoscape