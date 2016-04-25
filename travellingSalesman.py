#Felipe Pazos
#4/4/2016
#
#Code to generate solution to N-Queens problem utilizing hill climbing approach.
#

from sys import argv
from random import shuffle, choice

from travellingSalesmanResources import createImage
from math import sqrt
import time
import heapq
import pickle
import os.path

#N=4 by default, or first argument.

def main():	

	cities = readFile( "cities.txt" )

	print( score( cities ) )
	print( cities )

	results = hillClimb( cities )

	print( "Score: ", score( results[0] ) )
	print( "Steps: ", results[1] ) 

	createImage( results[0] , "travel.ppm" )

	'''for k in range( 10 ):	
		for i in range( 4, 15 ):

			data = pickle.load( open( "nQueensData.pkl", "rb" ) )

			tick = time.clock()

			board = genRandomArray( i )
			board = findSolution( board, i )

			print( board, i )

			tock = time.clock()

			if i not in data:
				data[i] = []

			data[i].append( (tock-tick, board[1]) )

			pickle.dump( data, open( "nQueensData.pkl", "wb" ) )'''



#Attempt to find a solution to given board.
def hillClimb( startState ):

	traversed = {}


	currState = startState[:]
	currScore = score( currState )
	traversed[tuple(currState)] = True

	shuffleCount = 0
	stepCount = 0

	localMaxima = False

	while not localMaxima:
		print( score( currState) )
		nextState = currState
		newState = currState[:]

		betterScore = False

		currScore = score( currState )

		#Swap all permutationsself.

		improvement = False
		for a in range( len(startState) - 1):
			for b in range( a + 1, len(startState) ):

				if not improvement:
					temp = newState[a]
					newState[a] = newState[b]
					newState[b] = temp

					newStateScore = score( newState )

					#If the new board is an improvement, keep track of it.
					if newStateScore < currScore:
						currScore = newStateScore
						betterScore = True
						nextState = newState[:] 
						improvement = True

					#If the new board is equal, make sure we haven't traversed it before and switch to it.
					elif newStateScore == currScore and tuple(newState) not in traversed:

						betterScore = True
						nextState = newState[:]
						improvement = True

					temp = newState[a]
					newState[a] = newState[b]
					newState[b] = temp

		#Randomly choose a score from the possible scores, and go with it.

		#If we couldn't find a better board, re shuffle it.
		if not betterScore:
			#Make sure we clear the traversed boards, in case our path brings us to them again.
			localMaxima = True

		currState = nextState

		traversed[tuple(currState)] = True

		stepCount += 1

	return ( currState, stepCount )

#Find how many pairs of queens are capable of attacking each other.

def score( cities ):

	score = 0

	length = len( cities )

	for i in range( length ):
		cityA = cities[i]
		cityB = cities[(i+1)%length]

		score += sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )

	return score


def genRandomArray( N ):
	board = list( range( N ) )
	shuffle( board )

	return board

def readFile( filename ):

	cities = []

	f = open( filename, 'r' ).read().split()

	numcities = f.pop(0)

	print( "Numcities: ", numcities )

	for i in range( int(numcities) ):


		x = f.pop(0)
		y = f.pop(0)

		cities.append( (float(x), float(y) ) )

	return cities


main()