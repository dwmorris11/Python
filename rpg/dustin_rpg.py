#!/usr/bin/python3

# Replace RPG starter project with this code when new instructions are live
def showInstructions():
  #print a main menu and the commands
  print('''
RPG Game
========
Commands:
  go [direction]
  get [item]
''')

def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Inventory : ' + str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom] and "inventory" in rooms[currentRoom]['item']:
    print('You see a ' + rooms[currentRoom]['item']['inventory'])
  elif "item" in rooms[currentRoom] and "trap" in rooms[currentRoom]['trap']:
    print(f"You have been killed by {rooms[currentRoom]['trap']}")
    exit(0)
  print("---------------------------")

def addToInventory(item):
  inventory += [item]
  #display a helpful message
  print(item + ' got!')
  #delete the item from the room
  del rooms[currentRoom]['item']['inventory']

#an inventory, which is initially empty
inventory = []

#a dictionary linking a room to other rooms
## A dictionary linking a room to other rooms
rooms = {

            'Hall' : {
                  'south' : 'Kitchen',
                  'east'  : 'Dining Room',
                  'west'  : 'Stairs',
                  'item'  : {'inventory': 'key'},
                },
            'Kitchen' : {
                  'north' : 'Hall',
                  'item'  : {'trap': 'monster'},
                },
            'Dining Room' : {
                  'west' : 'Hall',
                  'south': 'Garden',
                  'item' : {'inventory': 'potion'},
                  'north' : 'Pantry',
               },
            'Garden' : {
                  'north' : 'Dining Room',
                  'item' : {'trap': 'snake'},
               },
            'Pantry' : {
                  'south' : 'Dining Room',
                  'item' : {'inventory': 'cookie'},
               },
            'Stairs' : {
                  'up' : 'Upstairs Hall',
                'down' : 'Hall',
                'item' : {'inventory': 'creepy oil portrait'},
               },
            'Upstairs Hall' : {
              'north' : 'Stairs',
              'west'  : 'Attic',
              'south' : 'Master Bedroom',
              'east'  : 'Guest Bedroom',
              'item'  : {'inventory': 'urn'},
            },
            'Attic': {
              'east' : 'Upstaris Hall',
              'item' : {'trap': 'ghost'},
            },
            'Master Bedroom': {
              'north' : 'Upstairs Hall',
              'item' : {'inventory': 'gun'},
            },
            'Guest Bedroom' : {
              'west' : 'Upstairs Hall',
              'item' : {'trap' : 'seductress'},
            }
        }

#start the player in the Hall
currentRoom = 'Hall'

showInstructions()

#loop forever
while True:

  showStatus()

  #get the player's next 'move'
  #.split() breaks it up into an list array
  #eg typing 'go east' would give the list:
  #['go','east']
  move = ''
  while move == '':
    move = input('>')

  # split allows an items to have a space on them
  # get golden key is returned ["get", "golden key"]
  move = move.lower().split(" ", 1)

  #if they type 'go' first
  if move[0] == 'go':
    #check that they are allowed wherever they want to go
    if move[1] in rooms[currentRoom]:
      #set the current room to the new room
      currentRoom = rooms[currentRoom][move[1]]
    #there is no door (link) to the new room
    else:
        print('You can\'t go that way!')

  #if they type 'get' first
  if move[0] == 'get':
    #if the room contains an item, and the item is the one they want to get
    if "item" in rooms[currentRoom] and len(move)>1 and move[1] in rooms[currentRoom]['item']: #added to fix bug in original if a noun is not given
      #add the item to their inventory
      if(move[1].get('item').get('inventory')):  #item is an inventory item
        addToInventory(move[1].get('item').get('inventory'))
      elif(move[1].get('item').get('trap')):  #item is a trap
        print(f"You were killed by {move[1].get('item').get('trap')}!!!")
        exit(0)
    #otherwise, if the item isn't there to get
    else:
      if(len(move) <= 1):  #added to fix bug in orginal if a noun is not given
        print('Get what?')
      else:
        #tell them they can't get it
        print('Can\'t get ' + move[1] + '!')

  ## Define how a player can win
  if currentRoom == 'Garden' and 'key' in inventory and 'potion' in inventory:
    print('You escaped the house with the ultra rare key and magic potion... YOU WIN!')
    break

  ## If a player enters a room with a monster BUT HAS A COOKIE
  if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item'] and 'cookie' in inventory:
    print('The monster takes your cookie and runs away! Whew!')
    del rooms[currentRoom]['item']
    inventory.remove('cookie')

  ## If a player enters a room with a monster
  elif 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
    print('A monster has got you... GAME OVER!')
    break
