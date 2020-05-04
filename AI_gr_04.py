import random

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