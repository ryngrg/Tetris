import random
import pygame
pygame.init()

linesCleared=0

pygame.mixer.music.load('TetrisMusic.mp3')
pygame.mixer.music.play(-1)

display_width = 500
display_height = 650

currentpiece=0
score=0

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Tetris')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,225,0)
grey = (128,128,128)
pink = (255,0,255)
orange = (255,128,0)
cyan = (0,255,255)

clock = pygame.time.Clock()

def dispGrid():
    for i in range(1,10):
        pygame.draw.line(gameDisplay, black, (30*i,0), (30*i,600),1)
    pygame.draw.line(gameDisplay, black, (300,0), (300,600),2)
    for i in range(1,20):
        pygame.draw.line(gameDisplay, black, (0,30*i), (300,30*i),1)
    pygame.draw.line(gameDisplay, black, (0,600), (300,600),2)

board=[]
for i in range(20):
    board.append([0,0,0,0,0,0,0,0,0,0])

def dispBoard():
    for i in range(20):
        for j in range(10):
            if board[i][j]==1:
                pygame.draw.rect(gameDisplay, grey, (30*j,30*i,30,30))
            elif board[i][j]==2:
                pygame.draw.rect(gameDisplay, red, (30*j,30*i,30,30))
            elif board[i][j]==3:
                pygame.draw.rect(gameDisplay, yellow, (30*j,30*i,30,30))
            elif board[i][j]==4:
                pygame.draw.rect(gameDisplay, blue, (30*j,30*i,30,30))
            elif board[i][j]==5:
                pygame.draw.rect(gameDisplay, green, (30*j,30*i,30,30))
            elif board[i][j]==6:
                pygame.draw.rect(gameDisplay, pink, (30*j,30*i,30,30))
            elif board[i][j]==7:
                pygame.draw.rect(gameDisplay, orange, (30*j,30*i,30,30))
            elif board[i][j]==8:
                pygame.draw.rect(gameDisplay, cyan, (30*j,30*i,30,30))

pieces=[2,3,4,5,6,7,8,2,3,4,5,6,7,8]
random.shuffle(pieces)

def newpiece():
    global pieces
    if pieces==[]:
        pieces=[2,3,4,5,6,7,8,2,3,4,5,6,7,8]
        random.shuffle(pieces)
    piece = pieces.pop()
    global currentpiece
    currentpiece = piece
    a = random.randint(0,7)
    if piece==2: # square
        board[0][a]=board[0][a+1]=board[1][a]=board[1][a+1]=2
    elif piece==3: # T
        board[0][a]=board[1][a]=board[1][a+1]=board[2][a]=3
    elif piece==4: # L
        board[1][a]=board[1][a+1]=board[1][a+2]=board[0][a+2]=4
    elif piece==5: # inverted L
        board[1][a]=board[1][a+1]=board[1][a+2]=board[0][a]=5
    elif piece==6: # line
        board[0][a+1]=board[1][a+1]=board[2][a+1]=board[3][a+1]=6
    elif piece==7: # Z
        board[0][a]=board[0][a+1]=board[1][a+1]=board[1][a+2]=7
    elif piece==8: # S
        board[0][a+2]=board[0][a+1]=board[1][a+1]=board[1][a]=8

def moveDown():
    freepiece = False
    for i in range(20):
        for j in range(10):
            if board[i][j]>1:
                freepiece = True
    if not(freepiece):
        newpiece()
    else:
        movable = True
        for x in board[19]:
            if x>1:
                movable = False
        for i in reversed(range(20)):
            for j in range(10):
                if (board[i][j]==1)and(board[i-1][j]>1):
                    movable = False
        if movable:
            for i in reversed(range(1,20)):
                for j in range(10):
                    if (board[i][j]==0)and(board[i-1][j]>1):
                        board[i][j],board[i-1][j] = board[i-1][j],board[i][j]
        else:
            for i in range(20):
                for j in range(10):
                    if board[i][j]!=0:
                        board[i][j]=1
                    
def xmvmt(direction):
    if direction=='r':
        for i in range(20):
            if board[i][9]>1:
                return None
        movable = True    
        for i in range(20):
            if movable==False:
                break
            for j in range(9):
                if (board[i][j]>1)and(board[i][j+1]==1):
                    movable = False
                    break    
        if movable:
            for j in reversed(range(1,10)):
                for i in range(20):
                    if (board[i][j]==0)and(board[i][j-1]>1):
                        board[i][j],board[i][j-1]=board[i][j-1],board[i][j]
    elif direction=='l':
        for i in range(20):
            if board[i][0]>1:
                return None
        movable = True    
        for i in range(20):
            if movable==False:
                break
            for j in range(1,10):
                if (board[i][j]>1)and(board[i][j-1]==1):
                    movable = False
                    break    
        if movable:
            for j in range(9):
                for i in range(20):
                    if (board[i][j]==0)and(board[i][j+1]>1):
                        board[i][j],board[i][j+1]=board[i][j+1],board[i][j]

def drop():
    go = False
    for i in range(20):
        for j in range(10):
            if board[i][j]>1:
                go = True
    if not go:
        return None
    moved= True
    while moved:
        movable = True
        for x in board[19]:
            if x>1:
                movable = False
        for i in reversed(range(20)):
            for j in range(10):
                if (board[i][j]==1)and(board[i-1][j]>1):
                    movable = False
        if movable:
            for i in reversed(range(1,20)):
                for j in range(10):
                    if (board[i][j]==0)and(board[i-1][j]>1):
                        board[i][j],board[i-1][j] = board[i-1][j],board[i][j]
        else:
            moved = False
            for i in range(20):
                for j in range(10):
                    if board[i][j]!=0:
                        board[i][j]=1

def clearline():
    global linesCleared
    global score
    n=0
    for i in range(20):
        if board[i]==[1,1,1,1,1,1,1,1,1,1]:
            linesCleared+=1
            n+=1
            for j in reversed(range(1,i+1)):
                board[j]=board[j-1]
            board[0]=[0,0,0,0,0,0,0,0,0,0]
    score+=(n*n*100)

def rotate():
    global board
    if currentpiece<3:
        return None
    elif currentpiece==3:
        for i in range(1,19):
            if board[i].count(3)==3:
                y = board[i].index(3)+1
                if (board[i+1][y]==3)and(board[i-1][y]==0):
                    board[i-1][y]=3
                    board[i][y+1]=0
                elif (board[i-1][y]==3)and(board[i+1][y]==0):
                    board[i+1][y]=3
                    board[i][y-1]=0
                return None
        for j in range(1,9):
            col = [board[i][j] for i in range(20)]
            if col.count(3)==3:
                x = col.index(3)+1
                if (board[x][j+1]==3)and(board[x][j-1]==0):
                    board[x][j-1]=3
                    board[x-1][j]=0
                elif (board[x][j-1]==3)and(board[x][j+1]==0):
                    board[x][j+1]=3
                    board[x+1][j]=0
                return None
    elif currentpiece==4:
        for i in range(1,19):
            if board[i].count(4)==3:
                y = board[i].index(4)+1
                if board[i+1][y-1]==4:
                    if (board[i-1][y-1]==0)and(board[i-1][y]==0)and(board[i+1][y]==0):
                        board[i-1][y-1]=4
                        board[i-1][y]=4
                        board[i+1][y]=4
                        board[i][y-1]=0
                        board[i][y+1]=0
                        board[i+1][y-1]=0
                elif board[i-1][y+1]==4:
                    if (board[i-1][y]==0)and(board[i+1][y]==0)and(board[i+1][y+1]==0):
                        board[i-1][y]=4
                        board[i+1][y]=4
                        board[i+1][y+1]=4
                        board[i][y-1]=0
                        board[i][y+1]=0
                        board[i-1][y+1]=0
                return None
        for j in range(1,9):
            col = [board[i][j] for i in range(20)]
            if col.count(4)==3:
                x=col.index(4)+1
                if board[x-1][j-1]==4:
                    if (board[x][j-1]==0)and(board[x][j+1]==0)and(board[x-1][j+1]==0):
                        board[x][j-1]=4
                        board[x][j+1]=4
                        board[x-1][j+1]=4
                        board[x-1][j]=0
                        board[x+1][j]=0
                        board[x-1][j-1]=0
                elif board[x+1][j+1]==4:
                    if (board[x][j-1]==0)and(board[x][j+1]==0)and(board[x+1][j-1]==0):
                        board[x][j-1]=4
                        board[x][j+1]=4
                        board[x+1][j-1]=4
                        board[x-1][j]=0
                        board[x+1][j]=0
                        board[x+1][j+1]=0
                return None
    elif currentpiece==5:
        for i in range(1,19):
            if board[i].count(5)==3:
                y = board[i].index(5)+1
                if board[i-1][y-1]==5:
                    if (board[i-1][y+1]==0)and(board[i-1][y]==0)and(board[i+1][y]==0):
                        board[i-1][y+1]=5
                        board[i-1][y]=5
                        board[i+1][y]=5
                        board[i][y-1]=0
                        board[i][y+1]=0
                        board[i-1][y-1]=0
                elif board[i+1][y+1]==5:
                    if (board[i-1][y]==0)and(board[i+1][y]==0)and(board[i+1][y-1]==0):
                        board[i-1][y]=5
                        board[i+1][y]=5
                        board[i+1][y-1]=5
                        board[i][y-1]=0
                        board[i][y+1]=0
                        board[i+1][y+1]=0
                return None
        for j in range(1,9):
            col = [board[i][j] for i in range(20)]
            if col.count(5)==3:
                x=col.index(5)+1
                if board[x-1][j+1]==5:
                    if (board[x][j-1]==0)and(board[x][j+1]==0)and(board[x+1][j+1]==0):
                        board[x][j-1]=5
                        board[x][j+1]=5
                        board[x+1][j+1]=5
                        board[x-1][j]=0
                        board[x+1][j]=0
                        board[x-1][j+1]=0
                elif board[x+1][j-1]==5:
                    if (board[x][j-1]==0)and(board[x][j+1]==0)and(board[x-1][j-1]==0):
                        board[x][j-1]=5
                        board[x][j+1]=5
                        board[x-1][j-1]=5
                        board[x-1][j]=0
                        board[x+1][j]=0
                        board[x+1][j-1]=0
                return None
    elif currentpiece==6:
        for i in range(2,19):
            if board[i].count(6)==4:
                y = board[i].index(6)+1
                if (board[i-2][y]==0)and(board[i-1][y]==0)and(board[i+1][y]==0):
                    board[i-2][y]=6
                    board[i-1][y]=6
                    board[i+1][y]=6
                    board[i][y-1]=0
                    board[i][y+1]=0
                    board[i][y+2]=0
                return None
        for j in range(1,9):
            col = [board[i][j] for i in range(20)]
            if col.count(6)==4:
                x = col.index(6)+2
                if (j==1)and(board[x-1][j-1]==0)and(board[x-1][j+1]==0)and(board[x-2][j+2]==0):
                    board[x-1][j-1]=6
                    board[x-1][j+1]=6
                    board[x-1][j+2]=6
                    board[x-2][j]=0
                    board[x][j]=0
                    board[x+1][j]=0
                elif (board[x][j-2]==0)and(board[x][j-1]==0)and(board[x][j+1]==0):
                    board[x][j-2]=6
                    board[x][j-1]=6
                    board[x][j+1]=6
                    board[x-2][j]=0
                    board[x-1][j]=0
                    board[x+1][j]=0
                return None
    elif currentpiece==7:
        for i in range(1,19):
            if (board[i].count(7)==2)and(board[i-1].count(7)==1)and(board[i+1].count(7)==1):
                y = board[i].index(7)
                if (y==0)and(board[i+1][1]==0)and(board[i+1][2]==0):
                    board[i+1][1]=7
                    board[i+1][2]=7
                    board[i+1][0]=0
                    board[i-1][1]=0
                elif (board[i-1][y]==0)and(board[i-1][y-1]==0):
                    board[i-1][y]=7
                    board[i-1][y-1]=7
                    board[i+1][y]=0
                    board[i-1][y+1]=0
                return None
        cols = [[board[i][j] for i in range(20)]for j in range(10)]
        for i in range(1,9):
            if (cols[i].count(7)==2)and(cols[i-1].count(7)==1)and(cols[i+1].count(7)==1):
                x = cols[i].index(7)
                if (x==0)and(board[0][i+1]==0)and(board[2][i]==0):
                    board[0][i+1]=7
                    board[2][i]=7
                    board[0][i-1]=0
                    board[0][i]=0
                elif (board[x-1][i]==0)and(board[x+1][i-1]==0):
                    board[x-1][i]=7
                    board[x+1][i-1]=7
                    board[x+1][i]=0
                    board[x+1][i+1]=0
                return None
    elif currentpiece==8:
        for i in range(1,19):
            if (board[i].count(8)==2)and(board[i-1].count(8)==1)and(board[i+1].count(8)==1):
                y = board[i].index(8)
                if (y==0)and(board[i-1][1]==0)and(board[i-1][2]==0):
                    board[i-1][1]=8
                    board[i-1][2]=8
                    board[i-1][0]=0
                    board[i+1][1]=0
                elif (board[i+1][y]==0)and(board[i+1][y-1]==0):
                    board[i+1][y]=8
                    board[i+1][y-1]=8
                    board[i-1][y]=0
                    board[i+1][y+1]=0
                return None
        cols = [[board[i][j] for i in range(20)]for j in range(10)]
        for i in range(1,9):
            if (cols[i].count(8)==2)and(cols[i-1].count(8)==1)and(cols[i+1].count(8)==1):
                x = cols[i].index(8)
                if (x==0)and(board[0][i-1]==0)and(board[2][i]==0):
                    board[0][i-1]=8
                    board[2][i]=8
                    board[0][i+1]=0
                    board[0][i]=0
                elif (board[x-1][i]==0)and(board[x+1][i+1]==0):
                    board[x-1][i]=8
                    board[x+1][i+1]=8
                    board[x+1][i]=0
                    board[x+1][i-1]=0
                return None

t=0
largeText = pygame.font.Font('freesansbold.ttf',15)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xmvmt('l')
            if event.key == pygame.K_RIGHT:
                xmvmt('r')
            if event.key == pygame.K_DOWN:
                drop()
            if event.key == pygame.K_UP:
                rotate()
    gameDisplay.fill(white)
    if (t>18000)and(t%10==0):
        moveDown()
    elif t%(30-int(t/900))==0:
        moveDown()
    clearline()
    dispBoard()
    dispGrid()
    txt="Score: "+str(score)+" Lines cleared: "+str(linesCleared)
    TextSurf = largeText.render(txt, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = (150,625)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    if 1 in board[0]:
        print("\ngame over,\nLines cleared:", linesCleared)
        print("Score:", score, "\n")
        break;
    t+=1
    clock.tick(30)
pygame.quit()
