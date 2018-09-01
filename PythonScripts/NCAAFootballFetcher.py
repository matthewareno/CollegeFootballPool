import urllib 

fbsConfId = 80
fcsConfId = 81
seasonYear = 2018
seasonType = 2
bowlType = 3

class NCAAFootballFetcher():
	baseFbsScoreboardURL = "http://espn.go.com/college-football/scoreboard/_/group/" + str(fbsConfId) + "/year/" + str(seasonYear) + "/seasontype/" + str(seasonType) + "/week/"
	baseFcsScoreboardURL = "http://espn.go.com/college-football/scoreboard/_/group/" + str(fcsConfId) + "/year/" + str(seasonYear) + "/seasontype/" + str(seasonType) + "/week/"
	bowlFbsScoreboardURL = "http://espn.go.com/college-football/scoreboard/_/group/" + str(fbsConfId) + "/year/" + str(seasonYear) + "/seasontype/" + str(bowlType) + "/week/"
	teamListingURL = "http://espn.go.com/college-football/teams"
	teamHomePageURL = "http://espn.go.com/college-football/team/_/id/"
	teamScheduleBaseURL = "http://espn.go.com/college-football/team/schedule/_/id/"
	teamRankingBaseURL = "http://espn.go.com/college-football/rankings/_/poll/1/week/"

	def fetchWeeklyFbsGames(self, weekNumber=1):
		if weekNumber == 17:
			return self.fetchFbsBowlGames( weekNumber )
		weeksURL = self.baseFbsScoreboardURL + str(weekNumber)
		print weeksURL
		f = urllib.urlopen(weeksURL)
		s = f.read()
		return s

	def fetchWeeklyFcsGames(self, weekNumber=1):
		if weekNumber > 16:
			return None
		weeksURL = self.baseFcsScoreboardURL + str(weekNumber)
		f = urllib.urlopen(weeksURL)
		s = f.read()
		return s

	def fetchFbsBowlGames( self, weekNumber=17):
		bowlsURL = self.bowlFbsScoreboardURL + str(1)
		f = urllib.urlopen(bowlsURL)
		s = f.read()
		return s

	def fetchTeamListings(self):
		f = urllib.urlopen(self.teamListingURL)
		s = f.read()
		return s

	def fetchTeamPage(self, teamID):
		teamPageURL = self.teamHomePageURL+str(teamID)+"/"
		f = urllib.urlopen(teamPageURL)
		s = f.read()
		return s

	def fetchTeamSchedule(self, teamID):
		teamScheduleURL = self.teamScheduleBaseURL+str(teamID)+"/"
		f = urllib.urlopen(teamScheduleURL)
		s = f.read()
		return s

	def fetchTeamRankings(self, week):
		teamRankingURL = self.teamRankingBaseURL+str(week)
		f = urllib.urlopen(teamRankingURL)
		s = f.read()
		return s

