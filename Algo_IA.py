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

while regeneration_rate < 50:
    create tanker
    if turn is pair:
        add tanker to attack_tankers
    else:
        add tanker to refuel_tankers
    for tanker in entities:
        move tankers towards different peaks
        for peaks in entities:
            if distance between tanker and peak <= 1:
                absorb energy from the peak
        end for
        if distance between tanker and hub <= 1:
            transfer all the energy from the tanker to the hub
    end for
    upgrade regeneration_rate of the hub
    turn += 1
end while

while moving_cost > 5 and regeneration rate == 50:
    create cruiser
    add cruiser to attack_cruisers
    for tanker in refuel_tankers:
        if tanker available_energy > 0:
            move tanker towards hub
            if distance between tanker and hub <= 1:
                transfer all the energy from the tanker to the hub
        else:
            move tanker towards different peaks
ohhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
            if distance between tanker and peak <= 1:
                absorb energy from the peak
            
    elif entity is a cruiser:
        move cruiser towards the opponent but on a case where there is no other cruiser from our team
