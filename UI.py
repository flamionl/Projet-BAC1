from colored import *
import random


case = '▒'
rond = '☬'
éclair = '●'
lines = 20
columns = 30
plateau = case * 30+"\n"

for line in range(1,lines-1) :
    #Création de la ligne
    plateau+= case
    for column in range(1,columns-1) :
    #Création des colonnes pour chaque lignes
        #Création du damier
        if (column +line) % 2 == 0  :
            plateau+=fg('#ff0000')
            plateau+=bg('#000000')
            plateau+= rond
            plateau+=attr('reset')
            
        else :
            plateau+=fg('#ff0000')
            plateau+=bg('#ffffff')
            plateau+=éclair
            plateau+=attr('reset')
            
    plateau+=case+'\n'
plateau+=case * 30
print(plateau)
