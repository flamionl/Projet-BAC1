# Découpage des fonctions

import colored
import random
import remote_play

## MISE EN PLACE ##

def game(file_path, player_1, player_2, id_player_1=0,id_player_2=0):
    """ General function which calls all the other sub-functions in order to run the game

    Parameters
    ----------
    player 1 : type of the player 1 (str)
    player 2 : type of player 2 (str)
    file_path : path of the file containing the information for the setup of the game (str)
    your_id : ID of your group if you play with a remote_player  (int) (optionnal)
    remote_id : ID of the remote group (int) (optionnal)

    Note
    ----
    The 3 types of player are : 'human', 'AI', and 'remote_player' if the player is respectively\
         a human playing on the local computer, an AI on the local computer, and a player (human or AI) on an other computer
    If you want to be connected to a referee set remote_id to 0

    Version
    -------
    specification :Louis Flamion & Gerry Longfils (v.3 12/04/2020)
    implementation : Louis Flamion & Gerry Longfils (v.3 12/04/2020)
    """

    #Getting connection information
    if player_1 == 'remote_player' and player_2 != 'remote_player' :
        connection = remote_play.create_connection(id_player_2,id_player_1,'127.0.0.1',True)
    elif player_2 == 'remote_player' and player_1 != 'remote_player' :
        connection = remote_play.create_connection(id_player_1,id_player_2,'127.0.0.1',True)

    #Creating data structures
    board, entities, nb_columns, nb_lines = create_data_structures(file_path)

    #Initialising turn variable
    turn = 1

    # Setting variables for naive AI
    ship_list_1 = []
    ship_list_2 = []

    #Setting the variables for upgrade function
    storage_capacity_blue, storage_capacity_red = 600, 600
    fire_range_blue, fire_range_red = 1, 1
    moving_cost_blue, moving_cost_red = 10, 10

    # Setting variables for AI

    # for team blue
    turn_AI_blue = 0
    AI_data_blue = {}
    tanker_to_peak_blue = {}
    peaks_blue = []
    tanker_to_cruiser_blue = {}
    state_phase_1_blue = 0
    state_phase_2_blue = 0
    for entity in entities:
        if entities[entity]['type'] == 'peak':
            peaks_blue.append(entity)

    #for team red
    turn_AI_red = 0
    AI_data_red = {}
    tanker_to_peak_red = {}
    tanker_to_cruiser_red = {}
    state_phase_1_red = 0
    state_phase_2_red = 0
    peaks_red = []
    for entity in entities :
        if entities[entity]['type'] == 'peak' :
            peaks_red.append(entity)

    while entities['hub_blue']['structure_points'] > 0 and entities['hub_red']['structure_points'] > 0 and turn < 5000 :

        #Printing the board
        display_board(board,entities,nb_columns,nb_lines)
        print('turn : %d' % turn)

        ## Player_1 ##

        #Checking player_1's type and getting orders
        if player_1 ==  'human' :
            orders = input('Quels sont vos ordres joueur 1 : ')
        elif player_1 == 'naive_AI':
            orders, ship_list_1 = get_naive_AI_orders(board, entities, turn, ship_list_1, nb_columns, nb_lines)
        elif player_1 == 'AI':
            orders, AI_data_blue, turn_AI_blue ,peaks_blue, tanker_to_peak_blue, tanker_to_cruiser_blue, state_phase_1_blue, state_phase_2_blue = get_AI_orders(board,entities, turn_AI_blue, AI_data_blue, peaks_blue, 'blue', tanker_to_peak_blue, tanker_to_cruiser_blue, state_phase_1_blue, state_phase_2_blue)
        else :
            orders = remote_play.get_remote_orders(connection)

        
        #Sending orders to the remote_player
        if player_2 == 'remote_player' :
            remote_play.notify_remote_orders(connection,orders)
        #player_1's orders sorting
        creation_orders_blue, upgrade_orders_blue, attack_orders_blue, movement_orders_blue, energy_absorption_blue, energy_giving_blue = sort_orders(orders,'blue')

        print('orders player 1 : %s' % orders)

        ## Player 2 ##

        #Checking player_2's type and getting orders
        if player_2 == 'human' :
            orders = input('Quels sont vos ordres joueur 2 : ')
        elif player_2 == 'naive_AI' :
            orders, ship_list_2 = get_naive_AI_orders(board, entities, turn, ship_list_2, nb_columns, nb_lines)
        elif player_2 == 'AI':
            orders, AI_data_red, turn_AI_red, peaks_red, tanker_to_peak_red, tanker_to_cruiser_red, state_phase_1_red, state_phase_2_red = get_AI_orders(board,entities, turn_AI_red, AI_data_red, peaks_red, 'red', tanker_to_peak_red, tanker_to_cruiser_red, state_phase_1_red, state_phase_2_red)
        else :
            orders = remote_play.get_remote_orders(connection)


        # Sending orders to the remote player
        if player_1 == 'remote_player':
            remote_play.notify_remote_orders(connection, orders)


        #player_2's orders sorting
        creation_orders_red, upgrade_orders_red, attack_orders_red, movement_orders_red, energy_absorption_red, energy_giving_red = sort_orders(orders,'red')

        print('orders_player 2 : %s' % orders)

        ## Orders execution ##

        #Creation vessel phase
        entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red = create_vessel(creation_orders_blue, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red)
        entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red = create_vessel(creation_orders_red, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red)


        board = actualise_board(board,entities)
        #upgrade entities phase
        entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red = upgrade(upgrade_orders_blue, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red)
        entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red = upgrade(upgrade_orders_red, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red)

        #attack phase
        entities = cruiser_attack(attack_orders_blue,board,entities)
        entities = cruiser_attack(attack_orders_red,board,entities)
        entities = remove_destroyed_entities(entities)

        board = actualise_board(board,entities)

        #move entities phase
        entities = movement(movement_orders_blue,board,entities, nb_columns, nb_lines)
        entities = movement(movement_orders_red,board,entities, nb_columns, nb_lines)

        board = actualise_board(board,entities)

        #energy absorption pics for tankers
        entities = energy_absorption(energy_absorption_blue,entities,board)
        entities = energy_absorption(energy_absorption_red,entities,board)

        #energy giving phase
        entities = energy_giving(energy_giving_blue,entities,board)
        entities = energy_giving(energy_giving_red,entities,board)

        entities= hubs_regeneration(entities)
        board = actualise_board(board,entities)
        
        display_information(entities)

        #Increment turn variable
        turn +=1
    
    if entities['hub_blue']['structure_points'] <= 0 and entities['hub_red']['structure_points'] <= 0:
        print('It\'s a draw !')
    elif entities['hub_blue']['structure_points'] <= 0:
        print('Team red wins !')
    elif entities['hub_red']['structure_points'] <= 0:
        print('Team blue wins !')
    #End communication with the remote player
    if player_1 == 'remote_player' or player_2 == 'remote_player' :
        remote_play.close_connection(connection)

def create_data_structures(file_path):
    """ Decodes the file for the setup of the game, creates the board dictionary and entities dictionary, and places the hubs and energy peaks

    Parameters
    ----------
    file_path : path of the file containing the information of the setup of the game (str)

    Returns
    -------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
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
    for line in board_info[6:]:
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
    implementation : Gerry Longfils & Louis Flamion (v.2 20/03/2020)
    """
    #Emojis used
    hub ='♜'
    tanker = '▲'
    case = '▒'
    cruiser = '☬'
    energy = '●'

    #Color used to print the board
    color1 = '#000000'
    color2 = '#ffffff'

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
                background_color = color1
                plateau += colored.bg(background_color)
            else :

                #Sets the background color on green
                background_color = color2
                plateau += colored.bg(background_color)

                #If there isn't any entities on the case
            if board[(line,column)]  == [] :
                plateau+=colored.fg(background_color)
                plateau += case

                #If there is one entity on the case
            elif len(board[line,column])==1:
                if entities[board[(line,column)][0]]['type'] != 'peak' :

                    #Looking to the entitiy's team to attribute the right color
                    if entities[board[(line,column)][0]]['team'] == 'blue' :
                        plateau+=colored.fg('#0033FF')
                    else :
                        plateau+=colored.fg('#FF0000')

                    #Looking to the entity's type to print on the board
                    if entities[board[(line,column)][0]]['type'] == 'cruiser':
                        plateau += cruiser
                    elif entities[board[(line,column)][0]]['type'] == 'tanker' :
                        plateau += tanker
                    elif entities[board[(line,column)][0]]['type'] == 'hub' :
                        plateau += hub

                    #Looks to the peak's available energy to print it with the right color
                else :

                    #Looking at biggest amount of energy of all peaks
                    energy_amount = []
                    for entity in entities :
                        if entities[entity]['type'] == 'peak' :
                            energy_amount.append(entities[entity]['available_energy'])

                    #Getting the biggest amount of energy
                    max_amount = max(energy_amount)

                    #Attributing colors to the peaks according their percentage of the biggest amount of energy
                    if entities[board[(line,column)][0]]['available_energy']>=(0.75*max_amount) :
                        plateau+= colored.fg('#008000')
                    elif entities[board[(line,column)][0]]['available_energy']<(0.75*max_amount) and entities[board[(line,column)][0]]['available_energy'] >= (0.5*max_amount) :
                        plateau+= colored.fg('#FF4500')
                    elif entities[board[(line,column)][0]]['available_energy']<(0.5*max_amount) and entities[board[(line,column)][0]]['available_energy'] >= (0.25*max_amount) :
                        plateau+= colored.fg('#efd807')
                    else :
                        plateau+= colored.fg('#bb0b0b')

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
                        plateau+=colored.fg('#0033FF')
                    else:
                        plateau+=colored.fg('#FF0000')
                    plateau += hub

                #Looking for cruiser
                elif 'cruiser' in type_of_entities :
                    if entities[board[(line,column)][type_of_entities.index('cruiser')]]['team'] == 'blue':
                        plateau+=colored.fg('#0033FF')
                    else:
                        plateau+=colored.fg('#FF0000')
                    plateau +=cruiser

                #Looking for tankers
                elif 'tanker' in type_of_entities :
                    if entities[board[(line,column)][type_of_entities.index('tanker')]]['team'] == 'blue':
                        plateau+=colored.fg('#0033FF')
                    else:
                        plateau+=colored.fg('#FF0000')
                    plateau+=tanker

                #Looking for colors of the peaks
                else :

                    #Looking at biggest amount of energy of all peaks
                    energy_amount = []
                    for entity in entities :
                        if entities[entity]['type'] == 'peak' :
                            energy_amount.append(entities[entity]['available_energy'])

                    #Getting the biggest amount of energy
                    max_amount = max(energy_amount)

                    #Attributing colors to the peaks according their percentage of the biggest amount of energy
                    if entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']>=(0.75*max_amount) :
                        plateau+= colored.fg('#008000')
                    elif entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<(0.75*max_amount) and entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy'] >= (0.5*max_amount) :
                        plateau+= colored.fg('#FF4500')
                    elif entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy']<(0.5*max_amount) and entities[board[(line,column)][type_of_entities.index('peak')]]['available_energy'] >= (0.25*max_amount) :
                        plateau+= colored.fg('#efd807')
                    else :
                        plateau+= colored.fg('#bb0b0b')
                    plateau+=energy

        #Reset colors
        plateau += colored.attr('reset')

        #Goes to the next line
        plateau+=case+'\n'

    #Bottom border creation

    plateau+=case * (nb_columns+2)
    #Print the board

    print(plateau)

def display_information(entities) :
    """get entities information for debugging more easier
    
    parameters
    ---------
    entities : dictinnary of entities (dict)
    """
    print('Hubs')
    print('----')
    for hub in entities :
        if entities[hub]['type'] == 'hub' :
            print('%s : ENERGIE : %d VIE : %d COORDONNEES : %s' %(hub,entities[hub]['available_energy'], entities[hub]['structure_points'],str(entities[hub]['coordinates'])))

    print('\nCruisers')
    print('--------')
    for cruiser in entities:
        if entities[cruiser]['type'] == 'cruiser':
            print('%s : ENERGIE : %d VIE : %d COORDONNEES : %s TEAM : %s MOVING COST : %d FIRE RANGE : %d' % (cruiser, entities[cruiser]['available_energy'], entities[cruiser]['structure_points'], str(entities[cruiser]['coordinates']), entities[cruiser]['team'], entities[cruiser]['moving_cost'], entities[cruiser]['fire_range']))
    print('\nTankers')
    print('-------')        
    for tanker in entities:
        if entities[tanker]['type'] =='tanker':
            print('%s : ENERGIE : %d  VIE: %d  COORDONNEES: %s   TEAM : %s   STORAGE CAPACITY: %d' %(tanker, entities[tanker]['available_energy'], entities[tanker]['structure_points'],str(entities[tanker]['coordinates']),entities[tanker]['team'], entities[tanker]['storage_capacity'])) 


## ORDRES ##


def sort_orders (orders, team):
    """ Sorts the orders of a player depending on the type of these orders

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

def get_naive_AI_orders (board, entities, turn, ship_list, nb_columns, nb_lines):
    """ Generates the orders of the AI

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    turn : turn of the game (int)
    ship_list : IA's ship list (list of str)
    nb_columns : number of columns of the board game (int)
    nb_lines : number of lines of the board game (int)

    Returns
    -------
    AI_order : orders of the IA (str)
    ship_list : IA's ship list (list of str)

    Version
    -------
    specification : Louis Flamion (v.1 22/02/2020)
    implementation : Gerry Longfils & Louis Flamion (v.1 19/03/2020)
    """
    # Initializing the order
    order = ''

    # Deleting the destroyed vessel from ship_list
    for ship in ship_list :
        if ship not in entities :
            del ship_list[ship_list.index(ship)]

    #Creating ship for the first turn
    if turn <=1 :
        ship_name = str(random.randint(1,100000000))
        ship_type = random.choice(['tanker','cruiser'])
        order += ship_name + ':' + ship_type
        ship_list.append(ship_name)
        return order, ship_list


    #generate ship orders
    if random.random() < 0.03 :
        ship_name = str(random.randint(1,100000000))
        ship_type = random.choice(['tanker','cruiser'])
        order += ' ' + ship_name + ':' + ship_type
        ship_list.append(ship_name)
        return order, ship_list

    #generate upgrade orders
    if random.random() < 0.1:
        upgrade_choice = random.choice(['regeneration','storage','range','move'])
        order += ' upgrade:' + upgrade_choice

    #generate movement orders
    if random.random() < 1.1 and len(ship_list) > 1:  # toujours
        for iteration in range (1, 5):
            ship_name=ship_list[random.randint(0,len(ship_list)-1)]
            ship_coord_y = entities[ship_name]['coordinates'][0]
            ship_coord_x = entities[ship_name]['coordinates'][1]
            coordinates_y = str(random.randint(ship_coord_y - 1,ship_coord_y + 1))
            coordinates_x=str(random.randint(ship_coord_x - 1,ship_coord_x + 1))
            order += ' ' + ship_name + ':@' + coordinates_y + '-' + coordinates_x
    #generate attack orders
    if random.random() < 1.1 and len(ship_list) > 1:  # toujours
        for iteration in range (1, 3):
            ship_name = ship_list[random.randint(0, len(ship_list) - 1)]
            coordinates_y = str(random.randint(1, nb_lines))
            coordinates_x = str(random.randint(1, nb_columns))
            damages = str(random.randint(1, 40))
            order += ' ' + ship_name + ':*' + coordinates_y + '-' + coordinates_x + '=' + damages

    #energy giving
    if random.random() < 1.1 and len(ship_list) > 1:
        giver = ship_list[random.randint(0,len(ship_list) - 1)]
        receiver = ship_list[random.randint(0,len(ship_list) - 1)]
        order += ' ' + giver + ':>' + receiver
    #energy abosorption
    if random.random() < 1.1 and len(ship_list) > 1:
        ship_name = ship_list[random.randint(0,len(ship_list) - 1)]
        coordinates_y = str(random.randint(1, nb_lines))
        coordinates_x = str(random.randint(1, nb_columns))
        order += ' ' + ship_name + ':<' + coordinates_y + "-" + coordinates_x


    return order, ship_list

def attribute_peaks(entities, AI_data, tanker_to_peak, peaks, regeneration_tankers, other_tankers) :
    """Attributes a tanker to the closest peak on the map
    
    Parameters
    ----------
    entities : entities of the game (dict)
    AI_data : dictionnary having the name of the ships as key, and a dictionary of its type and its function as a value (dict)
    tanker_to_peaks : dictionnary having the name of the tanker as key and a dictionnary containing the characteristics of the peak that he has to absorb as a value (dict)
    peaks : list containing the name of the peaks that are not attributed to a tanker (list)
    regeneration_tankers : list containing the names of all the regeneration tankers (list)
    other_tankers : list containing the names of the tankers that are not regeneration tankers (list)
    
    Returns
    -------
    tanker_to_peak : dictionnary having the name of the tanker as key  and a dictionnary containing the charactesristics of the peak that he has to absorb (dict)
    peaks : list containing the name of the peaks that are not attributed to a tanker (list)
    
    specification: Gerry Longfils (v.1 02/05/2020)
    implementation: Amaury Van Pevenaeyge, Gerry Longfils, Louis Flamion, Mathis Huet (v.1 02/02/2020)
    """
    

    # Removing the dead peaks from the peaks list
    for peak in peaks:

        if peak not in entities:

            peaks.remove(peak)
    
    #Getting all the tanker
    tanker_list = []

    for ship in AI_data :
        
        if ship in entities and entities[ship]['type'] == 'tanker' and ship in AI_data :

            tanker_list.append(ship)

    for ship in tanker_list :
        #If the tanker has not been attributed to a peak
        if ship in entities and peaks != [] and ship not in tanker_to_peak and ((ship in other_tankers and entities[ship]['available_energy'] == 0) or ship in regeneration_tankers):

        #Searching for the closest energy peak
            nearby_peak = peaks[0]

            if len(peaks) > 1  :

                for index in range(0,(len(peaks)-1)) :

                    if get_distance(entities[ship]['coordinates'],entities[peaks[index]]['coordinates']) < get_distance(entities[ship]['coordinates'],entities[nearby_peak]['coordinates']) :

                        nearby_peak =  peaks[index]
                
                # Attributing a peak to the ship
                tanker_to_peak[ship] = {'peak_name' : nearby_peak, 'peak_coordinates' : entities[nearby_peak]['coordinates']}
                
                #Removing the peak from the peak list
                peaks.remove(nearby_peak)
            
            elif len(peaks) == 1 :

                #Attributing the last peak to the tanker
                tanker_to_peak[ship] = {'peak_name' : peaks[0], 'peak_coordinates' : entities[peaks[0]]['coordinates']}

                #Removing the peak from the peak list 
                del peaks[0]

        #If the peak that was attributed to the tanker is dead
        if ship in tanker_to_peak and tanker_to_peak[ship]['peak_name'] not in entities and peaks != [] :

            # Attribute a new peak to the ship
            
            nearby_peak = peaks[0]

            if len(peaks) > 1 and ship in entities :

                for index in range(0,len(peaks)-1) :
                    
                    if get_distance(entities[ship]['coordinates'],entities[peaks[index]]['coordinates']) < get_distance(entities[ship]['coordinates'],entities[nearby_peak]['coordinates']) :

                        nearby_peak =  peaks[index]
            
                #Removing the peak from the peak list
                peaks.remove(nearby_peak)

                #Attributing a peak to the ship
                tanker_to_peak[ship] = {'peak_name' : nearby_peak, 'peak_coordinates' : entities[nearby_peak]['coordinates']}
                

            elif len(peaks) == 1 and ship in entities and peaks[0] in entities : 

                #Attributing the last peak to the tanker
                tanker_to_peak[ship] = {'peak_name' : peaks[0], 'peak_coordinates' : entities[peaks[0]]['coordinates']}
                
                #Removing the peak from the peak list
                del peaks[0]

        # if the peak originally attributed to the tanker is dead and that all the other peaks are already dead or attributed to another ship
        if ship in tanker_to_peak and tanker_to_peak[ship]['peak_name'] not in entities and peaks == []:

            del tanker_to_peak[ship]

    return tanker_to_peak, peaks

def refuel_cruisers(entities, fire_range, AI_data, other_tankers, cruiser_attack, hub_y, hub_x, tanker_to_cruiser, tanker_to_peak, peaks, hub, team, regeneration_tankers):
    """Moves a tanker to its associated cruiser in order to refuel this cruiser

    Parameters
    ----------
    
    entities: dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    fire_range: the fire range of all the cruisers (int)
    AI_data: dictionary having the name of the ships as key, and a dictionary of its type and its function as a value (dict)
    other_tankers: list that contains the name of the tanker that are not regeneration tankers (list)
    cruiser_attack: contain a list of all cruiser who will attack the opposite hub (list)
    hub_y: the "y" coordinate of the hub (int)
    hub_x: the "x" coordinate of the hub (int)
    tanker_to_cruiser: dictionnary having the name of the tanker as key  and the name of the associated cruiser as value (dict)
    tanker_to_peak: dictionnary having the name of the tanker as key and a dictionnary containing the characteristics of the peak that he has to absorb as a value (dict)
    peaks: list containing the name of the peaks that are not attributed to a tanker (list)
    hub: name of the hub's team of the IA (str)

    Returns
    -------

    orders: orders for moving refuel tankers (str)
    tanker_to_cruiser: dictionnary having the name of the tanker as key  and the name of the associated cruiser as value (dict)
    tanker_to_peak: dictionnary having the name of the tanker as key  and a dictionnary containing the charactesristics of the peak that he has to absorb (dict)
    peaks: list containing the name of the peaks that are not attributed to a tanker (list)

    Version
    -------

    specification: Amaury Van Pevenaeyge (v.1 02/05/2020)
    implementation: Amaury Van Pevenaeyge, Gerry Longfils, Louis Flamion, Mathis Huet (v.1 02/02/2020)
    """
    
    orders = ''

    # Updating other_tankers
    for ship in AI_data :
   
        if AI_data[ship]['type'] == 'tanker' and AI_data[ship]['function'] != 'regeneration' and ship not in other_tankers:

            other_tankers.append(ship)

    # Updating regeneration tankers
    for ship in AI_data :
   
        if AI_data[ship]['type'] == 'tanker' and AI_data[ship]['function'] == 'regeneration' and ship not in regeneration_tankers :

            regeneration_tankers.append(ship)

    #Getting cruisers
    cruisers = [] 

    for ship in AI_data :

        if ship in entities and AI_data[ship]['type'] == 'cruiser' :

            cruisers.append(ship) 
    
    # Getting defense cruisers
    cruiser_defense = []

    for ship in AI_data:
        if ship in entities and AI_data[ship]['type'] == 'cruiser' and AI_data[ship]['function'] == 'defense':
            cruiser_defense.append(ship)
               
    #Updating tanker_to_peak
    tanker_to_peak, peaks = attribute_peaks(entities,AI_data,tanker_to_peak,peaks, regeneration_tankers, other_tankers)

    for tanker in other_tankers:

        # if the tanker is a defense tanker which has been created this turn
        if tanker not in tanker_to_cruiser and 'defense_tanker' in tanker:
            tanker_to_cruiser[tanker] = {'associated_cruiser' : 'defense_cruiser_%s_%s' % (str(len(cruiser_defense)), team)}
        
        #Associate a cruiser to a tanker
        elif tanker not in tanker_to_cruiser and cruisers != []:

            index = random.randint(0, len(cruisers) - 1)
            tanker_to_cruiser[tanker] = {'associated_cruiser' : cruisers[index]}

        #move the tanker and give energy to the cruiser if the tanker has energy and has an associated_cruiser
        elif tanker in tanker_to_cruiser and tanker_to_cruiser[tanker]['associated_cruiser'] in entities and tanker in entities and entities[tanker]['available_energy'] != 0:

            target_coordinates = entities[tanker_to_cruiser[tanker]['associated_cruiser']]['coordinates']

            if get_distance(entities[tanker]['coordinates'], target_coordinates) > 1:
                
                # Move to the target coordinates
                orders += get_adequate_movement_order(entities[tanker]['coordinates'], target_coordinates, tanker)
            
            elif get_distance(entities[tanker]['coordinates'], target_coordinates) <= 1:

                # Give energy to the associated cruiser
                orders += ' %s:>%s' % (tanker, tanker_to_cruiser[tanker]['associated_cruiser'])
        
        #if the tanker has not energy and has not associated_cruiser
        elif tanker in tanker_to_cruiser and tanker_to_cruiser[tanker]['associated_cruiser'] in entities and tanker in entities and tanker in tanker_to_peak and  entities[tanker]['available_energy'] == 0:
            
            if get_distance(entities[tanker]['coordinates'],entities[tanker_to_peak[tanker]['peak_name']]['coordinates']) <= 1 :
                
                #Absorb the peak
                orders+=' %s:<%d-%d' %(tanker,tanker_to_peak[tanker]['peak_coordinates'][0],tanker_to_peak[tanker]['peak_coordinates'][1])
            else :

                #Move towards the peak
                orders+= get_adequate_movement_order(entities[tanker]['coordinates'],tanker_to_peak[tanker]['peak_coordinates'],tanker)

                            
        elif tanker in tanker_to_cruiser and tanker in entities and cruiser_attack == [] :
            
            #move to the hub
            orders += ' %s:@%d-%d' % (tanker, hub_y, hub_x)

            #give energy to the hub
            orders += ' %s:>hub' % tanker

        elif tanker not in tanker_to_cruiser and peaks == [] :

            #Move the tanker towards the hub
            if get_distance(entities[tanker]['coordinates'],entities[hub]['coordinates']) >= 1 :

                orders += get_adequate_movement_order(entities[tanker]['coordinates'],entities[hub]['coordinates'],tanker)
            else : 
                #Absorb energy
                orders += ' %s:<%d-%d' % (tanker, hub_y, hub_x)

    return orders, tanker_to_cruiser, tanker_to_peak, peaks
                       
def AI_attack (entities, enemy_hub, cruiser_attack,fire_range):
    """Moves the cruisers towards the enemy hub and attacks it if it is within the fire range 
    
    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    enemy_hub : ennemy hub name (str)
    cruiser_attack : list containing the names of all the attack cruisers (list)
    fire_range : fire range of the cruisers (int)

    Returns
    -------
    orders : orders for making moving and attacking the cruiser (str)

    Version
    -------

    specification : Louis Flamion (v.1 02/05/2020)
    implementation : Gerry Longfils, Amaury Van Pevenaeyge, Louis Flamion, Mathis Huet (v.1 02/05/2020)
    """

    orders = ''
    
    #Moving attack cruiser toward ennemy hub
    for ship in cruiser_attack :

        if ship in entities:

            #Checking if the ship is in fire range
            if get_distance(entities[ship]['coordinates'],entities[enemy_hub]['coordinates']) - fire_range <= 0 and entities[ship]['available_energy'] >= 10:

                enemy_hub_y = entities[enemy_hub]['coordinates'][0]
                enemy_hub_x = entities[enemy_hub]['coordinates'][1]

                #Generating attack order
                orders += ' %s:*%d-%d=%d' % (ship, enemy_hub_y, enemy_hub_x, int(entities[ship]['available_energy']/10))

            #If the ship is not in the fire range
            else :
                #Move the cruiser towards the enemy hubs
                orders+= get_adequate_movement_order(entities[ship]['coordinates'],entities[enemy_hub]['coordinates'],ship)
    return orders
    
def move_regeneration_tankers(entities, AI_data, tanker_to_peak, peaks, hub, other_tankers):
    """Moves the regeneration tankers to an energy peak, absorb the energy peak and move the tanker to the hub
    
    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    AI_data : dictionnary having the name of the ships as key, and a dictionary of its type and its function as a value (dict)
    tanker_to_peak : dictionnary having the name of the tanker as key  and a dictionnary containing the charactesristics of the peak that he has to absorb (dict)
    peaks : list containing the name of the peaks that are not attributed to a tanker (list)
    hub : name of the hub's team of the IA (str)
    other_tankers : list that contains the name of the tanker that are not regeneration tankers (list)

    Returns
    -------
    orders : orders for moving regeneration tankers
    tanker_to_peak : dictionnary having the name of the tanker as key  and a dictionnary containing the charactesristics of the peak that he has to absorb (dict)
    peaks : list containing the name of the peaks that are not attributed to a tanker (list)
    other_tankers : list that contains the name of the tanker that are not regeneration tankers (list)
    
    Version
    -------
    
    specification :  Mathis Huet (v.1 02/05/2020)
    implementation : Gerry Longfils, Amaury Van Pevenaeyge, Louis Flamion, Mathis Huet (v.1 02/05/2020)
    """
    orders = ''

    #Getting regeneration tankers
    regeneration_tankers  = []

    for ship in AI_data :

        if AI_data[ship]['type'] == 'tanker' and AI_data[ship]['function'] == 'regeneration' :

            regeneration_tankers.append(ship)

    #Updating tanker_to_peak and peaks
    tanker_to_peak,peaks = attribute_peaks(entities,AI_data,tanker_to_peak,peaks, regeneration_tankers, other_tankers)

            
    for ship in regeneration_tankers:

        #If the tanker is full or if the aren't any peaks left to absorb for the tanker
        if ship in entities and ((entities[ship]['available_energy'] == entities[ship]['storage_capacity']) or (ship not in tanker_to_peak and peaks == [])):
            # Move tanker to the hub
            ship_coordinates = entities[ship]['coordinates']
            hub_coordinates = entities[hub]['coordinates']
            orders += get_adequate_movement_order(ship_coordinates, hub_coordinates, ship)

            # Transfer tanker's energy to the hub
            if get_distance(hub_coordinates, ship_coordinates) <= 1:

                orders += ' %s:>hub' % ship
                
            #Transforming regeneration tanker into refuel tankers
            if ship not in tanker_to_peak and peaks == []:

                regeneration_tankers.remove(ship)
                other_tankers.append(ship)
                AI_data[ship]['function'] = 'refuel'

        elif ship in tanker_to_peak and ship in entities:
            
            if get_distance(entities[ship]['coordinates'],tanker_to_peak[ship]['peak_coordinates']) <= 1 :  

                #Absorb energy if the tanker is close enough
                orders += ' %s:<%d-%d' %(ship,tanker_to_peak[ship]['peak_coordinates'][0],tanker_to_peak[ship]['peak_coordinates'][1])

            else :

                #Move the tanker to an energy peak
                
                orders += get_adequate_movement_order(entities[ship]['coordinates'],entities[tanker_to_peak[ship]['peak_name']]['coordinates'],ship)

    return orders, tanker_to_peak, peaks, other_tankers

def AI_defense(board,entities,cruiser_defense,fire_range,team,hub,enemy_hub_coordinates, AI_data):
    """Gives the defense orders of the defense cruisers of the AI

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    cruiser_defense : list containing the name of all the defense cruisers (list)
    fire_range : fire range of the cruisers (int)
    team : name of the team (str)
    hub : name of the team's hub (str)
    enemy_hub_coordinates : ennemy hub coordinates (tuples)
    AI_data: dictionnary having the name of the ships as key, and a dictionary containing its type and its function as a value (dict)
    
    Returns
    -------
    orders : defense orders of the AI (str)

    Version
    -------
    specification : Mathis Huet (v.1 02/05/2020)
    implementation: Louis Flamion, Mathis Huet, Gerry Longfils, Amaury Van Pevenaeyge (v.1 02/05/2020)
    """
    orders = ''
    other_cruiser_flag = 0
    
    #For every defense cruiser
    for ship in cruiser_defense :
        moving_flag = 0

        if ship in entities :

            hub_y = entities[hub]['coordinates'][0]
            hub_x = entities[hub]['coordinates'][1]

            # Moving the defense cruisers to their good position
            if get_distance(entities[ship]['coordinates'], (hub_y, hub_x)) < 2:
                orders += get_adequate_movement_order(entities[ship]['coordinates'], enemy_hub_coordinates, ship)
                moving_flag = 1

            # If there's another cruiser on the same coordinates, move one of them
            if moving_flag == 0 and other_cruiser_flag == 0:
                entities_on_case = board[entities[ship]['coordinates']]
                if ship in entities_on_case:
                    entities_on_case.remove(ship)
                if entities_on_case != []:
                    for entity in entities_on_case : 
                        if entity in AI_data and AI_data[entity]['type'] == 'cruiser' and AI_data[entity]['function'] == 'defense':
                            other_cruiser_flag += 1
                            if other_cruiser_flag >= 1:
                                orders += get_adequate_movement_order(entities[ship]['coordinates'], enemy_hub_coordinates, ship)

            #Attacking every enemy in the fire range
            for coord in board :

                if get_distance(coord,entities[ship]['coordinates']) <= fire_range and board[coord] != [] :

                    #Checking if there is an enemy on the case
                    flag = 0
                    for entity in board[coord] :

                        if entities[entity]['type']=='cruiser' and entities[entity]['team'] != team:

                            flag = 1

                    #Attack the case if there is an enemy on the case
                    if flag == 1 and moving_flag == 0 and entities[ship]['available_energy'] >= 10:

                        orders += ' %s:*%d-%d=%d' %(ship, coord[0],coord[1],entities[ship]['available_energy'] // 10)   
        
    return orders

def get_AI_orders(board,entities, turn_AI, AI_data, peaks, team, tanker_to_peak, tanker_to_cruiser, state_phase_1, state_phase_2):
    """Gives all the orders of the AI

    Parameters
    ----------

    board: dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities: dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    turn_AI: the number of AI's turns (int)
    AI_data: dictionnary having the name of the ships as key, and a dictionary containing its type and its function as a value (dict)
    peaks: list containing the name of the peaks that are not attributed to a tanker (list) 
    team : name of the team (str)
    tanker_to_peak: dictionnary having the name of the tanker as key and a dictionnary containing the characteriistics of the peak that it has to absorb as a value (dict)
    tanker_to_cruiser: dictionnary having the name of the tanker as key and the name of the associated cruiser as value (dict)
    state_phase_1: the state of the phase 1 (int)
    state_phase_2: the state of the phase 2 (int)

    Returns
    -------

    orders: all the orders of the AI (str)
    AI_data: dictionnary having the name of the ships as key, and a dictionary of its type and functions as a value (dict)
    turn_AI: the number of AI's turns (int)
    peaks: list containing the name of the peaks that are not attributed to a tanker (list) 
    tanker_to_peak: dictionnary having the name of the tanker as key  and a dictionnary containing the charactesristics of the peak that he has to absorb (dict)
    tanker_to_cruiser: dictionnary having the name of the tanker as key  and the name of the associated cruiser as value (dict)
    state_phase_1:the state of the phase 1 (int)
    state_phase_2:the state of the phase 2 (int)
    
    Specification : Mathis Huet, Louis Flamion, Gerry Longfils, Amaury Van Pevenaeyge (v.2 02/05/2020)
    implementation : Mathis Huet, Louis Flamion, Gerry Longfils, Amaury Van Pevenaeyge(v.2 02/05/2020)
    """
    orders = ''
    fire_range = 1

    #Getting the hub name of the AI
    if team == 'blue' :
        hub = 'hub_blue'
        enemy_hub = 'hub_red'

    else :

        hub = 'hub_red'
        enemy_hub = 'hub_blue'

    # Getting the coordinates of the hubs
    hub_coordinates = entities[hub]['coordinates']
    hub_y = hub_coordinates[0]
    hub_x = hub_coordinates[1]

    enemy_hub_coordinates = entities[enemy_hub]['coordinates']

    #Getting fire range value
    for ship in AI_data :

        if ship in entities and AI_data[ship]['type'] == 'cruiser' :
            fire_range = entities[ship]['fire_range']

    #Getting the defense cruisers
    cruiser_defense = []

    for ship in AI_data :

        if ship in entities :

            if AI_data[ship]['type'] == 'cruiser' and AI_data[ship]['function'] == 'defense' :

                cruiser_defense.append(ship)

    #Getting the attacks cruisers
    cruiser_attack = []

    for ship in AI_data :

        if ship in entities:

            if AI_data[ship]['type'] == 'cruiser' and AI_data[ship]['function'] == 'attack':

                cruiser_attack.append(ship)

    #Getting refuel tankers
    other_tankers = []

    for ship in AI_data : 

        if ship in entities :  

            if AI_data[ship]['type'] == 'tanker' and AI_data[ship]['function'] != 'regeneration' :

                other_tankers.append(ship)
    
    #Getting regeneration tankers
    regeneration_tankers = []
    
    for ship in AI_data :

        if ship in entities :
            
            if AI_data[ship]['type'] == 'tanker' and AI_data[ship]['function'] == 'regeneration' :

                regeneration_tankers.append(ship)

    ### Phase 1 ###

    if peaks == [] and entities[hub]['available_energy'] >= 750:
        # create an attack_cruiser
        flag = 0

        while flag == 0:

            ship_name = str(random.randint(0, 1000000))

            if ship_name not in AI_data and ship_name not in entities:

                flag = 1
                orders += ' %s:cruiser' % ship_name
                AI_data[ship_name] = {'type' : 'cruiser', 'function' : 'attack'}

    if len(cruiser_defense) == 2 and entities[hub]['available_energy'] >= 1000:
        if len(other_tankers) < 2:
            # create a defense tanker
            flag = 0

            while flag == 0:

                ship_name = 'defense_tanker_%d' % random.randint(0, 1000000)

                if ship_name not in AI_data and ship_name not in entities:

                    flag = 1
                    orders += ' %s:tanker' % ship_name
                    AI_data[ship_name] = {'type' : 'tanker', 'function' : 'defense'}

    if len(cruiser_attack) == 1 and entities[hub]['available_energy'] >= 1000 and len(other_tankers) < 2:

        # create a refuel tanker
        flag = 0

        while flag == 0:

            ship_name = 'refuel_tanker_%d' % random.randint(0, 1000000)

            if ship_name not in AI_data and ship_name not in entities:

                flag = 1
                orders += ' %s:tanker' % ship_name
                AI_data[ship_name] = {'type' : 'tanker', 'function' : 'refuel'}

    if not (len(regeneration_tankers) < 7 and not (len(regeneration_tankers) == 0 and fire_range == 5)):

        state_phase_1 = 1
    
    if state_phase_1 == 0:
        if len(regeneration_tankers) == 1 and entities[hub]['available_energy'] >= 750 and len(cruiser_defense) < 2 :
            #Create a defense cruiser
            flag = 0

            while flag == 0:

                ship_name = 'defense_cruiser_%s_%s' % (str(len(cruiser_defense) + 1), team)

                if ship_name not in AI_data and ship_name not in entities:

                    flag = 1
                    orders += ' %s:cruiser' % ship_name
                    AI_data[ship_name] = {'type' : 'cruiser', 'function' : 'defense'}
       
        if len(regeneration_tankers) == 2 and entities[hub]['available_energy'] >= 750 and len(cruiser_attack) < 1:

            #create an attack cruiser
            flag = 0

            while flag == 0:

                ship_name = str(random.randint(0, 1000000))

                if ship_name not in AI_data and ship_name not in entities:

                    flag = 1
                    orders += ' %s:cruiser' % ship_name
                    AI_data[ship_name] = {'type' : 'cruiser', 'function' : 'attack'}

        elif entities[hub]['available_energy'] >= 1000 and (turn_AI % 2 == 0 or fire_range == 5 or len(regeneration_tankers) < 3):

            # create a regeneration tanker
            flag = 0
            
            while flag == 0:
                
                ship_name = str(random.randint(0, 1000000))
                
                if ship_name not in AI_data and ship_name not in entities:
                    
                    flag = 1
                    orders += ' %s:tanker' % ship_name
                    AI_data[ship_name] = {'type' : 'tanker', 'function' : 'regeneration'}
                    
        elif entities[hub]['available_energy'] >= 600 and fire_range < 5 and turn_AI % 2 == 1:
            
            # Upgrade the storage capacity of the tankers
            orders += ' upgrade:range'
    
    ### Phase 2 ###

    if state_phase_1 == 1 and entities[hub]['available_energy'] >= 1000:
        
    # Create a refuel tanker 
        flag = 0
        while flag == 0:
            
            ship_name = str(random.randint(0, 1000000))
            
            if ship_name not in AI_data and ship_name not in entities:
                
                flag = 1
                orders += ' %s:tanker' % ship_name
                AI_data[ship_name] = {'type' : 'tanker', 'function' : 'refuel'}
                state_phase_2 = 1

    
    ### Phase 3 ###
    
    if state_phase_1 == 1 and state_phase_2 == 1 and len(other_tankers) >= 1:
    
        if entities[hub]['available_energy'] >= 750 and len(cruiser_attack) < 7:
            
            #create a cruiser
            flag = 0

            while flag == 0:

                ship_name = str(random.randint(0, 1000000))
                
                if ship_name not in AI_data and ship_name not in entities:
                    
                    flag = 1
                    orders += ' %s:cruiser' % ship_name
                    AI_data[ship_name] = {'type' : 'cruiser', 'function' : 'attack'}
        
    #send tankers towards peaks
    tanker_orders, tanker_to_peak, peaks, other_tankers = move_regeneration_tankers(entities, AI_data, tanker_to_peak, peaks, hub, other_tankers)
    orders += tanker_orders

    # Move the attack tankers to the hub, absorb its energy, and transfer it to the cruiser with the less energy
    refuel_orders, tanker_to_cruiser, tanker_to_peak, peaks = refuel_cruisers(entities, fire_range, AI_data, other_tankers, cruiser_attack, hub_y, hub_x, tanker_to_cruiser, tanker_to_peak,peaks, hub, team, regeneration_tankers)
    orders += refuel_orders

    #Move the attack cruisers towards the enemy hub and attack it
    AI_attack_orders = AI_attack(entities, enemy_hub, cruiser_attack, fire_range)
    orders += AI_attack_orders

    AI_defense_orders = AI_defense(board,entities,cruiser_defense,fire_range,team,hub,enemy_hub_coordinates, AI_data)
    orders+=AI_defense_orders

    turn_AI += 1
    
    if orders != '':
        
        orders = orders[1:]

    return orders, AI_data, turn_AI, peaks, tanker_to_peak, tanker_to_cruiser, state_phase_1, state_phase_2
    
def get_adequate_movement_order(departure_coordinates, arrival_coordinates, ship_name):
    """ Gives the adequate movement order (1 case range) in order to deplace an entity to the arrival_coordinates

    Parameters
    ----------
    departure_coordinates : current coordinates of the entity (tuple of integers)
    arrival_coordinates : coordinates where the entity has to go, on a long term (tuple of integers)
    ship_name : name of the ship (int)

    Returns
    -------
    adequate_order : adequate order of movement (str)

    Note
    ----
    This function is only used in the AI

    Version
    -------
    specification : Mathis Huet (v.1 15/04/2020)
    implementation : Mathis Huet (v.1 15/04/2020)
    """
    y_difference = arrival_coordinates[0] - departure_coordinates[0]
    x_difference = arrival_coordinates[1] - departure_coordinates[1]

    if y_difference > 0:

        adequate_y = departure_coordinates[0] + 1

    elif y_difference == 0:

        adequate_y = departure_coordinates[0]

    elif y_difference < 0:

        adequate_y = departure_coordinates[0] - 1

    if x_difference > 0:

        adequate_x = departure_coordinates [1] + 1

    elif x_difference == 0:

        adequate_x = departure_coordinates [1]

    if x_difference < 0:

        adequate_x = departure_coordinates [1] - 1

    adequate_order = ' %s:@%d-%d' % (ship_name, adequate_y, adequate_x)

    return adequate_order

## CRÉATION D'UNITÉS ##

def create_vessel (creation_orders, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red):
    """Creates a vessel (cruiser or tanker)

    Parameters
    ----------
    creation_orders : orders of creation (list of str)
    entities : dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    storage_capacity_blue : current storage capacity of the tankers of the team blue (int)
    fire_range_blue : current fire range of the cruisers of the team blue (int)
    moving_cost_blue : current moving cost of the cruisers of the team blue (int)
    storage_capacity_red : current storage capacity of the tankers of the team red (int)
    fire_range_red : current fire range of the cruisers of the team red (int)
    moving_cost_red : current moving cost of the cruisers of the team red (int)

    Returns
    -------
    entities : updated dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    storage_capacity_blue : current storage capacity of the tankers of the team blue (int)
    fire_range_blue : current fire range of the cruisers of the team blue (int)
    moving_cost_blue : current moving cost of the cruisers of the team blue (int)
    storage_capacity_red : current storage capacity of the tankers of the team red (int)
    fire_range_red : current fire range of the cruisers of the team red (int)
    moving_cost_red : current moving cost of the cruisers of the team red (int)

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 23/02/2020)
    implementation : Amaury Van Pevenaeyge (v.1 15/03/2020)
    """
    #Get the name of the team in the creation order list
    if creation_orders != []:
        team = creation_orders[-1]
        del creation_orders[-1]
        hub_name = 'hub_%s' % team

    #Split orders in two strings
    for order in creation_orders:

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
        if vessel_type == 'tanker' and entities[hub_name]['available_energy'] >= 1000:

            if team == 'blue':
                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'tanker', 'team': team,
                                            'storage_capacity': storage_capacity_blue, 'available_energy': storage_capacity_blue, 'structure_points': 50}

                #Removes energy from the hub following the creation of a tanker
                entities['hub_blue']['available_energy'] -= 1000

            elif team == 'red':
                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'tanker', 'team': team,
                                            'storage_capacity': storage_capacity_red, 'available_energy': storage_capacity_red, 'structure_points': 50}

                #Removes energy from the hub following the creation of a tanker
                entities['hub_red']['available_energy'] -= 1000

        elif vessel_type == 'cruiser' and entities[hub_name]['available_energy'] >= 750:

            if team == 'blue':
                entities[vessel_name] = {'coordinates': coordinates_hub_blue, 'type': 'cruiser', 'team': team, 'structure_points': 100,
                                            'available_energy': 400, 'moving_cost': moving_cost_blue, 'fire_range': fire_range_blue, 'storage_capacity': 400}

                #Removes energy from the hub following the creation of a cruiser
                entities['hub_blue']['available_energy'] -= 750

            elif team == 'red':
                entities[vessel_name] = {'coordinates': coordinates_hub_red, 'type': 'cruiser', 'team': team, 'structure_points': 100,
                                            'available_energy': 400, 'moving_cost': moving_cost_red, 'fire_range': fire_range_red, 'storage_capacity': 400}

                #Removes energy from the hub following the creation of a cruiser
                entities['hub_red']['available_energy'] -= 750

    return entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red

def upgrade (upgrade_orders, entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red):
    """Upgrades the characteristic of an entity as asked in the orders

    Parameters
    ----------
    upgrade_orders : orders of upgrade of the player (list of str)
    entities : dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    storage_capacity_blue : current storage capacity of the tankers of the team blue (int)
    fire_range_blue : current fire range of the cruisers of the team blue (int)
    moving_cost_blue : current moving cost of the cruisers of the team blue (int)
    storage_capacity_red : current storage capacity of the tankers of the team red (int)
    fire_range_red : current fire range of the cruisers of the team red (int)
    moving_cost_red : current moving cost of the cruisers of the team red (int)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    storage_capacity_blue : current storage capacity of the tankers of the team blue (int)
    fire_range_blue : current fire range of the cruisers of the team blue (int)
    moving_cost_blue : current moving cost of the cruisers of the team blue (int)
    storage_capacity_red : current storage capacity of the tankers of the team red (int)
    fire_range_red : current fire range of the cruisers of the team red (int)
    moving_cost_red : current moving cost of the cruisers of the team red (int)

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 23/02/2020)
    implementation : Mathis Huet & Amaury Van Pevenaeyge (v.2 19/03/2020)
    """

    # Getting back and deleting the name of the team from the list if the list is not empty
    if upgrade_orders != []:
        team = upgrade_orders[-1]
        del upgrade_orders[-1]
        hub_name = 'hub_%s' % team

    for order in upgrade_orders:

        # Treating the order
        order = order.split(':')
        characteristic = order[1]

        # Setting the variables depending on the type of upgrade
        if characteristic == 'regeneration':
            entity_type = 'hub'
            upgrade_cost = 750
            characteristic_in_board = 'regeneration_rate'
            upper_limit = 50
            upgrade_step = 5

        elif characteristic == 'storage':
            entity_type = 'tanker'
            upgrade_cost = 600
            characteristic_in_board = 'storage_capacity'
            upper_limit = 900
            upgrade_step = 100

        elif characteristic == 'range':
            entity_type = 'cruiser'
            upgrade_cost = 400
            characteristic_in_board = 'fire_range'
            upper_limit = 5
            upgrade_step = 1

        elif characteristic == 'move':
            entity_type = 'cruiser'
            upgrade_cost = 500
            characteristic_in_board = 'moving_cost'
            under_limit = 5
            upgrade_step = -1

        # Checking if there is enough available energy in the team's hub
        if entities[hub_name]['available_energy'] >= upgrade_cost:
            entities[hub_name]['available_energy'] -= upgrade_cost

            if characteristic == 'regeneration' or characteristic == 'storage' or characteristic == 'range':

                # Upgrading
                for entity in entities:
                    if entities[entity]['type'] == entity_type and entities[entity]['team'] == team and entities[entity][characteristic_in_board] < upper_limit:
                        entities[entity][characteristic_in_board] += upgrade_step

                # Upgrading the characteristic for the future vessels created depending on the team
                if team == 'blue':
                    if characteristic == 'storage' and storage_capacity_blue < upper_limit:
                        storage_capacity_blue += upgrade_step
                    elif characteristic == 'range' and fire_range_blue < upper_limit:
                        fire_range_blue += upgrade_step
                elif team == 'red' :
                    if characteristic == 'storage' and storage_capacity_red < upper_limit:
                        storage_capacity_red += upgrade_step
                    elif characteristic == 'range' and fire_range_red < upper_limit:
                        fire_range_red += upgrade_step

            elif characteristic == 'move':

                # Upgrading
                for entity in entities:
                    if entities[entity]['type'] == entity_type and entities[entity]['team'] == team and entities[entity][characteristic_in_board] > under_limit:
                        entities[entity][characteristic_in_board] += upgrade_step

                # Upgrading the characteristic for the future cruisers created
                if team == 'blue' and moving_cost_blue > under_limit:
                    moving_cost_blue += upgrade_step
                elif team == 'red' and moving_cost_red > under_limit:
                    moving_cost_red += upgrade_step

    return entities, storage_capacity_blue, fire_range_blue, moving_cost_blue, storage_capacity_red, fire_range_red, moving_cost_red

## COMBATS ##

def cruiser_attack (attack_orders, board, entities):
    """ attacks the other entities as oredered by a player

    Parameters
    ----------
    attack_orders : attack order of the player (list of str)
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
        del attack_orders[-1]

        #Getting info from the attack_orders
        for order in attack_orders :
            splited_order = order.split(':')
            vessel_name = splited_order[0]
            line = int(splited_order[1].split('-')[0][1:])
            column = int(splited_order[1].split('-')[1].split('=')[0])
            damages = int(splited_order[1].split('=')[1])
            if vessel_name in entities :
                #Getting coordinates of the ship that attacks
                vessel_coordinates = entities[vessel_name]['coordinates']

                #Checking if there is an entity on the case
                if board[(line,column)] != [] and entities[vessel_name]['type'] == 'cruiser' :
                    #Checking if the vessel is not too far from the case that he wants to attack and if the vessel has enough energy to attack
                    if get_distance(vessel_coordinates,(line,column)) <= entities[vessel_name]['fire_range'] and entities[vessel_name]['available_energy'] - (damages*10) >= 0 and entities[vessel_name]['team'] == team :
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
    #Manathan's formule
    distance = max(abs(coordinates_1[1]-coordinates_2[1]),abs(coordinates_1[0]-coordinates_2[0]))

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

    # Adding the entities to remove in the list
    for entity in entities:
        if entities[entity]['type'] != 'peak' and entities[entity]['type'] != 'hub':
            structure_points = entities[entity]['structure_points']
            if structure_points <= 0:
                entities_to_remove.append(entity)

    # Removing the entities in the list, from entities dict
    for entity in entities_to_remove:
        del entities[entity]

    return entities

## DÉPLACEMENTS ##

def movement (movement_orders, board, entities, nb_columns, nb_lines):
    """Moves an entity by consequences of the orders given by player or an IA

    Parameters
    ----------
    movement_orders : orders of deplacement of the player (list of str)
    entities : dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.2 17/03/2020)
    implementation : Gerry Longfils & Amaury Van Pevenaeyge (v.1 17/03/2020)
    """
    # Getting back and deleting the name of the team from the list if the list is not empty
    if movement_orders != []:
        team = movement_orders[-1]
        del movement_orders[-1]

    for order in movement_orders:

        #Treating the order
        order = order.split(':@')
        vessel_name = order[0]
        coordinates = order[1]
        coordinates = coordinates.split('-')
        if vessel_name in entities:
            coordinates = (int(coordinates[0]), int(coordinates[1]))
            distance = get_distance(coordinates, entities[vessel_name]['coordinates'])

            #Check if the coordinates of the movement is in the board
            if int(coordinates[0]) > 0 and int(coordinates[1]) > 0:

                if int(coordinates[0]) <= nb_lines and int(coordinates[1]) <= nb_columns:

                    #Actualise the coordinates of the vessel
                    if distance <= 1 and entities[vessel_name]['team'] == team and entities[vessel_name]['type'] == 'tanker':

                        entities[vessel_name]['coordinates'] = coordinates

                    #If the vessel is a cruiser, remove the moving cost from his available energy
                    elif entities[vessel_name]['type'] == 'cruiser' and distance <= 1 and entities[vessel_name]['team'] == team and entities[vessel_name]['available_energy'] - entities[vessel_name]['moving_cost'] * distance >= 0:

                            # * distance in order to fix the case in which the player wants to move
                            entities[vessel_name]['coordinates'] = coordinates
                            entities[vessel_name]['available_energy'] -= entities[vessel_name]['moving_cost'] * distance

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

    Notes
    -----
    The order gives a coordinate and the entitiy absorbs the energy of the first entities which have the correct type
    (so it's a bit random if there are sevral entities of a correct type on the same coordinates)
    And it continues to absorb the enrgy of another entity on the case if the tanker is not full of energy

    Version
    -------
    specification : Gerry Longfils (v.1 24/02/2020)
    implementation : Mathis Huet (v.2 17/03/2020)
    """

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

        if coordinates in board :
            entities_on_case = board[coordinates]
            for entity in entities_on_case:
                absorbed_entity = entity

                if absorbed_entity in entities and tanker_name in entities:
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
                            if entities[absorbed_entity]['type'] == 'peak' and entities[absorbed_entity]['available_energy'] <= 0:
                                del entities[absorbed_entity]

    return entities

def energy_giving (energy_giving_orders, entities, board):
    """ Transfers energy from a tanker to a cruiser or a hub

    Parameters
    ----------
    energy_giving_orders : orders of energy giving od the player (list of str)
    entities : dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Returns
    -------
    entities : updated dictionary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

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
        if vessel_receiving == 'hub':
            vessel_receiving += '_%s' % team
        if vessel_giving in entities and vessel_receiving in entities :
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
            entities[entity]['available_energy'] += entities[entity]['regeneration_rate']

            #Set energy to 1500 if there is more than 1500
            if entities[entity]['available_energy'] > entities[entity]['storage_capacity'] :
                entities[entity]['available_energy'] = entities[entity]['storage_capacity']

    return entities