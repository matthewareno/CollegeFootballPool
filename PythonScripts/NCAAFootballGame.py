class NCAAFootballGame():
	gameID = 0
	awayID = 0
	awayFirstScore = 0
	awaySecondScore = 0
	awayThirdScore = 0
	awayFourthScore = 0
	awayOTScore = 0
	awayFinalScore = 0
	awayRecord = ""
	homeID = 0
	homeFirstScore = 0
	homeSecondScore = 0
	homeThirdScore = 0
	homeFourthScore = 0
	homeOTScore = 0
	homeFinalScore = 0
	homeRecord = ""
	winnerID = 0
	gameStatus = 0
	gameWeek = 0
	gameDate = ""
	gameTime = ""
	gameOdds = ""
	gameDivision = 0
	neutralSite = False
	gameIndex = 0
	
	def __init__( self ):
		self.gameID = 0
		self.awayID = 0
		self.awayFirstScore = 0
		self.awaySecondScore = 0
		self.awayThirdScore = 0
		self.awayFourthScore = 0
		self.awayOTScore = 0
		self.awayFinalScore = 0
		self.awayRecord = ""
		self.homeID = 0
		self.homeFirstScore = 0
		self.homeSecondScore = 0
		self.homeThirdScore = 0
		self.homeFourthScore = 0
		self.homeOTScore = 0
		self.homeFinalScore = 0
		self.homeRecord = ""
		self.winnerID = 0
		self.gameStatus = 0
		self.gameWeek = 0
		self.gameDate = ""
		self.gameTime = ""
		self.gameOdds = ""
		self.gameDivision = 0
		self.neutralSite = False
		self.gameIndex = 0
    
	def __str__( self ):
		return "GameID: %i\nawayID: %i\nawayFirstScore: %i\nawaySecondScore: %i\nawayThirdScore: %i\nawayFourthScore: %i\nawayOTScore: %i\nawayFinalScore: %i\nhomeID: %i\nhomeFirstScore: %i\nhomeSecondScore: %i\nhomeThirdScore: %i\nhomeFourthScore: %i\nhomeOTScore: %i\nhomeFinalScore: %i\nwinnerID: %i\ngameStatus: %i\ngameWeek: %i\ngameData: %s\ngameTime: %s\ngameOdds: %s\ngameDivision: %i\nneutralSite: %i\ngameIndex: %i\n" % (
				self.gameID,
				self.awayID,
				self.awayFirstScore,
				self.awaySecondScore,
				self.awayThirdScore,
				self.awayFourthScore,
				self.awayOTScore,
				self.awayFinalScore,
				self.homeID,
				self.homeFirstScore,
				self.homeSecondScore,
				self.homeThirdScore,
				self.homeFourthScore,
				self.homeOTScore,
				self.homeFinalScore,
				self.winnerID,
				self.gameStatus,
				self.gameWeek,
				self.gameDate,
				self.gameTime,
				self.gameOdds,
				self.gameDivision,
				self.neutralSite,
				self.gameIndex )
