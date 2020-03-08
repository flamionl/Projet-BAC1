# Structure of the project

    # Data structures
board = {(0,0) : ['cruiser_1', 'hub_1'], (0,1) : ['energy_1'], (0,2) : ['tanker_1']}

entities = {
'cruiser_1': {'coordinates' : (0,0), 'type' : 'cruiser', 'team' : 'blue', 'structure_points' : 12, 
             'available_energy' : 240, 'moving_cost': 10, 'fire_range': 1},
'hub_1': {'coordinates' : (0,0), 'type' : 'hub', 'team' : 'blue', 'structure_points' : 2000, 
               'available_energy' : 622, 'regeneration_rate' : 25},
'tanker_1' : {'coordinates' : (0,2), 'type' : 'tanker', 'team' : 'red', 'storage_capacity': 600, 
                'available_energy': 300, 'structure_points': 50},
'peak_1' : {'coordinates' : (0,1), 'type' : 'peak', 'value' : 25},
'peak_2' : {'coordinates' : (0,2), 'type' : 'peak', 'value' : 40}
}

     # Scenario : moving a cruiser

        # Changing coordinates in vehicles dict

entities['cruiser_1']['coordinates'] = [0,1]

        # deleting cruiser from old coordinates in board dict
index = board[(0,0)].index('cruiser_1')
del board[(0,0)][index]

        # Adding cruiser in new coordinates in board dict
board[(0,1)].append('cruiser_1')

print(board)