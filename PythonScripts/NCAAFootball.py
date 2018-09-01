from NCAAFootballDatabase import NCAAFootballDatabase
from NCAAFootballUserDatabase import NCAAFootballUserDatabase
from NCAAFootballGame import NCAAFootballGame
from NCAAFootballParser import NCAAFootballParser
from NCAAFootballTeam import NCAAFootballTeam
import MySQLdb

class NCAAFootball():

	def __init__(self):
		self.database = NCAAFootballDatabase()
		self.userDatabase = NCAAFootballUserDatabase()
		self.parser = NCAAFootballParser()

	def Initialize(self):
#		result = self.database.InitializeDatabase()
#		if result == 0 or result == 2:
#			self.LoadTeamsData()
#		if result == 0 or result == 1:
			self.LoadGamesData()

	def LoadTeamsData(self):
		self.teamList = self.parser.ParseTeamsPage()
		for team in self.teamList:
			team = self.parser.ParseTeamHomePage( team[0], team[1] )
			if team != None:
				self.database.AddNewTeam(team)	

	def LoadGamesData(self):
		for i in range(1, 16):
			print "Retrieving games for week %d..." % ( i )
			games = []
			teams = []
			self.parser.ParseFbsGameWeek(i, games, teams)
			self.parser.ParseFcsGameWeek(i, games, teams)
#			self.parser.ParseFbsBowlGames( games, teams )
			print "Found %i games.  Adding to database..." % (len(games))
			for game in games:
				self.database.AddNewGame(game)
#		databaseGames = []
#		websiteGames = []
#		websiteTeams = []
#		print "Updating bowl games..."
#		self.parser.ParseFbsBowlGames(games, teams)
#		for game in games:
#			self.database.AddNewGame(game)
#		databaseGames = self.database.GetAllGameDataByWeek( 17 )
#		self.parser.ParseFbsBowlGames( websiteGames, websiteTeams )
#		if not databaseGames:
#			print "Database appears empty for week %i.  Adding games from website..." % (17)
#			for game in websiteGames:
#				self.database.AddNewGame( game )
#		else:
#			print "Updating games in database with new data..." 
#			self.database.UpdateGamesInDatabase( databaseGames, websiteGames )

	def LoadTeamRankings(self):
		currentWeek = self.database.GetChallengeWeek()
		self.database.ResetTeamRankings( currentWeek )
		rankings = self.parser.ParseTeamRankings( currentWeek )
		count = 1
		for team in rankings:
			teamId = self.database.GetTeamIdByName( team )
			if( teamId == None ):
				if( team == "BYU" ):
					teamId = self.database.GetTeamIdByName( 'Brigham Young' )
				continue
			self.database.SetTeamRank( teamId, count, currentWeek )
			count += 1

	def UpdateAllTeamRecords(self):
		teams = self.database.GetAllTeamIds()
		for team in teams:
			self.parser.ParseTeamUpdate( team )

	def UpdateAllGameData(self):
		games = []
		teams = []
		currentWeek = self.database.GetScoresWeek()
		if currentWeek == 17:
			self.parser.ParseFbsBowlGames( games, teams )
		else:
			self.parser.ParseFbsGameWeek( currentWeek, games, teams )
			self.parser.ParseFcsGameWeek( currentWeek, games, teams )
		self.database.UpdateGames( games )
		self.database.UpdatePicks( games, currentWeek )
		self.database.UpdateTeamRecords( teams )

	def GetUserPointsByWeek( self, picks, userId, week ):
		correctPicks = self.database.GetUserCorrectPicksByWeek( userId, week )
		totalPoints = 0

		for correctPick in correctPicks:
			totalPoints += picks[correctPick[0]]

		return totalPoints

	def UpdateUserPoints(self):
		userIds = self.userDatabase.GetAllUserIds()
		currentWeek = self.database.GetScoresWeek()

		for user in userIds:
			totalPoints = 0
			for week in range( 1, currentWeek+1 ):
				pickInfo = self.database.GetPicksAndPointsByWeek( week )
				weeklyPoints = self.GetUserPointsByWeek( pickInfo, user, week )
				self.database.SetUserWeeklyPoints( user, week, weeklyPoints )
				totalPoints = totalPoints + weeklyPoints
			self.userDatabase.SetUserSeasonPoints( user, totalPoints )

	def UpdateChallengeResults(self):
		challenges = self.database.GetAllChallenges()
		currentWeek = self.database.GetChallengeWeek()

		for challenge in challenges:
			challengeId = challenge[0]
			challenger1 = challenge[1]
			challenger2 = challenge[2]
			challengeWeek = challenge[5]

			challenger1Points = self.database.GetUserWeeklyPoints( challenger1, challengeWeek )
			challenger2Points = self.database.GetUserWeeklyPoints( challenger2, challengeWeek )
			self.database.SetChallenger1Points( challengeId, challenger1Points )
			self.database.SetChallenger2Points( challengeId, challenger2Points )
			if( challengeWeek < currentWeek ):
				if( challenger1Points > challenger2Points ):
					self.database.SetChallengeWinner( challengeId, challenger1 )
				elif( challenger2Points > challenger1Points ):
					self.database.SetChallengeWinner( challengeId, challenger2 )
				else:
					self.database.SetChallengeWinner( challengeId, 255 )
			else:
				self.database.SetChallengeWinner( challengeId, 0 )

	def UpdateChallengePoints(self):
		userIds = self.userDatabase.GetAllUserIds()

		for user in userIds:
			userOverallWins = 0
			userOverallLoses = 0
			userOverallTies = 0
			userConferenceWins = 0
			userConferenceLoses = 0
			userConferenceTies = 0
			challenges = self.database.GetAllUserChallenges( user )
			for challenge in challenges:
				challengeWinner = challenge[6]
				if( challengeWinner == user ):
					userOverallWins = userOverallWins + 1
				elif( challengeWinner == 255 ):
					userOverallTies = userOverallTies + 1
				elif( challengeWinner == 0 ):
					continue
				else:
					userOverallLoses = userOverallLoses + 1

				c1_conference = self.userDatabase.GetUserConferenceById( challenge[1] )
				c2_conference = self.userDatabase.GetUserConferenceById( challenge[2] )
				if( c1_conference == c2_conference ):
					if( challengeWinner == user ):
						userConferenceWins = userConferenceWins + 1
					elif( challengeWinner ==255 ):
						userConferenceTies = userConferenceTies + 1
					elif( challengeWinner == 0 ):
						continue;
					else:
						userConferenceLoses = userConferenceLoses + 1

			userConferencePoints = ( userConferenceWins * 2 ) + ( userConferenceTies * 1 )
			userOverallPoints = ( userOverallWins * 2 ) + ( userOverallTies * 1 )
			self.userDatabase.SetUserConferenceChallengeRecord( user, userConferenceWins, userConferenceLoses, userConferenceTies )
			self.userDatabase.SetUserOverallChallengeRecord( user, userOverallWins, userOverallLoses, userOverallTies )
			self.userDatabase.SetUserConferencePoints( user, userConferencePoints )
			self.userDatabase.SetUserRegularPoints( user, userOverallPoints );

	def UpdateGameChronologies( self ):
		currentWeek = self.database.GetCurrentWeek()
		for i in range(1, 18):
			self.parser.ParseGameChronologies( i )

