import map_light
import navi_to_deltalist

def clear_field():
	MOVES = map_light.generate_moves(get_world_size()**2,get_world_size(),get_pos_x(),get_pos_y())
	for dir in MOVES:
		while not can_harvest():
			pass
		harvest()
		move(dir)


def run_sunflowers(fields,MOVES = map_light.generate_moves_light()):
	navi_to_deltalist.update()
	#move_data_x, move_data_y = loadDataList(get_world_size())
	power_modifier = {
		15: 100000000,
		14: 200000000,
		13: 300000000,
		12: 400000000,
		11: 500000000,
		10: 600000000,
		9:  700000000,
		8:  800000000,
		7:  900000000,
	}
	for _ in range(fields):
		power = {}
		i = 0
		for direction in MOVES:
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			if num_items(Items.Water) > 1:
				use_item(Items.Water)
			plant(Entities.Sunflower)
			power[power_modifier[measure()]+i] = (get_pos_x(), get_pos_y())
			i += 1
			move(direction)
		
		while len(power) > 10:
			next_petal = power.pop(min(power))
			navi_to_deltalist.move_to(next_petal[0],next_petal[1])
			while not can_harvest():
				use_item(Items.Water)
				use_item(Items.Fertilizer)
				pass
			harvest()

		while power:
			next_petal = power.pop(min(power))
			navi_to_deltalist.move_to(next_petal[0],next_petal[1])
			harvest()

def sunflowers_into_pumpkins():
	navi_to_deltalist.update()
	MOVES = map_light.generate_moves_light()
	#move_data_x, move_data_y = loadDataList(get_world_size())
	power_modifier = {
		15: 100000000,
		14: 200000000,
		13: 300000000,
		12: 400000000,
		11: 500000000,
		10: 600000000,
		9:  700000000,
		8:  800000000,
		7:  900000000,
	}

	pumpkin_set = list()

	power = {}
	i = 0
	for direction in MOVES:
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		if num_items(Items.Water) > 1:
			use_item(Items.Water)
		plant(Entities.Sunflower)
		power[power_modifier[measure()]+i] = (get_pos_x(), get_pos_y())
		i += 1
		move(direction)
	
	while len(power) > 10:
		next_petal = power.pop(min(power))
		navi_to_deltalist.move_to(next_petal[0],next_petal[1])
		while not can_harvest():
			use_item(Items.Water)
			use_item(Items.Fertilizer)
			pass
		harvest()
		plant(Entities.Pumpkin)
		pumpkin_set.append((get_pos_x(),get_pos_y()))

	while power:
		next_petal = power.pop(min(power))
		navi_to_deltalist.move_to(next_petal[0],next_petal[1])
		harvest()
		plant(Entities.Pumpkin)
		pumpkin_set.append((get_pos_x(),get_pos_y()))
	
	while len(pumpkin_set) > num_items(Items.Fertilizer)/2+2:
		for pos in pumpkin_set:
			navi_to_deltalist.move_to(pos[0],pos[1])
			if can_harvest():
				pumpkin_set.remove(pos)
			else:
				plant(Entities.Pumpkin)
				if (get_water() < 0.4):
					use_item(Items.Water)
	for pos in pumpkin_set:
		navi_to_deltalist.move_to(pos[0],pos[1])
		while not can_harvest():
			plant(Entities.Pumpkin)
			use_item(Items.Fertilizer)
	harvest()

def multi_drones_sunflowers():
	from move_to import move_to

	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle
	
	move_to(0,0)
	drone = []
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
				harvest()
			use_item(Items.Water)
			plant(Entities.Sunflower)
			power[measure()].append((get_pos_x(), get_pos_y()))
			move(East)
		return power

	for _ in range(get_world_size()):
		while num_drones() == max_drones():
			continue
		drone.append(spawn_drone(plant_line))
		move(North)
	for _ in range(len(drone)):
		dict = wait_for(drone[_])
		for key in dict:
			for value in range(len(dict[key])):
				total_power[key].append(dict[key][value])

	def wrapper_collector(pos):
		def collect():
			move_to(pos[0],pos[1])
			while not can_harvest():
				continue
			harvest()
		return collect

	for key in total_power:
		for i in range(len(total_power[key])):
			if num_drones() < max_drones():
				ensure_spawn(wrapper_collector(total_power[key][i]))
			else:
				wrapper_collector(total_power[key][i])()

def plant_sunflowers_wrapper(fields,MOVES = map_light.generate_moves_light(),k=0):
	def plant_sunflowers():
		navi_to_deltalist.update()
		#move_data_x, move_data_y = loadDataList(get_world_size())
		power_modifier = {
			15: 100000000,
			14: 200000000,
			13: 300000000,
			12: 400000000,
			11: 500000000,
			10: 600000000,
			9:  700000000,
			8:  800000000,
			7:  900000000,
		}
		for _ in range(fields):
			power = {}
			i = k
			for direction in MOVES:
				harvest()
				if get_ground_type() != Grounds.Soil:
					till()
				if num_items(Items.Water) > 1:
					use_item(Items.Water)
				plant(Entities.Sunflower)
				power[power_modifier[measure()]+i] = (get_pos_x(), get_pos_y())
				i += 1
				move(direction)
		return power
			
	return plant_sunflowers

def collect_sunflowers_wrapper(next_petal):
	def collect_sunflowers():
		navi_to_deltalist.update()
		navi_to_deltalist.move_to(next_petal[0],next_petal[1])
		while not can_harvest():
			use_item(Items.Water)
			use_item(Items.Fertilizer)
			pass
		harvest()
	return collect_sunflowers

def two_drones_sunflower():
	navi_to_deltalist.update()
	clear()
	navi_to_deltalist.move_to(0,0)
	midpoint = len(map_light.generate_moves_light()) // 2
	drone = spawn_drone(plant_sunflowers_wrapper(1,map_light.generate_moves_light()[:midpoint],500))
	move(West)
	main_power = plant_sunflowers_wrapper(1,map_light.generate_moves_light_reversed()[:midpoint],0)()
	second_power = wait_for(drone)
	for key in second_power:
		main_power[key] = second_power[key]
	while len(main_power) > 10:
		next_petal = main_power.pop(min(main_power))
		drone = spawn_drone(collect_sunflowers_wrapper(next_petal))
		next_petal = main_power.pop(min(main_power))
		collect_sunflowers_wrapper(next_petal)()
		wait_for(drone)
	while main_power:
		next_petal = main_power.pop(min(main_power))
		navi_to_deltalist.move_to(next_petal[0],next_petal[1])
		harvest()


# set_world_size(6)
# navi_to_deltalist.update()
# two_drones_sunflower()
# while True:
# 	do_a_flip()