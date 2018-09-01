import os
import MySQLdb

class NCAAFootballUserDatabase():
	host = "<Enter MySQL Server address here>"
	user = "<Enter MySQL Username here>"
	passwd = "<Enter MySQL Password here>"
	db = "<Enter MySQL Database name here>"
	__databaseInitialized = 0
	
	def __init__(self):
		self.conn = MySQLdb.connect (self.host, self.user, self.passwd, self.db)
		self.cursor = self.conn.cursor()

	def GetAllUserIds(self):
		sqlCommand = "SELECT id FROM Users";
		results = []
		try:
			self.cursor.execute( sqlCommand )
			users = self.cursor.fetchall()
			for user in users:
				results.append( user[0] )
			return results
		except MySQLdb.Error, e:
			print 'GetAllUserIds SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetUserRegularPoints(self, userId):
		sqlCommand = "SELECT regularPoints FROM Users WHERE id={0}".format( userId )
	
		try:
			self.cursor.execute( sqlCommand )
			points = self.cursor.fetchone()
			return points[0]
		except MySQLdb.Error, e:
			print 'GetUserRegularPoints SQL Error [%d}: %s' % (e.args[0], e.args[1] )
			return None

	def SetUserSeasonPoints( self, userId, seasonPoints ):
		sqlCommand = "UPDATE Users SET seasonWins={0} WHERE id={1}".format( seasonPoints, userId )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
		except MySQLdb.Error, e:
			print 'SetUserSeasonPoints SQL Error[%d]: %s' % ( e.args[0], e.args[1] )

	def SetUserRegularPoints( self, userId, points ):
		sqlCommand = "UPDATE Users SET regularPoints={0} WHERE id={1}".format( points, userId )
		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
		except MySQLdb.Error, e:
			print 'SetUserRegularPoints SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
	
	def GetUserConferencePoints(self, userId):
		sqlCommand = "SELECT conferencePoints FROM Users WHERE id={0}".format( userId )
	
		try:
			self.cursor.execute( sqlCommand )
			points = self.cursor.fetchone()
			return points[0]
		except MySQLdb.Error, e:
			print 'GetUserRegularPoints SQL Error [%d}: %s' % (e.args[0], e.args[1] )
			return None

	def SetUserConferencePoints( self, userId, points ):
		sqlCommand = "UPDATE Users SET conferencePoints={0} WHERE id={1}".format( points, userId )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
		except MySQLdb.Error, e:
			print 'SetUserRegularPoints SQL Error[%d]: %s' % ( e.args[0], e.args[1] )

	def GetUserFirstNameById( self, userId ):
		sqlCommand = "SELECT firstName FROM Users WHERE id={0}".format( userId )
	
		try:
			self.cursor.execute( sqlCommand )
			firstName = self.cursor.fetchone()
			return firstName[0]
		except MySQLdb.Error, e:
			print 'GetUserRegularPoints SQL Error [%d}: %s' % (e.args[0], e.args[1] )
			return None

	def SetUserOverallChallengeRecord( self, userId, userWins, userLoses, userTies ):
		sqlCommand = "UPDATE Users SET overallWins={0},overallLoses={1},overallTies={2} WHERE id={3}".format( userWins, userLoses, userTies, userId )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
			return 0
		except MySQLdb.Error, e:
			print 'SetUserOverallChallengeRecord SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def SetUserConferenceChallengeRecord( self, userId, userWins, userLoses, userTies ):
		sqlCommand = "UPDATE Users SET conferenceWins={0},conferenceLoses={1},conferenceTies={2} WHERE id={3}".format( userWins, userLoses, userTies, userId )

		try:
			self.cursor.execute( sqlCommand )
			self.conn.commit()
			return 0
		except MySQLdb.Error, e:
			print 'SetUserConferenceChallengeRecord SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None

	def GetUserConferenceById( self, userId ):
		sqlCommand = "SELECT conferenceId FROM Users WHERE id={0}".format( userId )

		try:
			self.cursor.execute( sqlCommand )
			conferenceId = self.cursor.fetchone()
			return conferenceId[0]
		except MySQLdb.Error, e:
			print 'GetUserConferenceById SQL Error[%d]: %s' % ( e.args[0], e.args[1] )
			return None
