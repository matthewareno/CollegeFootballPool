<?php

require("constants.php");

//error_reporting( E_ALL );
//ini_set( 'display_errors', 'on' );

function do_query( $sql ) 
{
	if( $db = mysqli_connect( DB_SERVER, DB_USER, DB_PASS, DB_NAME ) )
	{
		$result = mysqli_query( $db, $sql ) or die( "Database error:".mysql_error() );
		$data = array();
		if( gettype( $result ) == 'boolean' )
		{
			return $result;
		}
		while( $row = mysqli_fetch_array( $result ) )
		{
			$data[] = $row;
		}
		mysqli_close( $db );
		return $data;
	}
	else
	{
		die( "Cannot connect to database:".mysql_error() );
	}
}

function get_current_score_week()
{
	for( $i = 1; $i <= 17; $i++ )
	{
		$sql = "SELECT GameTime FROM Games WHERE GameWeek=$i";
		$gameTimes = do_query( $sql );
		foreach( $gameTimes as $gameTime )
		{
			if( strstr( $gameTime['GameTime'], "Final" ) == false )
			{
				if( strstr( $gameTime['GameTime'], "Suspend" ) == false )
				{
					if( strstr( $gameTime['GameTime'], "Postponed" ) == false )
					{
						if( strstr( $gameTime['GameTime'], "Canceled" ) == false )
						{
							return $i;
						}
					}

				}
			}
		}
	}

	return 1;
}

function get_current_pick_week()
{
	$lastPickWeek = 1;

	for( $i = 1; $i <= 17; $i++ )
	{
		$sql = "SELECT * FROM Picks WHERE week=$i";
		$picks = do_query( $sql );
		if( count( $picks ) > 0 )
			$lastPickWeek = $i;
	}

	return $lastPickWeek;
}

function get_current_week()
{
	$currentScoreWeek = get_current_score_week();
	$currentPickWeek = get_current_pick_week();

	if( $currentPickWeek < $currentScoreWeek )
		return $currentPickWeek;
	else
		return $currentScoreWeek;
}

