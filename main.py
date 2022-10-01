# CINF 308 - Fall 2022 - Assignment 6
# Text adventure game
# John Logiudice

import random  # Random will be used for matters of chance
import time    # Time will be used for dramatic delays

# Check if string can be converted to an integer
def is_int(f_string):
    try:
        int(f_string)
        return True
    except ValueError:
        return False


# Get and confirm a Y of N answer
def get_yn():
    while True:
        # Convert response to lower case since case does not matter
        response = input("Please enter (Y)es or (N)o: ").lower()

        # Only check first letter in case player types Yes or No
        if response[0] in ('y', 'n'):
            return response


# Exits the game when play is over
def quit_game():
    print()
    print('Thanks for playing!')
    quit()


# Print the room menu and get player response
def room_menu(f_room, f_room_dict):
    this_room_feature = f_room_dict[f_room]['features']

    # iterate over and print each feature in the room to the menu
    for i in range(0, len(this_room_feature)):
        print(f"{i + 1}. {this_room_feature[i]}")

    # print general options
    print()
    print("I. for inventory")
    print("Q. to quit game")

    # loop until player chooses valid menu response
    while True:
        response = input("What would you like to look at (enter the number)? ")
        # Check that integer was entered
        if is_int(response):
            # Subtract 1 to match tuple index
            response = int(response) - 1
            # Return feature value
            if int(response) in range(0, len(this_room_feature)):
                return f_room_dict[f_room]['features'][response]
        # Player chose to quit
        elif response.lower() in ('q', 'quit'):
            quit_game()
        # Player wants to see Inventory
        elif response.lower() in ('i', 'inventory'):
            print_inventory()
        # Invalid choice
        else:
            print('Please enter a valid menu choice')


# Print item found in feature and ask if player wants to take it
def feature_menu(f_feature, f_feature_dict, f_item_dict):
    this_feature_item = f_item_dict[f_feature_dict[f_feature]['item']]

    # If item is not already found, ask player Y/N to take it
    if not this_feature_item['taken']:
        print(this_feature_item['description'])
        print(f"Would you like to take the {f_feature_dict[f_feature]['item']}?")
        response = get_yn()
        print()

        # Player chose to take item
        if response == 'y':
            this_feature_item['taken'] = 'True'
            print(f"You took the {f_feature_dict[f_feature]['item']}.")
            return f_feature_dict[f_feature]['item']
        # Player decided not to take item
        else:
            print(f"You left the {f_feature_dict[f_feature]['item']} where it is.")
            return None
    # player already found this item
    else:
        print(f"There is nothing to see in the {f_feature}.")
        return None


# Change the state of or walk through a door
def door_state(f_feature, f_feature_dict, f_room):
    this_feature = f_feature_dict[f_feature]

    print(f"The {this_feature['title']} is currently {this_feature['state']}")

    # If door is currently closed
    if this_feature['state'] == 'closed':
        print()
        print(f"Would you like to open the {this_feature['title']}?")
        response = get_yn()

        # Open the door
        if response == 'y':
            # Is door locked?
            if this_feature['locked']:
                # Player found key
                if unlock_door(this_feature):
                    print()
                    print(f"You unlock the {this_feature['title']} with the key.")
                    this_feature['state'] = 'open'
                    print(f"The {this_feature['title']} is now open")
                # Player did not find the key
                else:
                    print()
                    print(f"The {this_feature['title']} is locked. Do you have the key?")
            # Door was not locked
            else:
                print()
                this_feature['state'] = 'open'
                print(f"The {this_feature['title']} is now open")

    # If door is currently open, ask if Player wants to close it
    else:
        print()
        print(f"Would you like to close the {this_feature['title']}?")
        response = get_yn()

        # Player chose to close door
        if response == 'y':
            print()
            this_feature['state'] = 'closed'
            print(f"The {this_feature['title']} is now closed")

    # If the door is now in an open state, ask if player wants to walk through it
    if this_feature['state'] == 'open':
        print()
        print(f"Would you like to walk through the {this_feature['title']}?")
        response = get_yn()

        # Player chose to walk through door
        if response == 'y':
            # If reply is yes, call function to swap rooms
            f_room = leave_room(f_feature, f_feature_dict)

    # Return the current room
    return f_room


# Swap current room with next room according to the dictionary definition
def leave_room(f_feature, f_feature_dict):
    f_feature_dict[f_feature]['next_room'], f_feature_dict[f_feature]['curr_room'] = \
        f_feature_dict[f_feature]['curr_room'], f_feature_dict[f_feature]['next_room']
    return f_feature_dict[f_feature]['curr_room']


# Unlock a door if key in inventory
def unlock_door(f_this_feature):
    # Player found Key
    if 'key' in inventory_list:
        f_this_feature['locked'] = False
        return True
    # Player did not find key
    else:
        return False


# Print the current inventory of items carried
def print_inventory():
    print()
    print("You are carrying: ", end="")
    # If there are items in inventory
    if len(inventory_list) > 0:
        item_string = ""
        for item in inventory_list:
            item_string += item + ", "
        item_string = item_string.rstrip(" ").rstrip(",")
        print(item_string)
    # If there are no items in the inventory
    else:
        print("nothing")

# For features that are interactable
def feature_interact(f_feature, f_feature_dict):
    this_feature = f_feature_dict[f_feature]

    # Ship Controls
    if this_feature['title'] == 'ship controls':
        # Show avaliable action
        print(this_feature['action text'])
        print(f"Would you like to {this_feature['action']}?")
        response = get_yn()
        if response == 'y':
            start_engine(f_feature_dict)

    # Engine
    elif this_feature['title'] == 'engine':
        # Check if capacitor is already in engine
        if this_feature['equipped']:
            print("There is already a capacitor in the slot.")
        else:
            # Succeed or do not succeed inserting capacitor
            success = insert_capacitor(f_feature_dict)

            # If success is False, player did not equip gloves and will die
            if not success:
                # Show failure message
                print()
                time.sleep(2)
                print()
                print('       !!!!!!! zzzzZAPpppp !!!!!!!')
                print('I guess you should have listened to the warnings.')
                print('The moment you inserted the capacitor, two terawatts of electricity flowed')
                print('to the capacitor then through your hands straight through your heart and')
                print('other vital organs exiting from your feet into the hull of the ship.')
                print('Obviously you have expired and will be no help to the crew.')
                print('I wish you better luck in future adventures...')

                quit_game()

    # Radio
    elif this_feature['title'] == 'radio':
        print(this_feature['action text'])
        print(f"Would you like to {this_feature['action']}?")
        response = get_yn()
        # Player chose to use the radio
        if response == 'y':
            # Check if radio is not working
            if this_feature['fried']:
                print()
                print('Sorry, the radio appears to be out of commission.')
            # If radio is working
            else:
                # Chance that aliens intercept radio call and invade ship
                aliens_invade = call_earth()
                # The radio always breaks after one use
                this_feature['fried'] = True
                if aliens_invade:
                    # Print failure message
                    print()
                    print("- " * 25)
                    print()
                    print("You feel a strong vibration run through the ship.")
                    time.sleep(1)
                    print("The vibration grows stronger.")
                    time.sleep(1)
                    print("The sound of a metal tearing and a sudden jolt tells you something bad has happened.")
                    print("")
                    print("Ironically, with a damaged ship, you managed to complete your mission.")
                    print("Alien life forms from the planet Fligiborp orbiting Tau Ceti intercepted your radio call.")
                    print("It so happens that Fligiborp does have lifeforms and contains a perfect environment for Human life.")
                    print("Unfortunately for you and the ship's crew, the rest of your lives will be spent as forced labor")
                    print("in a Fligiborppian underground mining camp.")
                    print('I wish you better luck in future adventures...')
                    quit_game()
        # Player chose not to use Radio
        else:
            print("You can always try to call Earth later.")


# Print message from Earth and determine if aliens invade ship
def call_earth():
    print()
    print("You press the 911 button and wait for a response")
    time.sleep(2)
    print("You hear a crackle and then a voice:")
    print("  Earth here.")
    print("...crackle...")
    print("  We received telemetry that the ship hit an interstellar gas cloud.")
    print("  The engine hyperflux capacitor may have been damaged.")
    print("...hiss...")
    print("  Replace it if you can and try to restart the ship.")
    print()
    print("Before you can say anything, a small puff of white smoke rises from the radio.")

    # Calculate 60/40 chance that aliens invade the ship after using the radio
    chance = random.randint(0, 100)
    if chance > 60:
        # Aliens invade
        return True
    else:
        # Aliens do not invade
        return False


# Attempt to start engine and print success or failure message
def start_engine(f_feature_dict):
    print()
    # Player equipped the engine with a capacitor
    if f_feature_dict['engine']['equipped']:
        print("You press the Autopilot button.")
        time.sleep(2.0)
        print()
        # Check if engine explodes or not
        if ship_explode(f_feature_dict):
            # Engine explodes failure message
            print('       !!!!!!! KABLAM !!!!!!!')
            print('The old capacitor must have been damaged.')
            print('The ship and its entire crew have perished.')
            print('I wish you better luck in future adventures...')
            quit_game()
        else:
            # Engine does not explode
            print("The engines groan a little and then whir back to life!")
            print("Excellent job saving the crew and continuing the mission!")
            quit_game()

    # Player has not equipped the engine with a capacitor
    else:
        print("Nothing happens. Maybe you should check the Engine Room.")


# Check if player is wearing gloves and which capacitor to install
def insert_capacitor(f_feature_dict):
    # Initialize success as True
    success = True

    # If player has not equipped the gloves
    if not item_dict['gloves']['equipped']:
        # Warning message
        print("Working on electrical equipment could be dangerous.")
        print("There may be safety precautions to think of before proceeding.")
        print("Do you still want to work on the engine?")
        response = get_yn()

        # Player decided not ignore warning - Guaranteed failure
        if response == 'y':
            success = False

        # Player heeded warning and found gloves so puts them on
        else:
            print()
            print('That is a good decision.')
            equip_gloves()
            return True

    # Player has equipped the gloves
    print()
    # If player found both capacitors, ask which to equip in engine
    if 'new capacitor' in inventory_list and 'old capacitor' in inventory_list:
        print("You are carrying the old capacitor and the new capacitor.")
        print()
        print("1. Old Capacitor")
        print("2. New Capacitor")
        # Loop until valid choice
        while True:
            # Ask user which capacitor to insert
            response = input("Which would you like to insert? ")
            if is_int(response):
                response = int(response)
                if response == 1:
                    equip_capacitor(f_feature_dict, 'old capacitor')
                    break
                elif response == 2:
                    equip_capacitor(f_feature_dict, 'new capacitor')
                    break
            print("Please enter 1 or 2.")

    # Player only found old capacitor
    elif 'old capacitor' in inventory_list:
        print("You are carrying the old capacitor.")
        print("Would you like to insert it?")
        response = get_yn()
        if response == 'y':
            equip_capacitor(f_feature_dict, 'old capacitor')
        else:
            print("You are still carrying the old capacitor.")

    # Player only found new capacitor
    elif 'new capacitor' in inventory_list:
        print("You are carrying the new capacitor.")
        print("Would you like to insert it?")
        response = get_yn()
        if response == 'y':
            equip_capacitor(f_feature_dict, 'new capacitor')
        else:
            print("You are still carrying the old capacitor.")

    # Player found neither capacitor
    else:
        print('You do not have a capacitor to insert.')
        # Success is still True since ship did not explode
        success = True

    return success


# Update dictionary with capacitor inserted
def equip_capacitor(f_feature_dict, capacitor_type):
    inventory_list.remove(capacitor_type)
    f_feature_dict['engine']['equipped'] = capacitor_type
    print()
    print(f"You are no longer carrying the {capacitor_type}.")


# Update dictionary with gloves equipped
def equip_gloves():
    this_item = item_dict['gloves']

    # If the player did not find the gloves
    if not this_item['taken']:
        print("Maybe there are electrician's gloves hidden somewhere on this ship.")

    # If the player did find the gloves
    else:
        print("You smartly put the rubber gloves on your hands")
        this_item['equipped'] = True


# Determine if the ship explodes
def ship_explode(f_feature_dict):
    this_feature = f_feature_dict['engine']
    # If new capacitor is used, there is no explosion
    if this_feature['equipped'] == 'new capacitor':
        return False
    else:
        # If old capacitor is used
        # Use random to select a number, where > 80 means ship explodes
        chance = random.randint(0, 100)
        if chance >= 80:
            return True
        else:
            return False



# Main

# Initialize inventory
inventory_list = []

# Set the starting room
room = 'quarters'

# Describes features available in each room
room_dict = {}
room_dict['quarters'] = {'features': ('quarters', 'bed', 'table', 'grey door'),
                         'title': 'your quarters'}
room_dict['hall'] = {'features': ('hall', 'plant', 'grey door', 'blue door', 'red door'),
                     'title': 'the hall'}
room_dict['helm'] = {'features': ('helm', 'blue door', 'ship controls', 'radio'),
                     'title': 'the helm'}
room_dict['engine room'] = {'features': ('engine room', 'engine', 'cabinet', 'floor', 'red door'),
                            'title': 'the engine room'}

# Describes the details and state of all features
feature_dict = {}
feature_dict['quarters'] = {'type': 'room',
                            'description': "You are in your quarters, a tiny space with just enough room for a table and bed.\n"
                                           "The bed is a mess of ruffled sheets and a pillow.\n"
                                           "There is a grey door which is closed.\n"}
feature_dict['hall'] = {'type': 'room',
                        'description': "This is a sterile looking white hallway with a black and grey tiled floor.\n"
                                       "There are three doors colored grey, blue, and red.\n"
                                       "Oddly, there is a well cared for potted plant in the corner.\n"
                                       "Someone must have a green thumb."
                        }
feature_dict['helm'] = {'type': 'room',
                        'description': "The helm is where the captain and crew navigate and operate the ship.\n"
                                       "You see the captain and crew are lying unconscious on the floor.\n"
                                       "Maybe there was an impact or explosion?\n"
                                       "There is the blue door that you entered from.\n"
                                       "The ship control station is where the helmsman 'flies' the ship."}
feature_dict['engine room'] = {'type': 'room',
                               'description': "The engine room is lined with wires and pipes.\n"
                                              "While you are not an engineer, you have some rudimentary knowledge of the engine systems.\n"
                                              "Interstellar Drive is electrically powered by a sealed nuclear fusion battery.\n"
                                              "You can see the hyperflux capacitor is missing from the engine.\n"
                                              "You think to yourself, 'We are not moving without the capacitor in place...'\n"
                                              "'Can I fix this?'"}
feature_dict['plant'] = {'type': 'object',
                         'item': 'key',
                         'description': "The plant is a happy rubber tree in a wicker basket."}
feature_dict['bed'] = {'type': 'object',
                       'item': 'gloves',
                       'description': "The bed is a mess of ruffled sheets with a thin pillow."}
feature_dict['table'] = {'type': 'object',
                         'description': "This is a simple metal table."}
feature_dict['ship controls'] = {'type': 'interact',
                                 'title': 'ship controls',
                                 'action text': "The ship's control panel has a flashing button labeled 'Resume Autopilot'",
                                 'action': 'press autopilot',
                                 'requires': 'capacitor',
                                 'description': "This is where the helmsman 'flies' the ship."}
feature_dict['engine'] = {'type': 'interact',
                          'title': 'engine',
                          'equipped': None,
                          'action text': "There is an empty capacitor slot.",
                          'action': 'insert a capacitor',
                          'description': "The engine appears to be in good shape."}
feature_dict['radio'] = {'type': 'interact',
                         'title': 'radio',
                         'action text': "You can try to call for help.",
                         'action': 'call Earth',
                         'fried': False,
                         'description': "The radio uses a subspace quantum tunnel to communicate with Earth at greater than lightspeed."}
feature_dict['cabinet'] = {'type': 'object',
                           'item': 'new capacitor',
                           'description': "This is spare parts cabinet"}
feature_dict['floor'] = {'type': 'object',
                         'item': 'old capacitor',
                         'description': "It's a floor."}
feature_dict['grey door'] = {'type': 'door',
                             'title': 'grey door',
                             'state': 'closed',
                             'locked': False,
                             'curr_room': 'quarters',
                             'next_room': 'hall',
                             'description': "The door is an ordinary door."}
feature_dict['blue door'] = {'type': 'door',
                             'title': 'blue door',
                             'state': 'closed',
                             'locked': False,
                             'curr_room': 'hall',
                             'next_room': 'helm',
                             'description': "The door is an ordinary door."}
feature_dict['red door'] = {'type': 'door',
                            'title': 'red door',
                            'state': 'closed',
                            'locked': True,
                            'curr_room': 'hall',
                            'next_room': 'engine room',
                            'description': "The door is an ordinary door."}

# Describes the details and state of all findable items
item_dict = {}
item_dict['key'] = {'taken': False,
                    'description': "There is a shiny piece of metal. It looks like a key."}
item_dict['gloves'] = {'taken': False,
                       'equipped': False,
                       'description': "There is a pair of heavy canvas gloves with a thick rubber coating."}
item_dict['old capacitor'] = {'taken': False,
                              'description': "There is the fallen capacitor. It looks alright. Maybe you should reinsert it in the engine?"}
item_dict['new capacitor'] = {'taken': False,
                              'description': "There is a capacitor that looks a lot like the one that fell from the engine."}

# Welcome Message
title = " * * * * * * * Space Adventure * * * * * * *"
welcome_message = "You are a crew member of a spaceship travelling to Tau Ceti, a star 12 light-years from Earth.\n" \
                  "The mission is to investigate the planets around Tau Ceti to determine if life exists there and\n" \
                  "if they are capable of supporting human life. After an evening spent in the ship’s tavern, you\n" \
                  "return to your quarters and immediately fall into a deep sleep.\n"\
                  "A sudden jolt wakes you up.\n" \
                  "You feel the vibration of the engines slow, then stop.\n" \
                  "You are alone in your dimly lit room."

print(title)
print(welcome_message)
print(" -" * 23)

# Main loop to call functions until game ends or player quits
while True:
    print()
    # Room title
    print(f"You are in {room_dict[room]['title']}.")
    print()
    # Menu items
    print('- - - - MENU - - - -')
    feature = room_menu(room, room_dict)

    # Feature description
    print()
    print(feature_dict[feature]['description'])
    print()
    # If this feature has items to find
    if 'item' in list(feature_dict[feature]):
        item = feature_menu(feature, feature_dict, item_dict)
        # If player picked up an item, add it to the inventory
        if item is not None:
            inventory_list.append(item)

    # If the player can interact with the item
    if feature_dict[feature]['type'] == 'interact':
        feature_interact(feature, feature_dict)

    # If this feature is a door
    if feature_dict[feature]['type'] == 'door':
        room = door_state(feature, feature_dict, room)
