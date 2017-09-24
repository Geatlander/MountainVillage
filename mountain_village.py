# mountain village program

""" Jason Cox- February 2017
My First big python project

An idea for a mountain-climber game.
It uses the livewires package, a watered-down version of pygame.
It can be installed with all the necessary packages here: https://github.com/livewires/python

If I were to refactor it now, I would separate it into different packages so that it is less jumbled into one file.
I would also make better utilization of abstract methods instead of typing stuff out over and over for subclasses.

CONTROLS FOR GAME:

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

Hope you enjoy!
"""

import random, threading, time
from livewires import games, color

games.init(screen_width = 1920, screen_height = 1080, fps = 50)

class Game(object):
    pres = ["Weiss", "Ham", "Ober", "Eich", "Andels", "Wach"]
    suff = ["berg", "dorn", "swil", "stein", "wald", "wier", "haft"]
    VILLAGE_NAME = str(random.choice(pres) + random.choice(suff))
    # Randomely chosen village name based off of German fixes for fun :)
    
    
    def __init__(self, name = VILLAGE_NAME):
        #initializes game, sets resources, adds mountain to screen

        self.name_label = games.Text(value = "Your Village: " + str(name),
                                size = 100,
                                color = color.dark_gray,
                                top = 15,
                                right = games.screen.width - 100)
        
        buff = 90
        self.wood = games.Text(value = 200,
                                        size = 75,
                                        color = color.brown,
                                        top = 15, left = 50)
        self.food = games.Text(value = 200,
                                        size = 75,
                                        color = color.red,
                                        top = 15 + buff, left = 50)
        self.gold = games.Text(value = 200,
                                        size = 75,
                                        color = color.yellow,
                                        top = 15 + (2*buff), left = 50)
        self.pop = games.Text(value = 0,
                                        size = 75,
                                        color = color.white,
                                        top = 15 + (3* buff), left = 50)
        self.housing = games.Text(value = 0,
                                        size = 75,
                                        color = color.light_gray,
                                        top = 15 + (4*buff), left = 50)

        self.instructions = games.Message(value = "1-House, 2-Church, 3-Barracks, 4-Woodcutter, 5-Farmer, 6-Mountain Climber",
                                            size = 75,
                                            color = color.red,
                                            y = games.screen.height/2,
                                            x = games.screen.width/2, lifetime = 3 * games.screen.fps)

        labels = [self.name_label, self.wood, self.food, self.gold, self.pop, self.housing]

        for label in labels:
            games.screen.add(label)
        

    
        self.victory = 0    
        self.mountain_image = games.load_image("village_images/bmp/Mountain.png")
        self.the_mountain = Mountain(game = self, x = games.screen.width/2, y = games.screen.height/2, m_image = self.mountain_image)
        games.screen.add(self.the_mountain)
        
        #Creates the builder object for the game
        self.builder = Builder(game = self)
        #Puts the trees on the screen
        self.treelist = self.builder.tree_construct(random.randint(10, 20))





        class myThread(threading.Thread):
            """ Class for a separate thread that
            listens for keypresses while the main thread of the game runs."""

            def __init__(self, builder, countdown):
                threading.Thread.__init__(self)
                self.builder = builder
                self.countdown = countdown
                self.gameover = False
            def run(self):
                while not self.gameover:
                    self.countdown = self.builder.update(countdown = self.countdown)
                    time.sleep(self.countdown)
                    if self.countdown != 0:
                        self.countdown -= 0.5
           
            def set_gameover(self, value):
                self.gameover = value
                
        self.thread1 = myThread(builder= self.builder, countdown = 0.5)
        self.thread1.daemon = True
        self.thread1.start()    

    def add_instructions(self):
        games.screen.add(self.instructions)


    #Checks if the population is zero and food is zero so that the game can end.
    def everybody_dead(self):
        if (self.food.value <= 0 and self.pop.value == 0) or (self.gold.value <= 0 and self.pop.value == 0):
            self.end(1)
            return True
        elif (self.wood.value <= 0 and self.housing.value <= 0):
            self.end(3)
            return True
    


    def play(self):
        background_image = games.load_image("village_images/bmp/grassy.png", transparent = True)
        games.screen.background = background_image
        games.screen.mainloop()

    def change_resource(self, resource, amount):
        resource.value += amount
        if int(resource.value) < 100:
            resource.size = 90
            if int(resource.value) < 10:
                resource.size = 100
        else:
            resource.size = 75


    def get_treelist(self):
        return self.treelist

    # Displays a message depending on if the player won or not, exiting the game shortly afterwards.
    def end(self, victory):
        if victory == 2:
            display_value = "Du Hast Gewonnen! (You Won!)"
        elif victory == 1:
            display_value = "Spiel ist aus (Game Over)"
        elif victory == 3:
            display_value = "Patt (Stalemate)"
        
        endlabel = games.Message(value = display_value, size = 150, x = games.screen.width/2, y = games.screen.height/2, color = color.red,
                                 lifetime = 3 * games.screen.fps, after_death = self.end_thread_game, is_collideable = False) 
        
        games.screen.add(endlabel)
        self.victory = victory

    def end_thread_game(self, value = True):
        games.screen.quit()
        self.thread1.set_gameover(value)






class Builder(object):
    """ builder class to build all objects"""
    def __init__(self, game):
        self.game = game
        self.hammer = games.load_sound("village_sounds/hammer.wav")
        self.starting_haus = None
        self.starting_barracks = None
        self.starting_church = None            

    def rejection(self):
        
        rejection_message = games.Message(value = "You cannot build that", size = 70,
                                    x = games.mouse.get_x(), y = games.mouse.get_y(),
                                    is_collideable = False,
                                    lifetime = 1 * games.screen.fps, color = color.red)
        games.screen.add(rejection_message)





    def update(self, countdown):
        """ Listens for keypresses and builds an object if there are enough resources"""
        if games.keyboard.is_pressed(games.K_1) and countdown == 0:
            if Haus.enough_resources(self.game):        
                self.starting_haus = Haus.build(gameobj = self.game)
                self.hammer.play()
            else:
                self.rejection()
            countdown = 0.5 

        elif games.keyboard.is_pressed(games.K_2) and countdown == 0:
            if Church.enough_resources(self.game):
                self.starting_church = Church.build(gameobj = self.game)
                self.hammer.play()
            else:
                self.rejection()
            countdown = 0.5

        elif games.keyboard.is_pressed(games.K_3) and countdown == 0:
            if Barracks.enough_resources(self.game):
                self.starting_barracks = Barracks.build(gameobj = self.game)
                self.hammer.play()
            else:
                self.rejection()
            countdown = 0.5
        elif games.keyboard.is_pressed(games.K_4) and countdown == 0:
            Lumberjack.build(gameobj = self.game, starting_haus = self.starting_haus)
            countdown = 0.5
        elif games.keyboard.is_pressed(games.K_5) and countdown == 0:
            Farmer.build(gameobj = self.game, starting_haus = self.starting_haus)
            countdown = 0.5
        elif games.keyboard.is_pressed(games.K_6) and countdown == 0:
            Climber.build(gameobj = self.game, starting_barracks = self.starting_barracks, starting_church = self.starting_church)
            countdown = 0.5
        elif games.keyboard.is_pressed(games.K_i) and countdown == 0:
            self.game.add_instructions()
            countdown = 0.5

        #check for everybody dead
        if countdown == 0:
            if self.game.everybody_dead():
                countdown = 10
    



        
        return countdown
  
  
    def tree_construct(self, x):
        trees = []
        for i in range(x):
            tree = Tree.build(gameobj = self.game)
            trees.append(tree)
        return trees
              
            


class Mountain(games.Sprite):
    """mountain in the center of the screen"""
    def __init__(self, x, y, game, m_image):
        super(Mountain, self).__init__(x = x, y = y, image = m_image)
        self.game = game




class Building(games.Sprite):
    def __init__(self, image, game, is_collideable = True):
        super(Building, self).__init__(image = image)
        self.game = game

class Haus(Building):
    def __init__(self, image, game, is_collideable = True):
        super(Haus, self).__init__(image = image, game = game)
        self.x = 0
        self.y = 0

    @staticmethod
    def enough_resources(game):
        if game.wood.value >=50:
            game.change_resource(game.wood, -50)
            game.change_resource(game.housing, 2)
            return True
        else:
            return False
       
    @staticmethod
    def build(gameobj):

        x = games.mouse.get_x()
        y = games.mouse.get_y()
        haus_image = games.load_image("village_images/bmp/house.png")
        new_haus = Haus(image = haus_image, game = gameobj)
        new_haus.x = x
        new_haus.y = y
        games.screen.add(new_haus)
        return new_haus


class Church(Building):
    def __init__(self, image, game):
        super(Church, self).__init__(image = image, game = game)
        self.x = 0
        self.y = 0

    @staticmethod
    def enough_resources(game):
        if game.wood.value >= 250 and game.gold.value >=250:
            game.change_resource(game.wood, -250)
            game.change_resource(game.gold, -250)
            return True
        else:
            return False

    @staticmethod
    def build(gameobj):
        x = games.mouse.get_x()
        y = games.mouse.get_y()
        church_image = games.load_image("village_images/bmp/church.png")
        new_church = Church(image = church_image, game = gameobj)
        new_church.x = x
        new_church.y = y
        games.screen.add(new_church)
        return new_church




class Barracks(Building):
    def __init__(self, image, game):
        super(Barracks, self).__init__(image = image, game = game)
        self.x = 0
        self.y = 0


    @staticmethod
    def enough_resources(game):
        if game.wood.value >= 230 and game.gold.value >= 230 and game.food.value >= 100:
            game.change_resource(game.wood, -230)
            game.change_resource(game.gold, -230)
            game.change_resource(game.food, -100)
            return True
        else:
            return False
    @staticmethod
    def build(gameobj):
        x = games.mouse.get_x()
        y = games.mouse.get_y()
        barracks_image = games.load_image("village_images/bmp/barracks.png")
        new_barracks = Barracks(image = barracks_image, game = gameobj)
        new_barracks.x = x
        new_barracks.y = y
        games.screen.add(new_barracks)
        return new_barracks



class Farm(Building):
    def __init__(self, image, game, farmer):
        super(Farm, self).__init__(image = image, game = game)
        self.x = 0
        self.y = 0
        self.farmer = farmer


    @staticmethod
    def build(gameobj, farmer):
        x = farmer.get_x()
        y = farmer.get_y() + 50
        farm_image = games.load_image("village_images/bmp/farm.png")
        new_farm = Farm(image = farm_image, game = gameobj, farmer = farmer)
        new_farm.x = x
        new_farm.y = y
        games.screen.add(new_farm)
        return new_farm
        new_farm.set_interval(games.screen.fps)

    def update(self):
        if self.farmer != None:
            self.game.change_resource(self.game.food, 1)































             

class Unit(games.Sprite):
    def __init__(self, image, game):
        super(Unit, self).__init__(image = image)
        self.game = game
        self.engaged = False


    @staticmethod
    def build(gameobj, starting_haus):
        """Adds the new unit to the location of the last built house if there are enough resources. """ 
        if gameobj.food.value >= 10 and gameobj.gold.value >= 10 and gameobj.housing.value > 0:
            gameobj.change_resource(gameobj.food, -10)
            gameobj.change_resource(gameobj.gold, -10)
            gameobj.change_resource(gameobj.housing, -1)
            gameobj.change_resource(gameobj.pop, 1)
            x = starting_haus.get_x()
            y = starting_haus.get_y()
            unit_image = games.load_image("village_images/bmp/lumberjack.png")
            new_unit = Unit(image = unit_image, game = gameobj)
            new_unit.x = x
            new_unit.y = y
            games.screen.add(new_unit)
            return new_unit
        else:

            rejection = games.Message(value = "You cannot add that unit", size = 70,
                                      x = games.mouse.get_x(), y = games.mouse.get_y(),
                                      is_collideable = False,
                                      lifetime = 1 * games.screen.fps, color = color.red)
            games.screen.add(rejection)

    def move(self):
        self.dx = 2



class Lumberjack(Unit):
    
    def __init__(self, image, game, treelist):
        super(Lumberjack, self).__init__(image = image, game = game)
        self.treelist = treelist

    @staticmethod
    def build(gameobj, starting_haus):
        if gameobj.food.value >= 20  and gameobj.housing.value > 0 and starting_haus != None:
            gameobj.change_resource(gameobj.food, -20)
            gameobj.change_resource(gameobj.housing, -1)
            gameobj.change_resource(gameobj.pop, 1)
            x = starting_haus.get_x()
            y = starting_haus.get_y()
            unit_image = games.load_image("village_images/bmp/lumberjack.png")
            treelist = gameobj.get_treelist()
            new_lumberjack = Lumberjack(image = unit_image, game = gameobj, treelist = treelist) 
            new_lumberjack.x = x
            new_lumberjack.y = y
            games.screen.add(new_lumberjack)
            new_lumberjack.cut_tree(game = gameobj, treelist = treelist)
        else:

            rejection = games.Message(value = "You cannot add that unit", size = 70,
                                      x = games.mouse.get_x(), y = games.mouse.get_y(),
                                      is_collideable = False,
                                      lifetime = 1 * games.screen.fps, color = color.red)
            games.screen.add(rejection)
    def cut_tree(self, game, treelist):
        """ Destroys a randomely selected tree, which creates more wood. Lumberjack then goes home and is hidden from view. Adds gold while method is in use."""
        self.engaged = True
        if len(treelist) != 0:
            location_tree = random.choice(treelist)
            start_x = self.get_x()
            start_y = self.get_y()
            dest_x = location_tree.get_x()
            dest_y = location_tree.get_y()
            x_vel = ((dest_x - start_x) / 200) * 2
            y_vel = ((dest_y - start_y) / 200) * 2
        
            while (abs(location_tree.get_x() - self.get_x()) > 1 and abs(location_tree.get_y() - self.get_y()) > 1):
                self.dx = x_vel
                self.dy = y_vel
            self.dx, self.dy = 0, 0

            location_tree.fell(game)
            treelist.remove(location_tree)
        
            while (abs(start_x - self.get_x()) > 1 and abs(start_y - self.get_y()) > 1):
                self.dx = -(x_vel)
                self.dy = -(y_vel)
            self.dx, self.dy = 0, 0
            self.x, self.y = -50, -50
            self.engaged = False
    
    def update(self):
        if self.game.food.value <= 0:
            if not self.engaged:
                self.game.change_resource(self.game.pop, -1)
                self.game.change_resource(self.game.housing, 1)
                self.die()
                #self.game.everybody_dead()
        else:
            self.game.change_resource(self.game.food, -0.5)
            self.game.change_resource(self.game.gold, 1)   

    def die(self):
        self.destroy()

class Farmer(Unit):

    @staticmethod
    def build(gameobj, starting_haus):
        if gameobj.food.value >= 10 and gameobj.gold.value >= 20 and gameobj.housing.value > 0 and starting_haus != None:
            gameobj.change_resource(gameobj.food, -10)
            gameobj.change_resource(gameobj.gold, -20)
            gameobj.change_resource(gameobj.housing, -1)
            gameobj.change_resource(gameobj.pop, 1)
            x = starting_haus.get_x()
            y = starting_haus.get_y()
            unit_image = games.load_image("village_images/bmp/farmer.png")
            new_farmer = Farmer(image = unit_image, game = gameobj)
            new_farmer.x = x
            new_farmer.y = y    
            games.screen.add(new_farmer)
            new_farmer.farm = None
            new_farmer.construct_farm(gameobj)
        else:

            rejection = games.Message(value = "You cannot add that unit", size = 70,
                                      x = games.mouse.get_x(), y = games.mouse.get_y(),
                                      is_collideable = False,
                                      lifetime = 1 * games.screen.fps, color = color.red)
            games.screen.add(rejection)

    def update(self):
        if self.game.food.value <= 0 or self.game.gold.value <= 0:
            if not self.engaged:
                self.game.change_resource(self.game.pop, -1)
                self.game.change_resource(self.game.housing, 1)
                if self.farm != None:
                    self.farm.farmer = None
                self.destroy()
        else:
            self.game.change_resource(self.game.gold, -1)





    def construct_farm(self, game):
        """ Creates a farm structure that adds food and takes gold to maintain. """
        self.engaged = True
        start_x, start_y = self.get_x(), self.get_y()
        end_list = (random.randint(-200, -50), random.randint(50, 200))
        end_x = start_x + random.choice(end_list)
        end_y = start_y + random.choice(end_list)
        x_vel = ((end_x - start_x) / 200) * 2
        y_vel = ((end_y - start_y) / 200) * 2
        

        while (abs(end_x - self.get_x()) > 1 and abs(end_y - self.get_y()) > 1):
            self.dx = x_vel
            self.dy = y_vel
        self.dx, self.dy = 0, 0
        self.farm = Farm.build(gameobj = game, farmer = self)  
        self.engaged = False

class Climber(Unit):
    alive = True
    angle_value = True
    @staticmethod
    def build(gameobj, starting_barracks, starting_church):
        if gameobj.food.value >= 50 and gameobj.gold.value >= 50 and gameobj.wood.value >= 50 and gameobj.housing.value > 0 and (starting_barracks != None):
            gameobj.change_resource(gameobj.food, -50)
            gameobj.change_resource(gameobj.gold, -50)
            gameobj.change_resource(gameobj.wood, -50)
            gameobj.change_resource(gameobj.housing, -1)
            gameobj.change_resource(gameobj.pop, 1)
            x = games.screen.width / 2
            y = games.screen.height - 100
            unit_image = games.load_image("village_images/bmp/climber.png")
            new_climber = Climber(image = unit_image, game = gameobj)
            new_climber.x = x
            new_climber.y = y    
            games.screen.add(new_climber)
            new_climber.climb(gameobj, starting_church)
             
        else:

            rejection = games.Message(value = "You cannot add that unit", size = 70,
                                      x = games.mouse.get_x(), y = games.mouse.get_y(),
                                      is_collideable = False,
                                      lifetime = 1 * games.screen.fps, color = color.red)
            games.screen.add(rejection)
    def climb(self, game, starting_church):
        """Ascends the mountain in the middle of the screen.
        If there is a church built, then the chance of death is reduced (as a fraction of 1/deathChance).
        This is the probability that he will fall to his death at any given step of execution.""" 
        if starting_church != None:
            deathChance = 100000000
        else:
            deathChance = 10000000
        while self.alive and self.get_y() > 100:
            self.dy = -12
            rdeath = random.randint(0, deathChance)
            if rdeath == deathChance:
                self.alive = False
                self.die(game)
                break
        if self.get_y() <= 100:
            game.end(victory = 2)
            self.dy = 0
    
    def die(self, game):
        fall_vel = self.dy * -2
        game.change_resource(game.pop, -1)
        while self.get_y() <= games.screen.height:
            self.dy = fall_vel
        self.destroy()
        
        


    def update(self):
        # Creates rotating back and forth motion as mountain climber ascends.
        if self.alive:
            time.sleep(0.3)
            if self.angle_value == True:
                self.angle += 30
                self.angle_value = False
            else:
                self.angle -= 30
                self.angle_value = True
            self.game.change_resource(self.game.food, -1)
            self.game.change_resource(self.game.gold, -1)     
        



class Tree(games.Sprite):
    WOOD = 50
    def __init__(self, image, game, is_collideable = True):
        super(Tree, self).__init__(image = image)
        self.game = game
        self.x = 0
        self.y = 0
    
    @staticmethod
    def build(gameobj):
        x = random.randint(200, games.screen.width - 200)
        y = random.randint(200, games.screen.height - 200)
        if x > (games.screen.width/3) and x < ((games.screen.width/3) * 2):
            while x > (games.screen.width/3) and x < ((games.screen.width/3) * 2):
                x += random.randint(-100, 100)

        tree_image = games.load_image("village_images/bmp/tree.png")
        new_tree = Tree(image = tree_image, game = gameobj)
        new_tree.x = x
        new_tree.y = y
        games.screen.add(new_tree)
        return new_tree

    def fell(self, game):
        game.change_resource(game.wood, self.WOOD)
        self.destroy()






















def main():
    newgame = Game()

    newgame.play()      
main()

