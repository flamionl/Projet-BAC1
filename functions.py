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

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 19/02/2020)
    """
    

def actualise_board (board, entities):
    """ Actualises the information of entities dictionary in the board dictionary

    Parameters
    ----------
    board : dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)
    Note
    ----
    For a good render use the Monospace Bold policy

    Returns
    -------
    board : upated dictionary of the board having coordinates as a key, and all the entities on these coordinates as a value (dict)

    Version
    -------
    specification : Mathis Huet (v.1 21/02/2020)
    """

def display_board (board):
    """ Displays the board's game in the terminal

    Parameters
    ----------
    board : dictionary that contains coordinates as a key, and all the entities on these coordinates as a value (dict)

    Prints
    ------
    board_game : the board game

    Version
    -------
    specification : Louis Flamion (v.1 23/02/2020)
    """
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
    
    Version
    -------
    specification : Mathis Huet (v.1 22-02-2020)
    """
    
    # Creating all the lists
    creation_orders = []
    upgrade_orders = []
    attack_orders = []
    movement_orders = []
    energy_transfer_orders = []

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
        elif '<' in order or '>' in order:
            energy_transfer_orders.append(order)
        elif ':' in order:
            creation_orders.append(order)
    
    # Adding the name of the team at the end of each list (identification convention)
    upgrade_orders.append(team)
    attack_orders.append(team)
    movement_orders.append(team)
    energy_transfer_orders.append(team)
    creation_orders.append(team)
            
    return creation_orders, upgrade_orders, attack_orders, movement_orders, energy_transfer_orders

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
    """Creates a vessel (cruiser or tanker)

    Parameters
    ----------
    creation_orders : list of the orders of the creations for the player (list of str)
    player : the name of the player (str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Amaury Van Pevenaeyge (v.1 23/02/2020)
    """

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
    """ Removes all the entities which have structure points under or equal to 0

    Parameters
    ----------
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 20/02/2020)
    """
    
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

def energy_absorption (energy_transfer_orders, coordinates, entities):
    """ Absorbs the energy of an energy peak, and removes the peak from the map

    Parameters
    ----------
    energy_transfer_orders : receive the orders given by a player or an IA and check if he wants to take the energy peak (str)
    coordinates : coordinates of the the entity where the tanker picks up the energy (tuple of integers)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Returns
    -------
    entities : updated dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

    Version
    -------
    specification : Gerry Longfils (v.1 24/02/2020)
    """

def energy_transfer (energy_transfer_orders, entities):
    """ Transfers energy from a tanker to a cruiser or a hub

    Parameters
    ----------
    energy_transfer_order : list that contains the name of the tanker and the entity that the player wants to refuel (list of str)
    entities : dictionnary having the name of entities as key, and a dictionary of its characteristics as a value (dict)

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
