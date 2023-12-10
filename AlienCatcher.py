# -*- coding: utf-8 -*-
"""
https://pngtree.com/freepng/cartoon-spaceship-element_4498783.html
https://www.pinterest.com/pin/stones-and-rocks-png-image--584482857867709034/
https://pixabay.com/sound-effects/search/ding/

Created on Thu Nov  9 11:02:16 2023

@author: Kyle Sanders
"""
import pygame, simpleGE, random

class SpaceShip(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("SpaceShip.png")
        self.setSize(60, 60)
        self.pingSound = simpleGE.Sound("ping.mp3")
        
    def checkEvents(self):
        if not self.scene.gameOver:
            if self.scene.isKeyPressed(pygame.K_LEFT):
                self.rotateBy(9)
            if self.scene.isKeyPressed(pygame.K_RIGHT):
                self.rotateBy(-9)
            if self.scene.isKeyPressed(pygame.K_UP):
                self.addForce(.4, self.rotation)
            if self.scene.isKeyPressed(pygame.K_DOWN):
                self.addForce(-.4, self.rotation)

    def checkCollision(self):
        if self.collidesWith(self.scene.alien):
            self.pingSound.play()
        if self.collidesWith(self.scene.asteroid):
            self.pingSound.play()

class Asteroid(simpleGE.SuperSprite):
    def __init__(self, scene):
        simpleGE.SuperSprite.__init__(self, scene)
        self.setImage("Asteroid.png")
        self.setSize(25, 25)
        self.reset()
    
    def reset(self):     
        self.dx = 1
        self.dy = 1
        self.damage = 20
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.setPosition((random.randint(0, self.screen.get_width()), 0))
            self.dy = random.randint(1, 3)
            self.dx = random.randint(-3, 3)
        elif side == "bottom":
            self.setPosition((random.randint(0, self.screen.get_width()), self.screen.get_height()))
            self.dy = random.randint(-3, -1)
            self.dx = random.randint(-3, 3)
        elif side == "left":
            self.setPosition((0, random.randint(0, self.screen.get_height())))
            self.dx = random.randint(1, 3)
            self.dy = random.randint(-3, 3)
        elif side == "right":
            self.setPosition((self.screen.get_width(), random.randint(0, self.screen.get_height())))
            self.dx = random.randint(-3, -1)
            self.dy = random.randint(-3, 3)
                
        self.updateVector()

        self.rotSpeed = random.randint(-5, 5)

    def checkEvents(self):
        self.rotateBy(self.rotSpeed)
        if not self.scene.gameOver:
            if self.collidesWith(self.scene.spaceShip):
                self.scene.lives -= 1
    
    def checkBounds(self):
        if not self.scene.gameOver:
            if self.rect.bottom > self.screen.get_height():
                self.reset()
            if self.rect.right < 0:
                self.reset()
            if self.rect.top < 0:
                self.reset()
            if self.rect.left > self.screen.get_width():
                self.reset()
            
class Alien(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Alien.png")
        self.setSize(30, 30)
        self.reset()
    
    def reset(self):
        self.dx = 0
        self.dy = 0
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.setPosition((random.randint(0, self.screen.get_width()), 0))
            self.dy = random.randint(1, 3)
            self.dx = random.randint(-3, 3)
        elif side == "bottom":
            self.setPosition((random.randint(0, self.screen.get_width()), self.screen.get_height()))
            self.dy = random.randint(-3, -1)
            self.dx = random.randint(-3, 3)
        elif side == "left":
            self.setPosition((0, random.randint(0, self.screen.get_height())))
            self.dx = random.randint(1, 3)
            self.dy = random.randint(-3, 3)
        elif side == "right":
            self.setPosition((self.screen.get_width(), random.randint(0, self.screen.get_height())))
            self.dx = random.randint(-3, -1)
            self.dy = random.randint(-3, 3)
        
        self.updateVector()
    

    def checkEvents(self):
        if not self.scene.gameOver:
            if self.collidesWith(self.scene.spaceShip):
                self.scene.score += 1
                self.reset()
    
    def checkBounds(self):
        if not self.scene.gameOver:
            if self.rect.bottom > self.screen.get_height():
                self.reset()
            if self.rect.right < 0:
                self.reset()
            if self.rect.top < 0:
                self.reset()
            if self.rect.left > self.screen.get_width():
                self.reset()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.spaceShip = SpaceShip(self)        
        
        self.aliens = []
        self.asteroids = []
        for i in range(10):
            self.asteroids.append(Asteroid(self))
        for i in range(4):
            self.aliens.append(Alien(self))
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Score: 0"
        self.lblScore.center = (95, 50)
        self.score = 0
        
        self.lblTime = simpleGE.Label()
        self.lblTime.text = "Time Left: 30"
        self.lblTime.center = (550, 50)
        
        self.lblLives = simpleGE.Label()
        self.lblLives.text = "Lives Left: 2"
        self.lblLives.center = (320, 50)
        self.lives = 2
        
        self.timer = simpleGE.Timer()
        self.gameOver = False
        
        self.sprites = [self.lblScore, self.lblTime, self.lblLives, self.spaceShip, self.asteroids, self.aliens]
        
    def update(self):
         if not self.gameOver:   
            time = 0 + self.timer.getElapsedTime()
            if time > 99999:
                self.stop()
            self.lblTime.text = f"Time: {time:0.01f}"
            self.lblScore.text = f"score: {self.score}"
            self.lblLives.text = f"Lives Left: {self.lives}"
            if self.lives == 0:
               self.gameOver = True
               gameOverScene = GameOverScene(self.score)
               gameOverScene.start()

class StartMenu(simpleGE.Scene):
    def __init__(self):
        simpleGE.Scene.__init__(self)
        self.background.fill((0, 255, 0))
        
        self.addLabels()
        self.startButton()
        self.addMultiLabel()
        
        self.sprites = [self.lblTitle, self.label,
                        self.lblButton, self.button,
                        self.multi]
    
    def addLabels(self):
        self.lblTitle = simpleGE.Label()
        self.lblTitle.text = "Alien Catcher!"
        self.lblTitle.center = (320, 40)
        self.lblTitle.size = (300, 30)
        
        self.label = simpleGE.Label()
        self.label.text = "1 Player"
        self.label.center = (500, 180)
        self.label.size = (180, 30)
        
    def startButton(self): 
        self.lblButton = simpleGE.Label()
        self.lblButton.center = (200, 180)
        self.lblButton.text = "START!"
        self.lblButton.fgColor = (255, 255, 255)
        self.lblButton.bgColor = (0, 0, 0)
        
        self.button = simpleGE.Button()
        self.button.center = (200, 180)
        self.button.text = "START!"
        self.button.onRelease = self.startGame
    
    def addMultiLabel(self):
        self.multi = simpleGE.MultiLabel()
        self.multi.textLines = [
            "How to Play:",
            "Use the up and down arrow keys,",
            "to go forward and backwards.",
            "Use the left and right arrow keys to rotate.",
            "Catch as many aliens as possible without hitting asteroids.",
            "You have 2 lives, so be VERY CAREFUL! "
            ]
        self.multi.size = (610, 200)
        self.multi.center = (320, 370)
        
    def update(self):        
        if self.button.clicked:
            game = Game()
            game.start()
        
    def startGame(self):
        gameScene = Game()
        gameScene.start()

class GameOverScene(simpleGE.Scene):
    def __init__(self, finalScore):
        simpleGE.Scene.__init__(self)
        self.finalScore = finalScore
    
        self.gameOverLabel()
        self.scoreLabel(finalScore)
        self.restartAction()
        self.quitAction()
        
        self.sprites = [self.lblGameOver, self.lblScore,
                        self.lblButton, self.restartButton,
                        self.lblQuitButton, self.quitButton]
    
    def gameOverLabel(self):
        self.lblGameOver = simpleGE.Label()
        self.lblGameOver.text = "Game Over"
        self.lblGameOver.center = (300, 200)
        
    def scoreLabel(self, finalScore):    
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Final Score: {finalScore}"
        self.lblScore.center = (300,230)
    
    def restartAction(self):
        self.lblButton = simpleGE.Label()
        self.lblButton.center = (200, 300)
        self.lblButton.text = "Restart"
        self.lblButton.fgColor = (0, 0, 0)
        self.lblButton.bgColor = (255, 255, 255)
        
        self.restartButton = simpleGE.Button()
        self.restartButton.center = (200, 300)
        self.restartButton.text = "Restart"
        self.restartButton.onRelease = self.startGame
    
    def quitAction(self):
        self.lblQuitButton = simpleGE.Label()
        self.lblQuitButton.center = (400, 300)
        self.lblQuitButton.text = "Quit"
        self.lblQuitButton.fgColor = (0, 0, 0)
        self.lblQuitButton.bgColor = (255, 255, 255)
        
        self.quitButton = simpleGE.Button()
        self.quitButton.center = (400, 300)
        self.quitButton.text = "Quit"
        self.quitButton.onRelease = self.quit
            
    def update(self):
        if self.restartButton.clicked:
            game = Game()
            game.start()
        if self.quitButton.clicked:
            self.stop()
    
    def startGame(self):
        gameScene = Game()
        gameScene.start()
    
    def quit(self):
        self.stop()
        
def main():
    startMenu = StartMenu()
    startMenu.start()
    
if __name__ == "__main__":
    main()
            
