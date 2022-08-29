"""
Focuses here:

1) GUI!!!

"""
import itertools as it
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

""" Input Variables"""

class Ability:
    def __init__(self, name, min_dmg_x10, max_dmg_x10, duration, cooldown, channeled, can_crit,\
                 hits, adrenaline, ability_type, hitsplat_profile):
        self.name = name  # Ability name
        self.min_dmg_x10 = min_dmg_x10  # min damage multipled by 10 (so it will always be an integer)
        self.max_dmg_x10 = max_dmg_x10  # max damage multipled by 10 (so it will always be an integer)
        self.min_dmg = self.min_dmg_x10 / 10  # min damage, as a float
        self.max_dmg = self.max_dmg_x10 / 10  # max damage, as a float
        self.duration = duration  # In ticks
        self.cooldown = cooldown  # In ticks
        self.channeled = channeled  # Binary
        self.can_crit = can_crit  # Binary
        self.hits = hits  # Amount of hits within the max duration
        self.adrenaline = adrenaline  # Adrenaline, cost is negative, gain is positive
        self.ability_type = ability_type
        self.hitsplat_profile = [int(x) for x in str(int(hitsplat_profile))] # creates a hitsplat profile

    def natural_crit_chance(self):
        x = 1 - (0.95 * self.max_dmg - self.min_dmg) / (
                self.max_dmg - self.min_dmg)
        return x

""" Importing Data & Choosing the Ability"""

# importing ability data from csv
abilities_df = pd.read_csv('Ability_information.csv', index_col='name')
# asking the user to choose an ability
user_input = input(f"""Select from the following: {list(abilities_df.index)}\n
Which ability would you like to choose?""")
while user_input not in abilities_df.index:
    user_input = input("Choose another ability")

# creates a list of all the ability attributes imported from the csv
ability_info_list = list(abilities_df.loc[user_input])
print(ability_info_list)

# creates an object which is the ability that the user has decided
ability_choice = Ability(user_input, *ability_info_list)
print(vars(ability_choice))
print(ability_choice.hitsplat_profile)
print(type(ability_choice.hitsplat_profile))

# for number in ability_choice.hitsplat_profile:
#     print(number + 1)

""" Player Buffs etc"""

# asks the user their goal adrenaline
adren_refund_goal = None
while adren_refund_goal is None or adren_refund_goal > 100 or adren_refund_goal < 0:
    try:
        adren_refund_goal = int(input("How much adrenaline would you like refunded?"))
        continue
    except:
        print("Enter a number between 0 and 100.")

# setting default values of buffs to 0
tsunami_status = False
natural_instinct_status = False
vigour_status = False
invigorating_rank = 0
forced_crit_chance = 0

crit_data = [['grimoire', 0.12], ['kalg_spec', 0.05], ['kalg_passive', 0.01], ['reaver', 0.05]]

""" User inputs"""
if input("Would you like to use max crit chance?").lower() == "yes":
    for name, crit_bonus in crit_data:
        for i in crit_data:
            forced_crit_chance += i[1]
        break
    # adding max biting rank (4) to the forced crit data
    biting_rank = 4
    forced_crit_chance += 0.02 * biting_rank
    print(f"You are using the max forced crit chance, which is{round(forced_crit_chance * 100, 1)}%.")
    forced_crit_selected = True
else:
    for name, crit_bonus in crit_data:
        if input(f"Would you like to use {name}?").lower() == "yes":
            forced_crit_chance += crit_bonus
    forced_crit_selected = False

# selecting biting rank
while forced_crit_selected == False:
    try:
        biting_rank = int(input("What Biting rank are you using?"))
    except:
        print("Select a rank from 0 to 4.")
    else:
        if 0 <= biting_rank <= 4:
            print(f"Your Biting rank is {biting_rank}.")
            # asking the user if their gear is level 20 (yes/no)
            while forced_crit_selected == False:
                lvl20_gear = input("Is Biting on level 20 gear? (yes/no)").lower()
                if lvl20_gear == "yes":
                    forced_crit_chance += 0.022 * biting_rank
                    print(f"You are using level 20 gear, and have {round(forced_crit_chance*100,1)}% forced crit chance.")
                    forced_crit_selected = True
                elif lvl20_gear == "no":
                    forced_crit_chance += 0.02 * biting_rank
                    print(f"You are NOT using level 20 gear, and have {round(forced_crit_chance*100,1)}% forced crit chance.")
                    forced_crit_selected = True
                else:
                    print("Select a rank from 0 to 4.")

# asking if user wants Tsunami
if input("Would you like to use Tsunami?").lower() == "yes":
    tsunami_status = True
    print("You are using Tsunami.")
else:
    tsunami_status = False
    print("You are NOT using Tsunami.")

# asking if user wants Natural Instinct
if input("Would you like to use Natural Instinct?").lower() == "yes":
    natural_instinct_status = True
    print("You are using Natural Instinct.")
else:
    natural_instinct_status = False
    print("You are NOT using Natural Instinct.")

# asking if using ring of vigour - only pops up if ability_type for the ability is NOT none
if ability_choice.ability_type == 'spec' or ability_choice.ability_type == 'ult':
    if input("Are you using a ring of vigour?").lower() == "yes":
        vigour_status = True
        print("You are using a Ring of Vigour.")
    else:
        vigour_status = False
        print("You are NOT using a Ring of Vigour.")

# selecting invigorating rank
while True:
    try:
        invigorating_rank = int(input("What Invigorating rank are you using?"))
    except:
        print("try again")
    else:
        if 0 <= invigorating_rank <= 4:
            print(f"Your invigorating rank is {invigorating_rank}.")
            break

""" Defining new natty and tsunami variables to be used in calculations"""

# gives a value of 2 when active, 1 when inactive
natural_instinct = natural_instinct_status + 1
# gives a value of 10 when active, 0 when inactive
tsunami = 10 * tsunami_status

""" Calculating crit chances given the data"""

ability_natural = ability_choice.natural_crit_chance()
# eventually not going to hard-code the natural crit chance of the auto
auto_natural = 0.05

ability_crit_chance = forced_crit_chance + (1 - forced_crit_chance) * ability_natural
auto_crit_chance = forced_crit_chance + (1 - forced_crit_chance) * auto_natural

""" Functions defined below"""

def hitsplat_adren(hitsplat_type, crit):
    # crit is either 1 or 0
    if hitsplat_type == 'ability':
        adren_refund = natural_instinct * (tsunami * crit)
    elif hitsplat_type == 'auto':
        adren_refund = natural_instinct * (tsunami * crit + (2 + 0.2 * invigorating_rank))
    return adren_refund

def stream_adren(hitsplats, crit_end_value):
    stream_adren_refund = 0
    # if 1 hitsplat, the is only an ability hit
    if hitsplats == 1:
        stream_adren_refund += hitsplat_adren('ability', crit_end_value)
    # if more than 1 hitsplat, there is 1 ability hit plus (hitsplats-1) auto hits
    elif hitsplats > 1:
        stream_adren_refund += hitsplat_adren('ability', 1)
        stream_adren_refund += max((hitsplats-2),0) * hitsplat_adren('auto', 1)
        stream_adren_refund += hitsplat_adren('auto', crit_end_value)

    return stream_adren_refund

def crit_end(hitsplats):
    # if it's a crit end, abs must crit
    stream_probability = ability_crit_chance * auto_crit_chance**max((hitsplats-1),0)
    return stream_probability

def non_crit_end(hitsplats):
    if hitsplats == 1:
        stream_probability = (1-ability_crit_chance)
    elif hitsplats > 1:
        stream_probability = ability_crit_chance * auto_crit_chance**max((hitsplats-2),0) * (1-auto_crit_chance)
    return stream_probability

""" Creating the ability hitsplat profile etc"""

# these two values will depend on the ability
# need to make it import from the csv file
ability_hitsplat_profile = ability_choice.hitsplat_profile
cancel_tick = ability_choice.duration
# creates a list which shows the max hitsplats per chain (in order of when the chains are generated, so this list
# should be in descending order
max_chain_hitsplats = [cancel_tick + 1 - x for x in ability_hitsplat_profile]

# number of chains
no_of_chains = len(ability_hitsplat_profile)

# producing a list of all chains (which are themselves lists)
chain_list = []
for number in ability_hitsplat_profile:
    chain_list.append(list(range(1, cancel_tick - number + 2)))

print(chain_list)

""" All hitsplat permutations"""

# all possible hitsplat permutations - each number represents how many hitsplats in that chain
# products a list of lists
hitsplat_profiles_lists = list(it.product(*chain_list))

print(hitsplat_profiles_lists)
print(len(hitsplat_profiles_lists))

# converts the list of lists into a list of strings, which we will work with
hitsplat_profiles = []
for profile in hitsplat_profiles_lists:
    profile = ''.join(str(i) for i in profile)
    hitsplat_profiles.append(profile)

print(hitsplat_profiles)
print(len(hitsplat_profiles))

""" Crit ending permutations - defined with 0's and 1's"""

# generating the possible crit endings - number of permutations is 2 to the power of the number of chains
# because each ending is either a crit or non-crit
# eg asphyx has 4 chains - number of crit_ending permutations = 2^4 = 16
crit_endings_list = []
crit_endings = it.product([0, 1], repeat=no_of_chains)
for x in crit_endings:
    y = [str(i) for i in x]
    y = "".join(y)
    crit_endings_list.append(y)

print(crit_endings_list)
print(len(crit_endings_list))

""" Combining the hitsplat profiles & crit endings to give 'overall' permuations"""

total_permutations_list = list(it.product(hitsplat_profiles, crit_endings_list))

print(total_permutations_list)
print(len(total_permutations_list))

""" Removing impossible permutations - left with (possible) scenarios"""

# this list is going to become the list without any 'broken' pairs
# scenarios will represent all possible scenarios, with which we will make calculations off
scenarios = []
for permutation in total_permutations_list:
    # check if a pair is possible, if not, discard
    # max hitsplats is 54321 - 11111 & 00100 isn't possible because it would suggest the hitsplat profile is 11211
    # ie the two values cannot be the same
    broken = False
    for i in range(no_of_chains):
        # if the last hit is a crit, and that last hit does not occur on tick 5
        # eg 12111, 01000 cannot work because if the last hit in stream 2 is a crit, stream2 would have more than 2 crits
        # it would cap at 4 if this were the case
        """ max_chain_hitsplats[i] is the max number of hitsplats in the relevant chain"""
        if int(permutation[1][i]) == 1 and int(permutation[0][i]) != max_chain_hitsplats[i]:
            # print(f"{permutation} is broken on stream {i+1}. This was the {counter} item.")
            broken = True
            break
    if not broken:
        scenarios.append(permutation)

print(scenarios)
print(len(scenarios))

""" Calculating and compiling all adren gains and their probabilities"""

# data calculations - adren gains and probabilities to be added, in pairs, to data_pairs
data_pairs = []
for permutation in scenarios:
    adren_refund = 0
    probability = 1
    # calculating probability per stream of hitsplats
    for i in range(no_of_chains):
        if int(permutation[1][i]) == 1:
            adren_refund += stream_adren(int(permutation[0][i]), int(permutation[1][i]))
            probability *= crit_end(int(permutation[0][i]))
        elif int(permutation[1][i]) == 0:
            adren_refund += stream_adren(int(permutation[0][i]), int(permutation[1][i]))
            probability *= non_crit_end(int(permutation[0][i]))
    data_pair = [adren_refund, probability]
    data_pairs.append(data_pair)

print(data_pairs)
print(len(data_pairs))

""" Defining ability_cost to be used for the graph. Ability_cost is used to work out the 
overall_adren_gain for each successful scenario"""

if ability_choice.ability_type == 'spec':
    ability_cost = ability_choice.adrenaline * 0.9
elif ability_choice.ability_type == 'ult':
    ability_cost = ability_choice.adrenaline + 10
else:
    ability_cost = ability_choice.adrenaline

""" Creating a list of scenarios & data pairs where the adren goal is reached"""

full_data = []
for data_pair in data_pairs:
    overall_adren_gain = data_pair[0] + ability_cost
    data_item = [*data_pair, overall_adren_gain]
    full_data.append(data_item)

print(full_data)
print(len(full_data))

success_data = []
for data_item in full_data:
    if data_item[0] > adren_refund_goal:
        success_data.append(data_item)

print(success_data)
print(len(success_data))

# summing all the successful probabilities
success_probability = math.fsum(x[1] for x in success_data)
success_percentage = success_probability * 100

""" Printing out results"""

if natural_instinct == 2 and tsunami == 10:
        print(f"Chance of refunding {adren_refund_goal} adrenaline from {ability_choice.name}"
              f" with Tsunami & Natty is {round(success_percentage, 1)}%.")
elif natural_instinct == 1  and tsunami == 10:
    print(f"Chance of refunding {adren_refund_goal} adrenaline from {ability_choice.name}"
          f" with Tsunami (no Natty) is {round(success_percentage, 1)}%.")
elif natural_instinct == 2  and tsunami == 0:
    print(f"Chance of refunding {adren_refund_goal} adrenaline from {ability_choice.name}"
          f" with Natty (no Tsunami) is {round(success_percentage, 8)}%.")
elif natural_instinct == 1  and tsunami == 0:
    print(f"Chance of refunding {adren_refund_goal} adrenaline from {ability_choice.name},"
          f" with neither Tsunami nor Natty, is {success_percentage}%.")

# creating a sorted list of all data items
sorted_full_data = sorted(full_data, key=lambda a:a[0])
print(sorted_full_data)
print(len(sorted_full_data))

cumulative_probabilities = []
for i in range(len(sorted_full_data)):
    cumulative_list = sorted_full_data[i:]
    """ this bit is incorrect I think"""
    cumulative_probability = sum(item[1] for item in cumulative_list)
    cumulative_probabilities.append(cumulative_probability)

ascending_adren_values = [x[0] for x in sorted_full_data]

print(cumulative_probabilities)
print(ascending_adren_values)

fig, ax=plt.subplots()
ax.plot(ascending_adren_values,cumulative_probabilities)
ax.axhline(y=success_probability, color="red", linestyle='--')
plt.title("Adrenaline Refunded (x) vs Probability (y)")
plt.xlabel("Adrenaline Refunded")
plt.ylabel("Probability")
plt.xlim([0,100])

trans = transforms.blended_transform_factory(
    ax.get_yticklabels()[0].get_transform(), ax.transData)
ax.text(0,success_probability, f"{success_probability:.3f}", color="red", transform=trans,
        ha="right", va="center")

# # plotting the cumulative probability graph from 0 to max adren
# plt.plot(ascending_adren_values, cumulative_probabilities)
# plt.title("Adrenaline Refunded (x) vs Probability (y)")
# plt.xlabel("Adrenaline Refunded")
# # setting limits of the x axis
# plt.xlim([0,100])
# plt.ylabel("Probability")
# # labels the success probability (relating to the adren refund goal)
# plt.axhline(y=success_probability, color='black', linestyle='--')

plt.show()