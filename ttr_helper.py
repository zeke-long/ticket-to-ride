import ticket_to_ride as ttr

#tickets stored as (string city, string city, value)
possible_tickets = {
	("Denver","El Paso"):4,
	("Kansas City","Houston"):5,
	("New York City","Atlanta"):6,
	("Chicago","New Orleans"):7,
	("Calgary","Salt Lake City"):7,
	("Helena","Los Angeles"):8,
	("Duluth","Houston"):8,
	("Sault Ste. Marie","Nashville"):8,
	("Montreal","Atlanta"):9,
	("Sault Ste. Marie","Oklahoma City"):9,
	("Seattle","Los Angeles"):9,
	("Chicago","Santa Fe"):9,
	("Duluth","El Paso"):10, 
	("Toronto","Miami"):10,
	("Portland","Phoenix"):11, 
	("Dallas","New York City"):11, 
	("Denver","Pittsburgh"):11, 
	("Winnipeg","Little Rock"):11,
	("Winnipeg","Houston"):12, 
	("Boston","Miami"):12,
	("Vancouver","Santa Fe"):13, 
	("Calgary","Phoenix"):13, 
	("Montreal","New Orleans"):13,
	("Los Angeles","Chicago"):16,
	("San Francisco","Atlanta"):17,
	("Portland","Nashville"):17,
	("Vancouver","Montreal"):20, 
	("Los Angeles","Miami"):20,
	("Los Angeles","New York City"):21,
	("Seattle","New York City"):22}

possible_colors = {	'grey','yellow','red','blue','rainbow','green','orange','white','black'}

#city map stored as {string city:{string neighbor city:[value,color]}}
city_map = {
	'Vancouver':{'Seattle':[1,'grey'],'Calgary':[4,'grey']},
	'Seattle':{'Vancouver':[1,'grey'],'Calgary':[7,'grey'],'Portland':[1,'grey'],'Helena':[15,'yellow']},
	'Portland':{'San Francisco':[10,'pink','green'],'Seattle':[1,'grey'],'Salt Lake City':[15,'blue']},
	'San Francisco':{'Portland':[10,'pink','green'],'Salt Lake City':[10,'orange','white'],'Los Angeles':[4,'pink','yellow']},
	'Los Angeles':{'San Francisco':[4,'pink','yellow'],'Las Vegas':[2,'grey'],'Phoenix':[4,'grey'],'El Paso':[15,'black']},
	'Calgary':{'Vancouver':[4,'grey'],'Seattle':[7,'grey'],'Helena':[7,'grey'],'Winnipeg':[15,'white']},
	'Salt Lake City':{'Portland':[15,'blue'],'San Francisco':[10,'orange','white'],'Las Vegas':[4,'orange'],'Helena':[4,'pink'],'Denver':[4,'red','yellow']},
	'Las Vegas':{'Los Angeles':[2,'grey'],'Salt Lake City':[4,'orange']},
	'Phoenix':{'Los Angeles':[4,'grey'],'El Paso':[4,'grey'],'Denver':[10,'white'],'Santa Fe':[4,'grey']},
	'Helena':{'Calgary':[7,'grey'],'Seattle':[15,'yellow'],'Salt Lake City':[4,'pink'],'Denver':[7,'green'],'Omaha':[10,'red'],'Duluth':[15,'orange'],'Winnipeg':[10,'blue']},
	'Denver':{'Helena':[7,'green'],'Salt Lake City':[4,'red','yellow'],'Phoenix':[10,'white'],'Santa Fe':[2,'grey'],'Oklahoma City':[7,'red'],'Kansas City':[7,'black','orange'],'Omaha':[7,'pink']},
	'Santa Fe':{'Denver':[2,'grey'],'Phoenix':[4,'grey'],'Oklahoma City':[4,'blue'],'El Paso':[2,'grey']},
	'El Paso':{'Los Angeles':[15,'black'],'Phoenix':[4,'grey'],'Santa Fe':[2,'grey'],'Oklahoma City':[10,'yellow'],'Dallas':[7,'red'],'Houston':[15,'green']},
	'Winnipeg':{'Calgary':[15,'white'],'Helena':[7,'blue'],'Duluth':[7,'black'],'Sault Ste. Marie':[15,'grey']},
	'Duluth':{'Helena':[15,'orange'],'Winnipeg':[7,'black'],'Sault Ste. Marie':[4,'grey'],'Toronto':[15,'pink'],'Chicago':[4,'red'],'Omaha':[2,'grey','grey']},
	'Omaha':{'Helena':[10,'red'],'Duluth':[2,'grey','grey'],'Denver':[7,'pink'],'Kansas City':[1,'grey','grey'],'Chicago':[7,'blue']},
	'Kansas City':{'Omaha':[1,'grey','grey'],'Denver':[7,'orange','black'],'Oklahoma City':[2,'grey','grey'],'Saint Louis':[2,'blue','pink']},
	'Oklahoma City':{'Kansas City':[2,'grey','grey'],'Denver':[7,'red'],'Santa Fe':[4,'blue'],'El Paso':[10,'yellow'],'Dallas':[2,'grey','grey'],'Little Rock':[2,'grey']},
	'Dallas':{'Oklahoma City':[2,'grey','grey'],'El Paso':[7,'red'],'Houston':[1,'grey','grey'],'Little Rock':[2,'grey']},
	'Houston':{'Dallas':[1,'grey','grey'],'El Paso':[15,'green'],'New Orleans':[2,'grey']},
	'Sault Ste. Marie':{'Winnipeg':[15,'grey'],'Duluth':[4,'grey'],'Toronto':[2,'grey'],'Montreal':[10,'black']},
	'Toronto':{'Sault Ste. Marie':[2,'grey'],'Duluth':[15,'pink'],'Chicago':[7,'white'],'Pittsburgh':[2,'grey'],'Montreal':[4,'grey']},
	'Chicago':{'Duluth':[4,'red'],'Omaha':[7,'blue'],'Saint Louis':[2,'green','white'],'Pittsburgh':[4,'orange','black'],'Toronto':[7,'white']},
	'Saint Louis':{'Chicago':[2,'green','white'],'Kansas City':[2,'blue','pink'],'Little Rock':[2,'grey'],'Nashville':[2,'grey'],'Pittsburgh':[10,'green']},
	'Little Rock':{'Saint Louis':[2,'grey'],'Oklahoma City':[2,'grey'],'Dallas':[2,'grey'],'New Orleans':[4,'green'],'Nashville':[4,'white']},
	'New Orleans':{'Houston':[2,'grey'],'Little Rock':[4,'green'],'Atlanta':[7,'orange','yellow'],'Miami':[15,'red']},
	'Pittsburgh':{'Washington':[2,'grey'],'Toronto':[2,'grey'],'Chicago':[4,'orange','black'],'Saint Louis':[10,'green'],'Nashville':[7,'yellow'],'Raleigh':[2,'grey'],'New York City':[2,'green','white']},
	'Nashville':{'Pittsburgh':[7,'yellow'],'Raleigh':[4,'black'],'Atlanta':[1,'grey'],'Saint Louis':[2,'grey'],'Little Rock':[4,'white']},
	'Atlanta':{'Nashville':[1,'grey'],'New Orleans':[7,'orange','yellow'],'Miami':[10,'blue'],'Raleigh':[2,'grey','grey'],'Charleston':[2,'grey']},
	'Montreal':{'Sault Ste. Marie':[10,'black'],'Toronto':[4,'grey'],'New York City':[4,'blue'],'Boston':[2,'grey','grey']},
	'Boston':{'Montreal':[2,'grey','grey'],'New York City':[2,'red','yellow']},
	'New York City':{'Montreal':[4,'blue'],'Boston':[2,'red','yellow'],'Pittsburgh':[2,'green','white'],'Washington':[2,'orange','black']},
	'Washington':{'Pittsburgh':[2,'grey'],'New York City':[2,'orange','black'],'Raleigh':[2,'grey','grey']},
	'Raleigh':{'Washington':[2,'grey','grey'],'Pittsburgh':[2,'grey'],'Nashville':[4,'black'],'Atlanta':[2,'grey','grey'],'Charleston':[2,'grey']},
	'Charleston':{'Raleigh':[2,'grey'],'Atlanta':[2,'grey'],'Miami':[7,'pink']},
	'Miami':{'New Orleans':[15,'red'],'Atlanta':[10,'blue'],'Charleston':[7,'pink']}	}

new_map = ttr.Map(city_map,possible_tickets)

def setup(game_map):
	setup = True
	while setup == True:
	### Input Tickets ###
		inputting_tickets = True
		while inputting_tickets:
			print()
			print('What are you starting tickets? - City1, City2, City3, City4, City5, City6 -')
			player_tickets_string = input()
			split_tickets = player_tickets_string.split(', ')
			start_tickets = set()
			for i in range(len(split_tickets)):
				if i%2 == 0:
					if (split_tickets[i-1],split_tickets[i]) in possible_tickets:
						start_tickets.add((split_tickets[i-1],split_tickets[i]))
					elif (split_tickets[i],split_tickets[i-1]) in possible_tickets:
						start_tickets.add((split_tickets[i],split_tickets[i-1]))
					else:
						start_tickets.add('invalid')
			if 'invalid' not in start_tickets:
				inputting_tickets = False
				break
			print()
			print('Invalid Ticket')
			print()

	### Input Starting Cards ###
		inputting_cards = True
		while inputting_cards:
			print()
			print('What are your starting track cards? - color, color, color, color -')
			player_track_string = input()
			split_tracks = player_track_string.split(', ')
			start_hand = []
			for i in split_tracks:
				if i in possible_colors:
					start_hand.append(i)
				else:
					start_hand.append('invalid')
			if 'invalid' not in start_hand:
				inputting_cards = False
				break
			print()
			print('Invalid Cards')
			print()

	### Make Sure Player is Correct ###
		[ideal_path, car, val] = new_map.ticket_route(start_tickets)

		print()
		print('##########################################################')
		print('Tickets: ' + str(start_tickets))
		print('Train Cards: ' + str(start_hand))
		print('##########################################################')
		print()

		print('Is this correct? - yes or no -')
		continue_game = input()
		if continue_game == 'yes':
			setup = False
		if continue_game != 'yes' and continue_game != 'no':
			print()
			print('Invalid Response')
			print()

	player = ttr.Player(start_tickets,start_hand, ideal_path, game_map, possible_tickets)
	return player

def game(game_map,player):
	### GAMEPLAY PHASE ###
	playing_the_game = True
	while playing_the_game:
		print()
		print('Is it your turn? - yes or no or quit - ')
		whose_turn = input()
		if whose_turn == 'yes':
			### something ###
			print()
			print('What do you want to do? - place or draw or ticket or display - ')
			user_input = input()

			if user_input == 'place':
				[game_map,player] = place_track(game_map, player, True)
				return game_map, player

			if user_input == 'draw':
				player = draw_trains(player)
				return game_map, player

			if user_input == 'ticket':
				player = draw_tickets(game_map, player)
				return game_map, player

			if user_input == 'display':
				player.display_player()

		if whose_turn == 'no':
			### not the players turn ###
			print()
			print('What did they do? - place or complete or display -')
			other_player_turn = input()

			if other_player_turn == 'place':
				[game_map,player] = place_track(game_map, player)
				return game_map, player

			if other_player_turn == 'complete':
				print('dang')
				return game_map, player

			if other_player_turn == 'display':
				player.display_player()
				
		if whose_turn == 'quit':
			game_map = False
			break

		if whose_turn != 'quit' and whose_turn != 'no' and whose_turn != 'yes':
			print()
			print('Invalid Response')
			print()
			break

	return game_map, player

def place_track(game_map, player, for_user = False):
	placing = True
	while placing:
		print()
		print('Where did they place the track? - City1, City2 - ')
		placed_track_string = input()
		split_placed = placed_track_string.split(', ')
		if split_placed[0] not in city_map[split_placed[1]]:
			print('Invalid Road')
		elif split_placed[0] in city_map[split_placed[1]]:
			if not for_user:
				game_map.update_roads((split_placed[0],split_placed[1]))
			
			if for_user:
				player.update_map((split_placed[0],split_placed[1]))

			placing = False
			print()
			print('Trains placed from ' + str(split_placed[0]) + ' to ' + str(split_placed[1]))
			print()

			break
		
	return game_map, player

def draw_tickets(game_map, player):
	inputting_tickets = True
	while inputting_tickets:
		print()
		print('What are your new tickets? - City1, City2, City3, City4, City5, City6 -')
		player_tickets_string = input()
		split_tickets = player_tickets_string.split(', ')
		start_tickets = set()
		for i in range(len(split_tickets)):
			if i%2 == 0:
				if (split_tickets[i-1],split_tickets[i]) in possible_tickets:
					start_tickets.add((split_tickets[i-1],split_tickets[i]))
				elif (split_tickets[i],split_tickets[i-1]) in possible_tickets:
					start_tickets.add((split_tickets[i],split_tickets[i-1]))
				else:
					start_tickets.add('invalid')
				if 'invalid' not in start_tickets:
					inputting_tickets = False
					new_tickets = player.tickets.union(start_tickets)
					[ideal_path, car, val] = game_map.ticket_route(new_tickets)
					print()
					print('This is your new ideal path: '+ str(ideal_path))
					print('Continue with these tickets? - yes or no - ')
					print()
					user_input = input()
					if user_input == 'no':
						inputting_tickets = True
					break
				print()
				print('Invalid Ticket')


	player.update_tickets(start_tickets)
	return player

def draw_trains(player):
	inputting_cards = True
	while inputting_cards:
		print()
		print('What are your new track cards? - color, color -')
		player_track_string = input()
		split_tracks = player_track_string.split(', ')
		new_hand = []
		for i in split_tracks:
			if i in possible_colors:
				new_hand.append(i)
			else:
				new_hand.append('invalid')
		if 'invalid' not in new_hand:
			inputting_cards = False
			break
		print()
		print('Invalid Cards')
		print()
	
	player.update_hand(new_hand)
	return player
