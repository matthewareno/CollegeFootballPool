from NCAAFootballTeam import NCAAFootballTeam
from NCAAFootballFetcher import NCAAFootballFetcher
from BeautifulSoup import BeautifulSoup
from NCAAFootballGame import NCAAFootballGame
from NCAAFootballDatabase import NCAAFootballDatabase
import json
import pprint

class NCAAFootballParser():
	def ParseTeamsPage(self):
		teamURLTag = 'http://www.espn.com/college-football/team/_/id/'
		teamList = []

		myFetcher = NCAAFootballFetcher()
		teamListPage = myFetcher.fetchTeamListings()
		soup = BeautifulSoup(teamListPage)
		teamTags = soup.findAll( 'h5' )
		for teamTag in teamTags:
			if str(teamURLTag) not in str(teamTag):
				continue
			urlTag = teamTag.find( 'a' )
			if urlTag == None:
				break;
			teamURL = urlTag['href']
			teamName = urlTag.text
			if teamName == None:
				break;
			teamList.append( [teamName, teamURL] )
		
		return teamList

	def ParseTeamHomePage(self, teamName, teamURL):
		teamRecordTag = 'Overall: '
		teamRecordFound = 0

		print "Retrieving information for %s..." % ( teamName.encode( "utf8" ) )
		myFetcher = NCAAFootballFetcher()
		teamID = teamURL.split("/")[7]
		teamData = myFetcher.fetchTeamPage(teamID)
		soup = BeautifulSoup(teamData)
		newTeam = NCAAFootballTeam(teamID)
		teamName = teamName.replace( ';', '' )
		newTeam.SetTeamName( teamName )
        # URLs can contain the ' character, which is bad for SQL entries, so replace them with the correct URL encoding
		teamURL = teamURL.replace( '\'', '\%27' )
		newTeam.SetTeamURL( teamURL )
		teamNameTag = soup.find( 'meta', {'property' : 'og:title'} )
		if teamNameTag == None:
			print 'Found invalid teamNameTag for team: %s' % ( teamName )
			return
		teamFullName = teamNameTag['content']
		# Some team names have a ' in them, which can be a problem for SQL entries, so remove them
		teamFullName = teamFullName.replace( '\'', '' ).replace( ';', '' )
		if teamFullName.find( "College Football" ) != -1:
			teamFullName = teamFullName.split( " College Football" )[0]
		newTeam.SetTeamFullName( teamFullName )
		teamIconTag = soup.find( 'meta', {'property' : 'og:image'} )
		if teamIconTag == None:
			print 'Found invalid teamIconTag for team: %s' % ( teamName )
			return
		teamIconURL = teamIconTag['content']
        # URLs can contain the ' character, which is bad for SQL entries, so replace them with the correct URL encoding
		teamIconURL = teamIconURL.replace( '\'', '\%27' );
		newTeam.SetTeamIconURL( teamIconURL )
		
		recordTag = soup.find( 'li', {"class" : "record"} )
		if recordTag == None:
			newTeam.SetTeamWins( 0 )
			newTeam.SetTeamLoses( 0 )
			newTeam.SetTeamTies( 0 )
		else:
			record = recordTag.text
			teamRecord = record.split('-')
			newTeam.SetTeamWins( int(teamRecord[0]) )
			newTeam.SetTeamLoses( int(teamRecord[1]) )
			if len(teamRecord) == 3:
				newTeam.SetTeamTies( int(teamRecord[2]) )
			else:
				newTeam.SetTeamTies( 0 )
		
		conferenceTag = soup.find( 'li', {"class" : "ranking"} )
		if conferenceTag == None:
			conference = "Independent"
		else:
			conference = conferenceTag.text
			if len(conference.split('in ')) != 1:
				conference = conference.split('in ')[1]
			else:
				conference = "Independent"

		return newTeam

	def ConvertGameDataToJSON( self, gameData ):
		if gameData.startswith("<script>"):
			gameData = gameData[8:]
		if gameData.endswith("</script>"):
			gameData = gameData[:-9]
		#check and see if there are more than on JSON element in the script
		if gameData.count( "};" ) != 1:
			gameData = gameData.split( "};")[0] + "};"
		jsonValue = '{%s}' % (gameData.split('{', 1)[1].rsplit('}', 1)[0],)
		value = json.loads( jsonValue )
		return value

	def ConvertStartDateToString( self, startDate ):
		months = { "01" : "January",
					"02" : "February",
					"03" : "March",
					"04" : "April",
					"05" : "May",
					"06" : "June",
					"07" : "July",
					"08" : "August",
					"09" : "September",
					"10" : "October",
					"11" : "November",
					"12" : "December"
				}

		month = startDate.split( "-" )[1]
		day = startDate.split( "-" )[2]
		year = startDate.split( "-" )[0]
		dateString = "%s %s, %s" % ( months[month], day, year )
		return dateString

	def ConvertMonthDayToString( self, monthDay ):
		months = { "1" : "January",
					"2" : "February",
					"3" : "March",
					"4" : "April",
					"5" : "May",
					"6" : "June",
					"7" : "July",
					"8" : "August",
					"9" : "September",
					"10" : "October",
					"11" : "November",
					"12" : "December"
				}
		month = monthDay.split( "/" )[0]
		day = monthDay.split( "/" )[1]
		dateString = "%s %s" % ( months[month], day )
		return dateString

	def ParseGameWeek( self, gamesData, week, division, gameList, teamList ):
		gameCount = 0
		homeIndex = 0 # just set default value, will determine correct value later
		awayIndex = 1 # just set default value, will determine correct value later

		soup = BeautifulSoup(gamesData)
		for element in soup('script'):
			elementString = '{0}'.format(element)
			if elementString.find( "window.espn.scoreboardData" ) != -1:
				value = self.ConvertGameDataToJSON( elementString )
				for game in value["events"]:
					newGame = NCAAFootballGame()
					awayTeam = NCAAFootballTeam()
					homeTeam = NCAAFootballTeam()
					# get the game ID
					newGame.gameID = int( game["competitions"][0]["id"] )
					gameTime = game["competitions"][0]["status"]["type"]["detail"]
					# get the game date and time.  this will be different based on whether the
					# game is already over, in progress, or hasn't started
					if len( gameTime.split( " at " ) ) == 2:
						newGame.gameDate = gameTime.split( " at " )[0]
						newGame.gameTime = gameTime.split( " at " )[1]
					elif gameTime.find( "Final" ) != -1:
						newGame.gameTime = gameTime
						# startDate format is YYYY-MM-DDTHH:MM", so pull the date from everything before T
						gameTime = game["competitions"][0]["startDate"].split( "T" )[0]
						newGame.gameDate = self.ConvertStartDateToString( gameTime )
					elif gameTime.find( "TBD" ) != -1:
						newGame.gameTime = "TBD"
						newGame.gameDate = self.ConvertMonthDayToString( gameTime.split( " - " )[0] )
					elif game["competitions"][0]["status"]["type"]["state"] == "in":
						newGame.gameTime = gameTime
						newGame.gameDate = ""
					elif gameTime.find( "Canceled" ) != -1 or gameTime.find( "Postponed" ) != -1:
						newGame.gameTime = gameTime
						newGame.gameDate = ""
					else:
						print "Found weird gameTime: %s" % ( gameTime )
					# ok, figure out who is the home team and who is the away team
					if game["competitions"][0]["competitors"][0]["homeAway"] == "home":
						homeIndex = 0
						awayIndex = 1
					else:
						homeIndex = 1
						awayIndex = 0

					# next, get the competitor information, starting with IDs
					newGame.homeID = int( game["competitions"][0]["competitors"][homeIndex]["team"]["id"] )
					newGame.awayID = int( game["competitions"][0]["competitors"][awayIndex]["team"]["id"] )
					awayTeam.id = newGame.awayID
					homeTeam.id = newGame.homeID
					# then get their final scores, 0 if the game hasn't started
					newGame.homeFinalScore = int( game["competitions"][0]["competitors"][homeIndex]["score"] )
					newGame.awayFinalScore = int( game["competitions"][0]["competitors"][awayIndex]["score"] )
					if 'linescore' in game["competitions"][0]["competitors"][awayIndex]:
						scoreEntries = len( game["competitions"][0]["competitors"][awayIndex]["linescore"] )
						if scoreEntries > 0:
							newGame.awayFirstScore = int( game["competitions"][0]["competitors"][awayIndex]["linescore"][0]["value"] )
						if scoreEntries > 1:
							newGame.awaySecondScore = int( game["competitions"][0]["competitors"][awayIndex]["linescore"][1]["value"] )
						if scoreEntries > 2:
							newGame.awayThirdScore = int( game["competitions"][0]["competitors"][awayIndex]["linescore"][2]["value"] )
						if scoreEntries > 3:
							newGame.awayFourthScore = int( game["competitions"][0]["competitors"][awayIndex]["linescore"][3]["value"] )
						if scoreEntries > 4:
							newGame.awayOTScore = int( game["competitions"][0]["competitors"][awayIndex]["linescore"][4]["value"] )
					if 'linescore' in game["competitions"][0]["competitors"][homeIndex]:
						scoreEntries = len( game["competitions"][0]["competitors"][homeIndex]["linescore"] )
						if scoreEntries > 0:
							newGame.homeFirstScore = int( game["competitions"][0]["competitors"][homeIndex]["linescore"][0]["value"] )
						if scoreEntries > 1:
							newGame.homeSecondScore = int( game["competitions"][0]["competitors"][homeIndex]["linescore"][1]["value"] )
						if scoreEntries > 2:
							newGame.homeThirdScore = int( game["competitions"][0]["competitors"][homeIndex]["linescore"][2]["value"] )
						if scoreEntries > 3:
							newGame.homeFourthScore = int( game["competitions"][0]["competitors"][homeIndex]["linescore"][3]["value"] )
						if scoreEntries > 4:
							newGame.homeOTScore = int( game["competitions"][0]["competitors"][homeIndex]["linescore"][4]["value"] )
					# check if there is a winner
					if "winner" in game["competitions"][0]["competitors"][0]:
						if game["competitions"][0]["competitors"][0]["winner"] == True:
							newGame.winnerID = game["competitions"][0]["competitors"][0]["id"]
					if "winner" in game["competitions"][0]["competitors"][1]:
						if game["competitions"][0]["competitors"][1]["winner"] == True:
							newGame.winnerID = game["competitions"][0]["competitors"][1]["id"]
					# get the game status
					newGame.gameStatus = int( game["competitions"][0]["status"]["period"] )
					# the gameStatus is normally the period.  however, the game could be postponed or 
					# canceled, but the period would show 0 or whatever quarter theey were in when it
					# happened.  double check and see if the game is actually over
					if( game["competitions"][0]["status"]["type"]["state"] == "post" ):
						newGame.gameStatus = 5

					# grab the team records.  not all teams (Division 1-AAA) will have records, so 
					# make sure to check if the value is None before proceeding.
					teamRecord = {}
					teamRecord = game["competitions"][0]["competitors"][awayIndex].get( "records" )
					if teamRecord is not None:
						newGame.awayRecord = game["competitions"][0]["competitors"][awayIndex]["records"][0]["summary"]
						awayTeam.wins = newGame.awayRecord.split( "-" )[0]
						awayTeam.loses = newGame.awayRecord.split( "-" )[1]
						if len( newGame.awayRecord.split( "-" ) ) == 3:
							awayTeam.ties = newGame.awayRecord.split( "-" ) [2]
						else:
							awayTeam.ties = 0
					else:
						newGame.awayRecord = ""
					
					teamRecord = game["competitions"][0]["competitors"][homeIndex].get( "records" )
					if teamRecord is not None:
						newGame.homeRecord = game["competitions"][0]["competitors"][homeIndex]["records"][0]["summary"]
						homeTeam.wins = newGame.homeRecord.split( "-" )[0]
						homeTeam.loses = newGame.homeRecord.split( "-" )[1]
						if len( newGame.homeRecord.split( "-" ) ) == 3:
							homeTeam.ties = newGame.homeRecord.split( "-" ) [2]
						else:
							homeTeam.ties = 0
					else:
						newGame.homeRecord = ""
					# check if odds are available
					if "odds" in game["competitions"][0]:
						if len( game["competitions"][0]["odds"] ) != 0:
							if "details" in game["competitions"][0]["odds"][0]:
								newGame.gameOdds = game["competitions"][0]["odds"][0]["details"]

					newGame.neutralSite = game["competitions"][0]["neutralSite"]
					newGame.gameDivision = division
					newGame.gameIndex = gameCount
					newGame.gameWeek = week
					gameList.append( newGame )
					teamList.append( awayTeam )
					teamList.append( homeTeam )
					gameCount += 1

	def ParseFbsGameWeek( self, week, games, teams ):
		myFetcher = NCAAFootballFetcher()
		gamesData = myFetcher.fetchWeeklyFbsGames( week )
		return self.ParseGameWeek( gamesData, week, 0, games, teams )

	def ParseFcsGameWeek(self, week, games, teams):
		myFetcher = NCAAFootballFetcher()
		gamesData = myFetcher.fetchWeeklyFcsGames(week)
		return self.ParseGameWeek( gamesData, week, 1, games, teams )

	def	ParseFbsBowlGames(self, games, teams):
		myFetcher = NCAAFootballFetcher()
		gamesData = myFetcher.fetchFbsBowlGames(17)
		return self.ParseGameWeek( gamesData, 17, 0, games, teams )

	def ParseTeamRankings(self, week):
		rankings = []

		myFetcher = NCAAFootballFetcher()
		rankingsPage = myFetcher.fetchTeamRankings( week )
		soup = BeautifulSoup( rankingsPage )
		teams = soup.findAll( 'span', {'class':'team-names'} )
		for team in teams:
			teamStr = team.text
			teamStr = teamStr.replace( ";", "" )
			rankings.append( teamStr )
		return rankings

	def ParseGamesUpdate(self, week):
#		Grab all game IDs from database
		
		myFetcher = NCAAFootballFetcher()
		myDatabase = NCAAFootballDatabase()
		
		fbsScoreData = myFetcher.fetchWeeklyFbsGames(week)
		dateIndex = fbsScoreData.find( dateTag )
		nextDateIndex = fbsScoreData.find( dateTag, dateIndex+1 )
		while dateIndex != -1:
			currentDaysGames = fbsScoreData[dateIndex:nextDateIndex]
			soup = BeautifulSoup(currentDaysGames)
			gameDate = soup.h4
			gameDate = gameDate.string
			if gameDate.find('\'') != -1:
				gameDate = gameDate.split('\'')[0]
			# Scan for games and update their dates
			games = soup.findAll( 'div', {'class':'game-status'} )
			for game in games:
				# this should provide a set of strings with the format:
				# <div class="game-status"><p id="[gameId]-statusText">Time</p></div>
				gameTime = game.text
				gameStr = game.find('p')
				gameId = gameStr['id']
				gameId = gameId.split('-')[0]
				myDatabase.UpdateGameDateTime( int(gameId), gameDate, gameTime )
			dateIndex = nextDateIndex
			nextDateIndex = fbsScoreData.find( dateTag, dateIndex+1 )
		if week < 17:
			fcsScoreData = myFetcher.fetchWeeklyFcsGames(week)
			dateIndex = fcsScoreData.find( dateTag )
			nextDateIndex = fcsScoreData.find( dateTag, dateIndex+1 )
			while dateIndex != -1:
				currentDaysGames = fcsScoreData[dateIndex:nextDateIndex]
				soup = BeautifulSoup(currentDaysGames)
				gameDate = soup.h4
				gameDate = gameDate.string
				if gameDate.find('\'') != -1:
					gameDate = gameDate.split('\'')[0]
				# Scan for games and update their dates
				games = soup.findAll( 'div', {'class':'game-status'} )
				for game in games:
					# this should provide a set of strings with the format:
					# <div class="game-status"><p id="[gameId]-statusText">Time</p></div>
					gameTime = game.text
					gameStr = game.find('p')
					gameId = gameStr['id']
					gameId = gameId.split('-')[0]
					myDatabase.UpdateGameDateTime( int(gameId), gameDate, gameTime )
				dateIndex = nextDateIndex
				nextDateIndex = fcsScoreData.find( dateTag, dateIndex+1 )
		gameIDs = myDatabase.GetWeeklyFbsGames(week)
		soup = BeautifulSoup(fbsScoreData)
		for gameID in gameIDs:
			gameContainerString = '{0}-gameContainer'.format(gameID)
			gameData = soup.find(attrs={"id" : gameContainerString})
			gameDataString = '{0}'.format(gameData)
			gameSoup = BeautifulSoup(gameDataString)
			gameStatusString = '{0}-statusText'.format(gameID)
			gameStatus = soup.find(attrs={"id" : gameStatusString})
			gameStatusString = '{0}'.format(gameStatus)
			gameStatusString = gameStatusString[gameStatusString.find(">")+1:gameStatusString.rfind("<")]
			awayScoreString = '{0}-aTotal'.format(gameID)
			awayScore = soup.find(attrs={"id" : awayScoreString})
			if awayScore == None:
				awayScoreString = "0"
			else:
				awayScoreString = '{0}'.format(awayScore)
				awayScoreString = awayScoreString[awayScoreString.find(">")+1:awayScoreString.rfind("<")]
			homeScoreString = '{0}-hTotal'.format(gameID)
			homeScore = soup.find(attrs={"id" : homeScoreString})
			if homeScore == None:
				homeScoreString = "0"
			else:
				homeScoreString = '{0}'.format(homeScore)
				homeScoreString = homeScoreString[homeScoreString.find(">")+1:homeScoreString.rfind("<")]
			myDatabase.UpdateGameScore(int(gameID),int(awayScoreString),int(homeScoreString))
		if week < 17:
			gameIDs = myDatabase.GetWeeklyFcsGames(week)
			soup = BeautifulSoup(fcsScoreData)
			for gameID in gameIDs:
				gameContainerString = '{0}-gameContainer'.format(gameID)
				gameData = soup.find(attrs={"id" : gameContainerString})
				gameDataString = '{0}'.format(gameData)
				gameSoup = BeautifulSoup(gameDataString)
				gameStatusString = '{0}-statusText'.format(gameID)
				gameStatus = soup.find(attrs={"id" : gameStatusString})
				gameStatusString = '{0}'.format(gameStatus)
				gameStatusString = gameStatusString[gameStatusString.find(">")+1:gameStatusString.rfind("<")]
				awayScoreString = '{0}-aTotal'.format(gameID)
				awayScore = soup.find(attrs={"id" : awayScoreString})
				awayScoreString = '{0}'.format(awayScore)
				awayScoreString = awayScoreString[awayScoreString.find(">")+1:awayScoreString.rfind("<")]
				if awayScoreString == None:
					awayScoreString = "0"
				homeScoreString = '{0}-hTotal'.format(gameID)
				homeScore = soup.find(attrs={"id" : homeScoreString})
				homeScoreString = '{0}'.format(homeScore)
				homeScoreString = homeScoreString[homeScoreString.find(">")+1:homeScoreString.rfind("<")]
				if homeScoreString == None:
					homeScoreString = "0"
				myDatabase.UpdateGameScore(int(gameID),int(awayScoreString),int(homeScoreString))

	def ParseTeamUpdate( self, teamId ):
		myFetcher = NCAAFootballFetcher()
		myDatabase = NCAAFootballDatabase()

		teamName = myDatabase.GetTeamName( teamId )
		teamData = myFetcher.fetchTeamPage( teamId )
		soup = BeautifulSoup(teamData)
		recordTag = soup.find( 'div', {"class" : "sub-title"} )
		recordAndConference = recordTag.text
		record = recordAndConference.split(',')[0]
		teamRecord = record.split('-')
		if len(teamRecord) == 3:
			myDatabase.UpdateTeamRecord( teamId, teamRecord[0], teamRecord[1], teamRecord[2] )
		else:
			myDatabase.UpdateTeamRecord( teamId, teamRecord[0], teamRecord[1], 0 )
		 
	def ParseGameChronologies( self, week ):
		dateTag = '<h4 class=\"games-date\"'
		lineTag = '<p class=\"oddsright\"'
		gameChronology = 1
		
		myFetcher = NCAAFootballFetcher()
		myDatabase = NCAAFootballDatabase()
		
		fbsScoreData = myFetcher.fetchWeeklyFbsGames(week)
		dateIndex = fbsScoreData.find( dateTag )
		nextDateIndex = fbsScoreData.find( dateTag, dateIndex+1 )
		while dateIndex != -1:
			currentDaysGames = fbsScoreData[dateIndex:nextDateIndex]
			soup = BeautifulSoup(currentDaysGames)
			gameDate = soup.h4
			gameDate = gameDate.string
			if gameDate.find('\'') != -1:
				gameDate = gameDate.split('\'')[0]
			# Scan for games and update their dates
			games = soup.findAll( 'div', {'class':'game-status'} )
			for game in games:
				# this should provide a set of strings with the format:
				# <div class="game-status"><p id="[gameId]-statusText">Time</p></div>
				gameTime = game.text
				gameStr = game.find('p')
				gameId = gameStr['id']
				gameId = gameId.split('-')[0]
				myDatabase.UpdateGameChronology( gameId, gameChronology )
				gameChronology = gameChronology + 1
			dateIndex = nextDateIndex
			nextDateIndex = fbsScoreData.find( dateTag, dateIndex+1 )
