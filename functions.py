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

    entities['hub_blue'] = {'coordinates': (int(hub_blue[0]),int(hub_blue[1])), 'type': 'hub', 'team': 'blue', 'structure_points': 2000,
                             'storage_capacity' : 1500, 'available_energy': int(hub_blue[2]), 'regeneration_rate': int(hub_blue[3])}
    entities['hub_red'] = {'coordinates': (int(hub_red[0]),int(hub_red[1])), 'type': 'hub', 'team': 'red', 'structure_points': 1500, 
                            'storage_capacity' : 1500, 'available_energy': int(hub_red[2]), 'regeneration_rate': int(hub_red[3])}
    
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
    implementation : Gerry Longfils and Louis Flamion (v.1 09/03/2020)
    """
    #Emojis used 
    hub ='♜'
    tanker = '☬'
    case = '▒'
    cruiser = '▲'
    energy = '●'

    #Color used to print the board
    red_color = '#F76262'
    green_color = '#25CB2B'

    #Top border creation  
    plateau = case * (nb_columns + 2)+"\n" 

    #Line creation
    for line in range(1,nb_lines+1) : 
        plateau+= case

    #Columns creation for every lines
        for column in range(1,nb_columns+1) : 

            #Checker board creatin   
            if (column +line) % 2 == 0  : 

                #Sets the background color on red
                background_color = red_color 
                plateau += bg(background_color)
            else :

                #Sets the background color on green
                background_color = green_color 
                plateau += bg(background_color)

                #If there isn't any entities on the case
            if board[(line,column)]  == [] : 
                plateau+=fg(background_color)
                plateau += case      

                #If there is one entity on the case
            elif len(board[line,column])==1:
                if entities[board[(line,column)][0]]['type'] != 'peak' :

                    #Looking to the entitiy's team to attribute the right color
                    if entities[board[(line,column)][0]]['team'] == 'blue' : 
                        plateau+=fg('#0033FF')
                    else :
                        plateau+=fg('#FF0000')

                    #Looking to the entity's type to print on the board
                    if entities[board[(line,column)][0]]['type'] == 'cruiser':
                        plateau += cruiser
                    elif entities[board[(line,column)][0]]['type'] == 'tanker' :
                        plateau += tanker
                    elif entities[board[(line,column)][0]]['type'] == 'hub' :
                        plateau += hub

                    #Looks to the peak's available energy to print it with the right color
                else :  
                    if entities[board[(line,column)][0]]['available_energy']>=100 :    
                        plateau+= fg('#008000')
                    elif entities[board[(line,column)][0]]['available_energy']<=75 :
                        plateau+= fg('#FF4500')
                    elif entities[board[(line,column)][0]]['available_energy']<=50 :
                        plateau+= fg('#efd807')
                    elif entities[board[(line,column)][0]]['available_energy']<=25 :
                        plateau+= fg('#bb0b0b') 

                    #Print an energy on the board
                    plateau += energy

                #If there is more than one entity on the case

            else :
                
                #Initialising a list that contains the type of entities on the case
                type_of_entities=[]

                #Getting all entities type
                for entity in board[(line,column)]:
                    type_of_entities.append(entities[entity]['type'])
                
                #Looking for hub 
                if 'hub' in type_of_entities:
                    if entities[board[(line,column)][type_of_entities.index('hub')]]['team'] == 'blue':
                        plateau+=fg('#0033FF')
                    else:
                        plateau+=fg('#FF0000')
                    plateau += hub

                #Looking for cruiser
                elif 'cruiser' in type_of_entities :
                    if entities[board[(line,column)][type_of_entities.index('cruiser')]]['team'] == 'blue':
                        plateau+=fg('#0033FF')
                    else:
                        plateau+=fg('#FF0000')
                    plateau +=cruiser

                #Looking for tankers
                elif 'tanker' in type_of_entities :
                    if entities[board[(line,column)][type_of_entities.index('tanker')]]['team'] == 'blue':
                        plateau+=fg('#0033FF')
                    else:
                        plateau+=fg('#FF0000')
                    plateau+=tanker

                #Looking for peaks
                else :
                    if entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<=100 :    
                        plateau+= fg('#008000')
                    elif entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<=75 :
                        plateau+= fg('#FF4500')
                    elif entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<=50 :
                        plateau+= fg('#efd807')
                    elif entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<=25 :
                        plateau+= fg('#bb0b0b') 
                    plateau+=energy

        #Reset colors                
        plateau += attr('reset')

        #Goes to the next line
        plateau+=case+'\n'
    
    #Bottom border creation

    plateau+=case * (nb_columns+2)
    #Print the board

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
    #Get the name of the team in the creation order list
    team = creation_orders[-1]

    #Split orders in two strings
    for order in creation_orders[0:-1]:

        order = order.split(':')
        
        vessel_name = order[0]
        vessel_type = order[1]

        #Get the coordinates of the two hubs in the dictionary of the entities
        for entity in entities:

            if entities[entity]['type'] == 'hub' and entities[entity]['team'] == 'blue':

                coordinates_hub_blue = entities[entity]['coordinates']

            elif entities[entity]['type'] == 'hub' and entities[entity]['team'] == 'red':

                coordinates_hub_red = entities[entity]['coordinates']

        #Add the vessel in the dictionary of entities according to their type and their team
        if vessel_type == 'tanker':
            
            if team == 'blue':

                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'tanker', 'team': team, 
                                            'storage_capacity': 600, 'available_energy': 600, 'structure_points': 50}
            elif team == 'red':

                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'tanker', 'team': team, 
                                            'storage_capacity': 600, 'available_energy': 600, 'structure_points': 50}

        elif vessel_type == 'cruiser':

            if team == 'blue':

                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'cruiser', 'team': team, 'structure_points': 100, 
                                            'available_energy': 400, 'moving_cost': 10, 'fire_range': 1, 'storage_capacity': 400}
            elif team == 'red':

                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'cruiser', 'team': team, 'structure_points': 100, 
                                            'available_energy': 400, 'moving_cost': 10, 'fire_range': 1, 'storage_capacity': 400}

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
    implementation : Gerry Longfils (v.1 12/03/2020)
    """

    #variable for the increment
    ranges=0
    move=0
    regeneration=0
    storage=0

    # list where the orders will be place 
    list_orders=[]

    #split the space
    upgrade_orders=upgrade_orders[0].split()
    for x in range(len(upgrade_orders)):
        list_orders.append(upgrade_orders[x].split(':'))

    #check what's the upgrade instruction to execute and increment the good variable 

    
    for count in range(len(list_orders)):
        if list_orders[count][1]=='range':
            ranges+=1
        
        elif list_orders[count][1]=='move':
            move+=1
        
        elif list_orders[count][1]=='regeneration':
            regeneration+=1
        
        elif list_orders[count][1]=='blue' or list_orders[count][1]=='red':
            team=list_orders[count][1]

        else:
            storage+=1
        


    #make the upgrade
    
    check=list(entities.keys())
    
    for execute in range(storage):
        for x in check:
            if entities[x]['type']=='tanker' and entities[x]['team']==team:
                if entities[x]['storage_capacity']<1200:
                    entities[x]['available_energy']-=600
                    if entities[x]['available_energy']>0:
                       entities[x]['regeneration_rate']+=100
                    else:
                        print('error')
                        entities[x]['available_energy']+=600
    
    
    for execute in range(regeneration):
        for x in check:
            if entities[x]['type']=='hub' and entities[x]['team']==team :
                if entities[x]['regeneration_rate']<50:
                    entities[x]['available_energy']-=750
                    if entities[x]['available_energy']>0:
                       entities[x]['regeneration_rate']+=5
                    else:
                        print('error')
                        entities[x]['available_energy']+=750

    for execute in range(move):
        for x in check:
            if entities[x]['type']=='cruiser' and entities[x]['team']==team :
                if entities[x]['moving_cost']>5:
                    entities[x]['available_energy']-=400
                    if entities[x]['available_energy']>0:
                       entities[x]['moving_cost']-=1
                    else:
                        print('error')
                        entities[x]['available_energy']+=400

    for execute in range(ranges):
        for x in check:
            if entities[x]['type']=='cruiser' and entities[x]['team']==team:
                if entities[x]['fire_range']<5:
                    entities[x]['available_energy']-=400
                    if entities[x]['available_energy']>0:
                       entities[x]['regeneration_rate']+=1
                    else:
                        print('error')
                        entities[x]['available_energy']+=400        
    return entities
    

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

    Version
    -------
    specification : Louis Flamion (v.2 13/03/2020)
    implementation : Louis Flamion (v.1 11/03/2020)
    """

     #Getting info from the attack_orders
    for order in attack_orders :
        splited_order = order.split(':')
        vessel_name = splited_order[0]
        line = int(splited_order[1].split('-')[0][1:])
        column = int(splited_order[1].split('-')[1].split('=')[0])
        damages = int(splited_order[1].split('=')[1])

        #Getting coordinates of the ship that attacks
        vessel_coordinates = entities[vessel_name]['coordinates']

        #Checking if there is an entity on the case
        if board[(line,column)] != [] :
            
            #Checking if the vessel is not too far from the case that he wants to attack and if the vessel has enough energy to attack
            if get_distance(vessel_coordinates,(line,column)) <= entities[vessel_name]['fire_range'] and entities[vessel_name]['available_energy'] - (damages*10) > 0 :

                #Remove the energy needed to attack to case 
                entities[vessel_name]['available_energy'] -= damages*10

                #Remove structures_points to the entities on the case
                for entity in board[(line,column)] :
                    if entities[entity]['type'] != 'peak' :
                        entities[entity]['structure_points'] -= damages

    return entities

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
    implementation : Louis Flamion (v.1 11/03/2020)
    """
    #Manthan's formule
    distance = abs(coordinates_1[1]-coordinates_2[1]) + abs(coordinates_1[0]-coordinates_2[0]) 

    return distance

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
    implementation : Gerry Longfils (v.1 07/03/2020)
    """
    #check if there's a movement order
    for x in range(len(movement_orders)):
        list_movement=movement_orders[x].split(':')
    print(list_movement)
    a=len(list_movement)
    for check_list in range(a):
        if list_movement[check_list][0]=='@':
            p=check_list-1
            #delete old coordinates from board
            take=entities[list_movement[p]]['coordinates']
            board[take].remove(list_movement[p])
            
            
            #update entities
            b=list_movement[check_list][1:]
            b=b.split('-')
            tuples=(int(b[0]),int(b[1]))
            entities[list_movement[p]] ['coordinates']=tuples
            #update board
            board[tuples].append(list_movement[p])

 
            


    return entities,board


## TRANSFERTS D'ÉNERGIE ##

def energy_absorption (energy_absorption_orders, entities, board):
    """ A tanker absorbs the energy of a peak or a hub, and if the energy of a peak goes under 0, removes it from the map

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
    implementation : Mathis Huet (v.2 17/03/2020)
    """
    ### L'ordre donne une coordonnée et la fonction absorbe l'énergie des premières entités qui ont le bon type s'il en existe plusieurs sur la case
    ### Jusqu'à ce que la soute du tanker soit pleine ou que toutes les entités absorbables sur la case visée n'aient plus d'énergie

    # Getting back and deleting the name of the team from the list if the list is not empty
    if energy_absorption_orders != []:
        team = energy_absorption_orders[-1]
        del energy_absorption_orders[-1]

    for order in energy_absorption_orders:

        # Treating the order
        order = order.split(':<')
        tanker_name = order[0]
        coordinates = order[1]
        coord_list = coordinates.split('-')
        y = int(coord_list[0])
        x = int(coord_list[1])
        coordinates = (y, x)

        # Checking what is on the coordinates
        entities_on_case = board[coordinates]

        for entity in entities_on_case:
            absorbed_entity = entity

            # Checking if the type of the entities is convenient
            if ((entities[absorbed_entity]['type'] == 'hub' and entities[absorbed_entity]['team'] == team) or entities[absorbed_entity]['type'] == 'peak') and entities[tanker_name]['type'] == 'tanker':

                # Computing distance
                distance = get_distance(entities[tanker_name]['coordinates'], entities[absorbed_entity]['coordinates'])

                # Checking the distance
                if distance <= 1:
            
                    # Computing the amount of energy that will be transfered
                    absorbed_energy = min(entities[absorbed_entity]['available_energy'], entities[tanker_name]['storage_capacity'] - entities[tanker_name]['available_energy'])

                    #Transfering the energy
                    entities[absorbed_entity]['available_energy'] = entities[absorbed_entity]['available_energy'] - absorbed_energy
                    entities[tanker_name]['available_energy'] = entities[tanker_name]['available_energy'] + absorbed_energy

                    # Deleting the peak from the map if its energy is below 0
                    if entities[absorbed_entity]['type'] == 'peak'and entities[absorbed_entity]['available_energy'] <= 0:
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

    #Getting back the name of the team
    if energy_giving_orders != []:
        team = energy_giving_orders[-1]

    for order in energy_giving_orders[0:-1]:

        #Treating the order
        order = order.split(':>')
        vessel_giving = order[0]
        vessel_receiving = order[1]

        #Checking what is on the coordinates
        coordinates_receiving = entities[vessel_receiving]['coordinates']
        coordinates_giving = entities[vessel_giving]['coordinates']
        distance = get_distance(coordinates_receiving, coordinates_giving)
        if distance <= 1:

            # Checking if the type of the entities is convenient
            if entities[vessel_receiving]['type'] == 'hub' or entities[vessel_receiving]['type'] == 'cruiser':

                if entities[vessel_giving]['type'] == 'tanker' and entities[vessel_receiving]['team'] == team:

                    # Computing the amount of energy that will be given
                    given_energy = min(entities[vessel_giving]['available_energy'], entities[vessel_receiving]['storage_capacity'] - entities[vessel_receiving]['available_energy'])
                        
                    #Transfering the energy
                    entities[vessel_receiving]['available_energy'] = entities[vessel_receiving]['available_energy'] + given_energy
                    entities[vessel_giving]['available_energy'] = entities[vessel_giving]['available_energy'] - given_energy

    return entities

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
    implementation : Gerry Longfils (v.1 13/03/2020)
    """

    #put each keys in a list 
    check=list(entities.keys())

    #Check if it's a hub then he regenerate it 
    for x in check:
        if entities[x]['type']=='hub':
            if (entities[x]['available_energy']+entities[x]['regeneration_rate'])<1500:
                entities[x]['available_energy']+=entities[x]['regeneration_rate']
            
        
    return entities

