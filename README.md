# README
# Preview
![image](https://user-images.githubusercontent.com/71220864/216835217-8636268b-f2f0-434b-a6ff-3e8babee4238.png)

![image](https://user-images.githubusercontent.com/71220864/216835225-5d4cbeb5-3f4a-4940-a7ef-80f4e9eba95c.png)

![image](https://user-images.githubusercontent.com/71220864/216835233-f55ae3a3-4443-4322-b24c-4296ae4361c8.png)

![image](https://user-images.githubusercontent.com/71220864/216835244-ab9a6700-30ef-41f7-9982-e3c3a06ed163.png)

![image](https://user-images.githubusercontent.com/71220864/216835253-d1ec774f-55db-42fd-95e2-3a8c2084a448.png)

![image](https://user-images.githubusercontent.com/71220864/216835264-3f9aa0fe-dd50-476a-b928-6679b5dc181c.png)


# OOPS Concepts
 ## Abstraction
  ### Barbarians
   - We use functions to abstract complicated behavior for barbarians
   - Since most of their behavior is automated, once a condition is satisfied, a function is called
   - To keep the code modular, we use the same attack mechanics for the barbarians as well as the king but with a different trigger condition, cooldown period and attack stats such as range and damage
   - use_attack() check for collision of the attack range rectangle with the building list and deals damage if the attack sequence is in effect
   - choose_target_and_move() chooses the closest building and returns dx and dy, the change in x and y coordinates in the required direction based on movement speed and direction
   - update() this calls the required functions and maintains loop order

  ### King
   - King uses Functions that are exactly the same as the barbarians to allow for easy changes to code, this also allows the same code to be reused, even the parametre names are the same which allows a simple copy pasting of the functions
   - use_attack() - uses the barbarian sword attack, cooldown, range and damage are customizable
   - use_leviathan_axe() uses the leviathan axe aoe attack to deal damage to surrounding structure, range is double of barbarian sword in x and y direction and also in -x and -y direction
   - animate() - handles king's animations
   - spawn_barb() - spawns a barbarian at the given coordinates
   - update() -  this registers the keys hit as well as the necessary changes to the game, note that the class is called Player and not king, with the same update function, you can customize the player to be anything, a couple of other details will be mentioned later
   - The update function gives complete control of the game to the player, this means that we dont have to make any changes to the main game loop and we simply need to call player.update(), this also allows customization for a two player cooperative game with just one extra player object being added, also, you'll have to change the key bindings for the second player.

  ### General 
   - Each class has an update method, show method and for the inheritors of the Sprite class, a draw method
   - To reflect all necessary updates to an object, only the update function needs to be called, this function in turn calls several other functions which have been abstracted for easy usage 
   - Groups - each class is appended to its required group, in the main game loop, we simply call the update on the group as a whole, this will update every object inside the group
   - Sprite super class - this contains the basic update and draw functions, the group.update() functions calls the update of each individual sprite in the group
   - The group has add and remove features to add or remove sprites 
   - It maintains a list of sprites currently in the game, only these sprites are rendered. Rest are considered dead or on standby
   - different types of buildings such as townhall, wall, turret can all be added to the same building_group()


 ## Polymorphism
  ### Compile time polymorphism
   - This is not supported by python
   - Here you basically have the same function but with different types of arguments like int, float, string etc. for the same function name, python only allows one function with a given name so this doesn't work
   - It isn't even that useful in python since you don't really have any types for variables, you can simply pass an array of arguments
  ### Run time Polymorphism
   - We use this
   #### Spells
   - We have a class called Spell, there are two subclasses called Heal_Spell and Rage_Spell, with the same init function but different update functions, the update function is overriden by the changes required, the factor and the attribute to which the spell is applied determines its effects
   #### Sprites
   - Sprites have an update function, draw function and spritecollide function which checks collision of a rectangle with a group
   - It also contains an Inner Class called Group which stores multiple entities with similar updates
   - A class inheriting the sprite class can override its update function and have a custom init function 
   - This allows the same sprite class to be used for barbarians, buildings, walls and everything else in the game

 ## Inheritance
  ### Sprites
   - Building class, Barbarian class, Wall class, Bullet class, Turret class and a couple of others, all use the same Sprite super class.
   - This class allows for easy updates - a custom function for every class, spritecollide - a function used everywhere to check collision with a group of objects (may be same or different), draw function - that draws an object on to the screen
   - Group inner class -  this stores objects as a group, each object of this inner class uses both update and draw functions of the Sprite class on an entire group of objects, this also allows easy additions and removal of sprites from the game\
  ### Buildings 
   - Building class - we use a parametre called img to choose the display for every building, so you can have different building derived from the same building class, you can use randomized colors by using the color parameter which is optional, the default color being white 
   - Couple of other details are top secret, this is enough for inheritance
  ### Barbarians
   - Are also derived from the sprite class
  ### Bullets
   - derived from sprite class
  ### Turret
   - derived from sprite class, part of the building group so they behave almost like a building but slightly different cause its a building that can fire.   

 ## Encapsulation
  - We used objects and classes for everything so that covers encapsulation as well

# Game 
 ## Controls
  - <kbd>W</kbd>: move up
  - <kbd>D</kbd>: move right
  - <kbd>A</kbd>: move left
  - <kbd>S</kbd>: move down
  - <kbd>SPACE</kbd>: use Barbarian sword
  - <kbd>X</kbd>: use leviathan axe
  - <kbd>1</kbd>: spawn a barbarian at spawn point 1 - leftmost spawn point
  - <kbd>2</kbd>: spawn a barbarian at spawn point 2 - middle spawn point
  - <kbd>3</kbd>: spawn a barbarian at spawn point 3 - rightmost spawn point
  - <kbd>4</kbd>: spawn an archer at spawn point 1 - leftmost spawn point
  - <kbd>5</kbd>: spawn an archer at spawn point 2 - middle spawn point
  - <kbd>6</kbd>: spawn an archer at spawn point 3 - rightmost spawn point
  - <kbd>7</kbd>: spawn a balloon at spawn point 1 - leftmost spawn point
  - <kbd>8</kbd>: spawn a balloon at spawn point 2 - middle spawn point
  - <kbd>9</kbd>: spawn a balloon at spawn point 3 - rightmost spawn point
  - <kbd>O</kbd>: use Rage Spell
  - <kbd>P</kbd>: use Healing Spell

 ## Gameplay
  ## Barbarian King
   - The king is a slow and heavy unit, his barbarian sword is a heavy attack but only deals damage infront of the king with a limited range, use this attack to attack turrets and the town hall, this attack is bad for destroying walls
   - The king can use his leviathan axe to destroy anything in a 6 tile radius around him, this includes front, back, up and down. This is a lighter attack and is best suited for destroying walls and a cluster of houses
   - You can support you troops by casting spells and spawning more troops even after the king dies, just like in the real clash of clans game.
  ## Archer Queen
   - The queen is a slow and heavy unit, her cuckoo attack is a light attack that deals an aoe damage in the direction of last movement of the queer with a limited range, use this attack to attack turrets and the town hall
   - The queen's attacks are not for destroying walls. use her to provide long range support to your troops and after they breach the walls, you can join in the fight
   - The queer (i misspelled on purpose) can use her eagle arrow to destroy anything in a large radius around the point of impact of the arrow. This is a lighter attack and is best suited for destroying walls and a cluster of houses/turrets.
   - You can support you troops by casting spells and spawning more troops even after the queen dies, just like in the real clash of clans  game.
  ## Barbarians 
   - The barbarians are savages, they're quite slow and weak individually but when under the effect of the rage spell they become faster and stronger.
   - A hoarde of barbarians, with or without the rage spell, is a fearsome force. These can be used to breach walls and draw cannon fire away from the king. However, you only have seven barbarians (customizable), so if you spawn them such that they draw fire from both the turrets, they'll be decimated before they can even reach the walls
   - They detect the closest building to their spawn point and attack there, destroying any walls in their way.
  ## Archers
   - The archers are your only long range unit with magic arrows, the archers move towards the closest building and when in range, they stop and start attacking. Once an arrow is launched, it is sure to hit a target, after its initial target is destroyed, it will pick a new target and attack there as long as it is within its detect radius. Otherwise, the arrow will perish.
   - A hoarde of archers is a bad idea as wizard towers can almost one shot them.
   - Use your archers to support your troops from a distance.
  # Balloons
   - This is your only aerial unit.
   - This is a literal hot air balloon. After you figured that hot air rises over cold air, you used a large tarp and lit a burner under it to make your troops fly. 
   - These specifically target the defense systems, however while moving they deal a little damage to other buildings in their way by dropping stones, oil and other objects on them. 
   - After destroying all the defenses, they will target the houses to kill the civillians. The balloons don't spare the women or the children either.
   - Although the balloon allows you to fly, because you are a barbarian and lack technology, the balloons are really fragile, avoid stacking them near wizard towers.
   - Use them to attack the turrets while you take out the wizard towers with your infantry.
  ## Spawn points
   - The spawn points are located and the three pressure points of the village
   - A proper stratergy with support from the king in the form of spells and attacks is essential to destroy the village with the limited number of barbarians
   - The spawn points are located such that each of the barbarians will draw fire from the turrets upon being spawned, if you send them one at a time, they will die before they even reach the walls
  ## Spells
   - Use the rage spell to double troop and king damage and speed -  this only affects the troops currently fighting and not those on standby, use this as a hint to decide when to use the spell
   - Use the heal spell to heal all units and the king, like the rage spell it only affects the units currently engaged in battle and not the ones on standby, use it carefully
   - Any more hints will make the game boring, i know cause i made it
  ## Turrets
   - These fire magic bullets that will follow you as long as you are in their range, with the default speed of the king, it is impossible to dodge them.
   - When attacking a building the barbarians move up and down to show that they are attacking it, this also helps them to slow down and (rarely) even dodge an incoming shell for a short duration, this helps to deal a critical blow to the village
   - Turrets have a fixed rate of fire which can be customized
   ## Turrets
   - These attack anything that moves with lethal intent towards your city.
   - These fire magic bullets that will follow you as long as you are in their range, with the default speed of the king, it is impossible to dodge them.
   - When attacking a building the barbarians move up and down to show that they are attacking it, this also helps them to slow down and (rarely) even dodge an incoming shell for a short duration, this helps to deal a critical blow to the village
   - Turrets have a fixed rate of fire which can be customized
  ## Buildings
   - Including the turrets, there are a lot of buildings now, destroy all of them without dying to win the game
  ## Victory and defeat
   - You are defeated when all your barbarians, archers and balloons (7 of each) (on standby and in battle) along with your king are dead.
   - You win when you destroy all the buildings before you lose, if the last barbarian dies and destroys a building at the same time, you might still lose
  ## Infinite scroll in x direction
   - You can travel as far as you want with this screen
   - I've used unbreakable blocks to limit the travel area and intensify the gameplay but without it you can travel as far as you want, forever!
   - You can place buildings on the grid, anywhere, your game is not restricted to a small screen, you can move and the screen will move with you when you hit the edge
  ## Forest
   - There is a forest at the edge of this world
   - You can hide there and plan your next attack
  ## Stats
   - You can monitor the current status of the game using the stats bar at the bottom of the screen
   - It tells you if you're winning or losing or if you're just hiding in the forest
   - It doesn't tell you if youre hiding in the forest, but it could for an extra $20  



# Additional Features
 ## Bonus
  - Leviathan ace (10 marks)
  - Character animations (the king moves and changes direction, he also is animated when walking)
  - Forest (hide in a forest like a thug)
  - Clouds (clouds are things in the sky)
  - Ground block (what you walk on)
  - Good looking buildings (european style castles and stuff)
  - Game skins (discussed later, for marketing purposes)
  - actually see the archers shooting
  - Queen's Eagle Arrow attack done
  - Total for 15 marks   
 ## Game library
  - I have created a custom game library based on pygame without using any additional libraries
  - This library supports ascii art games
  - The files sprite.py, image.py, screen.py are part of this library
 ## Screen 
  - The screen is cleared and generated every frame
  - To render an object onto the screen, you only need to pass the img of the object and its rectange to the screen.blit() function just like pygame
  - Call the screen.display() function to display all the objects currently on screen
 ## Image library
  - This allows you to easily color and animate ascii art
  - You can change the appearance of any character by simply loading it as an image ( see ImageLoader.py for details)
  - You can use foreground_color(to apply a custom color), invert_y to flip the character along the y axis to change its direction etc. This allows for easy animations to ascii art.
  - The invert Y can invert most ascii art automatically
 ## Custom skins
  - You can buy skins for you characters
  - jk you get them for free
  - To change the way you character looks, simple copy paste you favourite ascii art into the image loader file and import it, then instead of supplying the totoro image used, suppy the image that you imported
  - Check config.py to change the color of the game
  - You can make the king a tank, helicopter, even a building
  - You can change the barbarians, buildings, turrets, walls, even if the size changes, it'll make no difference
 ## Customizability
  - The image library, screen and Sprite.py allow you to create any game very easily
  - You can customize literally everything in this game with just a couple of lines of code
 ## Modularity
  - The code is extremely modular
  - The world generation is automated using loops, the layout can be changed at any time, check worldgen.py for details, you can add multiple turrets by just changing the array indices, you can make the game world as large as you want since we have infinite scroll
  - You can load a new "level" by keeping the world data in prestored arrays and simply swaping them out depending on the level
  - You can even store it in files so that you dont have to construct them every time   
  - Some other things i dont remember
 ## Some other stuff
  - There are some other things i dont remember, ask during the evals


    

# Notes
 - We use 256 bit color set
 - In case you terminal doesn't support it, ask me to demo it
 - Use a big screen, since the layout of the village requires atleast 50 to 60 columns

# How to run
 ## Normal Game
  - run python3 game.py to play
 ## Replay
  - to replay a game run python3 game.py replays/< replay name>.txt
  - This means that you have to pass it as command line argument
  - replay stored as a unique file based on game start time
  - replays are timed, so if you were sitting idle, the replay will be such
  - You can hide in the forest in the replay as well
  - If you supply a wrong name, it'll simply start the game in normal mode
 ## Game controls are with the player
  - The replay, kbhit etc are in the player class, this is so that no changes are made to the main game loop
  - player stores the information in the file for you since you are the player and you have to remember what you did.
  - It makes no difference, idk y i mentioned it
