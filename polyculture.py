import map_light
import navi_to_deltalist
import move_to
import map_subgrids

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

def multipoly_drones_hay(item,amount):
	navi_to_deltalist.update()
	
	clear()
	if item == Items.Carrot:
		entity = Entities.Carrot
	if item == Items.Wood:
		entity = Entities.Tree
	if item == Items.Hay:
		entity = Entities.Grass

	def max_farm(amount,entity,item):
		num_per_axis = get_world_size()

		drones = []
		k = 0
		for i in range(0,num_per_axis,4):
			for j in range(0,num_per_axis,4):
				if (i % 8) == (j % 8):
					k += 1

		for i in range(0,num_per_axis,4):
			for j in range(0,num_per_axis,4):
				if (i % 8) == (j % 8):
					center = (i, j)
					
					def task():
						if get_world_size() <= 10:
							navi_to_deltalist.move_to(center[0],center[1])
						else:
							move_to.move_to(center[0],center[1])
						if entity == Entities.Grass:
							pass
						else:
							till()
						while num_items(item) < amount:
							plant(entity)
							companion, pos = get_companion()
							if get_world_size() <= 10:
								navi_to_deltalist.move_to(pos[0],pos[1])
							else:
								move_to.move_to(pos[0],pos[1])
							if get_entity_type() != companion:
								# while not can_harvest():
								# 	if get_water() < 0.4:
								# 		use_item(Items.Water)
								# 	use_item(Items.Fertilizer)
								harvest()
							if get_ground_type() == Grounds.Grassland:
								till()
							plant(companion)
							if get_world_size() <= 10:
								navi_to_deltalist.move_to(center[0],center[1])
							else:
								move_to.move_to(center[0],center[1])
							while not can_harvest():
								if get_water() < 0.4:
									use_item(Items.Water)
								use_item(Items.Fertilizer)
							harvest()
							if num_items(item) >= amount:
								break
						#diamond(center, entity, amount)
						#harvest()

					k -=1
					if k > 0:
						drones.append(spawn_drone(task))
					else:
						task()
					# for drone in drones:
					# 	wait_for(drone)
					
	max_farm(amount,entity,item)

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
			for dir in MOVES:
				coords = (get_pos_x(),get_pos_y())
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
		return carrots_poly
	else:
		return trees_poly

def multi_drones_poly(item,amount):
	clear()
	ws = get_world_size()
	md = max_drones()
	#md = 16
	if md == 2:
		gsx = ws
		gsy = ws/2
	if md == 4:
		gsx = ws/2
		gsy = ws/2
	if md == 8:
		gsx = ws/2
		gsy = ws/4
	if md == 16:
		gsx = ws/4
		gsy = ws/4
	from move_to import move_to
	MOVES = map_subgrids.generate_moves_quadrant(gsx,gsy)
	COORDS = map_subgrids.generate_quadrant_coords(gsx,gsy,ws,md)
	drones = []
	for _ in range(len(COORDS)-1):
		move_to(COORDS[_][0],COORDS[_][1])
		drones.append(spawn_drone(single_drone_poly_wrapper(item,amount,MOVES)))
	move_to(COORDS[_+1][0],COORDS[_+1][1])
	single_drone_poly_wrapper(item,amount,MOVES)()


#set_execution_speed(8)
#set_world_size(16)
#multi_drones_poly(Items.Carrot,1000000000000000)
# ws = get_world_size()
# md = 8
# from move_to import move_to
# MOVES = map_subgrids.generate_moves_quadrant(4,8)
# COORDS = map_subgrids.generate_quadrant_coords(4,8,ws,md)
# drones = []
# for _ in range(len(COORDS)-1):
# 	move_to(COORDS[_][0],COORDS[_][1])
# 	drones.append(spawn_drone(single_drone_poly_wrapper(Items.Wood,1000000000000000,MOVES)))
# move_to(COORDS[_+1][0],COORDS[_+1][1])
# single_drone_poly_wrapper(Items.Carrot,1000000000000000,MOVES)()
# set_world_size(6)
# multi_drones_poly(Items.Wood,10000000000000000)