from room import Room
from player import Player
from item import Item
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", [Item("Key", "Opens stuff")]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", [Item("Book", "Read and be smart")]),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", [Item("Light", "Makes you see")]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", [Item("Stones", "A weapon?")]),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", [Item("Belt", "Holds up your trousers")]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

choices = ["n", "s", "w", "e"]
#
# Main
#

# Make a new player object that is currently in the 'outside' room.
# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
player = Player("Wanderer", room["outside"])


def get_input():
    user = input("> What shall thou do next:")
    user = user.split(" ")
    return user


def room_details(r):
    print("\n===============================================")
    print(f'You are currently in the {r.name}', end=': ')
    print(r.description)
    if len(r.items) == 0:
        print("No item in the room")
    else:
        print("You look around, and see: ", end="")
        for item in r.items:
            print(item, end=", ")

    print("\n===============================================")


def process_input(r, cmd):
    if len(cmd) == 1:
        val = cmd[0]
        if val == "q":
            print("Hope to see you again!")
            exit()

        if val in choices and r[f"{val}_to"] == None:
            print("**Map isn't that expensive yet, buy more DLCs, scrub!**")
            return

        if val == "inventory" or val == "i":
            if len(player.inventory):
                print("Your items are: ")
                for i in player.inventory:
                    print(i.name)
            else:
                print("You are broke broke")
            return

        if val == "h" or val == "help":
            print("COMMANDS: \nn ==> Go North\ns ==> Go South\nw ==> Go West\ne ==> Go East\nget ITEM_NAME ==> Pick up an item in a room\n\
drop ITEM_NAME ==> Drop an item in a room\ni ==> View your inventory\nq ==> Quit Game")
            return

        if val not in choices:
            print("Invalid input!. Enter \"h\" for help instructions")
            return

        player.current_room = r[f"{val}_to"]

        room_details(player.current_room)

    elif len(cmd) == 2:
        verb, item = cmd
        if(verb == "take" or verb == "get"):
            if(item in player.current_room.items):
                item_index = player.current_room.items.index(item)
                removed_item = player.current_room.items.pop(item_index)
                player.inventory.append(removed_item)
                removed_item.on_take()

            else:
                print("That item is not in the room")
        elif(verb == "drop"):
            if(item in player.inventory):
                item_index = player.inventory.index(item)
                removed_item = player.inventory.pop(item_index)
                player.current_room.items.append(removed_item)
                removed_item.on_drop()

            else:
                print("You dpo not have that item in your inventory")


print("Welcome warrior!")
room_details(player.current_room)
while True:
    inp = get_input()
    process_input(player.current_room, inp)
