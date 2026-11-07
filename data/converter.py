import csv

csv_regions = open("data/csv/regions.csv", "r")
csv_items = open("data/csv/items.csv", "r")
csv_locations = open("data/csv/locations.csv")

output = open("data.py", "w")

REGION_LIST = []
REGION_CONNECTIONS = {}
REGION_RULES = {}

ITEM_NAME_TO_ID = {}
ITEM_LIST = []
DEFAULT_ITEM_CLASSIFICATIONS = {}
ITEM_GROUPS = {}

LOCATION_REGIONS = {}
LOCATION_NAME_TO_ID = {}
LOCATION_RULES = {}
LOCATION_LIST = []

data = csv.reader(csv_regions)
for row in data:
    origin = row[0].strip()
    target = row[1].strip()
    logic = row[2].strip()

    if not origin in REGION_LIST:
        REGION_LIST.append(origin)
    if not target in REGION_LIST:
        REGION_LIST.append(target)

    if REGION_CONNECTIONS.get(origin):
        REGION_CONNECTIONS[origin].append(target)
    else:
        REGION_CONNECTIONS[origin] = [target]
    
    REGION_RULES[f"{origin} to {target}"] = logic
csv_regions.close()

data = csv.reader(csv_items)
for row in data:
    id = int(row[0])
    name = row[1].strip()
    classification = row[2].strip()
    count = int(row[3])
    group = row[4].strip()

    ITEM_NAME_TO_ID[name] = id
    DEFAULT_ITEM_CLASSIFICATIONS[name] = classification

    if group != '-':
        if ITEM_GROUPS.get(group):
            ITEM_GROUPS[group].append(name)
        else:
            ITEM_GROUPS[group] = [name]

    for i in range(count):
        ITEM_LIST.append(name)
csv_items.close()

data = csv.reader(csv_locations)
for row in data:
    id = int(row[0])
    region = row[1].strip()
    name = f"{region} - {row[2].strip()}"
    logic = row[3].strip()

    LOCATION_NAME_TO_ID[name] = id

    LOCATION_LIST.append(name)

    if LOCATION_REGIONS.get(region):
        LOCATION_REGIONS[region].append(name)
    else:
        LOCATION_REGIONS[region] = [name]

    if logic != '-':
        LOCATION_RULES[name] = logic
csv_locations.close()

output.write("from BaseClasses import ItemClassification\n")
output.write("from rule_builder.rules import Has, HasAll, HasAny\n\n")
output.write("from .helpers import CAN_ACCESS_GARDEN, CAN_ACCESS_DINING_ROOM, CAN_ACCESS_KITCHEN, CAN_ACCESS_POOL_AREA, CAN_ACCESS_SAUNA, CAN_ACCESS_STOREROOM, CAN_ACCESS_LAUNDRY, CAN_ACCESS_MECHANICAL_ROOM, CAN_ACCESS_HALLWAYS, CAN_ACCESS_ROOM_A1, CAN_ACCESS_ROOM_B3, CAN_ACCESS_ROOM_C2, CAN_USE_TOOLKIT, CAN_USE_PIPE_WRENCH, CAN_USE_PRUNING_SHEARS, CAN_USE_TOWELS, CAN_USE_SOAP_BAR, CAN_BEAT_CHALLENGE_GARDEN, CAN_BEAT_CHALLENGE_KITCHEN, CAN_BEAT_CHALLENGE_LOBBY, CAN_BEAT_CHALLENGE_POOL_AREA, CAN_BEAT_CHALLENGE_LAUNDRY, CAN_BEAT_CHALLENGE_HALLWAYS, CAN_CLEAN_FLOOR, CAN_CLEAN_STAINS, CAN_CLEAN_TRASH, CAN_COOK_FOOD, CAN_MOVE_PACKAGES, CAN_DELIVER_CLOTHES, CAN_DELIVER_LUGGAGES, CAN_DELIVER_FOOD, CAN_DELIVER_PACKAGES, CAN_DELIVER_DRINKS\n\n")



output.write(f"REGION_LIST = {REGION_LIST}\n")
output.write(f"REGION_CONNECTIONS = {REGION_CONNECTIONS}\n\n")

output.write(f"ITEM_LIST = {ITEM_LIST}\n")
output.write(f"ITEM_GROUPS = {ITEM_GROUPS}\n")
output.write(f"ITEM_NAME_TO_ID = {ITEM_NAME_TO_ID}\n")
output.write(f"LOCATION_LIST = {LOCATION_LIST}\n\n")

output.write(f"LOCATION_NAME_TO_ID = {LOCATION_NAME_TO_ID}\n")
output.write(f"LOCATION_REGIONS = {LOCATION_REGIONS}\n\n")

output.write("ENTRANCE_RULES = {\n")
for region in REGION_RULES.keys():
    logic = REGION_RULES[region]
    output.write(f"\t\"{region}\": {logic},\n")
output.write("}\n\n")

output.write("LOCATION_RULES = {\n")
for location in LOCATION_RULES.keys():
    logic = LOCATION_RULES[location]
    output.write(f"\t\"{location}\": {logic},\n")
output.write("}\n\n")

output.write("DEFAULT_ITEM_CLASSIFICATIONS = {\n")
for item in DEFAULT_ITEM_CLASSIFICATIONS.keys():
    classification = DEFAULT_ITEM_CLASSIFICATIONS[item]
    output.write(f"\t\"{item}\": {classification},\n")
output.write("}")


output.close()