from move_to import *
from map_subgrids import *


def hay_polyfarm(amount):
	#Generalizing for World Size and Max Drones
	moves = generate_moves_quadrant()
	coords = generate_quadrant_coords()

	for i in range(len(coords)):
		def task():
			x,y = coords[i][0], coords[i][1]
			move_to(x,y)
			for k in moves:
				plant(Entities.Bush)
				move(k)
			#moves_2 = [North,East,South,West]
			moves_2 = [North,South]
			while num_items(Items.Hay) < amount:
				for k in moves_2:
					move(k)
					if get_water() < 0.75:
						use_item(Items.Water)
					companion,pos = get_companion()
					while companion != Entities.Bush:
						harvest()
						companion,pos = get_companion()
					if not can_harvest():
						continue
					harvest()
		if num_drones() < max_drones():
			spawn_drone(task)
		else:
			task()

def trees_poly():
	companions = {}

	def plant_tree():
		global companions
		if (get_pos_x()+get_pos_y()) % 2 == 0:
			plant(Entities.Tree)
			companion,pos = get_companion()
			companions[pos] = companion


def multi_drones_poly(item,amount):

	if item == Items.Carrot:
		entity = Entities.Carrot
	if item == Items.Wood:
		entity = Entities.Tree

	moves = generate_moves_quadrant()
	coords = generate_quadrant_coords()
	
	for i in range(len(coords)):
		def task():
			x,y = coords[i][0], coords[i][1]
			move_to(x,y)

	

hay_polyfarm(2000000000)