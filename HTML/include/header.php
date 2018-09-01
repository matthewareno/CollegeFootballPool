<?php
//	error_reporting(E_ALL);
//	ini_set('display_errors', 'on');
	require('include/session_common.php');
    require('include/security.php');
	require('include/database_users.php');
	require('include/database_challenges.php');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<title>NCAA Football Pool</title>
	<link href="css/main.css" rel="stylesheet" type="text/css" media="screen, print" />
<?php
	if(!empty($_SESSION['user']))
	{
		$username = htmlentities($_SESSION['user']['username'], ENT_QUOTES, 'UTF-8');
		$theme = get_user_theme_by_username( $username )[0];

		if( $theme["theme"] == "1" ) {
			echo '<link href="css/lsu.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 2 ) {
			echo '<link href="css/latech.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 3 ) {
			echo '<link href="css/utah_state.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 4 ) {
			echo '<link href="css/texas.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 5 ) {
			echo '<link href="css/alabama.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 6 ) {
			echo '<link href="css/notre_dame.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 7 ) {
			echo '<link href="css/byu.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 8 ) {
			echo '<link href="css/clemson.css" rel="stylesheet" type="text/css" media="screen, print" />';
		} elseif( $theme["theme"] == 9 ) {
			echo '<link href="css/texas_am.css" rel="stylesheet" type="text/css" media="screen, print" />';
		}
	}
?>
</head>

<body>
	<!-- page header -->
	<div id="bgextend">
		<div id="pageContent">
			<div class="navbar">
				<table width="100%" height="12" cellspacing="0" border="0">
					<tr>
						<td width="50">
							<img src=images/ncaa-football-logo.jpg alt=" " height="50" width="50">
						</td>
						<td align="center">
							<h1 class="title">NCAA Football Pool</h1>
						</td>
						<td width="50">
							<img src=images/ncaa-football-logo.jpg alt=" " height="50" width="50">
						</td>
					</tr>
				</table>
			</div>
			<!-- menu -->
			<div class="menu">
				<ul>
					<li><a href="index.html">Home</a></li>
					<li><a href="picks.html" id="current_picks">Picks</a></li>
					<li><a href="standings.html" id="current_standings">Standings</a></li>
					<li><a href="scores.html" id="current_scores">Scores</a></li>
<?php
	if(empty($_SESSION['user'])) {

?>
					<li><a href="register.html" id="register">Register</a></li>
					<li><a href="login.html" id="signin">Sign In</a></li>
<?php	
	}
	else 
	{
		$user = htmlentities($_SESSION['user']['username'], ENT_QUOTES, 'UTF-8');
		$isAdmin = is_user_an_admin( $user );
		if( $isAdmin ) 
		{
?>
					<li><a href="admin.html" id="admin">Admin</a></li>
<?php
		}
		else {
?>
					<li><a href="private.html" id="private">My Account</a></li>
<?php
		}
?>
					<li><a href="logout.html" id="logout">Sign Out</a></li>
<?php
	}
?>
				</ul>
			</div>

