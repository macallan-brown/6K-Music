#!/usr/bin/python
''' index.py

    Created  by  Jeff Ondich, 4/6/12
    Modified by  Macallan Brown and Tom Choi, 2/9/16
    
    This application provides the platform for searching top 6000 songs of all time.
    Users can search songs by titles, artists, rank range(from 1 to 6000), and year range(from 1897 to 2014)
    A list of songs that match with user's search criteria will be displayed to its web application.
    
'''

import cgi
import datasource
import psycopg2


def getCGIParameters():
    ''' This function grabs the HTTP parameters we care about, sanitizes the
        user input, and returns the resulting values in a dictionary indexed by parameter names.
        Default values for song rank and year ranges are provided.
    '''
    
    form = cgi.FieldStorage()
    parameters = {'tomTop10':'', 'macallanTop20':'123','titleOrArtist':'', 'rankBegin':'1', 'rankEnd':'6000', 'yearBegin':'1897',
    'yearEnd':'2014'}
    
    parameters['macallanTop20'] = form.getvalue('macallanTop20')
    if 'tomTop10' in form:
        parameters['tomTop10'] = sanitizeUserInput(form['tomTop10'].value)
    
    if 'titleOrArtist' in form:
        parameters['titleOrArtist'] = sanitizeUserInput(form['titleOrArtist'].value)

    if 'rankBegin' in form:
        parameters['rankBegin'] = sanitizeUserInput(form['rankBegin'].value)
        
    if 'rankEnd' in form:
        parameters['rankEnd'] = sanitizeUserInput(form['rankEnd'].value)
    
    if 'yearBegin' in form:
        parameters['yearBegin'] = sanitizeUserInput(form['yearBegin'].value)
        
    if 'yearEnd' in form:
        parameters['yearEnd'] = sanitizeUserInput(form['yearEnd'].value)
        
    return parameters

def printMainPageAsHTML(parameters, templateFileName):
    ''' Finds the list of songs that match with user's title, artist, year range, and rank range inputs
        Then, displays the result to this web application.
    '''
    macallanTop20, tomTop10, titleOrArtist, rankBegin, rankEnd, yearBegin, yearEnd = allocateUserInputs(parameters)
    yearRange = checkYearRange(yearBegin, yearEnd)
    rankRange = checkRankRange(rankBegin, rankEnd)
    
    searchResult = getSearchResult(macallanTop20, tomTop10, titleOrArtist, rankRange, yearRange)
    songReport = getSongReport(macallanTop20, tomTop10, searchResult)
    sourceFileLinks = getSourceFileLinks(templateFileName)
    
    outputText = ''
    try:
        f = open(templateFileName)
        templateText = f.read()
        f.close()
        outputText = templateText % (titleOrArtist, str(rankBegin), str(rankEnd), str(yearBegin), str(yearEnd), songReport, sourceFileLinks)
    except Exception, e:
        outputText = 'Cannot read template file "%s."' % (templateFileName)

    print 'Content-type: text/html\r\n\r\n',
    print outputText
    
def addNumberOfSearches(songReport, numberOfSearches):
    ''' Incorporates the number of songs that are found to the song report
    '''
    finalReport = '%d Songs Found\n' % numberOfSearches
    finalReport += songReport
    return finalReport

def allocateUserInputs(parameters):
    ''' Neatly allocates and returns user's inputs to each corresponding variable.
    '''
    macallanTop20 = parameters['macallanTop20']
    tomTop10 = parameters['tomTop10']
    titleOrArtist = parameters['titleOrArtist']
    rankBegin = parameters['rankBegin']
    rankEnd = parameters['rankEnd']
    yearBegin = parameters['yearBegin']
    yearEnd = parameters['yearEnd']
    return macallanTop20, tomTop10, titleOrArtist, rankBegin, rankEnd, yearBegin, yearEnd

def checkYearRange(yearBegin, yearEnd):
    ''' Check if user's year range input is valid.
    '''
    if yearBegin.isdigit() == False:
    	yearBegin = 1897
    if yearEnd.isdigit() == False:
    	yearEnd = 2014
    if yearBegin > yearEnd:
        return [1897, 2014]
    else:
        return [yearBegin, yearEnd]
    
def checkRankRange(rankBegin, rankEnd):
    ''' Check if user's rank range input is valid.
    '''
    if rankBegin.isdigit() == False:
    	rankBegin = 1
    if rankEnd.isdigit() == False:
    	rankEnd = 6000
    if rankBegin > rankEnd:
        return [1, 6000]
    else:
        return [rankBegin, rankEnd]

def getSearchResult(macallanTop20, tomTop10, titleOrArtist, rankRange, yearRange):
    ''' Returns the list of songs that matches to user's inputs.
    '''
    query = datasource.MusicDataSource()
    if macallanTop20:
        searchResult = query.getMacallanTop20()
    elif tomTop10:
        searchResult = query.getTomTop10()
    else:
        searchResult = query.getSongsForUserInput(titleOrArtist, rankRange, yearRange)
    return searchResult

def getSongReport(macallanTop20, tomTop10, searchResult):
    ''' Creates the report that fits into the webpage's table.
    '''
    songReport, rank, title, artist, year = '', '', '', '', ''
    if not searchResult:
        songReport +='No results were found in the Top 6000 Songs that match your search. Please try again.'
    else:
        if macallanTop20 or tomTop10:
            songReport = createPersonalReport(searchResult)
        else:
            songReport = createUserSearchReport(searchResult)
        songReport = addNumberOfSearches(songReport, len(searchResult))

    return songReport

def createPersonalReport(searchResult):
    ''' Returns Macallan's top 10 report or Tom's top 10 report,
        depending on which links are clicked in the web template.
    '''
    personalReport = ''
    personalRank = 1
    for eachSong in searchResult:
        rank, title, artist, year = getSongInformation(eachSong)
        artistURL, titleURL = getArtistURL(artist), getTitleURL(artist, title)
        personalReport += '<tr class="tableRow"><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (personalRank, titleURL, artistURL, year)
        personalRank += 1
    return personalReport
    
def createUserSearchReport(searchResult):
    ''' Returns the report that corresponds to the user's search inputs
    '''
    userReport = ''
    for eachSong in searchResult:
        rank, title, artist, year = getSongInformation(eachSong)
        artistURL, titleURL = getArtistURL(artist), getTitleURL(artist, title)
        userReport += '<tr class="tableRow"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (rank, titleURL, artistURL, year)
    return userReport

def getSongInformation(eachSong):
    ''' Returns a song's rank, title, artist, and year respectively.
    '''
    return eachSong[0], eachSong[2], eachSong[1], eachSong[3]

def getArtistURL(artist):
    ''' Returns a wikipedia link to the artist
    '''
    return '<a target="_blank" href="https://en.wikipedia.org/wiki/%s">%s</a>' % (artist, artist)
    
def getTitleURL(artist, title):
    ''' Returns a YouTube link to the song title
    '''
    return '<a target="_blank" href ="https://www.youtube.com/results?search_query=%s">%s</a>' % (artist + ' ' + title, title)

def getSourceFileLinks(templateFileName):
    ''' Neatly creates hyperlinks to our source files.
    '''
    links = '<p><a href="showsource.py?source=index.py">index.py source</a></p>\n'
    links += '<p><a href="showsource.py?source=datasource.py">datasource.py source</a></p>\n'    
    links += '<p><a href="showsource.py?source=%s">%s source</a></p>\n' % (templateFileName, templateFileName)
    links += '<p><a href="showsource.py?source=showsource.py">the script we use for showing source</a></p>\n'
    links += '<p><a href="showsource.py?source=createtable.sql">createtable.sql source</a></p>\n'
    links += '<p><a href="showsource.py?source=About.html">About.html source</a></p>\n'
    links += '<p><a href="showsource.py?source=README.html">README.html source</a></p>\n'
    return links

def printFileAsPlainText(fileName):
    ''' Prints to standard output the contents of the specified file, preceded
        by a "Content-type: text/plain" HTTP header.
    '''
    text = ''
    try:
        f = open(fileName)
        text = f.read()
        f.close()
    except Exception, e:
        pass

    print 'Content-type: text/plain\r\n\r\n',
    print text

def sanitizeUserInput(searchInput):
    ''' Sanitizes user input by removing unnecessary punctuations.
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        searchInput = searchInput.replace(ch, '')
    return searchInput

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters, 'HomePage.html')
        
if __name__ == '__main__':
    main()