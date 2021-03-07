import random
import pygame
import copy
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

def dispBoard(board):
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

def newpiece(board, piece=None):
    global pieces
    if pieces==[]:
        pieces=[2,3,4,5,6,7,8,2,3,4,5,6,7,8]
        random.shuffle(pieces)
    if piece==None:
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

def moveDown(board):
    freepiece = False
    for i in range(20):
        for j in range(10):
            if board[i][j]>1:
                freepiece = True
    if not(freepiece):
        newpiece(board)
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
            global currentpiece
            currentpiece=0
                    
def xmvmt(direction, board):
    if direction=='r':
        for i in range(20):
            if board[i][9]>1:
                return 0
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
        else:
            return 0
    elif direction=='l':
        for i in range(20):
            if board[i][0]>1:
                return 0
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
        else:
            return 0

def drop(board):
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

def clearline(board):
    n=0
    for i in range(20):
        if board[i]==[1,1,1,1,1,1,1,1,1,1]:
            n+=1
            for j in reversed(range(1,i+1)):
                board[j]=board[j-1]
            board[0]=[0,0,0,0,0,0,0,0,0,0]
    return n

def rotate(board):
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

def evalboard(bd):
    rating = 0
    holepenality=60
    heighpenality=3
    bumpinesspenality=2
    for j in range(10):
        emp=False
        for i in range(20):
            if bd[i][j]==1:
                emp=True
                continue
            if emp:
                rating+=holepenality
    for i in range(20):
        rating+=(bd[i].count(1)*(19-i)*heighpenality)
##    if 1 in bd[10]:
##        bumpinesspenality=10
    j=0
    while (j<19)and(board[j][0]==0):
        j+=1
    h=j
    for i in range(1,10):
        j=0
        while (j<19)and(board[j][i]==0):
            j+=1
        rating+=abs(j-h)*bumpinesspenality
        h=j
    return rating

def aiplay(board):
    moves=[]
    if currentpiece==0:
        return moves
    
    if currentpiece ==2:
        testboard=[copy.deepcopy(board)]
        lef=0
        while True:
            testboard.insert(0,copy.deepcopy(testboard[0]))
            t=xmvmt('l',testboard[0])
            if t==0:
                testboard.pop(0)
                break
            lef+=1
        while True:
            testboard.append(copy.deepcopy(testboard[-1]))
            t=xmvmt('r',testboard[-1])
            if t==0:
                testboard.pop(-1)
                break

        drop(testboard[0])
        n = clearline(testboard[0])
        best = evalboard(testboard[0])
        choice = 0
        for i in range(1, len(testboard)):
            drop(testboard[i])
            n = clearline(testboard[i])
            eb = evalboard(testboard[i])
            if eb<best:
                best = eb
                choice = i

        if choice == lef:
            moves=['d']
        elif choice<lef:
            for i in range(lef-choice):
                moves.append('l')
            moves.append('d')
        else:
            for i in range(choice-lef):
                moves.append('r')
            moves.append('d')
        return moves

    if currentpiece in [3,4,5]:
        testboard1=[copy.deepcopy(board)]
        testboard2=[copy.deepcopy(board)]
        rotate(testboard2[0])
        testboard3=[copy.deepcopy(board)]
        rotate(testboard3[0])
        rotate(testboard3[0])
        testboard4=[copy.deepcopy(board)]
        rotate(testboard4[0])
        rotate(testboard4[0])
        rotate(testboard4[0])

        lef1=0
        while True:
            testboard1.insert(0,copy.deepcopy(testboard1[0]))
            t=xmvmt('l',testboard1[0])
            if t==0:
                testboard1.pop(0)
                break
            lef1+=1
        while True:
            testboard1.append(copy.deepcopy(testboard1[-1]))
            t=xmvmt('r',testboard1[-1])
            if t==0:
                testboard1.pop(-1)
                break

        lef2=0
        while True:
            testboard2.insert(0,copy.deepcopy(testboard2[0]))
            t=xmvmt('l',testboard2[0])
            if t==0:
                testboard2.pop(0)
                break
            lef2+=1
        while True:
            testboard2.append(copy.deepcopy(testboard2[-1]))
            t=xmvmt('r',testboard2[-1])
            if t==0:
                testboard2.pop(-1)
                break

        lef3=0
        while True:
            testboard3.insert(0,copy.deepcopy(testboard3[0]))
            t=xmvmt('l',testboard3[0])
            if t==0:
                testboard3.pop(0)
                break
            lef3+=1
        while True:
            testboard3.append(copy.deepcopy(testboard3[-1]))
            t=xmvmt('r',testboard3[-1])
            if t==0:
                testboard3.pop(-1)
                break

        lef4=0
        while True:
            testboard4.insert(0,copy.deepcopy(testboard4[0]))
            t=xmvmt('l',testboard4[0])
            if t==0:
                testboard4.pop(0)
                break
            lef4+=1
        while True:
            testboard4.append(copy.deepcopy(testboard4[-1]))
            t=xmvmt('r',testboard4[-1])
            if t==0:
                testboard4.pop(-1)
                break

        drop(testboard1[0])
        n = clearline(testboard1[0])
        best1 = evalboard(testboard1[0])
        choice1 = 0
        for i in range(1, len(testboard1)):
            drop(testboard1[i])
            n = clearline(testboard1[i])
            eb = evalboard(testboard1[i])
            if eb<best1:
                best1 = eb
                choice1 = i

        drop(testboard2[0])
        n = clearline(testboard2[0])
        best2 = evalboard(testboard2[0])
        choice2 = 0
        for i in range(1, len(testboard2)):
            drop(testboard2[i])
            n = clearline(testboard2[i])
            eb = evalboard(testboard2[i])
            if eb<best2:
                best2 = eb
                choice2 = i

        drop(testboard3[0])
        n = clearline(testboard3[0])
        best3 = evalboard(testboard3[0])
        choice3 = 0
        for i in range(1, len(testboard3)):
            drop(testboard3[i])
            n = clearline(testboard3[i])
            eb = evalboard(testboard3[i])
            if eb<best3:
                best3 = eb
                choice3 = i

        drop(testboard4[0])
        n = clearline(testboard4[0])
        best4 = evalboard(testboard4[0])
        choice4 = 0
        for i in range(1, len(testboard4)):
            drop(testboard4[i])
            n = clearline(testboard4[i])
            eb = evalboard(testboard4[i])
            if eb<best4:
                best4 = eb
                choice4 = i

        if (best1 <= best2)and(best1 <= best3)and(best1 <= best4):
            if choice1 == lef1:
                moves=['d']
            elif choice1<lef1:
                for i in range(lef1-choice1):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice1-lef1):
                    moves.append('r')
                moves.append('d')
        elif (best2 <= best1)and(best2 <= best3)and(best2 <= best4):
            moves=['u']
            if choice2 == lef2:
                moves.append('d')
            elif choice2<lef2:
                for i in range(lef2-choice2):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice2-lef2):
                    moves.append('r')
                moves.append('d')
        elif (best3 <= best1)and(best3 <= best2)and(best3 <= best4):
            moves=['u','u']
            if choice3 == lef3:
                moves.append('d')
            elif choice3<lef3:
                for i in range(lef3-choice3):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice3-lef3):
                    moves.append('r')
                moves.append('d')
        else:
            moves=['u','u','u']
            if choice4 == lef4:
                moves.append('d')
            elif choice4<lef4:
                for i in range(lef4-choice4):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice4-lef4):
                    moves.append('r')
                moves.append('d')
        return moves

    if currentpiece in [6,7,8]:
        testboard1=[copy.deepcopy(board)]
        testboard2=[copy.deepcopy(board)]
        rotate(testboard2[0])

        lef1=0
        while True:
            testboard1.insert(0,copy.deepcopy(testboard1[0]))
            t=xmvmt('l',testboard1[0])
            if t==0:
                testboard1.pop(0)
                break
            lef1+=1
        while True:
            testboard1.append(copy.deepcopy(testboard1[-1]))
            t=xmvmt('r',testboard1[-1])
            if t==0:
                testboard1.pop(-1)
                break

        lef2=0
        while True:
            testboard2.insert(0,copy.deepcopy(testboard2[0]))
            t=xmvmt('l',testboard2[0])
            if t==0:
                testboard2.pop(0)
                break
            lef2+=1
        while True:
            testboard2.append(copy.deepcopy(testboard2[-1]))
            t=xmvmt('r',testboard2[-1])
            if t==0:
                testboard2.pop(-1)
                break

        drop(testboard1[0])
        n = clearline(testboard1[0])
        best1 = evalboard(testboard1[0])
        choice1 = 0
        for i in range(1, len(testboard1)):
            drop(testboard1[i])
            n = clearline(testboard1[i])
            eb = evalboard(testboard1[i])
            if eb<best1:
                best1 = eb
                choice1 = i

        drop(testboard2[0])
        n = clearline(testboard2[0])
        best2 = evalboard(testboard2[0])
        choice2 = 0
        for i in range(1, len(testboard2)):
            drop(testboard2[i])
            n = clearline(testboard2[i])
            eb = evalboard(testboard2[i])
            if eb<best2:
                best2 = eb
                choice2 = i

        if best1 <= best2:
            if choice1 == lef1:
                moves=['d']
            elif choice1<lef1:
                for i in range(lef1-choice1):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice1-lef1):
                    moves.append('r')
                moves.append('d')
        else:
            moves=['u']
            if choice2 == lef2:
                moves.append('d')
            elif choice2<lef2:
                for i in range(lef2-choice2):
                    moves.append('l')
                moves.append('d')
            else:
                for i in range(choice2-lef2):
                    moves.append('r')
                moves.append('d')
        return moves

textFont = pygame.font.Font('freesansbold.ttf',15)
rightSurf=[]
rightRect=[]
rightpanel=["CONTROLS","(Arrow keys)","left: move left","right: move right" ,"up: rotate piece","down: hard drop"]
for i in range(len(rightpanel)):
    rightSurf += [textFont.render(rightpanel[i], True, black)]
    rightRect += [rightSurf[i].get_rect()]
    rightRect[i].center = (400,18*i+30)

pieces=[2,3,4,5,6,7,8,2,3,4,5,6,7,8]
random.shuffle(pieces)

board=[]
for i in range(20):
    board.append([0,0,0,0,0,0,0,0,0,0])

t=0
while True:
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            pygame.quit()
##            quit()
##        if event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_LEFT:
##                xmvmt('l',board)
##            if event.key == pygame.K_RIGHT:
##                xmvmt('r',board)
##            if event.key == pygame.K_DOWN:
##                drop(board)
##                currentpiece=0
##            if event.key == pygame.K_UP:
##                rotate(board)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    moves = aiplay(board)
    while len(moves)>0:
        ev=moves.pop(0)
        if ev=='l':
            xmvmt('l',board)
        elif ev=='r':
            xmvmt('r',board)
        elif ev=='d':
            drop(board)
            currentpiece=0                
        elif ev=='u':
            rotate(board)
        
    gameDisplay.fill(white)
    if (t%20)==0:
        moveDown(board)
##    if (t>18000)and(t%10==0):
##        moveDown(board)
##    elif t%(30-int(t/900))==0:
##        moveDown(board)

    num = clearline(board)
    linesCleared += num
    score += num*num*100
    dispBoard(board)
    dispGrid()
    
    scoreText="Score: "+str(score)+" Lines cleared: "+str(linesCleared)
    scoreTextSurf = textFont.render(scoreText, True, black)
    scoreTextRect = scoreTextSurf.get_rect()
    scoreTextRect.center = (150,625)
    gameDisplay.blit(scoreTextSurf, scoreTextRect)
    for i in range(len(rightpanel)):
        gameDisplay.blit(rightSurf[i], rightRect[i])
    pygame.display.update()

    if 1 in board[0]:
        print("\ngame over!\nLines cleared:", linesCleared)
        print("Score:", score, "\n")
        break;
    t+=1
    clock.tick(30)
pygame.quit()
