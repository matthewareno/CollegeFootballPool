<?php

function display_week_links( $title, $fileName )
{
	?>
	<fieldset>
		<legend><?php echo $title ?></legend>
		<table border="0">
			<tr>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=1">1</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=2">2</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=3">3</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=4">4</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=5">5</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=6">6</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=7">7</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=8">8</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=9">9</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=10">10</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=11">11</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=12">12</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=13">13</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=14">14</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=15">15</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=16">16</a></td>
				<td width="10"><a href="<?php echo $fileName ?>?gameWeek=17">Bowls</a></td>
			</tr>
		</table>
	</fieldset>
	<?php
}

function display_user_select_menu( $currUser, $fileName, $gameWeek )
{
	$users = get_all_user_ids();
	?>
	<form method="POST" action="<?php echo $fileName ?>">
		<input type="hidden" name="gameWeek" value="<?php echo $gameWeek ?>"></input>
		<select name="selected_user" onchange="this.form.submit()">

<?php
	foreach( $users as $user )
	{
		$name = get_user_first_name_by_id( $user['id'] )[0];
		if( $user['id'] == $currUser )
		{
			?>
			<option value="<?php echo $user['id'] ?>" selected="selected"><?php echo $name['firstName'] ?></option>
			<?php
		}
		else
		{
			?>
			<option value="<?php echo $user['id'] ?>"><?php echo $name['firstName'] ?></option>
			<?php
		}
	}
	?>
		</select>
	</form>
	<?php
}

function display_week_select_menu( $fileName, $gameWeek )
{
	echo '<form method="GET" action="' . $fileName . '">' . "\n";
	echo '<select name="gameWeek" onchange="this.form.submit()">' . "\n";

	if( is_string( $gameWeek ) )
	{
		if( $gameWeek == 'Overall' )
		{ 	
			echo '<option value="Overall" selected="selected">Overall</option>' . "\n";
			echo '<option value="17">Bowls</option>' . "\n";
		}
		else if ( $gameWeek == 'Bowls' )
		{ 	
			echo '<option value="Overall">Overall</option>' . "\n";
			echo '<option value="17" selected="selected">Bowls</option>' . "\n"; 
		}
		else
		{ 	
			echo '<option value="Overall">Overall</option>' . "\n";
			echo '<option value="17">Bowls</option>' . "\n";
		}
	}
	else
	{
		if( $gameWeek == 0 )
		{	
			echo '<option value="Overall" selected="selected">Overall</option>' . "\n";
			echo '<option value="17">Bowls</option>' . "\n";
		}
		else if( $gameWeek == 17 )
		{
			echo '<option value="Overall">Overall</option>' . "\n";
			echo '<option value="17" selected="selected">Bowls</option>' . "\n"; 
		}	
		else
		{	
			echo '<option value="Overall">Overall</option>' . "\n";
			echo '<option value="17">Bowls</option>' . "\n";
		}
	}
	
	$weeks = range( 1, 16 );
	foreach( $weeks as $week )
	{
		if( $gameWeek == $week )
			echo '<option value="' . $week . '" selected="selected">' . $week . '</option>' . "\n";
		else
			echo '<option value="' . $week . '">' . $week . '</option>' . "\n";
	}
	
	echo '</select>' . "\n";
	echo '</form>' . "\n";
}

?>
