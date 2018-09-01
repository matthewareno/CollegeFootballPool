<?php

//error_reporting(E_ALL);
//ini_set('display_errors', 'on');

require_once( "database_common.php" );

function get_all_games() 
{
	$sql = "SELECT * FROM Games";
	return do_query( $sql );
}

function get_all_games_by_week( $week ) 
{
	if( $week < 0 or $week > 17 ) {
		die( "Invalid week provided: $week" );
	}
	$sql = "SELECT * FROM Games WHERE GameWeek=$week ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_fbs_games_by_week( $week ) 
{
	if( $week < 0 or $week > 17 ) {
		die( "Invalid week provided: $week" );
	}
	$sql = "SELECT * FROM Games WHERE GameWeek=$week AND Division=0 ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_fcs_games_by_week( $week )
{
	if( $week < 0 or $week > 17 ) {
		die( "Invalid week provided: $week" );
	}
	$sql = "SELECT * FROM Games WHERE GameWeek=$week AND Division=1 ORDER BY Chronology";
	return do_query( $sql );
}

function get_game_by_id( $id )
{
	$gameId = (int)$id;

	$sql = "SELECT * FROM Games WHERE P_Id=$gameId";
	return do_query( $sql );
}

function get_game_away_team( $id ) 
{
	$sql = "SELECT VisitorID FROM Games WHERE P_Id=$id";
	return do_query( $sql );
}

function get_game_home_team( $id ) 
{
	$sql = "SELECT HomeID FROM Games WHERE P_Id=$id";
	return do_query( $sql );
}

function get_game_date_by_id( $id )
{
	$sql = "SELECT GameDate FROM Games WHERE P_Id=$id";
	return do_query( $sql );
}

function get_game_time_by_id( $id )
{
	$sql = "SELECT GameTime FROM Games WHERE P_Id=$id";
	return do_query( $sql );
}

// Format for Picks Database:
// gameId INT PRIMARY KEY, winner INT, week INT, type VARCHAR(255), points INT 

// Format for User Picks Database:
// gameId INT, userId INT, winner INT, week INT 

function add_game_to_picks( $gameID, $gameType, $gamePoints, $gameWeek, $gameFavorite, $chronology )
{
	$sql = "INSERT INTO Picks (gameId, winner, week, type, points, underdog, Chronology) VALUES ($gameID, 0, $gameWeek, '$gameType', $gamePoints, $gameFavorite, $chronology)";
	return do_query( $sql );
}

function get_all_pick_games_by_week( $gameWeek )
{
	$sql = "SELECT * FROM Games WHERE GameWeek=$gameWeek AND P_Id IN (SELECT gameId FROM Picks WHERE week=$gameWeek) ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_non_pick_games_by_week( $gameWeek )
{
	$sql = "SELECT * FROM Games WHERE GameWeek=$gameWeek AND P_Id NOT IN (SELECT gameId FROM Picks WHERE week=$gameWeek) ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_pick_games_by_week_not_started( $gameWeek )
{
	$sql = "SELECT * FROM Games WHERE GameWeek=$gameWeek AND GameStatus=0 AND P_Id IN (SELECT gameId FROM Picks WHERE week=$gameWeek) ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_picks_by_week( $gameWeek )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_available_picks_by_week( $gameWeek )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek AND gameId IN (SELECT P_Id FROM Games WHERE GameWeek=$gameWeek AND GameStatus=0) ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_picks_by_week_and_type( $gameWeek, $gameType )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek AND type='$gameType' ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_available_picks_by_week_and_type( $gameWeek, $gameType )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek AND type='$gameType' AND gameId IN (SELECT P_Id FROM Games WHERE GameWeek=$gameWeek AND GameStatus=0) ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_picks_by_week_not_finished( $gameWeek )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek AND winner=0 ORDER BY Chronology";
	return do_query( $sql );
}

function get_all_picks_by_week_and_type_not_finished( $gameWeek, $gameType )
{
	$sql = "SELECT gameId FROM Picks WHERE week=$gameWeek AND winner=0 type='$gameType' ORDER BY Chronology";
	return do_query( $sql );
}

function get_pick_by_game_id( $gameId )
{
	$sql = "SELECT * FROM Picks WHERE gameId=$gameId";
	return do_query( $sql );
}

function get_pick_winner( $gameId )
{
	$sql = "SELECT winner FROM Picks WHERE gameId=$gameId";
	return do_query( $sql );
}

function get_pick_type_by_id( $id )
{
	$sql = "SELECT type FROM Picks WHERE gameId=$id";
	return do_query( $sql );
}

function get_pick_chronology_by_id( $id )
{
	$sql = "SELECT Chronology FROM Picks WHERE gameId=$id";
	return do_query( $sql );
}

function add_user_pick( $gameId, $userId, $winner, $week, $chronology )
{
	$sql = "INSERT INTO UserPicks (gameId, userId, winner, week, Chronology) VALUES ($gameId, $userId, $winner, $week, $chronology)";
	return do_query( $sql );
}

function delete_user_pick( $userId, $gameId )
{
	$sql = "DELETE FROM UserPicks WHERE userId=$userId AND gameId=$gameId";
	return do_query( $sql );
}

function update_user_pick( $gameId, $userId, $winner, $week )
{
	$sql = "UPDATE UserPicks SET winner=$winner WHERE gameId=$gameId AND userId=$userId AND week=$week";
	return do_query( $sql );
}

function get_user_picks_for_week( $userId, $gameWeek )
{
	$sql = "SELECT gameId,winner FROM UserPicks WHERE userId='$userId' AND week=$gameWeek ORDER BY Chronology";
	return do_query( $sql );
}

function get_user_pick_by_game( $userId, $gameId )
{
	$sql = "SELECT winner FROM UserPicks WHERE userId=$userId AND gameId=$gameId";
	return do_query( $sql );
}

function get_user_upset_pick_by_week( $userId, $week )
{
	$sql = "SELECT gameId FROM UserPicks WHERE userId=$userId AND week=$week";
	$userPicks = do_query( $sql );
	$sql = "SELECT gameId FROM Picks WHERE week=$week AND type='upset'";
	$upsetPicks = do_query( $sql );
	foreach( $userPicks as $userPick )
	{
		foreach( $upsetPicks as $upsetPick )
		{
			if( $upsetPick['gameId'] == $userPick['gameId'] )
				return $userPick['gameId'];
		}
	}
	return false;
}

function get_underdog_by_game( $gameId )
{
	$sql = "SELECT underdog FROM Picks WHERE gameId='$gameId'";
	return do_query( $sql );
}

function delete_pick_by_id( $gameId )
{
	$sql = "DELETE FROM Picks WHERE gameId=$gameId";
	return do_query( $sql );
}

function get_number_of_pick_games_completed( $week )
{
	$sql = "SELECT COUNT(*) FROM Picks WHERE winner != 0 AND week=$week";
	return do_query( $sql );
}

function get_user_picks_by_week_and_type( $userId, $week, $type )
{
	$sql = "SELECT gameId,winner FROM UserPicks WHERE userId=$userId AND week=$week ORDER BY Chronology";
	$picks = do_query( $sql );
	$results = array();
	foreach( $picks as $pick )
	{
		$sql = "SELECT type FROM Picks WHERE gameId=" . $pick['gameId'];
		$gameType = do_query( $sql )[0];
		if( $gameType['type'] == $type )
			$results[] = $pick;
	}
	return $results;
}

function get_game_chronology_by_id( $gameId )
{
	$sql = "SELECT Chronology FROM Games where P_Id=$gameId";
	return do_query( $sql );
}

function get_all_players_and_weekly_points( $gameWeek )
{
	$sql = "SELECT userId,points FROM WeeklyResults WHERE week=$gameWeek ORDER BY points DESC";
	return do_query( $sql );
}

function get_user_points_by_week( $userId, $gameWeek )
{
	$sql = "SELECT points FROM WeeklyResults WHERE week=$gameWeek and userId=$userId";
	return do_query( $sql );
}

?>
