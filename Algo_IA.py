# Algo pour l'IA intelligente

"""
input : two dictionnaries composing our data structure board and entities
output : chain of characters containing orders for the game

attack_tankers = []
defense_tankers = []
refuel_tankers = []
attack_cruisers = []
defense_cruisers = []
turn = 0

#FIRST PHASE

while regeneration_rate < 50:
    create tanker
    if turn is pair:
        add tanker to attack_tankers

    else:
        add tanker to refuel_tankers

    upgrade regeneration_rate of the hub

    for tanker in entities:
        move tankers towards different peaks

        for peaks in entities:
            if distance between tanker and peak <= 1:
                absorb energy from the peak
        end for

        if distance between tanker and hub <= 1:
            transfer all the energy from the tanker to the hub
    end for

    turn += 1

end while

#SECOND PHASE

while moving_cost > 5 and regeneration rate == 50:
    create cruiser
    add cruiser to attack_cruisers
    upgrade the moving cost of the cruisers

    for tanker in refuel_tankers:

        if tanker available_energy > 0:
            move tanker towards hub

            if distance between tanker and hub <= 1:
                transfer all the energy from the tanker to the hub

            end if
        end if

        else:
            move tanker towards different peaks
            #il faudrait parcourir tous les peaks et vérifier quel tanker en est le plus proche pour bien répartir les transferts d'énergie

            if distance between tanker and peak <= 1:
                absorb energy from the peak

            end if
        end else
    end for
            
    for tanker in attack_tankers:

        if tanker available_energy > 0:
            move tanker towards the closest cruiser

            if distance between tanker and the closest cruiser <= 1:
                transfer all the energy from the tanker to the cruiser

            end if
        end if

        else:
            move tanker towards different peaks
            #il faudrait parcourir tous les peaks et vérifier quel tanker en est le plus proche pour bien répartir les transferts d'énergie

            if distance between tanker and peak <= 1:
                absorb energy from the peak

            end if
        end else
    end for

#THIRD PHASE

