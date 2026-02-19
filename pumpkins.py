import map_light
import navi_to_deltalist

def single_drone_pumpkin(item,amount):
	navi_to_deltalist.update()
	MOVES = map_light.generate_moves_light()
	
	while num_items(item) < amount:
		pumpkin_set = list()

		for direction in MOVES:
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			if num_items(Items.Water) > 1:
				use_item(Items.Water)
			plant(Entities.Pumpkin)
			move(direction)
		
		for direction in MOVES:
			if not can_harvest():
				plant(Entities.Pumpkin)
				pumpkin_set.append((get_pos_x(),get_pos_y()))
			move(direction)

		while len(pumpkin_set) > num_items(Items.Fertilizer)/2+2:
			for pos in pumpkin_set:
				navi_to_deltalist.move_to(pos[0],pos[1])
				if can_harvest():
					pumpkin_set.remove(pos)
				else:
					plant(Entities.Pumpkin)
					if (get_water() < 0.4) and num_items(Items.Water)>1:
						use_item(Items.Water)
		for pos in pumpkin_set:
			navi_to_deltalist.move_to(pos[0],pos[1])
			while not can_harvest():
				plant(Entities.Pumpkin)
				use_item(Items.Fertilizer)
		harvest()

def two_drones_pumpkin(amount):
	from map_light import generate_moves_light
	from map_light import generate_moves_light_reversed
	from move_to import move_to
	
	while num_items(Items.Pumpkin) < amount + 10:
		clear()
		MOVES = generate_moves_light()
		MOVES_2 = generate_moves_light_reversed()

		midpoint = len(MOVES) // 2
		MOVES = MOVES[:midpoint]
		MOVES_2 = MOVES_2[:midpoint]

		global pumpkin_set
		pumpkin_set = list()

		def clockwise(directions = MOVES):
			for dir in directions:
				if get_ground_type() == Grounds.Grassland:
					till()
				while get_water() < 0.4 and num_items(Items.Water)>1:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				pumpkin_set.append((get_pos_x(),get_pos_y()))
				move(dir)

			return pumpkin_set



		def cclockwise(directions = MOVES_2):
			for dir in directions:
				if get_ground_type() == Grounds.Grassland:
					till()
				while get_water() < 0.4 and num_items(Items.Water)>1:
					use_item(Items.Water)
				plant(Entities.Pumpkin)
				pumpkin_set.append((get_pos_x(),get_pos_y()))
				move(dir)
				
			return pumpkin_set

		DroneHandle = spawn_drone(clockwise)
		move(West)
		pumpkin_set_1 = cclockwise()
		pumpkin_set_2 = wait_for(DroneHandle)

		def main_visit(positions = pumpkin_set_1):
			while len(positions) > num_items(Items.Fertilizer)/2+2:
				for pos in positions:
					move_to(pos[0],pos[1])
					if can_harvest():
						positions.remove(pos)
					else:
						plant(Entities.Pumpkin)
						if get_water() < 0.4 and num_items(Items.Water)>1:
							use_item(Items.Water)
			for pos in positions:
				move_to(pos[0],pos[1])
				while not can_harvest():
					plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
			return True

		def drone_visit(positions = pumpkin_set_2):
			while len(positions) > num_items(Items.Fertilizer)/2+2:
				for pos in positions:
					move_to(pos[0],pos[1])
					if can_harvest():
						positions.remove(pos)
					else:
						plant(Entities.Pumpkin)
						if get_water() < 0.4 and num_items(Items.Water)>1:
							use_item(Items.Water)
			for pos in positions:
				move_to(pos[0],pos[1])
				while not can_harvest():
					plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
			return True

		DroneHandle = spawn_drone(drone_visit)
		can_harvest_1 = main_visit()
		can_harvest_2 = wait_for(DroneHandle)

		if can_harvest_1 and can_harvest_2:
			harvest()

def multidrone_pumpkin(item,amount):
	from move_to import move_to

	def check_vert():
		dead_pumpkins = []
		for i in range(get_world_size()):
			if not can_harvest():
				dead_pumpkins.append((get_pos_x(),get_pos_y()))
				use_item(Items.Water)
				use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)

			move(North)
		return dead_pumpkins

	def plant_pumpkin():
		for i in range(get_world_size()):
			till()
			use_item(Items.Water)
			use_item(Items.Water)
			plant(Entities.Pumpkin)
			move(North)

	def check_next_wraper(pos):
		def check_next():
			move_to(pos[0],pos[1])
			dead_pumpkin = 0
			if not can_harvest():
				dead_pumpkin = (get_pos_x(),get_pos_y())
				use_item(Items.Water)
				use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)
			if dead_pumpkin != 0:
				return dead_pumpkin
		return check_next

	def pumpkin_patch():
		clear()
		all_dead_pumpkins = []
		for j in range(2):
			for i in range(get_world_size()//2):
				drone = spawn_drone(plant_pumpkin)
				move(East)
			wait_for(drone)	
		wait_for(drone)
		drones = []
		move_to(0,0)

		for j in range(2):
			for i in range(get_world_size()//2):
				drones.append(spawn_drone(check_vert))
				move(East)

			for drone in drones:
				if drone == None:
					continue
				for item in wait_for(drone):
					all_dead_pumpkins.append(item)
		
		
		while all_dead_pumpkins != []:
			drones = []
			for pos in all_dead_pumpkins:
				while num_drones() == max_drones():
					pass
				drones.append(spawn_drone(check_next_wraper(pos)))
			all_dead_pumpkins = []
			for drone in drones:
				if drone == None:
					continue
				dead_pumpkin = wait_for(drone)
				if dead_pumpkin != None:
					all_dead_pumpkins.append(wait_for(drone))
				
		harvest()

	while num_items(item) < amount:
		pumpkin_patch()

def all_drones_pumpkins(item,amount):
	from move_to import move_to

	def check_vert():
		dead_pumpkins = []
		for i in range(get_world_size()):
			if not can_harvest():
				dead_pumpkins.append((get_pos_x(),get_pos_y()))
				use_item(Items.Water)
				use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)

			move(North)
		return dead_pumpkins

	def plant_pumpkin():
		for i in range(get_world_size()):
			till()
			use_item(Items.Water)
			use_item(Items.Water)
			plant(Entities.Pumpkin)
			move(North)

	def check_next_wraper(pos):
		def check_next():
			move_to(pos[0],pos[1])
			dead_pumpkin = 0
			if not can_harvest():
				dead_pumpkin = (get_pos_x(),get_pos_y())
				use_item(Items.Water)
				use_item(Items.Fertilizer)
				plant(Entities.Pumpkin)
			if dead_pumpkin != 0:
				return dead_pumpkin
		return check_next

	def pumpkin_patch():
		clear()
		all_dead_pumpkins = []

		for i in range(get_world_size()):
			drone = spawn_drone(plant_pumpkin)
			move(East)
		move(West)
		plant_pumpkin()
		#wait_for(drone)	

		drones = []
		move_to(0,0)

		for i in range(get_world_size()):
			drones.append(spawn_drone(check_vert))
			move(East)
		move(West)
		some_dead_pumpkins = check_vert()
		for item in some_dead_pumpkins:
			all_dead_pumpkins.append(item)

		for drone in drones:
			if drone == None:
				continue
			for item in wait_for(drone):
				all_dead_pumpkins.append(item)
		
		
		while all_dead_pumpkins != []:
			drones = []
			for pos in all_dead_pumpkins:
				while num_drones() == max_drones():
					pass
				drones.append(spawn_drone(check_next_wraper(pos)))
			all_dead_pumpkins = []
			for drone in drones:
				if drone == None:
					continue
				dead_pumpkin = wait_for(drone)
				if dead_pumpkin != None:
					all_dead_pumpkins.append(wait_for(drone))
			

			
		harvest()
	while num_items(item) <= amount:
		pumpkin_patch()

# set_world_size(12)
# multidrone_pumpkin(Items.Pumpkin,10000000000000)
# while True:
# 	do_a_flip()