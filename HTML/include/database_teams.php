<?php

//error_reporting(E_ALL);
//ini_set('display_errors', 'on');

require_once( "database_common.php" );

function get_all_teams() 
{
	$sql = "SELECT * FROM Teams";
	return do_query( $sql );
}

function get_team_by_id( $id ) 
{
	$sql = "SELECT * FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

function get_team_id_by_name( $name )
{
	$sql = "SELECT P_Id FROM Teams WHERE Name='$name'";
	return do_query( $sql );
}

function get_team_name_by_id( $id ) 
{
	$sql = "SELECT Name,FullName FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

function get_team_record_by_id( $id ) 
{
	$sql = "SELECT Wins,Loses,Ties FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

function get_team_url_by_id( $id ) 
{
	$sql = "SELECT URL FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

function get_team_icon_url_by_id( $id )
{
	$sql = "SELECT IconURL FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

function get_team_game_info_by_id( $id )
{
	$sql = "SELECT Name,IconURL FROM Teams WHERE P_Id=$id";
	return do_query( $sql );
}

?>
