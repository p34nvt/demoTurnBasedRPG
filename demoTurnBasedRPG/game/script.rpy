# Declare characters used by this game. The color argument colorizes the
# name of the character.
init python:
    character_colors = [
        "#FF0000",
        "#0000FF",
        "#008000",
        "#FFFF00",
        "#800080",
        "#FFA500"
    ]
    attacking = False

    # Define player and enemy statistics
    player_stats = {
        'HP': 100,
        'ATK': 15,
        'DEF': 50
    }

    enemy_stats = {
        'HP': 100,
        'ATK': 15,
        'DEF': 50
    }

    attack_dialogue = [
        "A bug like you is not worth my attention!",
        "I am like Invader Zim, a conqueror of planet Earth!"
    ]

    damage_dialogue = [
        "Grr! This cannot be happening...",
        "My invincibility cannot be challenged!"
    ]
    # Function to calculate damage
    def calculate_damage(attack, defense):
        bonus = renpy.random.randint(1,10)
        damage = (attack + bonus) - (defense + bonus)
        return damage
# Define the characteristics of each character such as their names, colors, and statistics.
define character1 = Character("Character 1", color=character_colors[0])
define character2 = Character("Character 2", color=character_colors[1])
define character3 = Character("Character 3", color=character_colors[2])
define character4 = Character("Character 4", color=character_colors[3])
define character5 = Character("Character 5", color=character_colors[4])
define character6 = Character("Character 6", color=character_colors[5])

image background_upper = Image("images/bugs.jpg", yalign=0)  # Background image for the upper half of the screen
image background_lower = "images/flowers.jpg"  # Background image for the lower half of the screen

# Define the screen structure for frame receiver
screen receiver(x_pos):
    frame:
        xalign x_pos
        yalign 0.05
        xsize 100
        ysize 10
        background Solid("ff0000aa")

# Define the screen structure for frame sender
screen sender(x_pos):
    frame:
        xalign x_pos
        yalign 0.5
        xsize 100
        ysize 10
        background Solid("#00ff00aa")

# Now let's define the turn-based combat system.
label start_battle:

    show background_upper
    show background_lower

    # TODO: Display the combat interface and the status of each character.

    "The battle begins!"

    menu:
        "Ready for battle?"
        "Attack":
            jump attack_sequence
        "Flee":
            "Coward!"
            jump end_battle

label attack_sequence:

    $ attacking = True

    $ characters = [character1, character2, character3, character4, character5, character6]

    $ attacker = renpy.random.choice(characters[-3:])
    $ target = renpy.random.choice([character for character in characters[:3] if character != attacker])
    if attacking:
        $ xreceiver = 0.25 * (characters.index(target) + 1)
        $ print("xreceiver " + str(xreceiver))
        show screen receiver(x_pos=xreceiver)

        $ xsender = 0.25 * (characters.index(attacker) - 2)
        $ print("xsender " + str(xsender))
        show screen sender(x_pos=xsender)
        
        $ attacking = False
    else:
        hide screen receiver
        hide screen sender

    if characters.index(attacker)>3:
        attacker "[attack_dialogue[0]]"
    else:
        attacker "[attack_dialogue[1]]"
    if characters.index(target)<3:
        target "[damage_dialogue[0]]"
    else:
        target "[damage_dialogue[1]]"
    
    "[attacker] attacks [target]!"

    # Here would go the code to handle the attack and calculate the damage.

    if player_stats['HP'] > 0 and enemy_stats['HP'] > 0:

        $ enemy_damage = calculate_damage(player_stats['ATK'], enemy_stats['DEF'])
        $ enemy_stats['HP'] += enemy_damage
        $ enemy_health = enemy_stats['HP']

        "You dealt [enemy_damage] points of damage to the enemy."
        "enemy is at [enemy_health] of health"

        $ player_damage = calculate_damage(enemy_stats['ATK'], player_stats['DEF'])
        $ player_stats['HP'] += player_damage
        $ player_health = player_stats['HP']

        "The enemy dealt [player_damage] points of damage to you."
        "your health at [player_health]"
    else:
        # Check if the battle has ended.
        if player_stats['HP'] <= 0:
            "You have been defeated."
            jump end_battle
        elif enemy_stats['HP'] <= 0:
            "You have defeated the enemy."
            jump end_battle

    jump start_battle

label end_battle:

    "El combate ha terminado."
    return

# The game starts here.

label start:

    call start_battle from _call_start_battle

    return
