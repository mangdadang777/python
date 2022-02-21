import pygame, sys
from pygame.locals import *
import pygame.locals
from pygame import key,event

pygame.init()
fpsClock = pygame.time.Clock()
SIZE = 4
BLOCKSIZE=100
MAX=SIZE*BLOCKSIZE
_GameEnd=None
_GameOver=None
windowSurfaceObj = pygame.display.set_mode((MAX,MAX))
pygame.display.set_caption('2048')

redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color (255,255,255)
lightblue = pygame.Color(173, 216, 230)
lighterblue = pygame.Color(235,255,255)
grey =  pygame.Color(145,141,142)
gold =  pygame.Color(255,215,0)
black=  pygame.Color(0,0,0)
granite = pygame.Color(131,126,124)
box1 =  pygame.Color(201,196,194)
color2 =(229,228,227)
color4 = pygame.Color(229,182,147)

colors = {2:(229,228,227),4:(229,228-20,227-40),8:(229,228-30,227-60),16:(229,150,100),
          32:(200,100,50),64:(150,60,30),128:(255,219,90),
          256:(229,200,70),512:(229,180,50),1024:(229,170,40),2048:(229,160,20),
          4096:(0,0,0),8192:(0,0,100),16384:(30,0,0),32768:(60,0,0)}
mousex,mousey = 0,0

fontObj  = pygame.font.SysFont('verdana',32)
fontObj2  = pygame.font.SysFont('verdana',32)
fontObj16  = pygame.font.SysFont('verdana',28)
fontObj128  = pygame.font.SysFont('verdana',26,bold=True)
fontObj1024  = pygame.font.SysFont('verdana',24,bold=True)
fontObj16384  = pygame.font.SysFont('verdana',23,bold=True)
fontObjSmall  = pygame.font.SysFont('verdana',22,bold=True)
fonts =[fontObj2,fontObj16,fontObj128,fontObj1024,fontObj16384,fontObjSmall]

lineArray = []
for a in range(BLOCKSIZE,MAX,BLOCKSIZE) :
    lineArray.append( (0,a))
    lineArray.append((MAX,a))
    lineArray.append((MAX,a+BLOCKSIZE))
lineArray.append((MAX,0))
lineArray.append((0,0))
for a in range(BLOCKSIZE,MAX,BLOCKSIZE) :
    lineArray.append( (a,0))
    lineArray.append((a,MAX))
    lineArray.append((a+BLOCKSIZE,400))
print(lineArray)

def processMovement(myList:list,directive:int):

    print(myList)
    newList=[]
    Matrix = [[0 for x in range(SIZE)] for x in range(SIZE)]
    for (x,y,z) in myList:
        Matrix[y//BLOCKSIZE][x//BLOCKSIZE]=z

    if directive == pygame.K_DOWN:
        Matrix=[list(elem) for elem in zip(*Matrix[::-1])]
        Matrix,score=addMatrix(Matrix)
        Matrix=[list(elem[::-1]) for elem in zip(*Matrix[::-1])][::-1]
    if directive == pygame.K_UP:
        Matrix=[list(elem) for elem in zip(*Matrix)]
        Matrix,score=addMatrix(Matrix)
        Matrix=[list(elem) for elem in zip(*Matrix)]

    elif directive == pygame.K_LEFT:
        print('move left, no rotation\n')
        Matrix,score=addMatrix(Matrix)
    elif directive == pygame.K_RIGHT:
        print('move right, rotate 180\n')
        Matrix=[each [::-1] for each in Matrix[::-1]]
        Matrix,score=addMatrix(Matrix)
        Matrix=[each [::-1] for each in Matrix[::-1]]

    for j,line in enumerate(Matrix):
        for i,each in enumerate(line):
            if each!=0:
                newList.append([i*BLOCKSIZE,j*BLOCKSIZE,each])

    standStill = True if sorted(myList)==sorted(newList) else False
    return newList,standStill,score

def addMatrix(myList:list):

    newList=[]
    newLine=[]
    score=0
    lastPaired=False
    print("before add ",myList)
    for i,line in enumerate(myList):
        for i,each in enumerate(line):
            print("loop:",i,each)
            if each ==0:
                pass
            elif len(newLine)>0 and newLine[-1]==each and not lastPaired:
                print("what is this:",each)
                newLine[-1]= 2*int(each)
                score=score+2*int(each)
                lastPaired=True
                if  each==1048 and _GameEnd==None : _GameEnd=True
            else:
                lastPaired=False
                newLine.append(int(each))
                print("appending",i)
        lastPaired=False

        newLine.extend( [0] *(SIZE-len(newLine)))
        print("add test:",len(newLine))
        newList.append(newLine)
        newLine=[]

    return newList,score

def getRandBox(myList):
    simpleLock=[]
    simpleEmpty=[]
    for [x,y,z] in myList:
        simpleLock.append((y//100)*4+x//100)
    simpleEmpty=[x for x in range(0,16) if x not in simpleLock]
    import random
    x=random.choice(simpleEmpty)
    z = random.randint(0,10)
    z = 2 if z <= 9 else 4
    return  [(x%4)*100,(x//4)*100,z]

def drawBox(box,border=None):
    x,y,z=box

    if(border==None):
        border= color2
    fillColor=colors[z if z<32768 else -1 ]

    myRect=pygame.draw.rect(windowSurfaceObj,border,(x+2,y+2,98,98),0)
    windowSurfaceObj.fill(border,myRect)
    windowSurfaceObj.fill(fillColor, myRect.inflate(-5, -5))
    msg=str(z)

    msgSurfaceObj = fontObj.render(msg,True,granite if z<16 else whiteColor)
    msgRectobj = msgSurfaceObj.get_rect()

    msgRectobj.center = (x+50,y+52)
    windowSurfaceObj.blit(msgSurfaceObj,msgRectobj)

locked=[]
new  = (getRandBox(locked))
print ("first pick:",new)
locked.append(new)
action = None
Total = 0
while True:
    windowSurfaceObj.fill(lightblue)
    pygame.draw.lines(windowSurfaceObj,lighterblue,False,lineArray,2)

    if len(locked)==1:
        drawBox(locked[-1],gold)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos


        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT,pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN) :
                standStill=False

                print( "Arrow Key pressed.",event.key)
                action = event.key
                locked,standStill,score=processMovement(locked,event.key)

                if not standStill:
                    Total = Total + score
                    new =getRandBox(locked)
                    locked.append(new)
                    print("random picK:",new)
                    if(len(locked)==SIZE*SIZE):
                        _,standStill1,_=processMovement(locked,pygame.K_RIGHT)
                        _,standStill2,_=processMovement(locked,pygame.K_LEFT)
                        _,standStill3,_=processMovement(locked,pygame.K_UP)
                        _,standStill4,_=processMovement(locked,pygame.K_DOWN)
                        _GameOver = standStill1 or standStill2 or standStill3 or standStill4


            if event.key == pygame.K_a:
                msg = "'A'Key pressed"
                print("'A'Key pressed")
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    if action:
        for i in locked[:-1]:
            drawBox(i,grey)

        drawBox(locked[-1],gold)

    pygame.display.update()
    fpsClock.tick(30)