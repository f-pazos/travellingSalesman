#Felipe Pazos
#4/4/2016
#
#Code to generate solution to N-Queens problem utilizing hill climbing approach.
#

from sys import argv
from random import shuffle, choice, randint

from travellingSalesmanResources import createImage, score, distance
from math import sqrt, atan2
import time
import heapq
import pickle
import heapq
import os.path

#N=4 by default, or first argument.

def main():	

	cities = readFile( "cities.txt" )

	ordered = connectShortestSegments( cities )
	for cit in ordered:
		print( cit )
	createImage( ordered, "test.ppm" )

	'''print( "Score: ", score( cities ) )

	cities = orderRadially( cities )

	result = geneticAlg( cities, 8, 100, .01, 8 )

	print( "Score: ", result[0] )

	createImage( result[1] , "travel.ppm" )'''

#Takes in the cities and orders them by their angle from the center.
def connectShortestSegments( cities ):

	distances = {}

	chains = {}
	neighbors = {}

	for city in cities:
		chains[ city ] = { city: True }
		neighbors[ city ] = []
		
	q = []
		
	for cityA in cities:

		for cityB in cities:
			val = distance( cityA, cityB )

			print( val ) 

			if val > 0:
				distances[ cityA, cityB ] = val
				heapq.heappush( q, (val, (cityA, cityB) ) )
	

	while len( q )  >  0 and len( chains[cities[0]] ) < len( cities ):
		#Pop the smallest distance
		smallestDistance = heapq.heappop( q )

		firstCity = smallestDistance[1][0]
		secondCity = smallestDistance[1][1]

		#Make sure they aren't in the same chains, and both cities are edges.
		if secondCity not in chains[ firstCity ] and firstCity not in chains[ secondCity ] and len( neighbors[firstCity] ) < 2 and len( neighbors[secondCity] ) < 2:

			neighbors[ firstCity ].append( secondCity )
			neighbors[ secondCity].append( firstCity )

			newChain = {}

			for key in list( chains[firstCity].keys() ):
				newChain[ key ] = True
			for key in list( chains[secondCity].keys() ):
				newChain[ key ] = True

			chains[ firstCity ] = newChain
			chains[ secondCity] = newChain

	print( chains[cities[0] ] )
	input( len( chains[cities[0] ]))

	newOrder = [ cities[0] ]
	prevCity = cities[0]
	currCity = neighbors[ cities[0] ][0]

	while len( newOrder ) < len( cities ):
		newOrder.append( currCity )

		#Make the next city the neighbor of the current city that we haven't been to yet.
		nextCity = neighbors[currCity][ (neighbors[currCity].index( prevCity ) + 1 ) % 2 ]
		prevCity = currCity
		currCity = nextCity

	return newOrder







def orderRadially( cities ):
	sumX = 0
	sumY = 0

	for city in cities: 
		sumX += city[0]
		sumY += city[1]

	xctr = sumX / len( cities )
	yctr = sumY / len( cities )

	tempArr = []

	for city in cities:
		t = atan2( city[1] - yctr , city[0] - xctr )
		tempArr.append( (t, city) )

	tempArr.sort()

	finalArr = []

	for city in tempArr:

		finalArr.append( city[1] )

	return finalArr

def geneticAlg( cities, popLimit, generations, percentMutations, numChildren ):

	#Create the starting generation.
	population = []

	#Sort of shuffle and add.
	for i in range( popLimit ):
		
		for i in range( 0, len( cities ) ):
			if ( randint( 0, 100 ) < percentMutations * 100 ):
				temp = cities[i]
				rand = randint( 0, 5 )
				cities[i] = cities[ (i + rand) % len( cities ) ]
				cities[ (i + rand ) % len( cities ) ] = temp

		population.append ( (score(cities), cities[:]) )

	population.sort()

	for t in range( generations ):
		print("success")
		#Start by shuffling the mates some amount.
		'''skip = int( 1/percentShuffle )

		index = 2

		while index < len( population ):
			swapIndex = randint(2, len(population) - 1 )

			temp = population[index]
			population[index] = population[swapIndex]
			population[swapIndex] = temp

			index += skip'''

		newGeneration = []

		index = 0

		while index < len( population ):

			#Population is a list of (score, order) so choose the orders to mate.
			children = mate( population[index][1][:], population[(index + 1)%len(population)][1][:], numChildren, int( percentMutations * len( cities ) ) )


			for child in children:
				newGeneration.append( (score(child), child) )

			index += 2

		newGeneration.sort()

		#Keep only the population limit orders.

		population = newGeneration[0:popLimit]
		print( "Best: ", population[0][0], "Worst: ", population[-1][0])

	#Return the best.
	return population[0]

def mate( a, b, numChildren, maxMutations):

	if not contentsIdentical( a, b ):
		a.sort()
		b.sort()

		for i in range( len( a ) ):
			print( a[i], " ", b[i] )

		input( "PROBLEM!!")

	children = []

	for i in range( numChildren ):

		child = []
		inChild = {}

		for element in a:
			inChild[element] = False
		#Start with the a random element in a.

		startIndex = randint( 0, len(a) - 1 )

		child.append( a[ startIndex] )
		inChild[ a[ startIndex ] ]= True

		currElement = a[startIndex]

		#Find the indeces of the element in both arrays.
		aIndex = startIndex
		bIndex = b.index( currElement )

		#Repeat the process until you fill the array.
		while len( child ) < len( a ):

			#We're comparing the next elements in the list - essentially the orders.
			aNextElement = a[ (aIndex+1) % len(a) ]
			bNextElement = b[ (bIndex+1) % len(b) ]

			#If the parents agree on the next element, AND it hasn't been added yet, append that similarity.
			#The next element would simply be the next one in the list.

			if aNextElement == bNextElement and not inChild[ aNextElement ]:
				child.append( aNextElement )
				inChild[ aNextElement ] = True

				nextElement = aNextElement
				aIndex = (aIndex + 1) % len( a )
				bIndex = (bIndex + 1) % len( b )

			else:
				#If either aNextElement or bNextElement hasn't been added to the child yet, go with it. However, prioritize a and b equally.

				if not inChild[ aNextElement] and not inChild[ bNextElement ]:

					if randint( 0, 1 ) == 0:
						nextElement = aNextElement

						aIndex = (aIndex + 1) % len( a )
						bIndex = b.index( nextElement )

					else:
						nextElement = bNextElement

						aIndex = a.index( nextElement )
						bIndex = (bIndex + 1) % len( b )

					child.append( nextElement )
					inChild[ nextElement ] = True

				#Next if only one of them hasn't been added to the child yet, add them.

				elif not inChild[ aNextElement ]: 

					child.append( aNextElement )
					inChild[ aNextElement ] = True

					aIndex = (aIndex + 1) % len( a )
					bIndex = b.index( nextElement )

				elif not inChild[ bNextElement ]:

					child.append( bNextElement )
					inChild[ bNextElement ] = True

					aIndex = a.index( nextElement )
					bIndex = (bIndex + 1) % len( b )

				#Both the next elements have already been added to the child previously.
				#Make a list of elements which aren't in child yet, and choose a random one to be the next element.
				else:
					possibleElements = []

					for element in list( inChild.keys() ) :
						if not inChild[ element ]:
							possibleElements.append( element )

					nextElement = choice( possibleElements )

					child.append( nextElement )
					inChild[ nextElement ] = True

					aIndex = a.index( nextElement )
					bIndex = b.index( nextElement )

		#Mutate the child slightly.

		for i in range( randint(0, maxMutations) ):
			index= randint( 0, len( child ) - 1 )

			temp = child[index]
			child[index] = child[(index + 1) % len( child )]
			child[(index+1) % len( child )] = temp

		for i in range( randint(0, maxMutations // 10) ):
			index = randint(0, len(child) - 1)
			index2 = randint( 0, len(child) - 1)

			temp = child[index]
			child[index] = child[index2]
			child[index2] = temp
		children.append( child )

	return children

def contentsIdentical(a, b):

	aContents = {}
	for val in a:
		aContents[ val ] = True

	for val in b:
		if val not in aContents:
			print( val )
			return False

	return True


def genRandomArray( N ):
	board = list( range( N ) )
	shuffle( board )

	return board

def readFile( filename ):

	cities = []

	f = open( filename, 'r' ).read().split()

	numcities = f.pop(0)

	for i in range( int(numcities) ):


		x = f.pop(0)
		y = f.pop(0)

		cities.append( (int(float(x)), int(float(y)) ) )

	return cities


main()