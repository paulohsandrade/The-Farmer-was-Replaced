import map_light
import navi_to_deltalist
from move_to import *
from map_subgrids import *

def single_drone_poly(item, amount):
	if item == Items.Carrot:
		entity = Entities.Carrot
	if item == Items.Wood:
		entity = Entities.Tree
	if item == Items.Hay:
		entity = Entities.Grass
	def trees_poly():
		from map_pos import MOVES
		companions = {}
		flipflop = True

		def plant_tree():
			global companions
			plant(Entities.Tree)
			companion, pos = get_companion()
			x, y = pos
			while companion == Entities.Carrot or (pos in companions and companion != companions[pos]):
				harvest()
				plant(Entities.Tree)
				companion, pos = get_companion()
				x, y = pos
			companions[pos] = companion

		def handle_grass():
			plant_tree()
			if not get_water():
				use_item(Items.Water)

		def handle_bush():
			harvest()
			plant_tree()
			if not get_water():
				use_item(Items.Water)

		def handle_tree():
			global companions
			if can_harvest():
				harvest()
				plant_tree()
				if not get_water():
					use_item(Items.Water)
			else:
				if get_water() and use_item(Items.Fertilizer):
					use_item(Items.Weird_Substance)
					if can_harvest():
						harvest()
						plant_tree()
						if not get_water():
							use_item(Items.Water)
				else:
					companion, pos = get_companion()
					companions[pos] = companion

		handles = {
			Entities.Grass: handle_grass,
			Entities.Bush: handle_bush,
			Entities.Tree: handle_tree
		}

		while num_items(Items.Wood) < amount:
			for dir, coords in MOVES:
				# Companion
				if coords in companions:
					comp = companions.pop(coords)
					entity_type = get_entity_type()
					if entity_type != comp:
						if entity_type != Entities.Grass:
							if entity_type == Entities.Tree and get_water():
								if use_item(Items.Fertilizer):
									while not can_harvest():
										continue
							harvest()
						if comp != Entities.Grass:
							plant(comp)
				# Tree
				elif flipflop:
					handles[get_entity_type()]()
				flipflop = not flipflop
				move(dir)
		
	def carrots_poly():	
		navi_to_deltalist.update()
		MOVES = map_light.generate_moves_light()
		companions = {}
		#If we plant the entity and the companion overlaps with our dict, but is the wrong type
		#Replant until it either is not in our dict, or overlaps with the right type
		def plant_entity():
			global companions
			plant(entity)
			if get_entity_type() == entity:
				companion, pos = get_companion()
				while (pos in companions and companion != companions[pos]):
					harvest()
					plant(entity)
					companion, pos = get_companion()
				companions[pos] = companion
			else:
				plant(Entities.Grass)

		#If we encounter the entity in a situation where we can harvest it, we either:
		#Harvest it right away and plant again
		#Try to force a harvest with Fertilizer
		#Give up and update the companion list with it's companion
		def handle_entity():
			global companions
			if can_harvest():
				harvest()
				plant_entity()
				if not get_water():
					use_item(Items.Water)
			else:
				if get_water() and use_item(Items.Fertilizer):
					use_item(Items.Weird_Substance)
					if can_harvest():
						harvest()
						plant_entity()
						if not get_water():
							use_item(Items.Water)
				else:
					companion, pos = get_companion()
					companions[pos] = companion
		
		def handle_others():
			harvest()
			plant_entity()
			if not get_water():
				use_item(Items.Water)

		#first pass:
		for dir in MOVES:
			coord = (get_pos_x(),get_pos_y())
			if get_ground_type() != Grounds.Soil:
				till()
			if coord in companions:
				plant(companions.pop(coord))
			else:
				plant_entity()
				use_item(Items.Water)
			move(dir)
		
		#main loop:
		while num_items(item) < amount:
			for dir in MOVES:
				coord = (get_pos_x(), get_pos_y())
				#if it's a companion's position, check if it is the right crop.
				#if it's our farming crop, fertilize so it can be harvested.
				#plant the right companion
				if coord in companions:
					comp = companions.pop(coord)
					entity_type = get_entity_type()
					if entity_type != comp:
						if entity_type == entity:
							while not can_harvest():
								use_item(Items.Fertilizer)
						harvest()
					plant(comp)
				#if it isn't a companion's position, check if it is our farming crop
				#if we can harvest, do so and plant again, updating the companions dict
				else:
					if get_entity_type() == entity:
						handle_entity()
					else:
						handle_others()
				move(dir)
				if num_items(item) >= amount:
					break
			if num_items(item) >= amount:
				break
	if entity == Entities.Carrot:
		return carrots_poly()
	else:
		return trees_poly()

def single_drone_poly_wrapper(item,amount,MOVES):
	
	if item == Items.Carrot:
		entity = Entities.Carrot
	if item == Items.Wood:
		entity = Entities.Tree
	if item == Items.Hay:
		entity = Entities.Grass
	def trees_poly():
		companions = {}
		flipflop = True

		def plant_tree():
			global companions
			if (get_pos_x()+get_pos_y()) % 2 == 0:
				plant(Entities.Tree)
				companion, pos = get_companion()
				x, y = pos
				while companion == Entities.Carrot or (pos in companions and companion != companions[pos]):
					harvest()
					plant(Entities.Tree)
					companion, pos = get_companion()
					if not get_water():
						use_item(Items.Water)
					x, y = pos
				companions[pos] = companion

		def handle_grass():
			plant_tree()

		def handle_bush():
			harvest()
			plant_tree()

		def handle_tree():
			global companions
			if can_harvest():
				harvest()
				plant_tree()
			else:
				if get_water() < 0.75: #and use_item(Items.Fertilizer):
					#use_item(Items.Weird_Substance)
					use_item(Items.Water)
					if can_harvest():
						harvest()
						plant_tree()
					else:
						companion, pos = get_companion()
						companions[pos] = companion

		handles = {
			Entities.Grass: handle_grass,
			Entities.Bush: handle_bush,
			Entities.Tree: handle_tree
		}

		# first pass:
		for dir in MOVES:
			move(dir)
			harvest()
			coord = (get_pos_x(),get_pos_y())
			if get_ground_type() != Grounds.Soil:
				till()
			if coord in companions:
				plant(companions.pop(coord))
			else:
				plant_tree()

		while num_items(Items.Wood) < amount:
			move(dir)
			for dir in MOVES:
				coords = (get_pos_x(),get_pos_y())
				# Companion
				if coords in companions:
					comp = companions.pop(coords)
					entity_type = get_entity_type()
					if entity_type != comp:
						if entity_type != Entities.Grass:
							if entity_type == Entities.Tree:
								#if use_item(Items.Fertilizer):
								while not can_harvest():
									continue
							harvest()
						if comp != Entities.Grass:
							plant(comp)
				# Tree
				else:
					if get_entity_type() != None:
						handles[get_entity_type()]()
		
	def carrots_poly():	
		companions = {}
		#If we plant the entity and the companion overlaps with our dict, but is the wrong type
		#Replant until it either is not in our dict, or overlaps with the right type
		def plant_entity():
			global companions
			plant(entity)
			if not get_water():
				use_item(Items.Water)
			if get_entity_type() == entity:
				if get_companion() != None:
					companion, pos = get_companion()
				companions[pos] = companion
			else:
				plant(Entities.Grass)

		#If we encounter the entity in a situation where we can harvest it, we either:
		#Harvest it right away and plant again
		#Try to force a harvest with Fertilizer
		#Give up and update the companion list with it's companion
		def handle_entity():
			global companions
			if can_harvest():
				harvest()
				plant_entity()
			else:
				if get_water()<0.25: #and use_item(Items.Fertilizer):
					#use_item(Items.Weird_Substance)
					use_item(Items.Water)
					if can_harvest():
						harvest()
						plant_entity()
					else:
						companion, pos = get_companion()
						companions[pos] = companion
		
		def handle_others():
			harvest()
			plant_entity()

		#first pass:
		for dir in MOVES:
			move(dir)
			harvest()
			coord = (get_pos_x(),get_pos_y())
			if get_ground_type() != Grounds.Soil:
				till()
			if coord in companions:
				plant(companions.pop(coord))
			else:
				plant_entity()
		
		#main loop:
		while num_items(item) < amount:
			for dir in MOVES:
				move(dir)
				coord = (get_pos_x(), get_pos_y())
				#if it's a companion's position, check if it is the right crop.
				#if it's our farming crop, fertilize so it can be harvested.
				#plant the right companion
				if coord in companions:
					comp = companions.pop(coord)
					entity_type = get_entity_type()
					if entity_type != comp:
						if entity_type == entity:
							while not can_harvest():
								continue
						harvest()
					plant(comp)
				#if it isn't a companion's position, check if it is our farming crop
				#if we can harvest, do so and plant again, updating the companions dict
				else:
					if get_entity_type() == entity:
						handle_entity()
					else:
						handle_others()
				if num_items(item) >= amount:
					break
			if num_items(item) >= amount:
				break
	if entity == Entities.Carrot:
		return carrots_poly
	else:
		return trees_poly

def multi_drones_poly(item,amount):
	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle

	MOVES = generate_moves_quadrant()
	COORDS = generate_quadrant_coords()
	drones = []
	for _ in range(len(COORDS)-1):
		move_to(COORDS[_][0],COORDS[_][1])
		drones.append(ensure_spawn(single_drone_poly_wrapper(item,amount,MOVES)))
	move_to(COORDS[-1][0],COORDS[-1][1])
	single_drone_poly_wrapper(item,amount,MOVES)()
	for drone in drones:
		wait_for(drone)

def new_multi_drones_poly(item,amount):
	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle

	def plant_entity(entity):
		#If it's a carrot we need to till:
		if entity == Entities.Carrot:
			if get_ground_type() == Grounds.Grassland:
				till()
		#If it's a tree we need to plant on even tiles:
		if entity == Entities.Tree:
			if (get_pos_x()+get_pos_y()) % 2 == 0:
				plant(entity)
				return get_companion()
		else:
			plant(entity)
			return get_companion()
	
	def handle_entity(entity):
		if can_harvest():
			harvest()
			if not get_water():
				use_item(Items.Water)
			companion = plant_entity(entity)
			if companion != None:
				return companion
		else:
			companion = get_companion()
			if companion != None:
				return companion
	
	def handle_others(entity):
		harvest()
		companion = plant_entity(entity)
		if not get_water():
			use_item(Items.Water)
		if companion != None:
			return get_companion()
	
	def parse_column_wrapper(entity,companions):
		def parse_column():
			column_companions = {}
			for _ in range(get_world_size()):
				coord = (get_pos_x(),get_pos_y())
				if coord in companions:
					comp = companions.pop(coord)
					entity_type = get_entity_type()
					if entity_type != comp:
						if entity_type == entity:
							while not can_harvest():
								#use_item(Items.Fertilizer)
								pass
						harvest()
					plant(comp)
				else:
					if get_entity_type() == entity:
						handler = handle_entity(entity)
						if handler != None:
							companion, pos = handler
							column_companions[pos] = companion
					else:
						handler = handle_others(entity)
						if handler != None:
							companion, pos = handler
							column_companions[pos] = companion
				move(North)
			return column_companions
		return parse_column
	
	def polyculture(item,amount):
		if item == Items.Carrot:
			entity = Entities.Carrot
		if item == Items.Wood:
			entity = Entities.Tree
		if item == Items.Hay:
			entity = Entities.Grass

		companions = {}
		drones = []
		main_drone_companions = {}
		while num_items(item) < amount:
			for _ in range(max_drones()):
				if num_drones() < max_drones():
					drones.append(ensure_spawn(parse_column_wrapper(entity,companions)))
				else:
					main_drone_companions = parse_column_wrapper(entity,companions)()
				move(East)
				
			for key in main_drone_companions:
				companions[key] = main_drone_companions[key]
			for drone in drones:
				other_companions = wait_for(drone)
				for key in other_companions:
					companions[key] = other_companions[key]

	polyculture(item,amount)

def hay_polyfarm(amount):
	#Generalizing for World Size and Max Drones
	moves = generate_moves_quadrant()
	coords = generate_quadrant_coords()

	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle
	
	for i in range(len(coords)):
		def task():
			x,y = coords[i][0], coords[i][1]
			move_to(x,y)
			for k in moves:
				harvest()
				plant(Entities.Bush)
				move(k)
			#moves_2 = [North,East,South,West]
			moves_2 = [North,South]
			while num_items(Items.Hay) < amount:
				for k in moves_2:
					move(k)
					if get_ground_type() != Grounds.Grassland:
						till()
					if get_water() < 0.75:
						use_item(Items.Water)
					companion,pos = get_companion()
					while companion != Entities.Bush:
						harvest()
						companion,pos = get_companion()
					if not can_harvest():
						continue
					harvest()
				if num_items(Items.Hay) >= amount:
					break
		if num_drones() < max_drones():
			ensure_spawn(task)
		else:
			task()
					

#set_world_size(8)
#multipoly_drones_hay(Items.Hay,2000000000)
#new_multi_drones_poly_hay(Items.Hay,2000000000)