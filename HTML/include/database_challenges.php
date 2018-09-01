<?php

//error_reporting(E_ALL);
//ini_set('display_errors', 'on');

require_once( "database_common.php" );

function get_all_existing_challenges()
{
	$sql = "SELECT * From Challenges";
	return do_query( $sql );
}

function get_all_challenger_ids()
{
	$sql = "SELECT challenger1,challenger2 FROM Challenges";
	return do_query( $sql );
}

function add_challenge( $c1_id, $c2_id, $week )
{
	$sql = "INSERT INTO Challenges (challenger1, challenger2, c1_points, c2_points, week) values ($c1_id, $c2_id, 0, 0, $week)";
	return do_query( $sql );
}

function delete_challenge( $id )
{
	$sql = "DELETE From Challenges WHERE id=$id";
	return do_query( $sql );
}

function update_challenger1_points( $challenge_id, $c1_points )
{
	$sql = "UPDATE Challenges SET c1_points=$c1_points WHERE id=$challenge_id";
	return do_query( $sql );
}

function update_challenger2_points( $challenge_id, $c2_points )
{
	$sql = "UPDATE Challenges SET c2_points=$c2_points WHERE id=$challenge_id";
	return do_query( $sql );
}

function get_user_challenge_for_week( $userId, $week )
{
	$sql = "SELECT challenger1,challenger2,c1_points,c2_points FROM Challenges WHERE week=$week AND ( challenger1=$userId OR challenger2=$userId )";
	return do_query( $sql );
}

function get_all_user_challenges_by_week( $week )
{
	$sql = "SELECT * FROM Challenges WHERE week=$week";
	return do_query( $sql );
}

function get_latest_challenge_week()
{
	$sql = "SELECT DISTINCT( week ) FROM Challenges ORDER BY week DESC";
	$result = do_query( $sql );
	if( count( $result ) == 0 )
		return 1;
	else
		return $result[0]['week'];
}


?>
