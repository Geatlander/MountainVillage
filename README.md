# MountainVillage
A simple game made in Python 3 using the Livewires library.

In order to play, first install livewires by following the instructions at the web address listed
in the comments of the source code.

An idea for a mountain-climber game.
It uses the livewires package, a watered-down version of pygame, which can be installed with all the necessary packages here: https://github.com/livewires/python
If I were to refactor it now, I would separate it into different packages so that it is less jumbled into one file.
I would also make better utilization of abstract methods instead of typing stuff out over and over for subclasses.
CONTROLS:
1- builds a house
2- builds a church
3- builds a barracks
4- creates a lumberjack
5- creates a farmer
6- creates a mountain climber
OBJECTIVE:
Get a mountain climber to the top of the mountain without running out of food.
In order to do this, you will need to make a village.
Resources are represented on the left of the screen:
brown- wood
red- food
yellow- gold
white- population
grey- population capacity
Different buildings/units require different levels of resources. In order to create
a mountain climber, you must have a barracks, 50 food, 50 gold, and 50 wood.
Building a church decreases the chances that your mountain climber will die on his journey.

If you run out of money, all of your farmers will stop working because there is nothing left to pay them.

The buildings and units cost the following amounts:
    Farmer costs 10 food and 20 gold, 1 population
    Climber costs 50 food, 50 gold, 50 wood and 1 population
    Woodcutter costs 20 food and 1 population
    House: 50 wood
    Barracks: 230 wood, 230 gold, 100 food
    Church: 250 wood, 250 gold
    

![Alt text](../screenshots/mtn1.PNGraw=true "mtn1.PNG")

![Alt text](relative/path/to/img.jpg?raw=true "Title")


Hope you enjoy!
