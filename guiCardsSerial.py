import pygame
import serial
import math
import time

# Defines
RED             = (255,0,0)
LIGHTRED        = (255,64,64)
GREEN           = (0,255,0)
BLUE            = (0,0,255)
LIGHTBLUE       = (64,64,255)
BLACK           = (0,0,0)
WHITE           = (255,255,255)
LIGHTGREY       = (125,125,125)
DEPRESSEDBUTTON = (200,200,200)
FONTSIZELARGE   = 75
FONTSIZESMALL   = 25
TENSRESOLUTION  = 257
PLAYERONE       = 1
PLAYERTWO       = 2

pygame.init()


# Current display is scaled by 125% in windows settings. Therefore the visible screen size is actually 1536x960
window = pygame.display.set_mode((1920,1200), pygame.FULLSCREEN)
clock = pygame.time.Clock()
# window = pygame.display.set_mode((800,800))
window.fill(LIGHTGREY)


class DigitButton:
    """ DigitButton Class:\n
    This class creates the numerical buttons located on the screen. They are used to input numerical values into the calculator 
    to then be processed by a given opperand.
    
    Paramaters:
    - window: The Surface object to draw the button onto.
    - width = How wide the button should be drawn.
    - height = How tall the button should be drawn.
    - text = The text to write in the centre of the button.
    """
    def __init__(self, window:pygame.Surface, width: int, height:int, text:str, buttonCol):
        """Initialize the object with the given parameters. """
        self.window = window
        self.width = width
        self.height = height
        self.text = text
        self.buttonCol = buttonCol
        self.font = pygame.font.SysFont('Arial',FONTSIZELARGE) 
    
    def drawButton(self, xPos, yPos,col = None, rotation = 0):
        """Draws the button using the parameters the object was initialized with. """
        if col is not None:
            self.button = pygame.draw.rect(self.window,col,(xPos,yPos,self.width,self.height),0,2)
        else:
            self.button = pygame.draw.rect(self.window,self.buttonCol,(xPos,yPos,self.width,self.height),0,2)

        textImg = self.font.render(self.text, 1, BLACK)
        textImg = pygame.transform.rotozoom(textImg, rotation, 1)
        textWidth = textImg.get_width()
        textHeight = textImg.get_height()
        self.window.blit(textImg, (xPos + (self.width - textWidth)/2, yPos + (self.height - textHeight)/2))
        pygame.display.update()

def updateHealthP1(healthP1):
    x = 536
    y = 300
    offset = 4
    rotation = 270
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"Current Health: {str(healthP1)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    window.blit(textImg, (x,y+offset))
    pygame.display.update()

def displayInputP1(numP1):
    x = 500
    y = 300
    offset = 4
    rotation = 270
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"{str(numP1)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    window.blit(textImg, (x,y+offset))
    pygame.display.update()

def clearInputP1():
    x = 500
    y = 300
    offset = 4
    rotation = 270
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"{str(0)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    window.blit(textImg, (x,y+offset))
    pygame.display.update()

def updateHealthP2(healthP2):
    x = 964
    y = 300
    rotation = 90
    yOffset = 690
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"Current Health: {str(healthP2)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    textDim = textImg.get_rect()
    window.blit(textImg, (x,yOffset - textDim.height))
    pygame.display.update()

def displayInputP2(numP2):
    x = 1000
    y = 300
    rotation = 90
    yOffset = 690
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"{str(numP2)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    textDim = textImg.get_rect() 
    window.blit(textImg, (x,yOffset-textDim.height))
    pygame.display.update()

def clearInputP2():
    x = 1000
    y = 300
    rotation = 90
    yOffset = 690
    pygame.draw.rect(window, WHITE, (x,y,29,393),0,2)
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    textImg = font.render(f"{str(0)}",1,BLACK)
    textImg = pygame.transform.rotozoom(textImg, rotation, 1)
    textDim = textImg.get_rect() 
    window.blit(textImg, (x,yOffset-textDim.height))
    pygame.display.update()

def drawArena():
    rotationP1 = 270
    rotationP2 = 90
    pygame.draw.rect(window,LIGHTRED,(0,0,768,960))
    pygame.draw.rect(window,LIGHTBLUE,(768,0,1536,960))
    
    font = pygame.font.SysFont('Arial', FONTSIZESMALL)
    p1 = font.render("Player 1",1,BLACK)
    p1 = pygame.transform.rotozoom(p1, rotationP1,1)
    p1Dim = p1.get_rect()
    p2 = font.render("Player 2",1,BLACK)
    p2 = pygame.transform.rotozoom(p2, rotationP2,1)
    p2Dim = p1.get_rect()
    window.blit(p1,(768 - p1Dim.width,4))
    window.blit(p2,(768 ,956 - p2Dim.height))
    pygame.display.update()

def sendDamagePacket(damage, health, player, ser:serial.Serial):
    if player == 1:
        resistance = math.ceil((damage / health) * 257)
        ser.write()
    elif player == 2:
        resistance = math.ceil((damage / health) * 257)

# Button Layout for P1
buttonLayoutP1 = [(100,400), (200,300), (200,400), 
                (200,500), (300,300), (300,400), 
                (300,500), (400,300), (400,400),
                (400,500)]

# Button Layout for P2
buttonLayoutP2 = [(1436-100,500), (1436-200,600), (1436-200,500), 
                (1436-200,400), (1436-300,600), (1436-300,500), 
                (1436-300,400), (1436-400,600), (1436-400,500),
                (1436-400,400)]

if __name__ == "__main__":

    arduino = serial.Serial(port='COM9', baudrate=9600, timeout=1)
    time.sleep(2)

    # Create all buttons
    numButtonsP1 = [DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), f"{i}", WHITE) for i in range(10)]
    numButtonsP2 = [DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), f"{i}", WHITE) for i in range(10)]

    backSpaceP1 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "←", WHITE)
    backSpaceP2 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "←", WHITE)

    subtractP1 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "-", WHITE)
    subtractP2 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "-", WHITE)

    addP1 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "+", WHITE)
    addP2 = DigitButton(window, FONTSIZELARGE + (FONTSIZELARGE*0.25), FONTSIZELARGE + (FONTSIZELARGE*0.25), "+", WHITE)

    backSpacePosP1 = (400,600)
    subtractPosP1 = (300,600)
    addPosP1 = (200,600)

    backSpacePosP2 = (1436-400,300)
    subtractPosP2 = (1436-300,300)
    addPosP2 = (1436-200,300)

    # State variables
    numListP1 = []
    numListP2 = []
    inputNumP1 = 0
    inputNumP2 = 0
    healthP1 = 0
    healthP2 = 0
    
    # Draw initial board state (RED: PLayer 1, BLUE: Player 2)
    drawArena()
    updateHealthP1(healthP1)
    updateHealthP2(healthP2)
    displayInputP1(inputNumP1)
    displayInputP2(inputNumP2)

    for i in range(len(numButtonsP1)):
        numButtonsP1[i].drawButton(buttonLayoutP1[i][0],buttonLayoutP1[i][1],WHITE, 270)

    for i in range(len(numButtonsP2)):
        numButtonsP2[i].drawButton(buttonLayoutP2[i][0], buttonLayoutP2[i][1],WHITE, 90)

    backSpaceP1.drawButton(backSpacePosP1[0], backSpacePosP1[1], WHITE, 270)
    subtractP1.drawButton(subtractPosP1[0],subtractPosP1[1], WHITE, 270)
    addP1.drawButton(addPosP1[0],addPosP1[1], WHITE, 270)

    backSpaceP2.drawButton(backSpacePosP2[0], backSpacePosP2[1], WHITE, 90)
    subtractP2.drawButton(subtractPosP2[0],subtractPosP2[1], WHITE, 90)
    addP2.drawButton(addPosP2[0],addPosP2[1], WHITE, 90)
    
    running = True

    while(running):
        clock.tick(144)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Player 1 Numbers
                for i in range(len(numButtonsP1)):
                    if numButtonsP1[i].button.collidepoint(pos):
                        numButtonsP1[i].drawButton(buttonLayoutP1[i][0],buttonLayoutP1[i][1], DEPRESSEDBUTTON, 270)
                        break
                # Player 2 Numbers 
                for i in range(len(numButtonsP2)):
                    if numButtonsP2[i].button.collidepoint(pos):
                        numButtonsP2[i].drawButton(buttonLayoutP2[i][0],buttonLayoutP2[i][1], DEPRESSEDBUTTON, 90)
                        break
                # Player 1 Opperands
                if backSpaceP1.button.collidepoint(pos):
                    backSpaceP1.drawButton(backSpacePosP1[0], backSpacePosP1[1],DEPRESSEDBUTTON, 270)    
                elif subtractP1.button.collidepoint(pos):
                    subtractP1.drawButton(subtractPosP1[0],subtractPosP1[1],DEPRESSEDBUTTON, 270)
                elif addP1.button.collidepoint(pos):
                    addP1.drawButton(addPosP1[0],addPosP1[1], DEPRESSEDBUTTON, 270)
                # Player 2 Opperands
                if backSpaceP2.button.collidepoint(pos):
                    backSpaceP2.drawButton(backSpacePosP2[0], backSpacePosP2[1],DEPRESSEDBUTTON, 90)    
                elif subtractP2.button.collidepoint(pos):
                    subtractP2.drawButton(subtractPosP2[0],subtractPosP2[1],DEPRESSEDBUTTON, 90)
                elif addP2.button.collidepoint(pos):
                    addP2.drawButton(addPosP2[0],addPosP2[1], DEPRESSEDBUTTON, 90)  

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # Player 1 Numbers
                for i in range(len(numButtonsP1)):
                    if numButtonsP1[i].button.collidepoint(pos):
                        numButtonsP1[i].drawButton(buttonLayoutP1[i][0],buttonLayoutP1[i][1], WHITE, 270)
                        numListP1.append(numButtonsP1[i].text)
                        inputNumP1 = int(''.join(map(str,numListP1)))
                        displayInputP1(inputNumP1)
                        break
                # Player 2 Numbers
                for i in range(len(numButtonsP2)):
                    if numButtonsP2[i].button.collidepoint(pos):
                        numButtonsP2[i].drawButton(buttonLayoutP2[i][0],buttonLayoutP2[i][1], WHITE, 90)
                        numListP2.append(numButtonsP2[i].text)
                        inputNumP2 = int(''.join(map(str,numListP2)))
                        displayInputP2(inputNumP2)
                        break

                # Player 1 Opperands
                # Back Space
                if backSpaceP1.button.collidepoint(pos):
                    if not len(numListP1) == 0:
                        del numListP1[-1]
                        if numListP1:
                            inputNumP1 = int(''.join(map(str,numListP1)))
                            displayInputP1(inputNumP1)
                        else:
                            inputNumP1 = 0
                            displayInputP1(inputNumP1)
                    backSpaceP1.drawButton(backSpacePosP1[0], backSpacePosP1[1], WHITE, 270)
                
                # Subtract
                if subtractP1.button.collidepoint(pos):
                    if(healthP1 > 0):
                        damage = math.ceil((inputNumP1/healthP1) * TENSRESOLUTION)
                        if damage > 257:
                            damage = 257
                        packet = str(PLAYERONE) + ':' + str(damage) + '\n'
                        healthP1 -= inputNumP1
                        if healthP1 < 0:
                            healthP1 = 0
                        numListP1 = []
                        updateHealthP1(healthP1)
                        clearInputP1()
                        arduino.write(bytes(packet, 'ascii'))
                        print(packet)
                    subtractP1.drawButton(subtractPosP1[0],subtractPosP1[1], WHITE, 270)
                        

                # Addition
                if addP1.button.collidepoint(pos):
                    healthP1 += inputNumP1
                    numListP1 = []
                    updateHealthP1(healthP1)
                    clearInputP1()
                    addP1.drawButton(addPosP1[0],addPosP1[1], WHITE, 270)

                # Player 2 Opperands
                # Backspace
                if backSpaceP2.button.collidepoint(pos):
                    if not len(numListP2) == 0:
                        del numListP2[-1]
                        if numListP2:
                            inputNumP2 = int(''.join(map(str,numListP2)))
                            displayInputP2(inputNumP2)
                        else:
                            inputNumP2 = 0
                            displayInputP2(inputNumP2)
                    backSpaceP2.drawButton(backSpacePosP2[0], backSpacePosP2[1], WHITE, 90) 

                # Subtract               
                if subtractP2.button.collidepoint(pos):
                    if(healthP2 > 0):
                        damage = math.ceil((inputNumP2/healthP2) * TENSRESOLUTION)
                        if damage > 257:
                            damage = 257
                        packet = str(PLAYERTWO) + ':' + str(damage) + '\n'
                        healthP2 -= inputNumP2
                        if healthP2 < 0:
                            healthP2 = 0
                        numListP2 = []
                        print(healthP2)
                        updateHealthP2(healthP2)
                        clearInputP2()
                        arduino.write(bytes(packet, 'ascii'))
                        print(packet)
                    subtractP2.drawButton(subtractPosP2[0],subtractPosP2[1], WHITE, 90)
                
                # Addition
                if addP2.button.collidepoint(pos):
                    healthP2 += inputNumP2
                    numListP2 = []
                    updateHealthP2(healthP2)
                    clearInputP2()
                    addP2.drawButton(addPosP2[0],addPosP2[1], WHITE, 90)