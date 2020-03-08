# -*- coding: utf-8 -*-
from colored import *
import random
lines = 5
columns = 5
board = {}
#Création du board 
for x in range(1,lines+1) :
    for y in range(1, columns+1) :
        board[(x,y)] = []

board[(1,1)].append('cruiser_1')
board[(2,2)].append('hub_1')
board[(1,2)].append('tanker_1')
board[(3,1)].append('energy_1')
board[(4,2)].append('energy_2')
#Dico des entités
entities = {
'cruiser_1': {'coordinates' : (1,1), 'type' : 'cruiser', 'team' : 'blue', 'structure_points' : 12, 
             'available_energy' : 240, 'moving_cost': 10, 'fire_range': 1},
'hub_1': {'coordinates' : (2,2), 'type' : 'hub', 'team' : 'blue', 'structure_points' : 2000, 
               'available_energy' : 622, 'regeneration_rate' : 25},
'tanker_1' : {'coordinates' : (1,2), 'type' : 'tanker', 'team' : 'red', 'storage_capacity': 600, 
                'available_energy': 300, 'structure_points': 50},
'energy_1' : {'coordinates' : (3,1), 'type' : 'energy', 'value' : 25},
'energy_2' : {'coordinates' : (4,2), 'type' : 'energy', 'value' : 40}
}
#Emojis used to represent entities
hub ='♜'
tanker = '☬'
case = '▒'
cruiser = '▲'
energy = '●'
red_color = '#F76262'
green_color = '#25CB2B'
 
plateau = case * (columns+2)+"\n" #Top border creation    

for line in range(1,lines+1) : #Line creation
    plateau+= case
    for column in range(1,columns+1) :    #Columns creation for every lines
        if (column +line) % 2 == 0  :  #Création du damier
            background_color = red_color #Sets the background color on red
            plateau += bg(background_color)
        else :
            background_color = green_color #Sets the background color on green
            plateau += bg(background_color)
        if board[(line,column)]  == [] : #If entities's list is empty
            plateau+=fg(background_color)
            plateau += case      #Put a case
        else :
            for entity in board[(line,column)] : #Search for entity's type and print them on the board
                if entities[entity]['type'] != 'energy' :
                    if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                        plateau+=fg('#0033FF')
                    else :
                        plateau+=fg('#FF0000')
                    if entities[entity]['type'] == 'cruiser' :
                        plateau += cruiser
                    if entities[entity]['type'] == 'tanker' :
                        plateau += tanker
                    if entities[entity]['type'] == 'hub' :
                        plateau += hub
                else :                                      #Looking to the energy's value to attribute the right color
                    plateau += energy
                    if entities[entity]['value']<=100 : 
                        plateau+= fg('#008000')
                    if entities[entity]['value']<=75 :
                        plateau+= fg('#FF4500')
                    if entities[entity]['value']<=50 :
                        plateau+= fg('#efd807')
                    if entities[entity]['value']<=25 :
                        plateau+= fg('#bb0b0b')
                plateau += attr('reset')                    
    plateau += attr('reset')
    plateau+=case+'\n'

#Bottom border creation
plateau+=case * (columns+2)
print(plateau)
