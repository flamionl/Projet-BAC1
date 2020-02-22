# Découpage des fonctions

from colored import *
import random

# Les upgrades sont générales ou pas ?

# Attention ! coordinates en y puis x !!!!!!

# J'ai rajouté le type à energy dans entities

# On doit gérer le cas dans lequel une équipe voudrait contrôler une entité adverse ?

# J'ai rajouté team en paramètre à qlq fonctions

# Au début les hubs commencent avec full energy ?

# Un joueur peut faire autant d'upgrades qu'il le souhaite MAIS une unité ne peut avoir qu'un seul oredre par tour ???

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
    The 4 types of player are : 'human', 'IA', 'distant_human', and 'distant_IA' if the player is respectively\
         a human, an IA, a human but on an other computer, and an IA but on another computer
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

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
    """
    board = {}

    for x in range (1, nb_columns + 1):
        for y in range (1, nb_lines + 1):
            board[(x, y)] = []

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
    """

def display_board (board, entities):

    # A modifier
    """ Actualise the board with entities dictionnary and displays the board game in the terminal

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Prints
    ------
    board_game : the board game

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
    """

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

## ORDRES ##

def sort_order (order):
    """ Sorts the order of a player depending on the type of these orders

    Parameters
    ----------
    order : order from the player (str)

    Returns
    -------
    creation_orders : orders of creation of the player (list of str)
    upgrade_orders : orders of upgrade of the player (list of str)
    attack_orders : orders of attack of the player (list of str)
    movement_orders : orders of deplacement of the player (list of str)
    energy_transfer_orders : orders of energy transfer of the player (list of str)
    """

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

def create_vessel (creation_orders, player, entities):
    # A modifier
    """ Creates a vessel (cruiser or tanker)

    Parameters
    ----------
    vessel_name : name of the vessel (str)
    team : name of the team (str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 21/02/2020)
    """

## UPGRADES ##

def upgrade (upgrade_orders, entities):
    # A modifier
    """ Checks if there is enough energy in the hub. Upgrades the entity if there is enough. Prints a message if there is not enough.

    Parameters
    ----------
    entity_name : name of the entity to upgrade (str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Prints
    ------
    warning : if there is not enough energy in the hub for the upgrade

    Version
    -------
    specification : Mathis Huet (v.1 21/02/2020)
    """

## COMBATS ##

def cruiser_attack (attack_orders, board, entities):

    # Attention ! coordinates en y puis x !

    # A modifier
    """ attacks the other entities depending on the energy dedicated to the attack

    Parameters
    ----------
    attack_orders : 
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict) 
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : updated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
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
    """ Removes all the entities which have structure points under or equal to 0

    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 20/02/2020)
    """

    for entity in entities:
        if entities[entity]['type'] != 'energy':
            structure_points = entities[entity]['structure_points']
            if structure_points <= 0:
                if entities[entity]['type'] == 'hub':
                # une équipe a gagné
            else:
                del entities[entity]

## DÉPLACEMENTS ##

def movement (movement_orders, board, entities):
    # A modifier
    """ moves an entity

    Parameters
    ----------
    vessel_name : name of the vessel (cruiser or tanker) to move (str)
    coordinates : tuple of integers containing x coordinates before the comma and y coordinates after the comma (tuple)
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    board : updated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
    """

## TRANSFERTS D'ÉNERGIE ##

def energy_absorption (energy_transfer_orders, coordinates, entities):
    # A modifier
    """ Absorbs the energy of an energy peak, and removes the peak from the map

    Parameters
    ----------
    tanker_name : name of the tanker (str)
    coordinates : coordinates of the the entity where the tanker picks up the energy (tuple of integers)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
    """

def energy_transfer (energy_transfer_orders, entities):
    # A modifier
    """ transfers energy from an entity to an other one

    Parameters
    ----------
    transmitter_name : name of the entity which transmits the energy (str)
    receiver_name : name of the entity which receives the transmitted energy (str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 19/02/2020)
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
    specification : Mathis Huet (v.1 19/02/2020)
    """
