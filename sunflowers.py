from move_to import *

def multi_drones_sunflowers():
	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle
	
	drone = []
	main_drone_power = []
	total_power = {
		15: [],
		14: [],
		13: [],
		12: [],
		11: [],
		10: [],
		9:  [],
		8:  [],
		7:  [],
	}
	def plant_line():
		power = {
			15: [],
			14: [],
			13: [],
			12: [],
			11: [],
			10: [],
			9:  [],
			8:  [],
			7:  [],
		}
		for _ in range(get_world_size()):
			if get_ground_type() == Grounds.Grassland:
				till()
			if get_entity_type() != Entities.Sunflower:
				#while (get_entity_type() != None) and (not can_harvest()):
					#pass
				harvest()
			plant(Entities.Sunflower)
			if measure() == 15:
				use_item(Items.Water)
			power[measure()].append((get_pos_x(), get_pos_y()))
			move(East)
		return power
	#if we can, spawn a drone, if not, run the main one and save the dict:
	for _ in range(get_world_size()):
		if num_drones() < max_drones():
			drone.append(ensure_spawn(plant_line))
		else:
			main_drone_power.append(plant_line())
		move(North)
	#all flowers in the same dict:
	for _ in range(len(main_drone_power)):
		dict = main_drone_power[_]
		for key in dict:
			for value in range(len(dict[key])):
				total_power[key].append(dict[key][value])
	for _ in range(len(drone)):
		dict = wait_for(drone[_])
		for key in dict:
			for value in range(len(dict[key])):
				total_power[key].append(dict[key][value])

	def wrapper_collector(pos):
		def collect():
			move_to(pos[0],pos[1])
			while not can_harvest():
				if get_water() < 0.5:
					use_item(Items.Water)
				continue
			harvest()
		return collect

	drones = []
	for key in total_power:
		for i in range(len(total_power[key])):
			if num_drones() < max_drones():
				drones.append(ensure_spawn(wrapper_collector(total_power[key][i])))
			else:
				wrapper_collector(total_power[key][i])()
	for drone in drones:
		if drone != None:
			wait_for(drone)

def sunflowers_into_pumpkins():
	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle
	
	drone = []
	main_drone_power = []
	total_power = {
		15: [],
		14: [],
		13: [],
		12: [],
		11: [],
		10: [],
		9:  [],
		8:  [],
		7:  [],
	}
	def plant_line():
		power = {
			15: [],
			14: [],
			13: [],
			12: [],
			11: [],
			10: [],
			9:  [],
			8:  [],
			7:  [],
		}
		for _ in range(get_world_size()):
			if get_ground_type() == Grounds.Grassland:
				till()
			if get_entity_type() != Entities.Sunflower:
				#while (get_entity_type() != None) and (not can_harvest()):
					#pass
				harvest()
			plant(Entities.Sunflower)
			if measure() == 15:
				use_item(Items.Water)
			power[measure()].append((get_pos_x(), get_pos_y()))
			move(East)
		return power
	#if we can, spawn a drone, if not, run the main one and save the dict:
	for _ in range(get_world_size()):
		if num_drones() < max_drones():
			drone.append(ensure_spawn(plant_line))
		else:
			main_drone_power.append(plant_line())
		move(North)
	#all flowers in the same dict:
	for _ in range(len(main_drone_power)):
		dict = main_drone_power[_]
		for key in dict:
			for value in range(len(dict[key])):
				total_power[key].append(dict[key][value])
	for _ in range(len(drone)):
		dict = wait_for(drone[_])
		for key in dict:
			for value in range(len(dict[key])):
				total_power[key].append(dict[key][value])

	def wrapper_sunflower_collector(pos):
		def collect():
			move_to(pos[0],pos[1])
			while not can_harvest():
				if get_water() < 0.5:
					use_item(Items.Water)
				continue
			harvest()
			plant(Entities.Pumpkin)
		return collect

	for key in total_power:
		for i in range(len(total_power[key])):
			if num_drones() < max_drones():
				ensure_spawn(wrapper_sunflower_collector(total_power[key][i]))
			else:
				wrapper_sunflower_collector(total_power[key][i])()

	def check_vert():
		dead_pumpkins = []
		for i in range(get_world_size()):
			if not can_harvest():
				dead_pumpkins.append((get_pos_x(),get_pos_y()))
				use_item(Items.Water)
				#use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)

			move(North)
		return dead_pumpkins
	
	def check_next_wraper(pos):
		def check_next():
			move_to(pos[0],pos[1])
			dead_pumpkin = 0
			if not can_harvest():
				dead_pumpkin = (get_pos_x(),get_pos_y())
				use_item(Items.Water)
				#use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)
			if dead_pumpkin != 0:
				return dead_pumpkin
		return check_next

	def pumpkin_patch():
		some_dead_pumpkins = []
		all_dead_pumpkins = []
		drones = []

		#plant pumpkins
		# for i in range(get_world_size()):
		# 	if num_drones() < max_drones():
		# 		ensure_spawn(plant_pumpkin)
		# 	else:
		# 		plant_pumpkin()
		# 	move(East)
		#wait_for(drone)	

		#check for dead ones
		for i in range(get_world_size()):
			if num_drones() < max_drones():
				drones.append(ensure_spawn(check_vert))
			else:
				some_dead_pumpkins.append(check_vert())
			move(East)
		for item in some_dead_pumpkins:
			for _ in item:
				all_dead_pumpkins.append(_)

		for drone in drones:
			if drone == None:
				continue
			for item in wait_for(drone):
				all_dead_pumpkins.append(item)
		
		
		while all_dead_pumpkins != []:
			drones = []
			dead_pumpkins_main = []
			for pos in all_dead_pumpkins:
				if num_drones() < max_drones():
					drones.append(ensure_spawn(check_next_wraper(pos)))
				else:
					dead_pumpkins_main.append(check_next_wraper(pos)())
			all_dead_pumpkins = []
			for dead_pumpkin_main in dead_pumpkins_main:
				if dead_pumpkin_main != None:
					all_dead_pumpkins.append(dead_pumpkin_main)
			for drone in drones:
				dead_pumpkin = wait_for(drone)
				if dead_pumpkin != None:
					all_dead_pumpkins.append(wait_for(drone))
			

			
		harvest()
	
	pumpkin_patch()