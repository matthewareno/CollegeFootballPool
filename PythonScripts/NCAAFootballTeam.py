class NCAAFootballTeam():
	id = 0
	name = ""
	fullname = ""
	conference = ""
	wins = 0
	loses = 0
	ties = 0
	url = ""
	icon = ""
	
	def __init__(self, teamId = 0):
		self.id = teamId

	def SetTeamURL(self, teamURL):
		self.url = teamURL

	def SetTeamIconURL(self, iconURL):
		self.icon = iconURL

	def SetTeamName(self, teamName):
		self.name = teamName

	def SetTeamFullName( self, fullName ):
		self.fullname = fullName

	def SetTeamConference(self, teamConference):
		self.conference = teamConference

	def SetTeamWins(self, wins):
		self.wins = wins

	def SetTeamLoses(self, loses):
		self.loses = loses

	def SetTeamTies(self, ties):
		self.ties = ties

	def AddWin(self):
		self.wins = self.wins + 1

	def AddLose(self):
		self.loses = self.loses + 1
	
	def AddTies(self):
		self.ties = self.ties + 1

	def GetTeamName(self):
		return self.name

	def GetTeamURL(self):
		return self.url

	def GetTeamIconURL(self):
		return self.icon

	def GetTeamConference(self):
		return self.conference

	def GetTeamRecord(self):
		return [self.wins, self.loses, self.ties]


