import ticket_to_ride as ttr
import ttr_helper as play

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
	'Miami':{'New Orleans':[15,'red'],'Atlanta':[10,'blue'],'Charleston':[7,'pink']}	
}

game_map = ttr.Map(city_map,possible_tickets)


def input_tickets():
	
	return player_tickets


print('Begin Game? - yes or no -')
play_game = input()
need_setup = True


while play_game == 'yes':
### SETUP PHASE ###
	if need_setup == True:
		player = play.setup(game_map)
		player.display_player()
		need_setup = False
	
### GAME PLAY PHASE ###
	[game_map,player] = play.game(game_map, player)
	if game_map == False:
		play_game = 'no'

### SANTIY CHECK ###		
	# [ideal_path, car, val] = game_map.ticket_route(player.tickets)

	# print()
	# print('##########################################################')
	# print('Updated Path to Take: ' + str(ideal_path))
	# print('Your current Path: ' + str(player.self_map))
	# print('Number of cars it will take: ' + str(car))
	# print('Number of points you will get: ' + str(val))
	# print('##########################################################')
	# print()

print('Thanks for Playing!')