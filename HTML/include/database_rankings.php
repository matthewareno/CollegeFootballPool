<?php

//error_reporting(E_ALL);
//ini_set('display_errors', 'on');

require_once( "database_common.php" );

function get_team_rank_by_week( $teamId, $week )
{
	$sql = "SELECT rank FROM Rankings WHERE teamId=$teamId AND week=$week";
	return do_query( $sql );
}

?>
