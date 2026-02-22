HARD_MOVES_WEST_BUSHES = {
	(0,0): East,
	(1,0): South,
	(1,2): South,
	(1,1): West,
	(0,1): North,
	(0,2): North,
}

HARD_MOVES_3b3 = {
	(0,0): East,
	(1,0): East,
	(2,0): North,
	(2,1): West,
	(1,1): North,
	(1,2): East,
	(2,2): East,
	(0,2): South,
	(0,1): South
}

HARD_MOVES_4b4 = {
	(0,0): East,
	(1,0): East,
	(2,0): East,
	(3,0): North,
	(3,1): East,
	(0,1): East,
	(1,1): East,
	(2,1): North,
	(2,2): East,
	(3,2): East,
	(0,2): East,
	(1,2): North,
	(1,3): East,
	(2,3): East,
	(3,3): East,
	(0,3): North,
}

HARD_MOVES_6b6 = {
	(0,0): East,
	(1,0): East,
	(2,0): East,
	(3,0): East,
	(4,0): East,
	(5,0): North,
	(5,1): East,
	(0,1): East,
	(1,1): East,
	(2,1): East,
	(3,1): East,
	(4,1): North,
	(4,2): East,
	(5,2): East,
	(0,2): East,
	(1,2): East,
	(2,2): East,
	(3,2): North,
	(3,3): East,
	(4,3): East,
	(5,3): East,
	(0,3): East,
	(1,3): East,
	(2,3): North,
	(2,4): East,
	(3,4): East,
	(4,4): East,
	(5,4): East,
	(0,4): East,
	(1,4): North,
	(1,5): East,
	(2,5): East,
	(3,5): East,
	(4,5): East,
	(5,5): East,
	(0,5): North,
}

def early_hay(item,amount):
	while num_items(item) < amount:
		if get_ground_type() == Grounds.Soil:
			till()
		if can_harvest():
			harvest()
		else:
			move(North)
		if num_items(item) >= amount:
			break

def three_spaces(item,amount):
	while num_items(item) < amount:
		for _ in range(2):
			plant(Entities.Bush)
			move(North)
		for _ in range(6):
			while not can_harvest():
				pass
			harvest()
		move(North)
		for _ in range(2):
			while not can_harvest():
				pass
			harvest()
			if _ == 0:
				move(North)
		if num_items(item) >= amount:
			break

def west_bushes(item,amount):
	global HARD_MOVES_WEST_BUSHES
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			pass
		harvest()
		plant(Entities.Bush)
		move(HARD_MOVES_WEST_BUSHES[get_pos_x(),get_pos_y()])

def map_bushes_hay(item,amount):
	global HARD_MOVES_3b3
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			pass
		harvest()
		if get_pos_x() != 2:
			plant(Entities.Bush)
		if get_pos_x() == 2 and get_pos_y() == 2:
			for i in range(2):
				move(North)
				while (get_entity_type() != None) and (not can_harvest()):
					pass
				harvest()
				move(South)
				while (get_entity_type() != None) and (not can_harvest()):
					pass
				harvest()
		move(HARD_MOVES_3b3[get_pos_x(),get_pos_y()])

def early_carrots(item,amount):
	global HARD_MOVES_3b3
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			pass
		harvest()
		if (get_pos_x() == 0) or (get_pos_x() == 1 and get_pos_y() == 1):
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Carrot)
		elif get_pos_x() == 2 and get_pos_y() != 0:
			pass
		else:
			plant(Entities.Bush)
		if get_pos_x() == 2 and get_pos_y() == 2:
			for i in range(8):
				if i % 2:
					move(North)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
				else:
					move(South)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
		move(HARD_MOVES_3b3[get_pos_x(),get_pos_y()])

def trees_and_carrots_3b3(item,amount):
	global HARD_MOVES_3b3
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			pass
		harvest()
		if (get_pos_x() % 2 == 0 and get_pos_y() % 2 == 0) and get_pos_x() == 0:
			plant(Entities.Tree)
		elif (get_pos_x() % 2 == 0 and get_pos_y() % 2 == 0) and get_pos_x() == 2:
			if get_ground_type() == Grounds.Grassland:
				pass
			else:
				till()
		else:
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Carrot)
		if get_pos_x() == 2 and get_pos_y() == 2:
			for i in range(8):
				if i % 2:
					move(South)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
				else:
					move(North)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
		move(HARD_MOVES_3b3[get_pos_x(),get_pos_y()])

def trees_and_carrots_4b4(item,amount):
	global HARD_MOVES_4b4
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			if get_water() < 0.5:
				use_item(Items.Water)
			pass
		harvest()
		if get_pos_x() == 3 and (get_pos_y() == 0 or get_pos_y() == 3):
			if get_ground_type() != Grounds.Grassland:
				till()
		elif (get_pos_x() + get_pos_y()) % 2 == 0:
			plant(Entities.Tree)
		else:
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Carrot)
		if get_pos_x() == 3 and get_pos_y() == 3:
			for i in range(8):
				if i % 2:
					move(South)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
				else:
					move(North)
					while (get_entity_type() != None) and (not can_harvest()):
						pass
					harvest()
		move(HARD_MOVES_4b4[get_pos_x(),get_pos_y()])

def trees_6b6(item,amount):
	global HARD_MOVES_6b6
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			pass
		harvest()
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			if get_ground_type() == Grounds.Soil:
				till()
			plant(Entities.Tree)
		elif get_pos_x() == 3 or get_pos_x() == 2:
			if get_ground_type() == Grounds.Soil:
				till()
		else:
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Bush)
		move(HARD_MOVES_6b6[get_pos_x(),get_pos_y()])

def trees_and_carrots_6b6(item,amount):
	global HARD_MOVES_6b6
	while num_items(item) < amount:
		while (get_entity_type() != None) and (not can_harvest()):
			if get_water() < 0.5:
				use_item(Items.Water)
			pass
		harvest()
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			if get_ground_type() == Grounds.Soil:
				till()
			plant(Entities.Tree)
		elif get_pos_x() == 1 or get_pos_x() == 2:
			if get_ground_type() == Grounds.Soil:
				till()
		else:
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Carrot)
		move(HARD_MOVES_6b6[get_pos_x(),get_pos_y()])

