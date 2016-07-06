import psycopg2
import getpass

class MusicDataSource:
	database = ''
	user = ''
	password = ''
	
	def __init__(self):
		''' Get the database login info
		''' 
		self.database = 'choito'
		self.user = 'choito'
		self.password = 'books796cup'
	
	def getSongsForUserInput(self, titleOrArtist, rankRange, yearRange):
		''' Returns a list of songs that match with user's title, artist, year range, and rank range inputs
		'''	
		rankBegin, rankEnd, yearBegin, yearEnd = int(rankRange[0]), int(rankRange[1]), int(yearRange[0]), int(yearRange[1])

		try:
			connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
		except Exception, e:
			print 'Connection error: ', e
			raise
			exit()
		searchResults = []
		
		try:
			cursor = connection.cursor()
			query = 'SELECT * FROM top6000songsWithFav WHERE ((lower(songTitle)  LIKE \'%%%s%%\') OR (lower(songArtist) LIKE \'%%%s%%\')) AND (songRank BETWEEN %d AND %d) AND (songYear BETWEEN %d AND %d) ORDER BY songRank;' % (titleOrArtist.lower(), titleOrArtist.lower(), rankBegin, rankEnd, yearBegin, yearEnd)
			cursor.execute(query)
			searchResults = cursor.fetchall()

		except Exception, e:
			print 'Cursor error', e
			connection.close()
			exit()
        
		connection.close()
		
		return searchResults
		
	def getMacallanTop20(self):
	    ''' Returns a list of Macallan's top 20 songs
	    '''
	    try:
	        connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
	    except Exception, e:
	        print 'Connection error: ', e
	        raise
	        exit()
	    searchResults = []
	    
	    try:
	        cursor = connection.cursor()
	        query = 'SELECT songRank, songArtist, songTitle, songYear FROM top6000songsWithFav WHERE songFavoriteMacallan <= 20'
	        cursor.execute(query)
	        searchResults = cursor.fetchall()
	    except Exception, e:
	        print 'Cursor error', e
	        connection.close()
	        exit()
	        
	    connection.close()
	    
	    return searchResults
	    
	def getTomTop10(self):
	    ''' Returns a list of Tom's top 10 songs
	    '''
	    try:
	        connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
	    except Exception, e:
	        print 'Connection error: ', e
	        raise
	        exit()
	    searchResults = []
	    
	    try:
	        cursor = connection.cursor()
	        query = 'SELECT songRank, songArtist, songTitle, songYear FROM top6000songsWithFav WHERE songFavoriteTom <= 10'
	        cursor.execute(query)
	        searchResults = cursor.fetchall()
	    except Exception, e:
	        print 'Cursor error', e
	        connection.close()
	        exit()
	        
	    connection.close()
	    
	    return searchResults