import os
#import sqlite3
import MySQLdb
from NCAAFootballTeam import NCAAFootballTeam
from NCAAFootballGame import NCAAFootballGame

class NCAAFootballDatabase():
	host = "<Enter MySQL Server address here>"
	user = "<Enter MySQL Username here>"
	passwd = "<Enter MySQL Password here>"
	db = "<Enter MySQL Database name here>"
	__databaseInitialized = 0
	
	def __init__(self):
#		self.conn = sqlite3.connect( self.db )
#		self.cursor = self.conn.cursor()
		self.conn = MySQLdb.connect (self.host, self.user, self.passwd, self.db)
		self.cursor = self.conn.cursor()

	def InitializeDatabase(self):
		try:
			self.cursor.execute("show tables")
			currentTables = self.cursor.fetchall()
			foundTeams = 0
			foundGames = 0
			result = 0
			for table in currentTables:
				tableName = '{0}'.format(table)
				if tableName.find('Teams') != -1:
					foundTeams = 1
				if tableName.find('Games') != -1:
					foundGames = 1
			if foundTeams == 0:
				self.CreateTeamsTable()
			if foundGames == 0:
				self.CreateGamesTable()
			return result
		except sqlite3.Error, e:
			return -1

	def CreateTeamsTable(self):
		createTeamTable = 'CREATE TABLE Teams ({0},{1},{2},{3},{4},{5},{6},{7})'.format(
			"P_Id int NOT NULL",
			"Name varchar(255) NOT NULL",
			"FullName varchar(255) PRIMARY KEY NOT NULL",
			"Wins int",
			"Loses int",
			"Ties int",
			"URL varchar(1024) NOT NULL",
			"IconURL varchar(1024) NOT NULL"
			)
		try:	
			self.cursor.execute(createTeamTable)
			self.conn.commit()
		except sqlite3.Error, e:
			return

	def CreateGamesTable(self):
		createGameTable = 'CREATE TABLE Games ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10})'.format(
			"P_Id int PRIMARY KEY NOT NULL",
			"VisitorID int",
			"VisitorScore int",
			"HomeID int",
			"HomeScore int",
			"GameStatus int",
			"GameWeek int",
			"GameDate varchar(1024)",
			"GameTime varchar(1024)",
			"Division int",
			"Chronology int"
			)
		try:
			self.cursor.execute(createGameTable)
			self.conn.commit()
		except sqlite3.Error, e:
			return
	
	def AddNewTeam(self, team):
		encodedName = team.name.encode("utf-8")
		encodedFullName = team.fullname.encode("utf-8")
		encodedURL = team.url.encode("utf-8")
		encodedIcon = team.icon.encode("utf-8")
		addNewTeamCommand = 'INSERT INTO Teams (P_Id, Name, FullName, Wins, Loses, Ties, Ranking, URL, IconURL) VALUES ({0},"{1}","{2}",{3},{4},{5},{6},\'{7}\',\'{8}\')'.format(
			team.id,
			encodedName,
			encodedFullName,
			team.wins,
			team.loses,
			team.ties,
			0,
			encodedURL,
			encodedIcon
			)
		try:
			self.cursor.execute(addNewTeamCommand)
			self.conn.commit()
#		except sqlite3.Error, e:
		except MySQLdb.Error, e:
			# ignore error from team already existing
			if e.args[0] != 1062:
				print "AddNewTeam SQL Error: %s: %s" % ( e.args[0],  addNewTeamCommand )
			return

	def AddNewGame(self, game):
		addNewGameCommand = 'INSERT INTO Games (P_Id, VisitorID, VisitorFirstScore, VisitorSecondScore, VisitorThirdScore, VisitorFourthScore, VisitorOTScore, VisitorFinalScore, HomeID, HomeFirstScore, HomeSecondScore, HomeThirdScore, HomeFourthScore, HomeOTScore, HomeFinalScore, WinnerId, GameStatus, GameWeek, GameDate, GameTime, Odds, Division, NeutralSite, Chronology) VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},"{18}","{19}","{20}",{21},{22},{23})'.format(
			game.gameID,
			game.awayID,
			game.awayFirstScore,
			game.awaySecondScore,
			game.awayThirdScore,
			game.awayFourthScore,
			game.awayOTScore,
			game.awayFinalScore,
			game.homeID,
			game.homeFirstScore,
			game.homeSecondScore,
			game.homeThirdScore,
			game.homeFourthScore,
			game.homeOTScore,
			game.homeFinalScore,
			game.winnerID,
			game.gameStatus,
			game.gameWeek,
			game.gameDate,
			game.gameTime,
			game.gameOdds,
			game.gameDivision,
			game.neutralSite,
			game.gameIndex
			)
		try:
			self.cursor.execute(addNewGameCommand)
			self.conn.commit()
#		except sqlite3.Error, e:
		except MySQLdb.Error, e:
			# ignore error from game already existing
			if e.args[0] != 1062:
				print "AddNewGame SQL Error[%d]: %s" % ( e.args[0], e.args[1] )
			return       
 
	def UpdateTeamRecord(self, team, wins, loses, ties):
		updateTeamRecordCommand = 'UPDATE Teams SET Wins={0}, Loses={1}, Ties={2} WHERE P_Id={3}'.format(
			wins,
			loses,
			ties,
			team
			)
		try:
			self.cursor.execute(updateTeamRecordCommand)
			self.conn.commit()
		except sqlite3.Error, e:
			print 'UpdateTeamRecord SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return

	def UpdateTeamRecords( self, teams ):
		for team in teams:
			self.UpdateTeamRecord( team.id, team.wins, team.loses, team.ties )

	def UpdateGames( self, games ):
		self.UpdateGameScores( games )
		self.UpdateGameStatuses( games )
		self.UpdateGameDateTimes( games )

	def UpdatePicks( self, games, week ):
		picks = self.GetPicksByWeek( week )
		for pickID in picks:
			for game in games:
				if game.gameID == pickID:
					if game.winnerID != 0:
						self.SetPickWinnerByGameId( game.gameID, game.winnerID )
						break

	def UpdateGameScores( self, games ):
		for game in games:
			updateGameScoreCommand = 'UPDATE Games SET VisitorFirstScore={0}, VisitorSecondScore={1}, VisitorThirdScore={2}, VisitorFourthScore={3}, VisitorOTScore={4}, VisitorFinalScore={5}, HomeFirstScore={6}, HomeSecondScore={7}, HomeThirdScore={8}, HomeFourthScore={9}, HomeOTScore={10}, HomeFinalScore={11} WHERE P_Id={12}'.format(
				game.awayFirstScore,
				game.awaySecondScore,
				game.awayThirdScore,
				game.awayFourthScore,
				game.awayOTScore,
				game.awayFinalScore,
				game.homeFirstScore,
				game.homeSecondScore,
				game.homeThirdScore,
				game.homeFourthScore,
				game.homeOTScore,
				game.homeFinalScore,
				game.gameID
				)
			try:
				self.cursor.execute( updateGameScoreCommand )
				self.conn.commit()
			except sqlite3.Error, e:
				print 'UpdateGameScores SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
				return

	def UpdateGameStatuses(self, games ):
		updateGameStatusCommand = ""
		for game in games:
			if game.gameOdds != "":
				updateGameStatusCommand = 'UPDATE Games SET GameStatus={0}, WinnerId={1}, Odds="{2}" WHERE P_Id={3}'.format(
					game.gameStatus,
					game.winnerID,
					game.gameOdds,
					game.gameID
					)
			else:
				updateGameStatusCommand = 'UPDATE Games SET GameStatus={0}, WinnerId={1} WHERE P_Id={2}'.format(
					game.gameStatus,
					game.winnerID,
					game.gameID
					)
			try:
				self.cursor.execute(updateGameStatusCommand)
				self.conn.commit()
			except sqlite3.Error, e:
				print 'UpdateGameStatuses SQL Error[%d]: %s, %s' % (e.args[0], e.args[1], updateGameStatusCommand)
				return

	def UpdateGameDateTimes(self, games ):
		for game in games:
			updateGameDateTimeCommand = "UPDATE Games Set GameDate='{0}', GameTime='{1}' WHERE P_Id={2}".format(
				game.gameDate,
				game.gameTime,
				game.gameID
				)
			try:
				self.cursor.execute(updateGameDateTimeCommand)
				self.conn.commit()
			except sqlite3.Error, e:
				print 'UpdateGameDateTime SQL Error[%d]: %s' % (e.args[0], e.args[1])
				return

	def UpdateGamesInDatabase( self, databaseGames, websiteGames ):
		for websiteGame in websiteGames:
			gameUpdated = False
			for databaseGame in databaseGames:
				if databaseGame.gameID == websiteGame.gameID:
					print "Updating game %i in database..." % ( databaseGame.gameID )
					updateGameCommand = "UPDATE Games set VisitorID={0},VisitorFirstScore={1},VisitorSecondScore={2},VisitorThirdScore={3},VisitorFourthScore={4},VisitorOTScore={5},VisitorFinalScore={6},HomeID={7},HomeFirstScore={8},HomeSecondScore={9},HomeThirdScore={10},HomeFourthScore={11},HomeOTScore={12},HomeFinalScore={13},WinnerId={14},GameStatus={15},GameWeek={16},GameDate='{17}',GameTime='{18}',Odds='{19}',Chronology={20} WHERE P_Id={21}".format(
						websiteGame.awayID,
						websiteGame.awayFirstScore,
						websiteGame.awaySecondScore,
						websiteGame.awayThirdScore,
						websiteGame.awayFourthScore,
						websiteGame.awayOTScore,
						websiteGame.awayFinalScore,
						websiteGame.homeID,
						websiteGame.homeFirstScore,
						websiteGame.homeSecondScore,
						websiteGame.homeThirdScore,
						websiteGame.homeFourthScore,
						websiteGame.homeOTScore,
						websiteGame.homeFinalScore,
						websiteGame.winnerID,
						websiteGame.gameStatus,
						websiteGame.gameWeek,
						websiteGame.gameDate,
						websiteGame.gameTime,
						websiteGame.gameOdds,
						websiteGame.gameIndex,
						websiteGame.gameID )
					try:
						self.cursor.execute( updateGameCommand )
						self.conn.commit()
						gameUpdated = True
					except:
						print 'UpdateGamesInDatabase SQL Error[%d]: %s' % (e.args[0], e.args[1] )
						return
			if not gameUpdated:
				print "Adding new game %i..." % ( websiteGame.gameID )
				AddNewGame( websiteGame )

	def GetAllGameDataByWeek( self, week ):
		gameWeekData = []
		gameArray = []
		getGameDataByWeekCommand = 'SELECT * FROM Games WHERE GameWeek={0}'.format( week )
		try:
			self.cursor.execute( getGameDataByWeekCommand )
			gameWeekData = self.cursor.fetchall()
			for game in gameWeekData:
				gameString = '{0}'.format( game )
				gameString = gameString.lstrip( "(" )
				gameString = gameString.rstrip( ")" )
				gameData = gameString.split( "," )
				if len( gameData ) < 25:
					print gameData
				newGame = NCAAFootballGame()
				gameData[0] = gameData[0].rstrip( "L" )
				newGame.gameID = int( gameData[0] )
				gameData[1] = gameData[1].rstrip( "L" )
				newGame.awayID = int( gameData[1] )
				gameData[2] = gameData[2].rstrip( "L" )
				newGame.awayFirstScore = int( gameData[2] )
				gameData[3] = gameData[3].rstrip( "L" )
				newGame.awaySecondScore = int( gameData[3] )
				gameData[4] = gameData[4].rstrip( "L" )
				newGame.awayThirdScore = int( gameData[4] )
				gameData[5] = gameData[5].rstrip( "L" )
				newGame.awayFourthScore = int( gameData[5] )
				gameData[6] = gameData[6].rstrip( "L" )
				newGame.awayOTScore = int( gameData[6] )
				gameData[7] = gameData[7].rstrip( "L" )
				newGame.awayFinalScore = int( gameData[7] )
				gameData[8] = gameData[8].rstrip( "L" )
				newGame.homeID = int( gameData[8] )
				gameData[9] = gameData[9].rstrip( "L" )
				newGame.homeFirstScore = int( gameData[9] )
				gameData[10] = gameData[10].rstrip( "L" )
				newGame.homeSecondScore = int( gameData[10] )
				gameData[11] = gameData[11].rstrip( "L" )
				newGame.homeThirdScore = int( gameData[11] )
				gameData[12] = gameData[12].rstrip( "L" )
				newGame.homeFourthScore = int( gameData[12] )
				gameData[13] = gameData[13].rstrip( "L" )
				newGame.homeOTScore = int( gameData[13] )
				gameData[14] = gameData[14].rstrip( "L" )
				newGame.homeFinalScore = int( gameData[14] )
				gameData[15] = gameData[15].rstrip( "L" )
				newGame.winnerID = int( gameData[15] )
				gameData[16] = gameData[16].rstrip( "L" )
				newGame.gameStatus = int( gameData[16] )
				gameData[17] = gameData[17].rstrip( "L" )
				newGame.gameWeek = int( gameData[17] )
				newGame.gameDate = gameData[18] + ", " + gameData[19]
				newGame.gameTime = gameData[20]
				newGame.gameOdds = gameData[21]
				gameData[22] = gameData[22].rstrip( "L" )
				newGame.gameDivision = int( gameData[22] )
				gameData[23] = gameData[23].rstrip( "L" )
				newGame.gameIndex = int( gameData[23] )
				gameData[24] = gameData[24].rstrip( "L" )
				newGame.neutralSite = int( gameData[24] )
				gameArray.append( newGame )
			return gameArray
		except sqlite3.Error, e:
			print 'GetAllGameDataByWeek[%d]: %s, %s' % (e.args[0], e.args[1], getGameDataByWeekCommand)
			return None

	def GetTeamName(self, teamID):
		getTeamNameCommand = 'SELECT Name FROM Teams WHERE P_ID={0}'.format(teamID)
		try:
			self.cursor.execute(getTeamNameCommand)
			name = self.cursor.fetchone()
			if name != None:
				name = name[0]
			return name
		except sqlite3.Error, e:
			print 'GetTeamName SQL Error[%d]: %s, %s' % (e.args[0], e.args[1], getTeamNameCommand)
			return None

	def GetTeamFullName(self, teamID):
		getTeamFullNameCommand = 'SELECT FullName FROM Teams WHERE P_ID={0}'.format(teamID)
		try:
			self.cursor.execute(getTeamFullNameCommand)
			fullName = self.cursor.fetchone()[0]
			return fullName
		except sqlite3.Error, e:
			print 'GetTeamFullName SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None;

	def GetTeamURL(self, teamID):
		getTeamURLCommand = 'SELECT URL FROM Teams WHERE P_ID={0}'.format(teamID)
		try:
			self.cursor.execute(getTeamURLCommand)
			url = self.cursor.fetchone()
			return url
		except sqlite3.Error, e:
			print 'GetTeamURL SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None

	def GetTeamIconURL(self, teamID):
		getTeamIconURLCommand = 'SELECT Icon FROM Teams WHERE P_ID={0}'.format(teamID)
		try:
			self.cursor.execute(getTeamIconURLCommand)
			icon = self.cursor.fetchone()
			return icon
		except sqlite3.Error, e:
			print 'GetTeamIconURL SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None 

	def GetAllTeamIds( self ):
		teamIDList = []
		getAllTeamIdsCommand = 'SELECT P_Id FROM Teams'
		try:
			self.cursor.execute( getAllTeamIdsCommand )
			teamIds = self.cursor.fetchall()
			for teamId in teamIds:
				teamIDString = '{0}'.format( teamId )
				teamIDString = teamIDString.lstrip( "(" )
				teamIDString = teamIDString.rstrip( "L,)" )
				teamIDList.append( int(teamIDString) )
			return teamIDList	
		except sqlite3.Error, e:
			print 'GetAllTeamIds SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None 

	def GetTeamIdByName( self, name ):
		getTeamIdCommand = "SELECT P_Id FROM Teams WHERE Name='{0}'".format( name )

		try:
			self.cursor.execute(getTeamIdCommand)
			teamId = self.cursor.fetchone()
			if teamId != None:
				teamId = teamId[0]
			return teamId
		except sqlite3.Error, e:
			print 'GetTeamIdByName SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None

	def GetWeeklyFbsGames(self, week):
		gameIDList = []
		getWeeklyGamesCommand = 'SELECT P_Id FROM Games WHERE GameWeek={0} AND Division=0'.format(week)
		try:
			self.cursor.execute(getWeeklyGamesCommand)
			gameIDs = self.cursor.fetchall()
			for gameID in gameIDs:
				gameIDString = '{0}'.format(gameID)
				gameIDString = gameIDString.lstrip("(")
				gameIDString = gameIDString.rstrip("L,)")
				gameIDList.append(int(gameIDString))
			return gameIDList
		except sqlite3.Error, e:
			print 'GetWeeklyGames SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None
	
	def GetWeeklyFcsGames(self, week):
		gameIDList = []
		getWeeklyGamesCommand = 'SELECT P_Id FROM Games WHERE GameWeek={0} AND Division=1'.format(week)
		try:
			self.cursor.execute(getWeeklyGamesCommand)
			gameIDs = self.cursor.fetchall()
			for gameID in gameIDs:
				gameIDString = '{0}'.format(gameID)
				gameIDString = gameIDString.lstrip("(")
				gameIDString = gameIDString.rstrip("L,)")
				gameIDList.append(int(gameIDString))
			return gameIDList
		except sqlite3.Error, e:
			print 'GetWeeklyGames SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None

	def GetPicksByWeek(self, week):
		gameIDList = []
		getPicksByWeekCommand = 'SELECT gameId FROM Picks WHERE week={0}'.format(week)
		try:
			self.cursor.execute(getPicksByWeekCommand)
			gameIds = self.cursor.fetchall()
			for game in gameIds:
				gameIDList.append( game[0] )
			return gameIDList
		except sqlite3.Error, e:
			print 'GetPicksByWeek SQL Error[%d]: %s' % (e.args[0], e.args[1])
			return None

	def GetPicksAndPointsByWeek( self, week ):
		picks = {}
		sqlCommand = "SELECT gameId,points FROM Picks WHERE week={0}".format( week )

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchall()
			for result in results:
				picks[int(result[0])] = int( result[1] )
			return picks
		except sqlite3.Error, e:
			print 'GetPicksAndPointsByWeek SQL Error[%d]: %s, %s' % ( e.args[0], e.args[1], sqlCommand )
			return None

	def GetPickType( self, gameId ):
		sqlCommand = 'SELECT type FROM Picks WHERE gameId={0}'.format( gameId )
	
		try:
			self.cursor.execute( sqlCommand )
			gameType = self.cursor.fetchone()
			return gameType
		except sqlite3.Error, e:
			print 'GetPickType SQL Error[$d]: %s' % ( e.args[0], e.args[1] )
			return None

	def SetPickWinnerByGameId( self, gameId, winner ):
		setWinnerCommand = 'UPDATE Picks SET winner={0} WHERE gameId={1}'. format( winner, gameId )
		try:
			self.cursor.execute( setWinnerCommand )
			self.conn.commit()
		except sqlite3.Error, e:
			print 'SetWinnerByGameId SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetVisitorScoreForGame(self, gameId):
		getVisitorScoreCommand = 'SELECT VisitorScore FROM Games WHERE P_Id={0}'.format(gameId)
		try:
			self.cursor.execute( getVisitorScoreCommand )
			visitorScore = self.cursor.fetchone()
			return visitorScore[0]
		except sqlite3.Error, e:
			print 'GetVisitorScoreForGame SQL Error[%d]: %s' % (e.args[0], e.args[1] )
			return None

	
	def GetHomeScoreForGame(self, gameId):
		getHomeScoreCommand = 'SELECT HomeScore FROM Games WHERE P_Id={0}'.format(gameId)
		try:
			self.cursor.execute( getHomeScoreCommand )
			homeScore = self.cursor.fetchone()
			return homeScore[0]
		except sqlite3.Error, e:
			print 'GetHomeScoreForGame SQL Error[%d]: %s' % (e.args[0], e.args[1] )
			return None

	def GetVisitorIdByGame( self, gameId ):
		getVisitorIdCommand = 'SELECT VisitorID FROM Games WHERE P_Id={0}'.format( gameId )
		try:
			self.cursor.execute( getVisitorIdCommand )
			visitorId = self.cursor.fetchone()
			return visitorId[0]
		except sqlite3.Error, e:
			print 'GetVisitorIdByGame SQL Error[%d]: %s' % (e.args[0], e.args[1] )
			return None
			
	def GetHomeIdByGame( self, gameId ):
		getHomeIdCommand = 'SELECT HomeID FROM Games WHERE P_Id={0}'.format( gameId )
		try:
			self.cursor.execute( getHomeIdCommand )
			homeId = self.cursor.fetchone()
			return homeId[0]
		except sqlite3.Error, e:
			print 'GetHomeIdByGame SQL Error[%d]: %s' % (e.args[0], e.args[1] )
			return None

	def GetUserCorrectPicksByWeek( self, userId, week ):
		sqlCommand = "SELECT gameId FROM (SELECT Picks.gameId, Picks.winner FROM Picks WHERE week={0} UNION ALL SELECT UserPicks.gameId, UserPicks.winner FROM UserPicks WHERE week={1} AND userId={2}) t GROUP BY gameId, winner HAVING COUNT(*) = 2 ORDER BY gameId".format(
						week,
						week,
						userId
						)
		picks = []

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchall()
			return results
		except sqlite3.Error, e:
			print 'GetUserCorrectPicksByWeek SQL Error[%d]: %s, %s' % ( e.args[0], e.args[1], sqlCommand )
			return None

	def GetUserPicksByWeek( self, userId, week ):
		sqlCommand = "SELECT gameId,winner FROM UserPicks WHERE userId={0} AND week={1}".format( userId, week )
		picks = []

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchall()
			for result in results:
				picks.append( (result[0], result[1] ) )
			return picks
		except sqlite3.Error, e:
			print 'GetUserPicksByWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetWinnerByGame( self, gameId ):
		sqlCommand = "SELECT winner FROM Picks WHERE gameId={0}".format( gameId )

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchone()
			if results == False or results == None:
				return 0
			return results[0]
		except sqlite3.Error, e:
			print 'GetUserPicksByWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def ResetTeamRankings( self, week ):
		sqlCommand = "DELETE FROM Rankings WHERE week={0}".format( week )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
		except sqlite3.Error, e:
			print 'ResetTeamRankings SQL Error[%d}: %s' % ( e.args[0], e.args[1] )

	def SetTeamRank( self, team, rank, week ):
		sqlCommand = "INSERT INTO Rankings (teamId, week, rank) VALUES ({0},{1},{2})".format( team, week, rank )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
		except sqlite3.Error, e:
			print 'SetTeamRankings SQL Error[%d}: %s' % ( e.args[0], e.args[1] )


	def GetGameType( self, gameId ):
		sqlCommand = "SELECT type FROM Picks WHERE gameId={0}".format( gameId )

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchone()
			return results[0]
		except sqlite3.Error, e:
			print 'GetGameType SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetGameStatus( self, gameId ):
		sqlCommand = "SELECT GameTime FROM Games WHERE P_Id={0}".format( gameId )

		try:
			self.cursor.execute( sqlCommand )
			result = self.cursor.fetchone()
			return result[0]
		except sqlite3.Error, e:
			print 'GetGameStatus SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetNumberOfWinners( self, gameId, winner ):
		sqlCommand = "SELECT COUNT(*) FROM UserPicks WHERE gameId={0} AND winner={1}".format( gameId, winner )

		try:
			self.cursor.execute( sqlCommand )
			result = self.cursor.fetchone()
			return result[0]
		except sqlite3.Error, e:
			print 'GetNumberOfWinners SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return 0

	def SetUserWeeklyPoints( self, userId, week, points ):
		sqlInsertCommand = "INSERT INTO WeeklyResults ( userId, points, week ) VALUES ( {0}, {1}, {2} )".format( userId, points, week )
		sqlUpdateCommand = "UPDATE WeeklyResults SET points={0} WHERE userId={1} AND week={2}".format( points, userId, week )
		sqlSelectCommand = "SELECT points FROM WeeklyResults WHERE userId={0} AND week={1}".format( userId, week )

		try:
			self.cursor.execute( sqlSelectCommand )
			result = self.cursor.fetchone()
			if result == None:
				self.cursor.execute( sqlInsertCommand )
			else:
				self.cursor.execute( sqlUpdateCommand )
			self.conn.commit()
		except sqlite3.Error, e:
			print 'SetUserWeeklyPoints SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			print 'SQL command: %s' % ( sqlUpdateCommand )
			return None

	def GetUserWeeklyPoints( self, userId, week ):
		sqlCommand = "SELECT points FROM WeeklyResults WHERE userId={0} AND week={1}".format( userId, week )

		try:
			self.cursor.execute( sqlCommand )
			result = self.cursor.fetchone()
			if result == None or result[0] == None:
				return 0
			else:
				return result[0]
		except sqlite3.Error, e:
			print 'GetUserWeeklyPoints SQL Error[%d]: %s' % ( e.args[0], e.args[1] ) 
			return 0

	def GetLowestScoreByWeek( self, week, userId ):
		sqlCommand = "SELECT MIN(NULLIF(points,0)) FROM WeeklyResults WHERE week={0}".format( week )

		try:
			self.cursor.execute( sqlCommand )
			result = self.cursor.fetchone()
			if result == None or result[0] == None:
				return 0
			else:
				return result[0]
		except sqlite3.Error, e:
			print 'GetLowestScoreByWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return 0

	def GetAllChallenges( self ):
		sqlCommand = "SELECT * from Challenges"

		try:
			self.cursor.execute( sqlCommand )
			challenges = self.cursor.fetchall()
			return challenges
		except sqlite3.Error, e:
			print 'GetAllChallenges SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetAllUserChallenges( self, userId ):
		sqlCommand = "SELECT * FROM Challenges WHERE challenger1={0} OR challenger2={1}".format( userId, userId )

		try:
			self.cursor.execute( sqlCommand )
			challenges = self.cursor.fetchall()
			return challenges
		except sqlite3.Error, e:
			print 'GetAllUserChallenges SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None


	def SetChallenger1Points( self, challenge, points ):
		sqlCommand = "UPDATE Challenges Set c1_points={0} WHERE id={1}".format( points, challenge )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
			return 0
		except sqlite3.Error, e:
			print 'SetChallenge1Points SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def SetChallenger2Points( self, challenge, points ):
		sqlCommand = "UPDATE Challenges Set c2_points={0} WHERE id={1}".format( points, challenge )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
			return 0
		except sqlite3.Error, e:
			print 'SetChallenge1Points SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def SetChallengeWinner( self, challenge, winner ):
		sqlCommand = "UPDATE Challenges SET winner={0} WHERE id={1}".format( winner, challenge )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
			return 0
		except sqlite3.Error, e:
			print 'SetChallengeWinner SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetPicksWeek( self ):
		sqlCommand = "SELECT MAX( week ) FROM Picks"

		try:
			self.cursor.execute( sqlCommand )
			currentWeek = self.cursor.fetchone()
			if currentWeek == None or currentWeek[0] == None:
				return 1
			else:
				return currentWeek[0]
		except sqlite3.Error, e:
			print 'GetPicksWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return 0
		
	def GetScoresWeek( self ):	
		for i in range( 1,18 ):
			sqlCommand = "SELECT GameTime FROM Games WHERE GameWeek={0}".format( i )

			try:
				self.cursor.execute( sqlCommand )
				gameTimes = self.cursor.fetchall()
				for gameTime in gameTimes:
					if gameTime[0] == None:
						continue
					if 'Final' not in gameTime[0]:
						if 'Suspend' not in gameTime[0]:
							if 'Postponed' not in gameTime[0]:
								if 'Canceled' not in gameTime[0]:
									return i
#									pickSqlCommand = "SELECT * FROM Picks WHERE week={0}".format( i )
#									self.cursor.execute( pickSqlCommand )
#									picks = self.cursor.fetchall()
#									if len(picks) == 0:
#										return i-1
#									else:
#									return i
			except sqlite3.Error, e:
				print 'GetScoresWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )

		return 17
	

	def GetChallengeWeek( self ):
		currentWeek = self.GetPicksWeek()
		sqlCommand = "SELECT * FROM Picks WHERE week={0} and winner=0".format( currentWeek )

		try:
			self.cursor.execute( sqlCommand )
			results = self.cursor.fetchall()
			if results == None or len( results ) == 0:
				return currentWeek + 1
			else:
				return currentWeek
		except sqlite3.Error, e:
			print 'GetChallengeWeek SQL Error[%d]: %s' % ( e.args[0], e.args[1] )

	def UpdateGameChronology( self, gameId, chronology ):
		sqlCommand = "UPDATE Games SET Chronology={0} WHERE P_Id={1}".format( chronology, gameId )
		sqlCommand2 = "UPDATE UserPicks SET Chronology={0} WHERE gameId={1}".format( chronology, gameId )

		try:
			self.cursor.execute( sqlCommand )
			self.cursor.execute( sqlCommand2 )
			self.conn.commit()
			return 0
		except sqlite3.Error, e:
			print 'SetGameChronology SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

