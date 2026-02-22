import move_to

def all_drones_pumpkins(item,amount):
	def ensure_spawn(f):
		handle = None
		while handle == None:
			handle = spawn_drone(f)
		return handle

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

	def plant_pumpkin():
		for i in range(get_world_size()):
			if get_ground_type() == Grounds.Grassland:
				till()
			if get_entity_type() != Entities.Pumpkin:
				harvest()
			use_item(Items.Water)
			plant(Entities.Pumpkin)
			move(North)

	def check_next_wraper(pos):
		def check_next():
			move_to.move_to(pos[0],pos[1])
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
		for i in range(get_world_size()):
			if num_drones() < max_drones():
				ensure_spawn(plant_pumpkin)
			else:
				plant_pumpkin()
			move(East)
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
	while num_items(item) <= amount:
		pumpkin_patch()

#set_world_size(12)
#all_drones_pumpkins(Items.Pumpkin,10000000000000)
#while True:
#	do_a_flip()