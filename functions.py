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
    implementation : Louis Flamion and Gerry Longfils (v-1 18/03/2020)
    """
    #Creating data structures
    board, entities, nb_columns, nb_lines = create_data_structures(file_path)

    #Initialising turn variable
    turn = 0

    while entities['hub_blue']['structure_points'] > 0 and entities['hub_red']['structure_points'] > 0 and turn < 1000 :

        #Priting the board
        display_board(board,entities,nb_columns,nb_lines)

        #Checking player_1's type and getting orders
        if player_1 ==  'human' :
            order = str(input('Quels sont vos ordres joueur 1 :'))
        else :
            order = get_IA_orders(board,entities)

        #player_1's orders sorting
        creation_orders_blue, upgrade_orders_blue, attack_orders_blue, movement_orders_blue, energy_absorption_blue, energy_giving_blue = sort_orders(order,'blue')

        #Checking player_2's type and getting orders
        if player_2 == 'human' :
            order = str(input('Quels sont vos ordres joueur 2 :'))
        else :
            order = get_IA_orders(board,entities)

        #player_2's orders sorting
        creation_orders_red, upgrade_orders_red, attack_orders_red, movement_orders_red, energy_absorption_red, energy_giving_red = sort_orders(order,'red')

        #Creation vessel phase
        entities = create_vessel(creation_orders_blue,entities)
        entities = create_vessel(creation_orders_red,entities)

        #upgrade entites phase
        entities = upgrade(upgrade_orders_blue,entities)
        entities = upgrade(upgrade_orders_red,entities)

        #attack phase
        entities = cruiser_attack(attack_orders_blue,board,entities)
        entities = cruiser_attack(attack_orders_red,board,entities)
        entities = remove_destroyed_entities(entities)

        #move entities phase
        entities = movement(movement_orders_blue,board,entities)
        entities = movement(movement_orders_red,board,entities)

        #energy absorption pics for tankers
        entities = energy_absorption(energy_absorption_blue,entities,board)
        entities = energy_absorption(energy_absorption_red,entities,board)

        #energy giving phase
        entities = energy_giving(energy_giving_blue,entities,board)
        entities = energy_giving(energy_giving_red,entities,board)

        entities= hubs_regeneration(entities)
        board = actualise_board(board,entities)

        #Increment turn variable
        turn +=1


def create_data_structures(file_path):
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
    implementation : Mathis Huet & Amaury Van Pevenaeyge (v.2 17/03/2020)
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

    entities['hub_blue'] = {'coordinates': (int(hub_blue[0]),int(hub_blue[1])), 'type': 'hub', 'team': 'blue', 'structure_points': int(hub_blue[2]),
                             'storage_capacity' : int(hub_blue[3]), 'available_energy': int(hub_blue[3]), 'regeneration_rate': int(hub_blue[4])}
    entities['hub_red'] = {'coordinates': (int(hub_red[0]),int(hub_red[1])), 'type': 'hub', 'team': 'red', 'structure_points': int(hub_red[2]),
                            'storage_capacity' : int(hub_red[3]), 'available_energy': int(hub_red[3]), 'regeneration_rate': int(hub_red[4])}

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
    energy_giving_orders : orders of energy giving of the player (list of str)

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
    #Defines the action to do
    action_number = random.randint(0,100)
    if action_number <= 60 :
        return

## CRÉATION D'UNITÉS ##

def create_vessel (creation_orders, entities):
    """Creates a vessel (cruiser or tanker)

    Parameters
    ----------
    creation_orders : orders of creation of the player (list of str)
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
    """Checks if there is enough energy in the hub. Upgrades the entity if there is enough.

    Parameters
    ----------
    upgrade_orders : orders of upgrade of the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

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
    flag=0
    liste=[]

    #split the ':' and del each key word upgrade
    for index in range(len(upgrade_orders)):
        liste+=upgrade_orders[index].split(':')

    for count in range(len(liste)):
        if liste[count]=='range':
            ranges+=1

        elif liste[count]=='move':
            move+=1

        elif liste[count]=='regeneration':
            regeneration+=1

        elif liste[count]=='blue' or liste[count]=='red':
            team=liste[count]

        else:
            storage+=1

    #update the regeneration range for the hub
    for occurence in range(regeneration):
        for good_entities in entities:
            if entities[good_entities]['type']=='hub' and entities[good_entities]['team']==team:
                if entities[good_entities]['available_energy']-750>0 and entities[good_entities]['regeneration_rate']<50:
                    entities[good_entities]['regeneration_rate']+=5
                    entities[good_entities]['available_energy']-=750
                    



    #update the move cost for the cruiser
    for occurence in range(move):
        for is_hub in entities:
            if entities[is_hub]['type']=='hub' and entities[is_hub]['team']==team and entities[is_hub]['available_energy']-500>=0  :
                entities[is_hub]['available_energy']-=500
                flag=1
        #search the good entities for updating
        for good_entities in entities :
            if  flag==1 and entities[good_entities]['type']=='cruiser'  and entities[good_entities]['team']==team:
                    if entities[good_entities]['moving_cost']>5:
                        entities[good_entities]['moving_cost']-=1
                    MovingCostCruiser=entities[good_entities]['moving_cost']
        flag=0


    #update the storage for the tankers
    for occurence in range(storage):
        for is_hub in entities:
            if entities[is_hub]['type']=='hub' and entities[is_hub]['team']==team and entities[is_hub]['available_energy']-600>=0  :
                entities[is_hub]['available_energy']-=600
                flag=1
        #search the good entities for updating
        for good_entities in entities :
            if  flag==1 and entities[good_entities]['type']=='tanker'  and entities[good_entities]['team']==team:
                    if entities[good_entities]['storage_capacity']<1200:
                        entities[good_entities]['storage_capacity']+=(100/2)
                    StorageCapacityTanker=entities[good_entities]['storage_capacity']
        flag=0


    #update the fire ranges for the cruisers
    for occurence in range(ranges):
        for is_hub in entities:
            if entities[is_hub]['type']=='hub' and entities[is_hub]['team']==team and entities[is_hub]['available_energy']-500>=0  :
                entities[is_hub]['available_energy']-=500
                flag=1
        #search for the good entities for updating
        for good_entities in entities :
            if  flag==1 and entities[good_entities]['type']=='cruiser'  and entities[good_entities]['team']==team:
                    if entities[good_entities]['fire_range']<5:
                        entities[good_entities]['fire_range']+=1
                    FireRangeCruiser=entities[good_entities]['fire_range']
        flag=0

    return entities,MovingCostCruiser,StorageCapacityTanker,FireRangeCruiser


## COMBATS ##

def cruiser_attack (attack_orders, board, entities):
    """ attacks the other entities as oredered by a player

    Parameters
    ----------
    attack_orders : orders of attack of the player (list of str)
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

    #Getting the team of the vessel which is attacking
    if attack_orders != [] :
        team = attack_orders[-1]

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
                if get_distance(vessel_coordinates,(line,column)) <= entities[vessel_name]['fire_range'] and entities[vessel_name]['available_energy'] - (damages*10) > 0 and entities[vessel_name]['team'] == team :

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
        if entities[entity]['type'] != 'peak' and entities[entity]['type'] != 'hub':
            structure_points = entities[entity]['structure_points']
            if structure_points <= 0:
                entities_to_remove.append(entity)

    for entity in entities_to_remove:
        del entities[entity]

    return entities

## DÉPLACEMENTS ##

def movement (movement_orders, board, entities):
    """ moves an entity by consequences of the orders given by player or an IA

    Parameters
    ----------
    movement_orders : orders of deplacement of the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)


    Version
    -------
    specification : Gerry Longfils (v.2 17/03/2020)
    implementation : Gerry Longfils (v.1 17/03/2020)
    """
    list_movement=[]
    
    #check if there's a movement order
    for x in range(len(movement_orders)):
        list_movement+=movement_orders[x].split(':')
    
    for check_list in range(len(list_movement)):
        if list_movement[check_list][0]=='@':            

            #update entities
            coordinate=list_movement[check_list][1:]
            coordinate=coordinate.split('-')
            tuples=(int(coordinate[0]),int(coordinate[1]))
            if tuples[0]-entities[list_movement[check_list-1]]['coordinates'][0]<2 and tuples[1]-entities[list_movement[check_list-1]]['coordinates'][1]<2 and entities[list_movement[check_list-1]]['team']==movement_orders[-1]:
                entities[list_movement[check_list-1]]['coordinates']=tuples
                if entities[list_movement[check_list-1]]['type']=='cruiser':
                    entities[list_movement[check_list-1]]['available_energy']-=10
    return entities

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
    energy_giving_orders : orders of energy giving od the player (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Louis Flamion (v.1 23/02/2020)
    implementation : Amaury Van Pevenaeyge (v.2 17/03/2020)
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
    #Searching for hubs name in entities
    for entity in entities :
        if 'hub' in entity :

            #Computing the amount of energy to add to the hub
            entities[entity]['available_energy'] += (entities[entity]['available_energy']/100) *  entities[entity]['regeneration_rate']

            #Set energy to 1500 if there is more than 1500
            if entities[entity]['available_energy'] > 1500 :
                entities[entity]['available_energy'] = 1500


    return entities
