# -*- coding: utf-8 -*-
from colored import *
import random

#Board's dimensions
lines = 5
columns = 5

#Dico creation
board ={}
for x in range(1,lines+1) :
    for y in range(1,columns+1) :
        board[(x,y)] = []
board[(2,1)].append('cruiser_1')
board[(1,2)].append('hub_1')
board[(5,3)].append('energy_1')
entities = {
'cruiser_1': {'coordinates' : (0,0), 'type' : 'cruiser', 'team' : 'blue', 'structure_points' : 12, 
             'available_energy' : 240, 'moving_cost': 10, 'fire_range': 1},
'hub_1': {'coordinates' : (0,0), 'type' : 'hub', 'team' : 'blue', 'structure_points' : 2000, 
               'available_energy' : 622, 'regeneration_rate' : 25},
'tanker_1' : {'coordinates' : (0,2), 'type' : 'tanker', 'team' : 'red', 'storage_capacity': 600, 
                'available_energy': 300, 'structure_points': 50},
'energy_1' : {'coordinates' : (0,1), 'type' : 'energy', 'value' : 25},
'energy_2' : {'coordinates' : (0,2), 'type' : 'energy', 'value' : 40}
}
#Emojis used to represent entities
hub ='♜'
tanker = '☢️'
case = '▒'
cruiser = '☬'
eclair = '●'

#Top border creation    
plateau = case * (columns+2)+"\n"


for line in range(1,lines+1) :
    #Line creation
    plateau+= case
    for column in range(1,columns+1) :
    #Columns creation for every lines
        #Création du damier
        if (column +line) % 2 == 0  :
            plateau += bg('#F76262') #Sets the color of the case/entity on red
            #If entities's list is empty
            if board[(line,column)]  == [] :
                plateau+=fg('#F76262')
                plateau += case      #Put a case
            #If entities's list is not empty
            else :
                for entity in board[(line,column)] : #Search for entity's type and print them on the board
                    if entities[entity]['type'] == 'cruiser' :
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += cruiser
                    elif entities[entity]['type'] == 'tanker' :
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += tanker
                    elif entities[entity]['type'] == 'hub' :
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += hub
                    elif entities[entity]['type'] == 'energy' :
                        attr('reset')
                        plateau+=bg('#F76262')                     
                        #check the good colored
                        if entities[entity]['value']<=100 :
                            plateau+= fg('#008000')
                        if entities[entity]['value']<=75 :
                            plateau+= fg('#FF4500')
                        if entities[entity]['value']<=50 :
                            plateau+= fg('#efd807')
                        if entities[entity]['value']<=25 :
                            plateau+= fg('#bb0b0b')
                        plateau += eclair
                        plateau += attr('reset')
            plateau += attr('reset')   
        else :
            plateau += bg('#25CB2B') #Sets the color of the case/entity on green
            #If entities's list is empty
            if board[(line,column)]  == [] :
                plateau += fg('#25CB2B')
                plateau += case
            #If entities's list is not empty
            else :
                for entity in board[(line,column)] : #Search for entity's type and print them on the board
                    if entities[entity]['type'] == 'cruiser' : #If the entity is a cruiser
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += cruiser
                    elif entities[entity]['type'] == 'tanker' : #If the entity is a tanker
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += tanker
                    elif entities[entity]['type'] == 'hub' : #If the entity is a hub
                        if entities[entity]['team'] == 'blue' : #Looking to the entitiy's team to attribute the right color
                            plateau+=fg('#0033FF')
                        else :
                            plateau+=fg('#FF0000')
                        plateau += hub
                    elif entities[entity]['type'] == 'energy' : #If the entity is an energy
                                                
                        #check the good colored
                        if entities[entity]['value']<=100 :
                            plateau+= fg('#008000')
                        if entities[entity]['value']<=75 :
                            plateau+= fg('#FF4500')
                        if entities[entity]['value']<=50 :
                            plateau+= fg('#efd807')
                        if entities[entity]['value']<=25 :
                            plateau+= fg('#bb0b0b')
                        plateau += eclair
                        plateau += attr('reset')
            plateau += attr('reset')
                        
    plateau+=case+'\n'
    plateau += attr('reset')

#Bottom border creation
plateau+=case * (columns+2)
print(plateau)
