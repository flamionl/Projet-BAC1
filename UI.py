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
éclair = '●'

#Top border creation    
plateau = case * (columns+2)+"\n"


for line in range(1,lines+1) :
    #Line creation
    plateau+= case
    for column in range(1,columns+1) :
    #Columns creation for every lines
        #Création du damier
        if (column +line) % 2 == 0  :
            #If entities's list is empty
            if board[(line,column)]  == [] :
                plateau += bg('#CB2525')
                plateau += case
                plateau += attr('reset')
            #If entities's list is not empty
            else :
                for entity in board[(line,column)] :
                    if entities[entity]['type'] == 'cruiser' :
                        plateau += bg('#CB2525')
                        plateau += cruiser
                        plateau += attr('reset')
                    
        else :
            #If entities's list is empty
            if board[(line,column)]  == [] :
                plateau += bg('#25CB2B')
                plateau += case
                plateau += attr('reset')
            #If entities's list is not empty
            else :
                for entity in board[(line,column)] :
                    #If the entity is a cruiser
                    if entities[entity]['type'] == 'cruiser' :
                        plateau += bg('#25CB2B')
                        plateau += cruiser
                        plateau += attr('reset')
    plateau+=case+'\n'
    plateau += attr('reset')

#Bottom border creation
plateau+=case * (columns+2)
print(plateau)
