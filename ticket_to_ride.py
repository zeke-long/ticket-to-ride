import collections
import math
import itertools
import random
import copy

class Map(object):
	"""docstring for Map"""
	def __init__(self, city_map, possible_tickets):
		
		self.city_map = city_map
		self.possible_tickets = possible_tickets
		self.stations = self.get_stations()
		# if user_ticket == None:
		# 	self.tickets = []
		# if user_ticket != None:
		# 	self.tickets = user_ticket
		self.car_price = {1:1,2:2,4:3,7:4,10:5,15:6}

	def get_stations(self):
		stations = {}

		for i in self.city_map:
			stations[i] = Station(i, self.city_map[i])
		return stations

	def update_roads(self, road_taken):
		starting_city = road_taken[0]
		end_city = road_taken[1]

		self.stations[starting_city].remove_edge(end_city)
		self.stations[end_city].remove_edge(starting_city)

	def get_tickets(self):
		new_tickets_num = [random.randint(0,len(self.possible_tickets)-1),random.randint(0,len(self.possible_tickets)-1),random.randint(0,len(self.possible_tickets)-1)]
		new_tickets = []
		for i in new_tickets_num:
			if self.possible_tickets[i] not in new_tickets:
				new_tickets.append(self.possible_tickets[i])
		return new_tickets
		
	def shortest_path_cars(self, source, dest, old_vertices = None):
		'''
		Returns: path taken (deque()), value (int)
		'''
		if old_vertices == None:
			vertices = self.stations.copy()
			new_vertices = copy.deepcopy(self.stations)
			old_vertices = self.stations.copy()

		if old_vertices != None:
			vertices = old_vertices.copy()
			new_vertices = old_vertices.copy()

		assert source in self.stations, 'Such source node doesn\'t exist'


		distances = {vertex: math.inf for vertex in old_vertices}
		previous_vertices = {vertex: None for vertex in old_vertices}

		distances[source] = 0

		while vertices:

			current_vertex = min(vertices, key=lambda vertex: distances[vertex])
			if distances[current_vertex] == math.inf:
				break

			for neighbour in old_vertices[current_vertex].adj_len:

				alternative_route = distances[current_vertex] + self.car_price[old_vertices[current_vertex].adj_len[neighbour]]# + 1/old_vertices[current_vertex].adj_len[neighbour]

				if alternative_route < distances[neighbour]:
					distances[neighbour] = alternative_route
					previous_vertices[neighbour] = current_vertex
			del vertices[current_vertex]

		path, current_vertex = collections.deque(), dest
		total = 0
		car_total = 0
		while previous_vertices[current_vertex] is not None:
			path.appendleft(current_vertex)
			temp_var = old_vertices[current_vertex].adj_len[previous_vertices[current_vertex]]
			total+= temp_var
			car_total+= self.car_price[temp_var]
			###### Remove the edge from the path used #####
			new_vertices[current_vertex].remove_edge(previous_vertices[current_vertex])
			new_vertices[previous_vertices[current_vertex]].remove_edge(current_vertex)

			current_vertex = previous_vertices[current_vertex]
		if path:
			path.appendleft(current_vertex)
		return path, total, car_total, new_vertices

	def shortest_path_nodes(self, start, end, old_vertices = None):

		if old_vertices == None:
			vertices = self.stations.copy()
			new_vertices = copy.deepcopy(self.stations)
			old_vertices = self.stations.copy()

		if old_vertices != None:
			vertices = old_vertices.copy()
			new_vertices = old_vertices.copy()

		visited = {}
		for i in old_vertices:
			visited[i] = False

		queue = []

		queue.append(start)
		visited[start] = True 
		previous_vertices = {vertex: None for vertex in old_vertices}

		while queue:
			start = queue.pop(0)
			if start == end:
				break

			for i in old_vertices[start].adj_len:
				if visited[i] == False:
					queue.append(i)
					previous_vertices[i] = start
					visited[i] = True

		path, current_vertex = collections.deque(), end
		total = 0
		car_total = 0
		while previous_vertices[current_vertex] is not None:
			path.appendleft(current_vertex)
			temp_var = old_vertices[current_vertex].adj_len[previous_vertices[current_vertex]]
			total+= temp_var
			car_total+= self.car_price[temp_var]
			new_vertices[current_vertex].remove_edge(previous_vertices[current_vertex])
			new_vertices[previous_vertices[current_vertex]].remove_edge(current_vertex)
			current_vertex = previous_vertices[current_vertex]
		if path:
			path.appendleft(current_vertex)
		return list(path), total, car_total, new_vertices

	def heuristic(self, source, dest, old_vertices = None):
		'''
		Returns: path taken (deque()), value (int)
		'''
		if old_vertices == None:
			vertices = self.stations.copy()
			new_vertices = copy.deepcopy(self.stations)
			old_vertices = self.stations.copy()

		if old_vertices != None:
			vertices = old_vertices.copy()
			new_vertices = old_vertices.copy()

		assert source in self.stations, 'Such source node doesn\'t exist'


		distances = {vertex: math.inf for vertex in old_vertices}
		previous_vertices = {vertex: None for vertex in old_vertices}

		distances[source] = 0

		while vertices:

			current_vertex = min(vertices, key=lambda vertex: distances[vertex])
			if distances[current_vertex] == math.inf:
				break

			for neighbour in old_vertices[current_vertex].adj_len:

				alternative_route = distances[current_vertex] + 2/old_vertices[current_vertex].adj_len[neighbour]# + self.car_price[old_vertices[current_vertex].adj_len[neighbour]]

				if alternative_route < distances[neighbour]:
					distances[neighbour] = alternative_route
					previous_vertices[neighbour] = current_vertex
			del vertices[current_vertex]

		path, current_vertex = collections.deque(), dest
		total = 0
		car_total = 0
		while previous_vertices[current_vertex] is not None:
			path.appendleft(current_vertex)
			temp_var = old_vertices[current_vertex].adj_len[previous_vertices[current_vertex]]
			total+= temp_var
			car_total+= self.car_price[temp_var]
			###### Remove the edge from the path used #####
			new_vertices[current_vertex].remove_edge(previous_vertices[current_vertex])
			new_vertices[previous_vertices[current_vertex]].remove_edge(current_vertex)

			current_vertex = previous_vertices[current_vertex]
		if path:
			path.appendleft(current_vertex)
		return path, total, car_total, new_vertices

	def ticket_route(self, tickets):
		destination_cities = set()	
		for i in tickets:
			destination_cities.add(i[0])
			destination_cities.add(i[1])

		l=list(itertools.permutations(destination_cities))
		paths = []
		car_total_path = []
		total_path = []
		for permutation in l:
			vertices = copy.deepcopy(self.stations)
			permutation_total = 0
			permutation_car_total = 0
			permutation_path = []
			for i in range(len(permutation)):
				if i != len(permutation)-1:
					path, total, car_total, output = self.shortest_path_cars(permutation[i], permutation[i+1],vertices)				
					permutation_path += path
					permutation_total += total
					permutation_car_total += car_total

			paths.append(permutation_path)
			car_total_path.append(permutation_car_total)
			total_path.append(permutation_total)

		min_value = min(total_path)
		min_cars = car_total_path[total_path.index(min_value)]
		min_path = paths[total_path.index(min_value)]

		return min_path, min_cars, min_value

class Station(object):
	"""docstring for Station"""
	def __init__(self, name, neighbors):
		self.name = name
		self.neighbors = neighbors
		self.adj_len = self.get_adj_len()
		self.adj_color = self.get_adj_color()

	def get_adj_len(self):
		
		adj_len = {}
		
		for i in self.neighbors:
			adj_len[i] = self.neighbors[i][0]
		return adj_len

	def get_adj_color(self):
		
		adj_color = {}

		for i in self.neighbors:
			if len(self.neighbors[i]) == 2:
				adj_color[i] = self.neighbors[i][1] 
			if len(self.neighbors[i]) == 3:
				adj_color[i] = self.neighbors[i][1] + self.neighbors[i][2]
		return adj_color

	def remove_edge(self, vertex_to_del):
		del self.adj_color[vertex_to_del]
		del self.adj_len[vertex_to_del]

class Player(object):
	""" docstring for Player """
	def __init__(self,start_tickets,start_hand,ideal_path, game_map, possible_tickets):
		self.hand = start_hand
		self.tickets = start_tickets
		self.self_map = set()
		self.self_roads = set()
		self.completed_tickets = set()
		self.ideal_path = ideal_path
		self.game_map = game_map
		self.score = 0
		self.possible_tickets = possible_tickets

	def display_player(self):
		self.calc_score()
		print()
		print('##########################################################')
		print("Hand: " + str(self.hand))
		print("Tickets: " + str(self.tickets))
		# print()
		print('___________________________________________________________')
		# print()
		print("Player Has Access to: " + str(self.self_map))
		print("Ideal Path: " + str(self.ideal_path))
		print('Tickets Completed: '+str(self.completed_tickets))
		print('Your Score is: '+str(self.score))
		print('##########################################################')
		print()

	def update_hand(self, hand):
		for i in hand:
			self.hand.append(i)

	def update_tickets(self, tickets):
		for i in tickets:
			self.tickets.append(i)

	def calc_score(self):
		for i in self.self_roads:
			self.score+=self.game_map.city_map[i[0]][i[1]][0]
		for i in self.completed_tickets:
			self.score+= self.possible_tickets[i]


	def update_map(self, cities):
		self.self_roads.add(cities)

		for i in cities:
			self.self_map.add(i)

		for i in self.tickets:
			for x in self.self_map:
				for y in self.self_map:
					if x == i[0] and y == i[1] or x == i[1] and y == i[0]:
						self.completed_tickets.add(i)


#################################### LEGACY CODE ##########################################
"""
assert source in self.stations, 'Such source node doesn\'t exist'

		# 1. Mark all nodes unvisited and store them.
		# 2. Set the distance to zero for our initial node 
		# and to infinity for other nodes.
		distances = {vertex: math.inf for vertex in self.stations}
		previous_vertices = {
			vertex: None for vertex in self.stations
		}
		distances[source] = 0
		vertices = self.stations.copy()

		while vertices:
			# 3. Select the unvisited node with the smallest distance, 
			# it's current node now.
			current_vertex = min(vertices, key=lambda vertex: distances[vertex])

			# 6. Stop, if the smallest distance 
			# among the unvisited nodes is infinity.
			if distances[current_vertex] == math.inf:
				break

			# 4. Find unvisited neighbors for the current node 
			# and calculate their distances through the current node.
			#print(self.stations[current_vertex].adj_len)

			for neighbor in self.stations[current_vertex].adj_len:
				alternative_route = distances[current_vertex] + 1/self.stations[current_vertex].adj_len[neighbor]
				# Compare the newly calculated distance to the assigned 
				# and save the smaller one.
				if alternative_route < distances[neighbor]:
					distances[neighbor] = alternative_route
					previous_vertices[neighbor] = current_vertex

			# 5. Mark the current node as visited 
			# and remove it from the unvisited set.
			del vertices[current_vertex]


		path, current_vertex = collections.deque(), dest
		total = 0
		while previous_vertices[current_vertex] is not None:
			path.appendleft(current_vertex)
			total+=self.stations[current_vertex].adj_len[previous_vertices[current_vertex]]
			# remove path from the stations
			current_vertex = previous_vertices[current_vertex]
		if path:
			path.appendleft(current_vertex)
		return path, total

"""