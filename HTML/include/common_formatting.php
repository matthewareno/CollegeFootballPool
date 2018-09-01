<?php

require_once( 'include/football_common.php' );
require_once( 'include/database_common.php' );
require_once( 'include/database_games.php' );
require_once( 'include/database_teams.php' );
require_once( 'include/database_rankings.php' );

function display_game_pick( $pick )
{
	$gameInfo = get_game_by_id( $pick['gameId'] );
	if( empty( $gameInfo ) )
	{
		echo 'Failed to find game info';
		return;
	}
	$gameInfo = $gameInfo[0];

	$pickInfo = get_pick_by_game_id( $pick['gameId'] );

	$neutral = $gameInfo['NeutralSite'];
	$odds = $gameInfo['Odds'];
	$visitorInfo = get_team_by_id( $gameInfo['VisitorID'] );
	$homeInfo = get_team_by_id( $gameInfo['HomeID'] );
	$visitorRank = get_team_rank_by_week( $gameInfo['VisitorID'], $gameInfo['GameWeek'] );
	$homeRank = get_team_rank_by_week( $gameInfo['HomeID'], $gameInfo['GameWeek'] );
	if( count( $visitorRank ) != 0 )
		$visitorRank = $visitorRank[0]['rank'];
	else
		$visitorRank = 0;
	if( count( $homeRank ) != 0 )
		$homeRank = $homeRank[0]['rank'];
	else
		$homeRank = 0;

	$visitorPickIcon = "";
	$homePickIcon = "";

	if( empty( $pickInfo ) == false )
	{
		if( $pickInfo[0]['winner'] == 0 )
		{
			if( $pick['winner'] == $gameInfo['VisitorID'] )
				$visitorPickIcon = "images/question.png";
			else if( $pick['winner'] == $gameInfo['HomeID'] )
				$homePickIcon = "images/question.png";
			
			if( $gameInfo['GameDate'] != "" )
				$gameTime = $gameInfo['GameDate'] . ", " . $gameInfo['GameTime'];
			else
				$gameTime = $gameInfo['GameTime'];
		}
		else
		{
			if( $pick['winner'] == $pickInfo[0]['winner'] )
			{
				if( $pick['winner'] == $gameInfo['VisitorID'] )
					$visitorPickIcon = "images/correct.png";
				else if( $pick['winner'] == $gameInfo['HomeID'] )
					$homePickIcon = "images/correct.png";
			}
			else
			{
				if( $pick['winner'] == $gameInfo['VisitorID'] )
					$visitorPickIcon = "images/wrong.png";
				else if( $pick['winner'] == $gameInfo['HomeID'] )
					$homePickIcon = "images/wrong.png";
			}

			$gameTime = $gameInfo['GameTime'];
		}
	}

	echo '<div class="pickContainer">' . "\n";
	echo "\t" . '<div class="game_status">' . "\n";
	echo "\t\t" . '<div class="left_field"></div>' . "\n";
	echo "\t\t" . '<div class="right_field">' . "\n";
	echo "\t\t\t" . '<span>' . $gameTime . '</span>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	echo "\t" . '<div class="pick_team">' . "\n";
	echo "\t\t" . '<div class="game_team">' . "\n";
	echo "\t\t\t" . '<div class="team_icon">' . "\n";
	if( empty( $visitorInfo ) )
	{
		echo "\t\t\t\t" . '<a><img src="" width="30px" /></a>' . "\n";
		echo "\t\t\t" . '</div>' . "\n";
		echo "\t\t\t" . '<div class="team_name">' . "\n";
		echo "\t\t\t\t" . '<span>Division 3 Team</span>' . "\n";
	}
	else
	{
		echo "\t\t\t\t" . '<a><img src="' . $visitorInfo[0]['IconURL'] . '" width="30px" /></a>' . "\n";
		echo "\t\t\t" . '</div>' . "\n";
		echo "\t\t\t" . '<div class="team_name">' . "\n";
		if( $visitorRank != 0 )
			echo "\t\t\t\t" . '<span>#' . $visitorRank . ' ' . $visitorInfo[0]['Name'] . ' (' . $visitorInfo[0]['Wins'] . '-' . $visitorInfo[0]['Loses'] . '-' . $visitorInfo[0]['Ties'] . ')' . '</span>' . "\n";
		else
			echo "\t\t\t\t" . '<span>' . $visitorInfo[0]['Name'] . ' (' . $visitorInfo[0]['Wins'] . '-' . $visitorInfo[0]['Loses'] . '-' . $visitorInfo[0]['Ties'] . ')' . '</span>' . "\n";
	}
	echo "\t\t\t" . '</div>' . "\n";
	echo "\t\t\t" . '<div class="team_score">' . "\n";
	echo "\t\t\t\t" . '<span>' . $gameInfo['VisitorFinalScore'] . '</span>' . "\n";
	echo "\t\t\t" . '</div>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t\t" . '<div class="user_pick">' . "\n";
	if( $visitorPickIcon != "" )
		echo "\t\t\t" . '<a><img src="' . $visitorPickIcon . '" width="30px" /></a>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	echo "\t" . '<div class="pick_team">' . "\n";
	echo "\t\t" . '<div class="game_team">' . "\n";
	echo "\t\t\t" . '<div class="team_icon">' . "\n";
	if( empty( $homeInfo ) )
	{
		echo "\t\t\t\t" . '<span><a><img src="" width="30px" /></a></span>' . "\n";
		echo "\t\t\t" . '</div>' . "\n";
		echo "\t\t\t" . '<div class="team_name">' . "\n";
		echo "\t\t\t\t" . '<span>Division 3 Team</span>' . "\n";
	}
	else
	{
		echo "\t\t\t\t" . '<span><a><img src="' . $homeInfo[0]['IconURL'] . '" width="30px" /></a></span>' . "\n";
		echo "\t\t\t" . '</div>' . "\n";
		echo "\t\t\t" . '<div class="team_name">' . "\n";
		if( $homeRank != 0 )
			echo "\t\t\t\t" . '<span>#' . $homeRank . ' ' . $homeInfo[0]['Name'] . ' (' . $homeInfo[0]['Wins'] . '-' . $homeInfo[0]['Loses'] . '-' . $homeInfo[0]['Ties'] . ')' . '</span>' . "\n";
		else
			echo "\t\t\t\t" . '<span>' . $homeInfo[0]['Name'] . ' (' . $homeInfo[0]['Wins'] . '-' . $homeInfo[0]['Loses'] . '-' . $homeInfo[0]['Ties'] . ')' . '</span>' . "\n";
	}
	echo "\t\t\t" . '</div>' . "\n";
	echo "\t\t\t" . '<div class="team_score">' . "\n";
	echo "\t\t\t\t" . '<span>' . $gameInfo['HomeFinalScore'] . '</span>' . "\n";
	echo "\t\t\t" . '</div>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t\t" . '<div class="user_pick">' . "\n";
	if( $homePickIcon != "" )
		echo "\t\t\t" . '<a><img src="' . $homePickIcon . '" width="30px" /></a>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	if( $neutral )
	{
		echo "\t" . '<div class="pick_extra">' . "\n";
	    echo "\t\t" . '<div class="left_field">Played at neutral location</div>' . "\n";
		if( !empty( $odds ) )
		{
			echo "\t\t" . '<div class="right_field">' . $odds . '</div>' . "\n";
			echo "\t" . '</div>' . "\n";
		}
		else
		{
			if( !empty( $odds ) )
			{
				echo "\t" . '<div class="pick_extra">' . "\n";
				echo "\t\t" . '<div class="left_field">' . " " . '</div>' . "\n";
				echo "\t\t" . '<div class="right_field">' . $odds . '</div>' . "\n";
				echo "\t" . '</div>' . "\n";
	        }
		}
	}
	echo '</div>' . "\n";
}

function display_game_score( $gameId )
{
	$gameInfo = get_game_by_id( $gameId );
	if( empty( $gameInfo ) )
	{
		echo 'Failed to find game info';
		return;
	}
	$gameInfo = $gameInfo[0];

	if( strpos( $gameInfo['GameTime'], ':' ) == false )
		$gameTime = $gameInfo['GameTime'];
	else
		$gameTime = $gameInfo['GameDate'] . ' ' . $gameInfo['GameTime'];

	$neutral = $gameInfo['NeutralSite'];
	$odds = $gameInfo['Odds'];
	$visitorInfo = get_team_game_info_by_id( $gameInfo['VisitorID'] );
	$homeInfo = get_team_game_info_by_id( $gameInfo['HomeID'] );
	$visitorRank = get_team_rank_by_week( $gameInfo['VisitorID'], $gameInfo['GameWeek'] );
	$homeRank = get_team_rank_by_week( $gameInfo['HomeID'], $gameInfo['GameWeek'] );
	if( count( $visitorRank ) != 0 )
		$visitorRank = $visitorRank[0]['rank'];
	else
		$visitorRank = 0;
	if( count( $homeRank ) != 0 )
		$homeRank = $homeRank[0]['rank'];
	else
		$homeRank = 0;

	echo '<div class="gameContainer">' . "\n";
	echo "\t" . '<div class="game_status">' . "\n";
	echo "\t\t" . '<div class="left_field"></div>' . "\n";
	echo "\t\t" . '<div class="right_field">' . "\n";
	echo "\t\t\t" . '<span>' . $gameTime . '</span>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	echo "\t" . '<div class="game_team">' . "\n";
	echo "\t\t" . '<div class="team_icon">' . "\n";
	if( empty( $visitorInfo ) )
	{
		echo "\t\t\t" . '<a><img src="" width="30px" /></a>' . "\n";
		echo "\t\t" . '</div>' . "\n";
		echo "\t\t" . '<div class="team_name">' . "\n";
		echo "\t\t\t" . '<span>Division 3 Team</span>' . "\n";
	}
	else
	{
		echo "\t\t\t" . '<a><img src="' . $visitorInfo[0]['IconURL'] . '" width="30px" /></a>' . "\n";
		echo "\t\t" . '</div>' . "\n";
		echo "\t\t" . '<div class="team_name">' . "\n";
		if( $visitorRank != 0 )
			echo "\t\t\t" . '<span>#' . $visitorRank . ' ' . $visitorInfo[0]['Name'] . '</span>' . "\n";
		else
			echo "\t\t\t" . '<span>' . $visitorInfo[0]['Name'] . '</span>' . "\n";
	}
	echo "\t\t" . '</div>' . "\n";
	echo "\t\t" . '<div class="team_score">' . "\n";
	echo "\t\t\t" . '<span>' . $gameInfo['VisitorFinalScore'] . '</span>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	echo "\t" . '<div class="game_team">' . "\n";
	echo "\t\t" . '<div class="team_icon">' . "\n";
	if( empty( $homeInfo ) )
	{
		echo "\t\t\t" . '<span><a><img src="" width="30px" /></a></span>' . "\n";
		echo "\t\t" . '</div>' . "\n";
		echo "\t\t" . '<div class="team_name">' . "\n";
		echo "\t\t\t" . '<span>Division 3 Team</span>' . "\n";
	}
	else
	{
		echo "\t\t\t" . '<span><a><img src="' . $homeInfo[0]['IconURL'] . '" width="30px" /></a></span>' . "\n";
		echo "\t\t" . '</div>' . "\n";
		echo "\t\t" . '<div class="team_name">' . "\n";
		if( $homeRank != 0 )
			echo "\t\t\t" . '<span>#' . $homeRank . ' ' . $homeInfo[0]['Name'] . '</span>' . "\n";
		else
			echo "\t\t\t" . '<span>' . $homeInfo[0]['Name'] . '</span>' . "\n";
	}
	echo "\t\t" . '</div>' . "\n";
	echo "\t\t" . '<div class="team_score">' . "\n";
	echo "\t\t\t" . '<span>' . $gameInfo['HomeFinalScore'] . '</span>' . "\n";
	echo "\t\t" . '</div>' . "\n";
	echo "\t" . '</div>' . "\n";
	if( $neutral )
	{
		echo "\t" . '<div class="game_extra">' . "\n";
		echo "\t\t" . '<div class="left_field">Played at neutral location</div>' . "\n";
		if( !empty( $odds ) )
			echo "\t\t" . '<div class="right_field">' . $odds . '</div>' . "\n";
		echo "\t" . '</div>' . "\n";
	}
	else
	{
		if( !empty( $odds ) )
		{
			echo "\t" . '<div class="game_extra">' . "\n";
			echo "\t\t" . '<div class="left_field">' . " " . '</div>' . "\n";
			echo "\t\t" . '<div class="right_field">' . $odds . '</div>' . "\n";
			echo "\t" . '</div>' . "\n";
		}
	}
	echo '</div>' . "\n";
}

?>
