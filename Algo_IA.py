# Algo pour l'IA intelligente

"""
input : two dictionnaries composing our data structure board and entities
output : chain of characters containing orders for the game

#FIRST PHASE

while regeneration_rate < 50

    create tanker
    add tanker to regeneration_tankers list
    upgrade regeneration_rate of the hub

    for all the tankers in regeneration_tankers list
        if tanker available_energy different from its storage_capacity
            move tankers towards random peaks
            absorb the peak
        else
            move tanker to the hub
            transfer its energy to the hub

    end for

end while

#SECOND PHASE

initialize turn to 0

while (turn < 5 or fire_range < 5) and regeneration_rate == 50

    create tanker
    transfer energy to the hub
    upgrade fire_range

    for all the tankers

        if tanker available_energy different from its storage_capacity
            move tankers towards random peaks
            absorb the peak

    end for

while (moving_cost > 5 or turn < 20) and  regeneration rate == 50 and fire_range == 5

    if turn is pair
        create 2 cruisers
        add cruiser to attack_cruisers list
    else
        create one cruiser
        upgrade the moving cost of the cruisers

    for all the tankers in regeneration_tankers list

        if tanker available_energy different from its storage_capacity
            move tankers towards random peaks
            absorb the peak
        else
            move tanker to the hub
            transfer its energy to the hub

    end for

    for all the tankers not in regeneration_tankers list

        if the available energy of the tanker equals to its storage_capacity
            move tanker towards the cruiser which has the less available_energy
            transfer energy to the cruiser

        else
            move each tanker towards a differenet peak
            absorb energy from the peak

    end for

    for all the cruisers in attack_cruisers list
        move the cruiser towards hub
        attack the hub if it's possible

    end for

#THIRD PHASE

while fire_range == 5 and moving_cost == 5 and regeneration_rate == 50 and length of the defense_cruisers list < 15

    if turn is pair
        create 2 cruisers
        add the two cruisers in the defense_cruisers list

        if the length of defense_cruisers list <=10:
            for cruisers in defense_cruisers list
                move the cruiser on a case where the distance with the hub equals 4
                if there is another defense cruiser on the same case as the cruiser
                    move the cruiser to another case
        else
            for cruiser in cruisers_list:
                if distance between hub and cruiser != 4
                    move cruiser to a case where the distance equals 5

    else
        create a tanker
        add tanker to defense_tankers list

        for all the tankers in regeneration_tankers list

            if tanker available_energy different from its storage_capacity
                move tankers towards random peaks
                absorb the peak
            else
                move tanker to the hub
                transfer its energy to the hub

        end for

        for all the tankers not in regeneration_tankers list

            if the available energy of the tanker equals to its storage_capacity
                move tanker towards the cruiser which has the less available_energy
                transfer energy to the cruiser

            else
                move each tanker towards a differenet peak
                absorb energy from the peak

        end for

    for cruiser in defense_cruisers list
        if an opponent cruiser is in its fire_range
            attack this cruiser

# FOURTH PHASE

while fire_range == 5 and moving_cost == 5 and regeneration_rate == 50 and length of the defense_cruisers list == 15
    create max cruisers
    add cruiser to attack_cruisers list

    for all the cruisers in attack_cruisers list
        attack the hub if it's possible
        move the cruiser towards the hub if the hub is not in its fire_range

    for cruiser in defense_cruisers list
        if an opponent cruiser is in its fire_range
            attack this cruiser

        for all the tankers in regeneration_tankers list

            if tanker available_energy different from its storage_capacity
                move tankers towards random peaks
                absorb the peak
            else
                move tanker to the hub
                transfer its energy to the hub

        end for

        for all the tankers not in regeneration_tankers list

            if the available energy of the tanker equals to its storage_capacity
                move tanker towards the cruiser which has the less available_energy
                transfer energy to the cruiser

            else
                move each tanker towards a differenet peak
                absorb energy from the peak

        end for
