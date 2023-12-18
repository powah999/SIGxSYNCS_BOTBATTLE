from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.foodtype import FoodType
from submissionhelper.info.pettype import PetType


# Core class for the submission helper
# Use this to make moves and get game info
bot_battle = BotBattle()

carry_food = [FoodType.GARLIC, FoodType.HONEY, FoodType.MEAT_BONE]

useless_pet_t1 =[PetType.ANT,PetType.MOSQUITO,PetType.CRICKET,PetType.HORSE,PetType.FISH,PetType.PIG]
number_1_combo =[PetType.PEACOCK, PetType.CRAB, PetType.BUNNY, PetType.SKUNK, PetType.GIRAFFE]
no_can = [FoodType.CANNED_FOOD]


# Core game loop
# Each iteration you will be expected to make one move
prev_round_num = 0
while True:
    game_info = bot_battle.get_game_info()

    # Feel free to uncomment these lines if you want to inspect the info!
    print(game_info, flush=True)
    print("", flush=True)

    # How to detect whether it is a new round
    new_round = prev_round_num != game_info.round_num
    if new_round:
        print(f"Round {game_info.round_num}\n\n")
        prev_round_num = game_info.round_num

    def get_health_list(game_info: 'GameInfo'):
    
            health_list=[]
            index_list = []
            pet_list = []
            for index, pet in enumerate(game_info.player_info.pets):
                if pet is not None:
                    health_list.append(pet.health)
                    index_list.append(index)
                    pet_list.append(pet)

            health_list_sorted = sorted(health_list, reverse=True)
            pet_list_sorted = []

            for health in health_list_sorted:
                for pet in game_info.player_info.pets:
                    if pet is not None:
                        if pet.health == health:
                            pet_list_sorted.append(pet)
                            break
                
            return (pet_list_sorted, index_list, pet_list)

    def fill_pets(game_info: 'GameInfo'):
        #Fills empty lineup with shop pets
        if None in game_info.player_info.pets: #Checks if lineup is not full
            for shop_pet in game_info.player_info.shop_pets:
                for i, pet in enumerate(game_info.player_info.pets):
                    if pet is None and shop_pet.cost <= game_info.player_info.coins: #Checks if pet exists in slot AND enough coins for purchase
                        if shop_pet.is_frozen: 
                            bot_battle.unfreeze_pet(shop_pet) #Unfreezes shop_pet first if it was frozen
                            return 1
                        bot_battle.buy_pet(shop_pet, i)
                        return 1
                    
    def level_pets_shop(game_info: 'GameInfo'):
        #Loops through shop and check if you can level up a pet
        if None not in game_info.player_info.pets:
            for shop_pet in game_info.player_info.shop_pets:
                for i, pet in enumerate(game_info.player_info.pets):
                    if pet is not None:
                        if shop_pet.type == pet.type and shop_pet.cost <= game_info.player_info.coins:
                            if shop_pet.is_frozen:
                                bot_battle.unfreeze_pet(shop_pet)
                                return 1
                            if pet.level < 2 and shop_pet.cost <= game_info.player_info.coins:  # Check if the pet can still be leveled up
                                bot_battle.level_pet_from_shop(shop_pet, pet)
                                return 1
                        
    def level_pets_lineup(game_info: 'GameInfo'):
        i = 1
        pet_lineup = game_info.player_info.pets
        if None not in game_info.player_info.pets:
            for pet_to_level in pet_lineup[:-1]:
                for pet_to_use in pet_lineup[i:]:
                    if pet_to_use is not None and pet_to_level is not None:
                        if pet_to_use.level < 2 and pet_to_level.level < 2 and pet_to_use.type != PetType.BUNNY and pet_to_level.type != PetType.BUNNY and pet_to_use.type != PetType.SKUNK and pet_to_level.type != PetType.SKUNK:
                            if pet_to_use.type == pet_to_level.type:
                                bot_battle.level_pet_from_pets(pet_to_use, pet_to_level)
                                return 1
                i += 1    

    def better_pets(game_info: 'GameInfo'):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            for shop_pet_index,shop_pet in enumerate(game_info.player_info.shop_pets):
                if pet is not None:
                    if shop_pet is not None:
                        if shop_pet.type not in useless_pet_t1:
                            if None not in game_info.player_info.pets:
                                if pet.health + pet.attack < shop_pet.health + shop_pet.attack and shop_pet.cost <= game_info.player_info.coins-1:
                                    if game_info.remaining_moves>=2:     
                                        bot_battle.sell_pet(pet)
                                        game_info = bot_battle.get_game_info()
                                        shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                        bot_battle.buy_pet(shop_pet,pet_index)
                                        return 1
    
    def no_more_useless(game_info: 'GameInfo'):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            for shop_pet_index,shop_pet in enumerate(game_info.player_info.shop_pets):
                if None not in game_info.player_info.pets:
                    if pet.type in useless_pet_t1:
                        if shop_pet.type not in useless_pet_t1:
                            if game_info.player_info.coins>=2:
                                if game_info.round_num>2:
                                    if game_info.remaining_moves>=2:
                                        bot_battle.sell_pet(pet)
                                        game_info =bot_battle.get_game_info()
                                        shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                        bot_battle.buy_pet(shop_pet,pet_index)
                                        return 1
    
    def meta_pet(game_info: 'GameInfo'):
        pet_list = []
        for pet in game_info.player_info.pets:
            if pet is not None: 
                pet_list.append(pet.type)
        for pet_index, pet in enumerate(game_info.player_info.pets):
            for shop_pet_index,shop_pet in enumerate(game_info.player_info.shop_pets):
                if None not in game_info.player_info.pets:
                    if pet.type not in number_1_combo:
                        if shop_pet.type in number_1_combo and shop_pet.type != PetType.SKUNK and shop_pet.type != PetType.GIRAFFE and shop_pet.type != PetType.BUNNY:
                            if shop_pet.type not in pet_list:
                                if game_info.player_info.coins>=2:
                                    if game_info.remaining_moves>=2:
                                        bot_battle.sell_pet(pet)
                                        game_info =bot_battle.get_game_info()
                                        shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                        bot_battle.buy_pet(shop_pet,pet_index)
                                        return 1        
    def buy_giraffe(game_info: 'GameInfo'):
        has_giraffe = any(pet is not None and pet.type == PetType.GIRAFFE for pet in game_info.player_info.pets)
        player = game_info.player_info
        if not has_giraffe:
            for shop_pet_i, shop_pet in enumerate(player.shop_pets):
                if shop_pet is not None:
                    if shop_pet.type == PetType.GIRAFFE:
                        for pet_i, pet in enumerate(player.pets):
                            if pet is not None:
                                if game_info.player_info.coins>=2:
                                    if pet.type not in number_1_combo:
                                        bot_battle.sell_pet(pet)
                                        game_info =bot_battle.get_game_info()
                                        shop_pet = game_info.player_info.shop_pets[shop_pet_i]
                                        bot_battle.buy_pet(shop_pet, pet_i)
                                        return 1
                        for pet_i, pet in enumerate(player.pets):
                            if pet is not None:
                                if game_info.player_info.coins>=2:
                                    if pet.type == PetType.BUNNY:
                                        bot_battle.sell_pet(pet)
                                        game_info =bot_battle.get_game_info()
                                        shop_pet = game_info.player_info.shop_pets[shop_pet_i]
                                        bot_battle.buy_pet(shop_pet, pet_i)
                                        return 1 
                    
                         
    
    def swap_giraffe(game_info: 'GameInfo'):
        for index,pet in enumerate(game_info.player_info.pets):
            if pet is not None:
                if pet.type == PetType.GIRAFFE:
                    if pet.level == 1:
                        if index != 1:
                            bot_battle.swap_pets(index,1)
                            return 1
                    elif pet.level == 2:
                        if index != 2:
                            bot_battle.swap_pets(index,2)
                            return 1
                             
    def buy_bunny(game_info: 'GameInfo'):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            for shop_pet_index,shop_pet in enumerate(game_info.player_info.shop_pets):
                if None not in game_info.player_info.pets:
                    if pet_index>1:
                        if pet.type != PetType.BUNNY and pet.type != PetType.SKUNK and pet.type !=PetType.GIRAFFE and pet.type != PetType.CRAB and shop_pet.type == PetType.BUNNY:
                            if game_info.player_info.coins>=2:
                                if game_info.remaining_moves>=2:
                                    bot_battle.sell_pet(pet)
                                    game_info =bot_battle.get_game_info()
                                    shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                    bot_battle.buy_pet(shop_pet,pet_index)
                                    return 1                                

    

    def buy_skunk_crab(game_info: 'GameInfo'):

        skunk_num = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.SKUNK)
        has_giraffe = any(pet is not None and pet.type == PetType.PEACOCK for pet in game_info.player_info.pets)
        bunny_num = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.BUNNY)
        
        for shop_pet_index,shop_pet in enumerate(game_info.player_info.shop_pets):
            if None not in game_info.player_info.pets:
                if skunk_num < 1:  
                    if check_peacock_health(game_info, 30, 50):
                            if not bunny_num < 2:
                                if shop_pet.type == PetType.SKUNK:
                                    if game_info.player_info.coins>=3:
                                        if shop_pet.is_frozen:
                                            bot_battle.unfreeze_pet(shop_pet)
                                            game_info = bot_battle.get_game_info()
                                        if game_info.remaining_moves>=2:
                                            level_bunnies(game_info)
                                            game_info = bot_battle.get_game_info()
                                            shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                            bot_battle.buy_pet(shop_pet,4)
                                            return 1
                                        
                elif skunk_num < 2 and has_giraffe:
                    if check_peacock_health(game_info, 40, 50):
                        if shop_pet.type == PetType.SKUNK:
                            if game_info.player_info.coins>=3:
                                if shop_pet.is_frozen:
                                    bot_battle.unfreeze_pet(shop_pet)
                                    game_info = bot_battle.get_game_info()
                                if game_info.remaining_moves>=2:
                                    for i, pet in enumerate(game_info.player_info.pets):
                                        if i == 3:
                                            bot_battle.sell_pet(pet)
                                            game_info = bot_battle.get_game_info()
                                            shop_pet = game_info.player_info.shop_pets[shop_pet_index]
                                            bot_battle.buy_pet(shop_pet,3)
                                            return 1     
                else:
                    return                    

                                
                              
    def level_bunnies(game_info: 'GameInfo'):
        #FIX THIS FOR WHEN ONYL HAVE 2 BUNNIES YET PEACKOCK IS ALREADY GIGA STACKED
        has_bunny = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.BUNNY)
        has_skunk = any(pet is not None and pet.type == PetType.SKUNK for pet in game_info.player_info.pets)

        pets = game_info.player_info.pets
        slot_3_bunny = pets[2] is not None and pets[2].type == PetType.BUNNY
        slot_4_bunny = pets[3] is not None and pets[3].type == PetType.BUNNY
        slot_5_bunny = pets[4] is not None and pets[4].type == PetType.BUNNY
        slot_5_skunk = pets[4] is not None and pets[4].type == PetType.SKUNK

        if has_bunny == 3:
            if slot_4_bunny and slot_5_bunny:
                bot_battle.level_pet_from_pets(game_info.player_info.pets[4], game_info.player_info.pets[3])
                return 1
        elif has_bunny == 2:
            if has_skunk:
                bot_battle.level_pet_from_pets(game_info.player_info.pets[3], game_info.player_info.pets[2]) 
                return 1
            else:
                bot_battle.sell_pet(pets[4])
                return 1
            
        return

    def check_peacock_health(game_info: 'GameInfo', num1, num2):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            if pet is not None:
                if pet.type == PetType.PEACOCK:
                    if pet.health >= num1 and pet.health <= num2:
                        return True
        return False
                        
    def get_food(game_info: 'GameInfo'):
        # Buys food for pets, in order of highest health to lowest
        # Carriable foods like honey, garlic, meat_bone are only bought ONCE for each pet
        pet_list = []
        for shop_food in game_info.player_info.shop_foods:
            for pet_index, pet in enumerate(game_info.player_info.pets):
                pet_list.append(pet)
                if pet is not None:
                    if shop_food.cost <= game_info.player_info.coins:
                        if shop_food.type not in carry_food and shop_food.type not in no_can:
                            if pet.type == PetType.PEACOCK and not check_peacock_health(game_info, 40, 50):
                                bot_battle.buy_food(shop_food, pet)
                                return 1                       
                            elif pet.type == PetType.CRAB:
                                bot_battle.buy_food(shop_food, pet)
                                return 1                                            
                        if shop_food.type in carry_food:
                            if pet.carried_food == None:   
                                if pet.type == PetType.PEACOCK and shop_food.type == FoodType.GARLIC:
                                    bot_battle.buy_food(shop_food, pet)
                                    return 1
                                elif pet.type == PetType.CRAB and shop_food.type == FoodType.MEAT_BONE:
                                    bot_battle.buy_food(shop_food, pet)
                                    return 1
                                
    def check_giraffe(game_info: 'GameInfo'):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            if pet is not None:
                if pet.type == PetType.GIRAFFE:
                    if pet.level == 1:
                        if pet_index == 1:
                            return True
                    elif pet.level == 2:
                        if pet_index == 2:
                            return True
                    else:
                        return False
    def check_giraffe_lvl(game_info: 'GameInfo'):
        for pet_index, pet in enumerate(game_info.player_info.pets):
            if pet is not None:
                if pet.type == PetType.GIRAFFE:
                    if pet.level == 1:
                        if pet_index == 1:
                            return 1
                    elif pet.level == 2:
                        if pet_index == 2:
                            return 2
                    else:
                        return 

    def reroll(game_info: 'GameInfo'):
        # Rerolls shop,
        if game_info.player_info.coins > 0 :
            bot_battle.reroll_shop()
            return 1
        
    def freeze(game_info: 'GameInfo'):
        #Freeze shop pets that are the same as your pet lineup
            if game_info.player_info.coins < 3:
                for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
                    for pet_index, pet in enumerate(game_info.player_info.pets):
                        if pet is not None:
                            if shop_pet.type == pet.type and not shop_pet.is_frozen and pet.level != 3:
                                bot_battle.freeze_pet(shop_pet)
                                return 1
                            

    def swap_first(game_info: 'GameInfo'):
        for j,pet in enumerate(game_info.player_info.pets):
            if None not in game_info.player_info.pets:
                if j != 0:
                    if pet.type == PetType.PEACOCK:
                        bot_battle.swap_pets(j,0)
                        return 1

    
    def swap_third(game_info: 'GameInfo'):
        a = check_giraffe_lvl(game_info)
        for j,pet in enumerate(game_info.player_info.pets):
            if check_giraffe(game_info) == False or a==1:
                if None not in game_info.player_info.pets:
                    if j != 2:  
                        if pet.type == PetType.CRAB:
                            bot_battle.swap_pets(j,2)
                            return 1

    def swap_second(game_info: 'GameInfo'):
        bunny_found = False
        for j, pet in enumerate(game_info.player_info.pets):
            if j != 1 and pet is not None and pet.type == PetType.BUNNY:
                bunny_found = True
                break
        if not bunny_found:
            for j, pet in enumerate(game_info.player_info.pets):
                if check_giraffe(game_info) == False:                
                    if pet is not None:
                        if pet.type != PetType.SKUNK:
                            if j != 1 and pet.type == PetType.BUNNY:
                                bot_battle.swap_pets(j, 1)
                                return 1

    def swap_fourth(game_info: 'GameInfo'):
        bunny_found = False
        for j, pet in enumerate(game_info.player_info.pets):
            if j != 3 and pet is not None and pet.type == PetType.BUNNY:
                bunny_found = True
                break
        if not bunny_found:
            for j, pet in enumerate(game_info.player_info.pets):
                if pet is not None:
                    if pet.type != PetType.SKUNK:
                        if j != 3 and pet is not None and pet.type == PetType.BUNNY:
                            bot_battle.swap_pets(j, 3)
                            return 1

    def swap_fifth(game_info: 'GameInfo'):
        bunny_found = False
        for j, pet in enumerate(game_info.player_info.pets):
            if j != 4 and pet is not None and pet.type == PetType.BUNNY:
                bunny_found = True
                break
        if not bunny_found:
            for j, pet in enumerate(game_info.player_info.pets):
                if pet is not None:
                    if pet.type != PetType.SKUNK:
                        if j != 4 and pet is not None and pet.type == PetType.BUNNY:
                            bot_battle.swap_pets(j, 4)
                            return 1
                    
    
    def lvl_meta(game_info: 'GameInfo'):
        if None not in game_info.player_info.pets:
            for shop_pet in game_info.player_info.shop_pets:
                for i, pet in enumerate(game_info.player_info.pets):
                    if pet is not None:
                        if shop_pet.type == pet.type and shop_pet.cost <= game_info.player_info.coins:
                            if shop_pet.is_frozen:
                                bot_battle.unfreeze_pet(shop_pet)
                                return 1
                            if pet.level < 2 and shop_pet.cost <= game_info.player_info.coins and pet.type in number_1_combo and pet.type != PetType.BUNNY and pet.type != PetType.SKUNK:  # Check if the pet can still be leveled up
                                bot_battle.level_pet_from_shop(shop_pet, pet)
                                return 1
    
    def freeze_meta(game_info: 'GameInfo'):
        bunny_num = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.BUNNY)
        if game_info.player_info.coins < 3:
            for shop_pet_index, shop_pet in enumerate(game_info.player_info.shop_pets):
                if shop_pet.type == PetType.SKUNK and not shop_pet.is_frozen:
                    if check_peacock_health(game_info, 25, 50) and num_skunks_func(game_info) < 2:
                        bot_battle.freeze_pet(shop_pet)
                        return 1   
                else:
                    current_lineup = []
                    for pet_index, pet in enumerate(game_info.player_info.pets):
                        if pet is not None:
                            current_lineup.append(pet.type)
                            if pet.type == shop_pet.type:     
                                if shop_pet.type in number_1_combo and not shop_pet.is_frozen and pet.level < 2 and not bunny_num >=2 and not shop_pet.type == PetType.SKUNK:
                                    bot_battle.freeze_pet(shop_pet)
                                    return 1   
                                
                    if shop_pet.type not in current_lineup and shop_pet.type in number_1_combo and not shop_pet.is_frozen and not bunny_num >=2 and not shop_pet.type == PetType.SKUNK:
                        bot_battle.freeze_pet(shop_pet)
                        return 1   
                      
                              
    def num_skunks_func(game_info: 'GameInfo'):
        num_skunks = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.SKUNK)
        return num_skunks
    
    def make_move(game_info: 'GameInfo'):
        if game_info.round_num < 3:
            a = fill_pets(game_info)
            if a != None:
                return
            
            a = level_pets_lineup(game_info)
            if a != None:
                return
            
            if None not in game_info.player_info.pets:
                a = level_pets_shop(game_info)
                if a != None:
                    return

            a = better_pets(game_info)
            if a!=None:
                return
                
            a = no_more_useless(game_info)
            if a != None:
                return
            
            a = get_food(game_info)
            if a != None:
                return
        

            a = reroll(game_info)
            if a != None:
                return
            
            a = freeze(game_info)
            if a != None:
                return
            
            bot_battle.end_turn()
            
        elif game_info.round_num >= 3:

        
            a = fill_pets(game_info)
            if a != None:
                return
            
            a = level_pets_lineup(game_info)
            if a != None:
                return

            a = lvl_meta(game_info)
            if a != None:
                return

            a = meta_pet(game_info)
            if a != None:
                return

            a = buy_bunny(game_info)
            if a!= None:
                return
            
            a = buy_skunk_crab(game_info)
            if a != None:
                return

            a = buy_giraffe(game_info)
            if a != None:
                return
            
            has_peacock = any(pet is not None and pet.type == PetType.PEACOCK for pet in game_info.player_info.pets)
            has_crab = any(pet is not None and pet.type == PetType.CRAB for pet in game_info.player_info.pets)
            has_bunny = sum(1 for pet in game_info.player_info.pets if pet is not None and pet.type == PetType.BUNNY)
            if has_peacock and has_crab:
                if has_bunny>=2 or check_peacock_health(game_info,30,50):
                    a = get_food(game_info)
                    if a != None:
                        return

            a = swap_giraffe(game_info)
            if a != None:
                return
            
            a = swap_first(game_info)
            if a != None:
                return

            a = swap_second(game_info)
            if a != None:
                return

            a = swap_third(game_info)
            if a != None:
                return

            a = swap_fourth(game_info)
            if a != None:
                return

            a = swap_fifth(game_info)
            if a != None:
                return

            a = freeze_meta(game_info)
            if a != None:
                return
            
            a = reroll(game_info)
            if a != None:
                return


            bot_battle.end_turn()

              

        

     

    # Last but not least, don't forget to call the function!
    make_move(game_info)