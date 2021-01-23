class Display:
	def __init__(self, displayWidth, displayHeight, color, scale): # Add difference for if you are white/black
		self.dispWidth = displayWidth
		self.dispHeight = displayHeight
		
		self.dispSurface = pygame.display.set_mode((displayWidth,displayHeight))
		self.colour = color
		self.dispSurface.fill(color)
		self.scale = scale
		pygame.display.update()
		
	def giveAssets(self, images):
		self.assets = images
		self.sizeOfTile = (self.assets[0].get_width() - 4 * self.scale) / 8
		self.startX = 2 * self.scale
		self.startY = 2 * self.scale
		
	def drawBoard(self):
		self.dispSurface.blit(self.assets[0], (0,0)) # Board
		self.dispSurface.blit(self.assets[1], (self.assets[0].get_width(), self.assets[0].get_height()/6/self.scale)) # Numbers
		self.dispSurface.blit(self.assets[2], (self.assets[0].get_height()/6/self.scale, self.assets[0].get_height())) # Letters
		
	def drawPieces(self, positions):		
		pieces = positions.keys()
		for pieceIndex in pieces: # Loops through every type of piece (ex. white king, black king, ...)
			for position in positions[pieceIndex]: # Loops through every position of said piece
				image = self.assets[int(pieceIndex) + 3]
				dispX = position[0]*self.sizeOfTile + self.startX + (self.sizeOfTile - image.get_width())/2 # first term is positioning it on the desired tile, second/third term makes sure piece is in the middle
				dispY = (7-position[1])*self.sizeOfTile + self.startY / 2 + (self.sizeOfTile - image.get_height())
				self.dispSurface.blit(image, (dispX,dispY))
		
		pygame.display.update()
	def showPositions(self, tiles, colour):
		for tile in tiles: # Display all tiles you can go to
			x = tile[0]
			y = 7 - tile[1]
			# Draw does not do alpha values :(
			#pygame.draw.rect(self.dispSurface, colour, (x*self.sizeOfTile + self.startX, y*self.sizeOfTile + self.startY, self.sizeOfTile, self.sizeOfTile))
			s = pygame.Surface((self.sizeOfTile,self.sizeOfTile), pygame.SRCALPHA) # Size of rect, look for alpha values
			s.fill(colour) # Set colour
			self.dispSurface.blit(s, (x*self.sizeOfTile + self.startX, y*self.sizeOfTile + self.startY))
		
		pygame.display.update()
	def getPressed(self):
		return pygame.mouse.get_pos()
	def getTilePressed(self):
		pos = self.getPressed()
		return (int((pos[0] - self.startX) // self.sizeOfTile), int(7 - ((pos[1] - self.startY) // self.sizeOfTile)))

class ChessGame:
	def __init__(self):
		#initPositions = [[(4,0)]]
		#				kings						queens					rooks										bishops									knights										pawns
		self.positions = {"0": [(4,0)], "6": [(4,7)], "1": [(3,0)], "7": [(3,7)], "2": [(0,0),(7,0)], "8": [(0,7),(7,7)], "3": [(2,0),(5,0)], "9": [(2,7),(5,7)], "4": [(1,0),(6,0)], "10": [(1,7),(6,7)], "5": [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)], "11": [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]}
		self.grid = [["-1" for i in range(8)] for j in range(8)]
		for piece in self.positions.keys():
			for position in self.positions[piece]:
				self.grid[position[1]][position[0]] = piece
		self.numPiecesPerTeam = 6
		#print(self.grid)
		
		self.repeatPieces = ["1","7","2","8","3","9"]
		self.kings = ["0", "6"]
		self.pawns = ["5", "11"]
		self.pieceMove = {"0": [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)], "6": [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)], 
		"1": [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)], "7": [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)], 
		"2": [(0,-1), (-1,0), (1,0), (0,1)], "8": [(0,-1), (-1,0), (1,0), (0,1)], "3": [(-1,-1), (1,-1), (-1,1), (1,1)], "9": [(-1,-1), (1,-1), (-1,1), (1,1)], 
		"4": [(-2,-1), (-1,-2), (2,-1), (1,-2), (-2,1), (-1,2), (2,1), (1,2)], "10": [(-2,-1), (-1,-2), (2,-1), (1,-2), (-2,1), (-1,2), (2,1), (1,2)], 
		"5": [(0,1), (0,2), (1,1), (-1,1)], "11": [(0,-1), (0,-2), (1,-1), (-1,-1)]}
		self.piecesUnmoved = self.positions['0'] + self.positions['6'] + self.positions['2'] + self.positions['8'] + self.positions['5'] + self.positions['11'] # Rooks, kings and pawns unmoved (for castling and double-pushing)

	def getPositions(self):
		return self.positions
		
	def positionAfterMove(self, positionBefore, positionAfter):
		# INCOMPLETE: Make a function that returns the arrays where a piece will end up. Have a second function actually make changes
		piece = self.grid[positionBefore[1]][positionBefore[0]]
		otherPiece = self.grid[positionAfter[1]][positionAfter[0]]
		self.grid[positionBefore[1]][positionBefore[0]] = "-1"
		self.grid[positionAfter[1]][positionAfter[0]] = piece
		self.positions[piece].remove(positionBefore)
		self.positions[piece].append(positionAfter)
		if otherPiece != "-1":
			self.positions[otherPiece].remove(positionAfter)
		if positionBefore in self.piecesUnmoved:
			self.piecesUnmoved.remove(positionBefore)
		if positionAfter in self.piecesUnmoved:
			self.piecesUnmoved.remove(positionAfter)
		if piece in self.pawns:
			if positionAfter[1] == 0 or positionAfter[1] == 7:
				promotion(positionAfter, int(piece) < self.numPiecesPerTeam) # where, which team
	
	def movePiece(self, positionBefore, positionAfter):
		piece = self.grid[positionBefore[1]][positionBefore[0]]
		otherPiece = self.grid[positionAfter[1]][positionAfter[0]]
		self.grid[positionBefore[1]][positionBefore[0]] = "-1"
		self.grid[positionAfter[1]][positionAfter[0]] = piece
		self.positions[piece].remove(positionBefore)
		self.positions[piece].append(positionAfter)
		if otherPiece != "-1":
			self.positions[otherPiece].remove(positionAfter)
		if positionBefore in self.piecesUnmoved:
			self.piecesUnmoved.remove(positionBefore)
		if positionAfter in self.piecesUnmoved:
			self.piecesUnmoved.remove(positionAfter)
		if piece in self.pawns:
			if positionAfter[1] == 0 or positionAfter[1] == 7:
				promotion(positionAfter, int(piece) < self.numPiecesPerTeam) # where, which team
	
	def promote(self, position, piece):
		#INCOMPLETE
		print("PROMOTION!")
		
	def attacked(self, position, team):
		#INCOMPLETE
		# Returns True if the Tile is in "Check"
		#for piece in (self.positions[str(enemyTeam)] + self.positions[str(enemyTeam + 1)] + self.positions[str(enemyTeam) + 2] + self.positions[str(enemyTeam + 3)] + self.positions[str(enemyTeam) + 4] + self.positions[str(enemyTeam + 5)]) # For every enemy piece
		
		# Attacked by KING
		relevantPos = self.positions[str(team)][0] # king Position
		if position[0] - 2 < relevantPos[0] < position[0] + 2 and position[1] - 2 < relevantPos[1] < position[1] + 2:
			return True
		# Attacked by PAWN
		relevantPositions = self.positions[str(team + 5)] # Pawn positions
		for relevantPos in relevantPositions: # Pawn positions
			if (position[0] == relevantPos[0] - 1 or position[0] == relevantPos[0] +1): # Right x-cords
				if team == 6: 													
					if position[1] == relevantPos[1] - 1:
						return True
				else:
					if position[1] == relevantPos[1] + 1:
						return True
		# NOTE: All the following do not "Check" a position if an allied piece is in it.
		# Attacked by KNIGHTS
		relevantPositions = self.positions[str(team + 4)] # Knight positions
		for relevantPos in relevantPositions: # Knight positions
			moves = self.pieceMoves(relevantPos)
			if position in moves:
				return True
		# Attacked by BISHOPS
		relevantPositions = self.positions[str(team + 3)] # Bishop positions
		for relevantPos in relevantPositions: # Bishop positions
			moves = self.pieceMoves(relevantPos)
			if position in moves:
				return True
		# Attacked by ROOKS
		relevantPositions = self.positions[str(team + 2)] # Rook positions
		for relevantPos in relevantPositions: # Rook positions
			moves = self.pieceMoves(relevantPos)
			if position in moves:
				return True
		# Attacked by QUEENS
		relevantPositions = self.positions[str(team + 1)] # Queen positions
		for relevantPos in relevantPositions: # Queen positions
			moves = self.pieceMoves(relevantPos)
			if position in moves:
				return True
		return False
	
	def pieceMoves(self, position):
		positionsToGo = []
		piece = self.grid[position[1]][position[0]]
		pieceTeamBonus = (int(piece) // self.numPiecesPerTeam) * self.numPiecesPerTeam # 6
		print("Team:", pieceTeamBonus)
		# If not in Check
		
		if piece != "-1":
			if piece in self.repeatPieces: # QUEEN/ROOK/BISHOP
				# If not entering check
				moves = self.pieceMove[piece]
				for move in moves:
					for i in range(1,8):
						consideredTile = (position[0] + move[0] * i, position[1] + move[1] * i)
						if (0 <= consideredTile[0] <= 7) and (0 <= consideredTile[1] <= 7): # If in the board
							if not(pieceTeamBonus <= int(self.grid[consideredTile[1]][consideredTile[0]]) < pieceTeamBonus + self.numPiecesPerTeam): # If tile is not ocupied by a team piece
								positionsToGo.append((consideredTile[0], consideredTile[1]))
								if (6 - pieceTeamBonus) <= int(self.grid[consideredTile[1]][consideredTile[0]]) <= (6 - pieceTeamBonus + self.numPiecesPerTeam): # If tile is occupied by an enemy piece
									break
							else:
								break
				print("Repeat Piece:", positionsToGo)
				return positionsToGo
			elif piece in self.kings: # KING
				# If position to go in is not in check
				moves = self.pieceMove[piece]
				for move in moves:
					consideredTile = (position[0] + move[0], position[1] + move[1])
					if (0 <= consideredTile[0] <= 7) and (0 <= consideredTile[1] <= 7): # If in the board
						if not(pieceTeamBonus <= int(self.grid[consideredTile[1]][consideredTile[0]]) < pieceTeamBonus + self.numPiecesPerTeam): # If tile is not ocupied by a team piece
							positionsToGo.append((consideredTile[0], consideredTile[1]))
				# Castling #INCOMPLETE: If not passing through check
				if position in self.piecesUnmoved:
					# Queenside
					if ((0, position[1]) in self.piecesUnmoved): # If queenside rook unmoved
						if self.grid[position[1]][1] == "-1" and self.grid[position[1]][2] == "-1" and self.grid[position[1]][3] == "-1" and not(self.attacked((2,position[1]), pieceTeamBonus)) and not(self.attacked((3,position[1]), pieceTeamBonus)) and not(self.attacked((4,position[1]), pieceTeamBonus)):
							positionsToGo.append((position[0]-2, position[1]))
					if (7, position[1]) in self.piecesUnmoved:
						if self.grid[position[1]][6] == "-1" and self.grid[position[1]][5] == "-1" and not(self.attacked((6,position[1]), pieceTeamBonus)) and not(self.attacked((5,position[1]), pieceTeamBonus)) and not(self.attacked((4,position[1]), pieceTeamBonus)):
							positionsToGo.append((position[0]+2, position[1]))
				print("King", positionsToGo)
				return positionsToGo
			elif piece in self.pawns: # PAWN
				# En Passant (I hope this is spelled right :))
				# If not entering check
				# Promoting
				moves = self.pieceMove[piece]
				blocked = True
				# Single Push
				move = moves[0]
				consideredTile = (position[0] + move[0], position[1] + move[1])
				if self.grid[consideredTile[1]][consideredTile[0]] == "-1":
					blocked = False
					positionsToGo.append((consideredTile[0],consideredTile[1]))
				# Double Push
				if position in self.piecesUnmoved:
					move = moves[1]
					consideredTile = (position[0] + move[0], position[1] + move[1])
					print("PING:", self.piecesUnmoved)
					if self.grid[consideredTile[1]][consideredTile[0]] == "-1" and not(blocked):
						positionsToGo.append((consideredTile[0],consideredTile[1]))
				# Take Diagonals
				for i in range(2,4):
					move = moves[i]
					consideredTile = (position[0] + move[0], position[1] + move[1])
					if (0 <= consideredTile[0] <= 7) and (0 <= consideredTile[1] <= 7): # If in the board
						if (6 - pieceTeamBonus) <= int(self.grid[consideredTile[1]][consideredTile[0]]) <= (6 - pieceTeamBonus + self.numPiecesPerTeam):
							positionsToGo.append((consideredTile[0],consideredTile[1]))
				'''
				for i in range(len(moves)):
					move = moves[i]
					consideredTile = (position[0] + move[0], position[1] + move[1])
					# Push 1 up:
					if i
					
					if (0 <= position[0] + move[0] <= 7) and (0 <= position[1] + move[1] <= 7): # If in the board
						if not(pieceTeamBonus <= int(self.grid[position[1] + move[1]][position[0] + move[0]]) < pieceTeamBonus + self.numPiecesPerTeam): # If tile is not ocupied by a team piece
							positionsToGo.append((position[0] + move[0], position[1] + move[1]))
				'''
				print("Pawn:", positionsToGo)
				return positionsToGo
			else: # KNIGHT
				# If not entering check
				moves = self.pieceMove[piece]
				for move in moves:
					if (0 <= position[0] + move[0] <= 7) and (0 <= position[1] + move[1] <= 7): # If in the board
						if not(pieceTeamBonus <= int(self.grid[position[1] + move[1]][position[0] + move[0]]) < pieceTeamBonus + self.numPiecesPerTeam): # If tile is not ocupied by a team piece
							positionsToGo.append((position[0] + move[0], position[1] + move[1]))
				print("Knight:", positionsToGo)
				return positionsToGo
		else:
			print("No Piece Here")
			return positionsToGo
		
def loadInfoFromFile(fileName): # Acquire information from a text file
    try:
        file = open(fileName)
        myArray = []
        text = file.readlines()
        for line in text:
            line = line.strip() #Gets rid of end-of-line markers, etc.
            row = ""
            for c in line:
                row = row + c
            myArray.append(row.split(","))
        return myArray
    except IOError:
        print("Please include:", fileName, "in the folder")
    finally:
        file.close()	
def loadImages(imageListNames ):
	numImages = len(imageListNames)
	imageList = ["" for i in range(numImages)]
	for i in range(numImages):
		#print(imageListNames[i])
		imageList[i] = pygame.image.load(imageListNames[i])
	return(imageList)

def promotion(position, team): # (int, int), bool
	print("Promotion logic. NOTE: It might be better to have this in piece moves for the AI?")
	
	promote(position, "1")
	

# Start
import pygame, os

pygame.init()
imagesToLoad = loadInfoFromFile("images.txt")
#cwd = os.getcwd() # Use this if fail
imageNamesList = [os.path.join(imagesToLoad[0][0], imagesToLoad[1][0], imagesToLoad[2][i]) for i in range(len(imagesToLoad[2]))]

imageList = loadImages( imageNamesList )
scaleFactor = 4
xSize = (imageList[0].get_width() + imageList[1].get_width()) * scaleFactor
ySize = (imageList[0].get_height() + imageList[2].get_height()) * scaleFactor
for i in range (len(imageList)): # Resize images
	image = imageList[i]
	#print((image.get_width() * scaleFactor, image.get_height() * scaleFactor))
	imageList[i] = pygame.transform.scale(image, (image.get_width() * scaleFactor, image.get_height() * scaleFactor))



# Set up class to deal with the display of the board
myDisplay = Display(xSize, ySize, (200, 200, 200), scaleFactor)
myDisplay.giveAssets(imageList)

# Set up class to deal with the piecies and logic of the board
myBoard = ChessGame()
piecePositions = myBoard.getPositions()

myDisplay.drawBoard()
myDisplay.drawPieces(piecePositions)

'''
print("Images to Load:", imagesToLoad)
print("Images Names:", imageList)
'''

moves = []
selected = False

import time
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			break
		if event.type == pygame.MOUSEBUTTONUP:
			tilePressed = myDisplay.getTilePressed()
			print(tilePressed)
			
			if not selected: # Clicking after clicking off
				moves = myBoard.pieceMoves(tilePressed)
				myDisplay.showPositions(moves, (0,200,255))
				if moves != []:
					selected = True
					myDisplay.showPositions([tilePressed], (0,200,255,20))
				myDisplay.drawPieces(piecePositions)
				
			else:
				valid = tilePressed in moves
				if valid: # Clicking a tile to go to
					print("Move Piece")
					myBoard.movePiece(lastTile, tilePressed)
					piecePositions = myBoard.getPositions()
					selected = False
					myDisplay.drawBoard()
					myDisplay.drawPieces(piecePositions)
				else: # Clicking another tile, while having one selected, but not a place it can travel
					myDisplay.drawBoard()
					myDisplay.drawPieces(piecePositions)
					if lastTile != tilePressed: # If you aren't unselecting unit
						moves = myBoard.pieceMoves(tilePressed)
						myDisplay.showPositions(moves, (0,200,255))
						myDisplay.drawPieces(piecePositions)
						if moves != []:
							selected = True
							myDisplay.showPositions([tilePressed], (0,200,255,20))
						else:
							selected = False
						myDisplay.drawPieces(piecePositions)
					else:
						selected = False
			
			# Temporary check "Checks"
			checkedTiles = []
			for i in range(8):
				for j in range (8):
					checked = myBoard.attacked((i,j), 6)
					if checked:
						checkedTiles.append((i,j))
			myDisplay.showPositions(checkedTiles, (255,0,0,50))
			
			lastTile = tilePressed
			print("Selected:", selected)
			
			
		
			





