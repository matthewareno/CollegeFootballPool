<?php

//error_reporting(E_ALL);
//ini_set('display_errors', 'on');

require_once( "database_common.php" );

function is_user_an_admin( $username ) {
	$sql = "SELECT userType FROM Users WHERE username='".$username."'";
	$userType = do_query( $sql );
	if( $userType[0][0] == 1 ) {
		return true;
	}
	else {
		return false;
	}
}

function get_all_user_info() 
{
	$sql = "SELECT * FROM Users";
	return do_query( $sql );
}

function get_user_info_by_id( $id ) 
{
	$sql = "SELECT * FROM Users WHERE id='" . $id . "'";
	return do_query( $sql );
}

function get_all_user_ids() 
{
	$sql = "SELECT id FROM Users ORDER BY firstName";
	return do_query( $sql );
}

function get_all_usernames() 
{
	$sql = "SELECT username FROM Users";
	return do_query( $sql );
}

function get_all_email_addresses()
{
	$sql = "SELECT email FROM Users";
	return do_query( $sql );
}

function get_all_email_addresses_for_mass_email()
{
	$sql = "SELECT DISTINCT email FROM Users WHERE massEmails=TRUE";
	return do_query( $sql );
}

function get_all_email_addresses_for_weekly_email()
{
	$sql = "SELECT email FROM Users WHERE weeklyEmails=TRUE";
	return do_query( $sql );
}

function get_user_username_by_id( $id )
{
	$sql = "SELECT username FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_id_from_username( $username )
{
	$sql = "SELECT id FROM Users WHERE username='" . $username . "'";
	return do_query( $sql );
}

function get_user_theme_by_username( $username )
{
	$sql = "SELECT theme FROM Users WHERE username='" . $username . "'";
	return do_query( $sql );
}

function get_user_email_by_id( $id )
{
	$sql = "SELECT email FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_email_by_username( $username )
{
	$sql = "SELECT email FROM Users WHERE username='" . $username . "'";
	return do_query( $sql );
}

function get_user_first_name_by_id( $id )
{
	$sql = "SELECT firstName FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_name_by_id( $id )
{
	$sql = "SELECT firstName,lastName FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_first_name_by_username( $username )
{
	$sql = "SELECT firstName FROM Users WHERE username='" . $username . "'";
	return do_query( $sql );
}

function get_user_full_name_by_username( $username )
{
	$sql = "SELECT firstName,lastName FROM Users WHERE username='" . $username . "'";
	return do_query( $sql );
}

function get_user_theme_by_id( $id )
{
	$sql = "SELECT theme FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_mass_emails_by_id( $id )
{
	$sql = "SELECT massEmails FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_weekly_emails_by_id( $id )
{
	$sql = "SELECT weeklyEmails FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_overall_record_by_id( $id )
{
	$sql = "SELECT overallWins,overallLoses,overallTies FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_user_conference_record_by_id( $id )
{
	$sql = "SELECT conferenceWins,conferenceLoses,conferenceTies FROM Users WHERE id=$id";
	return do_query( $sql );
}

function get_all_players_and_season_points()
{
	$sql = "SELECT id,seasonWins FROM Users ORDER BY seasonWins DESC, conferenceLoses";
	return do_query( $sql );
}

function get_all_players_and_overall_points() 
{
	$sql = "SELECT id,regularPoints FROM Users ORDER BY regularPoints DESC, overallLoses";
	return do_query( $sql );
}

function delete_user( $user ) 
{
	$sql = "DELETE FROM Users WHERE id='" . $user . "'";
	return do_query( $sql );
}

function update_user_conference( $user, $conference ) 
{
	$sql = "UPDATE Users SET conferenceId='" . $conference . "' WHERE username='" . $user . "'";
	return do_query( $sql );
}

function update_user_username( $user, $username ) 
{
	$sql = "UPDATE Users SET username='" . $username . "' WHERE username='" . $user . "'";
	return do_query( $sql );
}

function update_user_email( $user, $email ) 
{
	$sql = "UPDATE Users SET email='" . $email . "' WHERE username='" . $user . "'";
	return do_query( $sql );
}

function update_user_theme( $user, $theme )
{
	$sql = "UPDATE Users SET theme='" . $theme . "' WHERE id='" . $user . "'";
	return do_query( $sql );
}

function update_user_mass_emails( $user, $mass_emails )
{
	if( $mass_emails )
		$sql = "UPDATE Users SET massEmails=TRUE WHERE id=$user";
	else
		$sql = "UPDATE Users SET massEmails=FALSE WHERE id=$user";
	return do_query( $sql );
}

function update_user_weekly_report( $user, $weekly_report )
{
	if( $weekly_report )
		$sql = "UPDATE Users SET weeklyEmails=TRUE WHERE id=$user";
	else
		$sql = "UPDATE Users SET weeklyEmails=FALSE WHERE id=$user";
	return do_query( $sql );
}

function get_all_conferences() 
{
	$sql = "SELECT name FROM conferences";
	return do_query( $sql );
}

function add_new_conference( $conferenceName ) 
{
	$sql = "INSERT INTO conferences ( name ) VALUES ('" . $conferenceName . "')";
	return do_query( $sql );
}

function remove_conference( $conferenceName ) 
{
	$sql = "DELETE FROM conferences WHERE name='" . $conferenceName . "'";
	return do_query( $sql );
}

function get_conference_name_by_id( $conferenceId ) 
{
	$sql = "SELECT name FROM conferences WHERE id='" . $conferenceId . "'";
	return do_query( $sql );
}

function get_conference_id_by_name( $conferenceName ) 
{
	$sql = "SELECT id FROM conferences WHERE name='" . $conferenceName . "'";
	return do_query( $sql );
}

function get_all_players_in_conference( $conferenceName ) 
{
	$id = get_conference_id_by_name( $conferenceName );
	$sql = "SELECT id FROM Users WHERE conferenceId='" . $id[0]['id'] . "' ORDER BY conferencePoints DESC";
	return do_query( $sql );
}

function get_user_conference_points_by_id( $userId )
{
	$sql = "SELECT conferencePoints FROM Users WHERE id='" . $userId . "'";
	return do_query( $sql );
}

?>
