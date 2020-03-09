# Découpage des fonctions

from colored import *
import random

## MISE EN PLACE ##

def game (file_path, player_1, player_2):
    """ General function which calls all the other sub-functions in order to run the game

    Parameters
    ----------
    player 1 : type of the player 1 (str)
    player 2 : type of player 2 (str)
    file_path : path of the file containing the information for the setup of the game (str)

    Note
    ----
    The 3 types of player are : 'human', 'IA', and 'distant_player' if the player is respectively\
         a human playing on the local computer, an IA on the local computer, and a player (human or IA) on an other computer
    
    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 22-02-2020)
    """

def create_data_structures (file_path):
    """ Decodes the file for the setup of the game, creates the board dictionary and entities dictionnary, and places the hubs and energy peaks

    Parameters
    ----------
    file_path : path of the file containing the information of the setup of the game (str)

    Returns
    -------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    nb_columns : number of columns of the board game (int)
    nb_lines : number of lines of the board game (int)

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 19/02/2020)
    implementation : Mathis Huet & Amaury Van Pevenaeyge (v.1 07/03/2020)
    """

    # Creating the base of the two data structures
    board = {}
    entities = {}

    # Reading the file
    fh = open(file_path, 'r')
    board_info = fh.readlines()
    fh.close()

    # Deleting all the \n
    element_id = 0
    for line in board_info:
        board_info[element_id] = line[0:-1]
        element_id += 1

    # Creating all the coordinates in the board
    nb_lines, nb_columns = board_info[1].split()
    nb_lines = int(nb_lines)
    nb_columns = int(nb_columns)

    for y in range (1, nb_lines + 1):
        for x in range(1, nb_columns + 1):
            board[(y, x)] = []
    
    # Creating the hubs in entities dict
    hub_blue = board_info[3].split()
    hub_red = board_info[4].split()

    entities['hub_blue'] = {'coordinates': (int(hub_blue[0]),int(hub_blue[1])), 'type': 'hub', 'team': 'blue', 'structure_points': 1500, 
                            'available_energy': int(hub_blue[2]), 'regeneration_rate': int(hub_blue[3])}
    entities['hub_red'] = {'coordinates': (int(hub_red[0]),int(hub_red[1])), 'type': 'hub', 'team': 'red', 'structure_points': 1500, 
                            'available_energy': int(hub_red[2]), 'regeneration_rate': int(hub_red[3])}
    
    # Creating the peaks in entities dict
    peak_id = 1
    for line in board_info[6:-1]:
        peak_info = line.split()
        entities['peak_%s' % str(peak_id)] = {'coordinates' : (int(peak_info[0]), int(peak_info[1])), 'type' : 'peak', 'available_energy' : int(peak_info[2])}
        peak_id += 1
    
    # actualising the board_dict with the information of entities dict
    board = actualise_board(board, entities)

    return board, entities, nb_columns, nb_lines

def actualise_board (board, entities):
    """ Actualises the information of entities dictionary in the board dictionary

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    board : upated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 21/02/2020)
    implementation : Mathis Huet (v.1 08/03/2020)
    """

    # Emptying the board
    for coordinates in board:
        board[coordinates] = []

    # Refilling the board with all the information from entities dict
    for entity in entities:
        board[entities[entity]['coordinates']].append(entity)
    
    return board

def display_board (board, entities, nb_columns, nb_lines):
    """ Displays the board's game in the terminal

    Parameters
    ----------
    board : dictionary that contains coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    nb_columns : number of columns of the board game (int)
    nb_lines : number of lines of the board game (int)

    Note
    ----
    For a better result, use the Monospace Bold policy

    Version
    -------
    specification : Louis Flamion (v.1 23/02/2020)
    """
    hub ='♜'
    tanker = '☬'
    case = '▒'
    cruiser = '▲'
    energy = '●'
    red_color = '#F76262'
    green_color = '#25CB2B'

    plateau = case * (nb_columns + 2)+"\n" #Top border creation    

    for line in range(1,nb_lines + 1) : #Line creation
        plateau += case
        for column in range(1,nb_columns + 1) :    #Columns creation for every lines
            if (column + line) % 2 == 0  :  #Création du damier
                background_color = red_color #Sets the background color on red
                plateau += bg(background_color)
            else :
                background_color = green_color #Sets the background color on green
                plateau += bg(background_color)
            if board[(line,column)]  == [] : #If entities's list is empty
                plateau += fg(background_color)
                plateau += case      #Put a case
            else :
                for entity in board[(line, column)] : #Search for entity's type and print them on the board
                    if entities[entity]['type'] != 'peak' :
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
                        if entities[entity]['available_energy']<=100 : 
                            plateau+= fg('#008000')
                        if entities[entity]['available_energy']<=75 :
                            plateau+= fg('#FF4500')
                        if entities[entity]['available_energy']<=50 :
                            plateau+= fg('#efd807')
                        if entities[entity]['available_energy']<=25 :
                            plateau+= fg('#bb0b0b')
                        plateau += energy
                    plateau += attr('reset')                    
        plateau += attr('reset')
        plateau += case+'\n'
    print(plateau)
## ORDRES ##

def sort_orders (orders, team):
    """ Sorts the order of a player depending on the type of these orders

    Parameters
    ----------
    orders : orders from the player (str)
    team : name of the team (str)

    Returns
    -------
    creation_orders : orders of creation of the player (list of str)
    upgrade_orders : orders of upgrade of the player (list of str)
    attack_orders : orders of attack of the player (list of str)
    movement_orders : orders of deplacement of the player (list of str)
    energy_absorption_orders : orders of energy absorption of the player (list of str)
    energy_giving_orders : orders of energy giving od the player (list od str)
    
    Version
    -------
    specification : Mathis Huet (v.2 06/03/2020)
    implementation : Mathis Huet (v.2 09/03/2020)
    """

    # Creating all the lists
    creation_orders = []
    upgrade_orders = []
    attack_orders = []
    movement_orders = []
    energy_absorption_orders = []
    energy_giving_orders = []

    # Separating all the orders and putting them in a list
    orders_list = orders.split()

    # Sorting every order in the correct list
    for order in orders_list:

        if 'upgrade:' in order:
            upgrade_orders.append(order)
        elif '*' in order:
            attack_orders.append(order)
        elif '@' in order:
            movement_orders.append(order)
        elif '<' in order:
            energy_absorption_orders.append(order)
        elif '>' in order:
            energy_giving_orders.append(order)
        elif ':' in order:
            creation_orders.append(order)
    
    # Adding the name of the team at the end of each non-empty list
    for List in [creation_orders, upgrade_orders, attack_orders, movement_orders, energy_absorption_orders, energy_giving_orders]:
        if List != []:
            List.append(team)
        
    return creation_orders, upgrade_orders, attack_orders, movement_orders, energy_absorption_orders, energy_giving_orders

def get_IA_orders (board, entities):
    """ Generates the orders of the IA

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    IA_order : orders of the IA (str)

    Version
    -------
    specification : Louis Flamion (v.1 22/02/2020)
    """

## CRÉATION D'UNITÉS ##

def create_vessel (creation_orders, entities):
    """Creates a vessel (cruiser or tanker)

    Parameters
    ----------
    creation_orders : list of the orders of the creations for the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 23/02/2020)
    """

    for order in creation_orders:

        order = str.split(':', 3)
        vessel_name = order[0]
        vessel_type = order[1]
        team = order[2]

        for entity in entities:
            if entities[entity]['type'] == 'hub' and entities[entity]['team'] == 'blue':
                coordinates_hub_blue = entities[entity]['coordinates']

            elif entities[entity]['type'] == 'hub' and entities[entity]['team'] == 'red':
                coordinates_hub_red = entities[entity]['coordinates']

        if vessel_type == 'tanker':
            
            if team == 'blue':
                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'tanker', 'team': team, 
                                            'storage_capacity': 600, 'available_energy': 300, 'structure_points': 50}
            else:
                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'tanker', 'team': team, 
                                            'storage_capacity': 600, 'available_energy': 300, 'structure_points': 50}

        elif vessel_type == 'cruiser':

            if team == 'blue':
                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'cruiser', 'team': team, 'structure_points': 12, 'available_energy': 240, 'moving_cost': 10, 
                                        'fire_range': 1}
            else:
                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'cruiser', 'team': team, 'structure_points': 12, 'available_energy': 240, 'moving_cost': 10, 
                                        'fire_range': 1}

    return entities

## UPGRADES ##

def upgrade (upgrade_orders, entities):
    """Checks if there is enough energy in the hub. Upgrades the entity if there is enough. Prints a message if there is not enough.

    Parameters
    ----------
    upgrade_orders : list of the orders of the upgrades for the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Prints
    ------
    warning : if there is not enough energy in the hub for the upgrade

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 23/02/2020)
    """

## COMBATS ##

def cruiser_attack (attack_orders, board, entities):
    """ attacks the other entities as oredered by a player

    Parameters
    ----------
    attack_orders : list of orders for the attacks for a player (list of str)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict) 
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : updated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 22/02/2020)
    """

def get_distance (coordinates_1, coordinates_2):
    """ Computes the distance between 2 coordinates

    Parameters
    ----------
    coordinates_1 : first coordinates (tuple of integers)
    coordinates_2 : second corrdinates (tuple of integers)

    Returns
    -------
    distance : distance between the 2 coordinates (int)

    Version
    -------
    specification : Mathis Huet (v.1 21/02/2020)
    """

def remove_destroyed_entities (entities):
    """ Removes all the entities which have structure points under or equal to 0 in the entities dict

    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 20/02/2020)
    implementation : Mathis Huet (v.1 08/03/2020)
    """
    entities_to_remove = []

    for entity in entities:
        if entities[entity]['type'] != 'peak':
            structure_points = entities[entity]['structure_points']
            if structure_points <= 0:
                if entities[entity]['type'] == 'hub':
                        # une équipe a gagné
                        print('WIN')
                else:
                        entities_to_remove.append(entity)
    
    for entity in entities_to_remove:
        del entities[entity]
    
    return entities
    
## DÉPLACEMENTS ##

def movement (movement_orders, board, entities):
    """ moves an entity by consequences of the orders given by player or an IA

    Parameters
    ----------
    movement_orders : check if there's a mouvement's order given by the player or IA (str) 
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : updated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 24/02/2020)
    """

## TRANSFERTS D'ÉNERGIE ##

def energy_absorption (energy_absorption_orders, entities, board):
    """ Absorbs the energy of an entity, and if it is a peak, removes it from the map if its energy goes under 0

    Parameters
    ----------
    energy_absorption_orders : orders of energy absorption of the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 24/02/2020)
    """

    # Getting back the name of the team
    team = energy_absorption_orders[-1]
    del energy_absorption_orders[-1]

    for order in energy_absorption_orders:

        # Treating the order
        order = order.split(':')
        vessel_name = order[0]
        coordinates = order[1]
        coordinates = (int(coordinates[1]), int(coordinates[3]))

        # Checking what is on the coordinates
        entities_on_case = board[coordinates]
        nb_potential_absorbed_entities = 0
        for entity in entities_on_case:

            # Getting back the name of the absorbed entity
            absorbed_entity = entity

            # Checking if the type of the entities is convenient
            if entities[absorbed_entity]['type'] == 'hub' or entities[absorbed_entity]['type'] == 'peak':
                nb_potential_absorbed_entities += 1

        # Checking the team and the number of "absorbable" entities on the coordinates
        if nb_potential_absorbed_entities == 1 and entities[vessel_name]['type'] == 'tanker':
            
            # Computing the amount of energy that will be transfered
            absorbed_energy = max(entities[absorbed_entity]['available_energy'], entities[vessel_name]['storage_capacity'] - entities[vessel_name]['available_energy'])

            #Transfering the energy
            if entities[absorbed_entity]['type'] == 'hub':
                if entities[absorbed_entity]['team'] == team:
                    entities[absorbed_entity]['available_energy'] = entities[absorbed_entity]['available_energy'] - absorbed_energy
                    entities[vessel_name]['available_energy'] = entities[vessel_name]['available_energy'] + absorbed_energy

            elif entities[absorbed_entity]['type'] == 'peak':
                entities[absorbed_entity]['available_energy'] = entities[absorbed_entity]['available_energy'] - absorbed_energy
                entities[vessel_name]['available_energy'] = entities[vessel_name]['available_energy'] + absorbed_energy

                if entities[absorbed_entity]['available_energy'] <= 0:
                    del entities[absorbed_entity]
    
    return entities

def energy_giving (energy_giving_orders, entities, board):
    """ Transfers energy from a tanker to a cruiser or a hub

    Parameters
    ----------
    energy_giving_orders : orders of energy giving od the player (list od str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Louis Flamion (v.1 23/02/2020)
    """

## FIN DE TOUR ##

def hubs_regeneration (entities):
    """ regenerates the two hubs at the end of a tour, depending on the regeneration rate

    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 19/02/2020)
    """

board, entities, nb_columns, nb_lines = create_data_structures('/home/mat2905h/Bureau/map1.equ')
entities['tanker_1'] = {'coordinates' : (1,3), 'type' : 'tanker', 'team' : 'red', 'storage_capacity': 600, 
                'available_energy': 300, 'structure_points': 50}
board = actualise_board(board, entities)
display_board(board, entities, nb_columns, nb_lines)

entities = energy_absorption(['tanker_1:<1-2', 'blue'], entities, board)

print(entities)