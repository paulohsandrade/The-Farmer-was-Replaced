import timing
import unlocking
import early_farming
import sunflowers
import pumpkins
import polyculture
import mazes
import cacti
from Dinos_2 import dinos

prev_time = 0
total_sunflower = 0
total_pumpkin = 0
total_poly = 0
total_maze = 0
total_cacti = 0
total_dinos = 0
total_weird = 0
total_early_farm = 0

#####################
#   grid size = 1   #
#####################
early_farming.early_hay(Items.Hay,100)

unlock_string, prev_time = unlocking.try_ulock(Unlocks.Speed,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Plant,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,0,prev_time)
quick_print(unlock_string)

#####################
#   grid size = 3   #
#####################

early_farming.three_spaces(Items.Wood,20)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,1,prev_time)
quick_print(unlock_string)

#####################
#  grid size = 3x3  #
#####################

early_farming.map_bushes_hay(Items.Wood,20)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Speed,1,prev_time)
quick_print(unlock_string)

early_farming.map_bushes_hay(Items.Wood,50)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,0,prev_time)
quick_print(unlock_string)

early_farming.map_bushes_hay(Items.Hay,300)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Grass,1,prev_time)
quick_print(unlock_string)

#####################
# Ahead of compared #
#####################

early_farming.early_carrots(Items.Carrot,70)
early_farming.map_bushes_hay(Items.Wood,50)
early_farming.map_bushes_hay(Items.Hay,300)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Trees,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Trees,1,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_3b3(Items.Carrot,20)
early_farming.trees_and_carrots_3b3(Items.Wood,30)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,2,prev_time)
quick_print(unlock_string)

#####################
#  grid size = 4x4  #
#####################

early_farming.trees_and_carrots_4b4(Items.Wood,250)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,1,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_4b4(Items.Carrot,50)
early_farming.trees_and_carrots_4b4(Items.Wood,50)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Speed,2,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_4b4(Items.Wood,350)
early_farming.trees_and_carrots_4b4(Items.Carrot,50)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,3,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,1,prev_time)
quick_print(unlock_string)

#####################
#  grid size = 6x6  #
#####################

early_farming.trees_and_carrots_6b6(Items.Wood,1250)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,2,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_6b6(Items.Wood,500)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Grass,2,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_6b6(Items.Carrot,550)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Sunflowers,0,prev_time)
quick_print(unlock_string)
total_early_farm += get_time()

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

early_farm_start = get_time()
early_farming.trees_and_carrots_6b6(Items.Wood,500)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Fertilizer,0,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_6b6(Items.Wood,800)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,2,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_6b6(Items.Carrot,500)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Speed,3,prev_time)
quick_print(unlock_string)

early_farming.trees_and_carrots_6b6(Items.Wood,3700)
early_farming.trees_and_carrots_6b6(Items.Carrot,200)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,3,prev_time)
quick_print(unlock_string)


early_farming.trees_and_carrots_6b6(Items.Carrot,600)
early_farm_end = get_time()
early_farming_time = early_farm_end - early_farm_start
total_early_farm += early_farming_time
start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,3000)
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += total_pumpkin
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Polyculture,0,prev_time)
quick_print(unlock_string)

#####################
#    Polyculture    #
#####################

start_poly = get_time()
polyculture.hay_polyfarm(1200)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += total_poly

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,100)
end_poly = get_time()

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Carrot,1200)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += total_poly
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Speed,4,prev_time)
quick_print(unlock_string)

start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,1000)
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += pumpkin_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,4,prev_time)
quick_print(unlock_string)

#####################
#  grid size = 8x8  #
#####################

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,1600)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Fertilizer,1,prev_time)
quick_print(unlock_string)

start_weird = get_time()
mazes.weird_sub(350)
end_weird = get_time()
weird_time = end_weird - start_weird
total_weird += weird_time
# unlock_string, prev_time = unlocking.try_ulock(Unlocks.Fertilizer,1,prev_time)
# quick_print(unlock_string)

start_weird = get_time()
mazes.weird_sub(1350)
end_weird = get_time()
weird_time = end_weird - start_weird
total_weird += weird_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Mazes,0,prev_time)
quick_print(unlock_string)

start_maze = get_time()
mazes.multi_drone_mazes(2000,8)
end_maze = get_time()
maze_time = end_maze - start_maze
total_maze += maze_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Megafarm,0,prev_time)
quick_print(unlock_string)

#####################
#    drones = 2     #
#####################

start_poly = get_time()
polyculture.hay_polyfarm(6100)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Trees,2,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Trees,3,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,6300)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,3,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,14000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,4,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.hay_polyfarm(8000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Carrot,10000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,1,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,2,prev_time)
quick_print(unlock_string)

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,8000)
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += pumpkin_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,5,prev_time)
quick_print(unlock_string)

#####################
# grid size = 12x12 #
#####################

start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,6500)
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += pumpkin_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Cactus,0,prev_time)
quick_print(unlock_string)

start_cacti = get_time()
cacti.multi_drones_cacti(15000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Dinosaurs,0,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Dinosaurs,1,prev_time)
quick_print(unlock_string)

start_dino = get_time()
dinos(10000)
end_dino = get_time()
dino_time = end_dino - start_dino
total_dinos += dino_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Polyculture,1,prev_time)
quick_print(unlock_string)

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_cacti = get_time()
cacti.multi_drones_cacti(84000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Mazes,1,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Mazes,2,prev_time)
quick_print(unlock_string)

start_weird = get_time()
mazes.weird_sub(5000)
end_weird = get_time()
weird_time = end_weird - start_weird
total_weird += weird_time
start_maze = get_time()
mazes.multi_drone_mazes(40000,12)
end_maze = get_time()
maze_time = end_maze - start_maze
total_maze += maze_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Megafarm,1,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Megafarm,2,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Grass,3,prev_time)
quick_print(unlock_string)

#####################
#    drones = 8     #
#####################

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_poly = get_time()
polyculture.hay_polyfarm(25000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Trees,4,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,65000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Fertilizer,2,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Fertilizer,3,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,85000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Watering,5,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,4,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,165000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Carrots,5,prev_time)
quick_print(unlock_string)

start_poly = get_time()
polyculture.hay_polyfarm(25000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Wood,25000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Carrot,100000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,3,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,4,prev_time)
quick_print(unlock_string)

start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,65000)
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += pumpkin_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Expand,6,prev_time)
quick_print(unlock_string)

#####################
# grid size = 16x16 #
#####################

#sub for multi drone sunflowers:
start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_weird = get_time()
mazes.weird_sub_multi_drones(85000,4)
end_weird = get_time()
weird_time = end_weird - start_weird
total_weird += weird_time
start_maze = get_time()
mazes.multi_drone_mazes(128000,8)
end_maze = get_time()
maze_time = end_maze - start_maze
total_maze += maze_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Megafarm,3,prev_time)
quick_print(unlock_string)

#####################
#    drones = 16    #
#####################

start_poly = get_time()
polyculture.hay_polyfarm(50000)
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time

start_poly = get_time()
polyculture.new_multi_drones_poly(Items.Carrot,80000) #from 80000 -> 450000
end_poly = get_time()
poly_time = end_poly - start_poly
total_poly += poly_time
# unlock_string, prev_time = unlocking.try_ulock(Unlocks.Pumpkins,5,prev_time)
# quick_print(unlock_string)

start_pumpkin = get_time()
pumpkins.all_drones_pumpkins(Items.Pumpkin,200000) #from 200000 -> 900000
end_pumpkin = get_time()
pumpkin_time = end_pumpkin - start_pumpkin
total_pumpkin += pumpkin_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Cactus,1,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Cactus,2,prev_time)
quick_print(unlock_string)
# unlock_string, prev_time = unlocking.try_ulock(Unlocks.Cactus,3,prev_time)
# quick_print(unlock_string)

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_cacti = get_time()
cacti.multi_drones_cacti(510000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Dinosaurs,2,prev_time)
quick_print(unlock_string)
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Dinosaurs,3,prev_time)
quick_print(unlock_string)

start_sunflower = get_time()
sunflowers.multi_drones_sunflowers()
end_sunflower = get_time()
sunflower_time = end_sunflower - start_sunflower
total_sunflower += sunflower_time

start_cacti = get_time()
cacti.multi_drones_cacti(1590000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time

# start_sunflower = get_time()
# sunflowers.multi_drones_sunflowers()
# end_sunflower = get_time()
# sunflower_time = end_sunflower - start_sunflower
# total_sunflower += sunflower_time

start_cacti = get_time()
cacti.multi_drones_cacti(2590000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Dinosaurs,4,prev_time)
quick_print(unlock_string)

# start_sunflower = get_time()
# sunflowers.multi_drones_sunflowers()
# end_sunflower = get_time()
# sunflower_time = end_sunflower - start_sunflower
# total_sunflower += sunflower_time

start_cacti = get_time()
cacti.multi_drones_cacti(440000)
end_cacti = get_time()
cacti_time = end_cacti - start_cacti
total_cacti += cacti_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Mazes,3,prev_time)
quick_print(unlock_string)

# start_sunflower = get_time()
# sunflowers.multi_drones_sunflowers()
# end_sunflower = get_time()
# sunflower_time = end_sunflower - start_sunflower
# total_sunflower += sunflower_time

start_dino = get_time()
dinos(2000000)
end_dino = get_time()
dino_time = end_dino - start_dino
total_dinos += dino_time

start_weird = get_time()
mazes.weird_sub_multi_drones(255000,4)
end_weird = get_time()
weird_time = end_weird - start_weird
total_weird += weird_time

start_maze = get_time()
mazes.multi_drone_mazes(1000000,4)
end_maze = get_time()
maze_time = end_maze - start_maze
total_maze += maze_time
unlock_string, prev_time = unlocking.try_ulock(Unlocks.Leaderboard,0,prev_time)
quick_print(unlock_string)




quick_print("Total time farming BEFORE polycultures:",timing.time_units(total_early_farm))
quick_print("Total time farming Polycultures:",timing.time_units(total_poly))
quick_print("Total time farming Sunflowers:",timing.time_units(total_sunflower))
quick_print("Total time farming Pumpkins:",timing.time_units(total_pumpkin))
quick_print("Total time farming Weird Substance:",timing.time_units(total_weird))
quick_print("Total time Doing Mazes:",timing.time_units(total_maze))
quick_print("Total time farming Cacti:",timing.time_units(total_cacti))
quick_print("Total time Doing Dino:",timing.time_units(total_dinos))
quick_print("Final list of items:")
quick_print("Hay:",num_items(Items.Hay))
quick_print("Wood:",num_items(Items.Wood))
quick_print("Carrot:",num_items(Items.Carrot))
quick_print("Pumpkin:",num_items(Items.Pumpkin))
quick_print("Cactus:",num_items(Items.Cactus))
quick_print("Bone:",num_items(Items.Bone))
quick_print("Weird_Substance:",num_items(Items.Weird_Substance))
quick_print("Gold:",num_items(Items.Gold))
quick_print("Power:",num_items(Items.Power))
# quick_print("doing flips now")
# while True:
# 	do_a_flip()
	
