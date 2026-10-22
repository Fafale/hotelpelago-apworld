from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import HotelpelagoWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: HotelpelagoWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: HotelpelagoWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    lobby       = Region("Lobby", world.player, world.multiworld)
    storeroom   = Region("Storeroom", world.player, world.multiworld)
    dining_room = Region("Dining Room", world.player, world.multiworld)
    kitchen     = Region("Kitchen", world.player, world.multiworld)
    laundry     = Region("Laundry", world.player, world.multiworld)
    hallways    = Region("Hallways", world.player, world.multiworld)
    room_1      = Region("Room 1", world.player, world.multiworld)
    room_2      = Region("Room 2", world.player, world.multiworld)
    room_3      = Region("Room 3", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [lobby, storeroom, dining_room, kitchen, laundry, hallways, room_1, room_2, room_3]

    #   # Some regions may only exist if the player enables certain options.
    #   # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    #   if world.options.hammer:
    #       top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #       regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: HotelpelagoWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    lobby       = world.get_region("Lobby")
    storeroom   = world.get_region("Storeroom")
    dining_room = world.get_region("Dining Room")
    kitchen     = world.get_region("Kitchen")
    laundry     = world.get_region("Laundry")
    hallways    = world.get_region("Hallways")
    room_1      = world.get_region("Room 1")
    room_2      = world.get_region("Room 2")
    room_3      = world.get_region("Room 3")


    #   # Okay, now we can get connecting. For this, we need to create Entrances.
    #   # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    #   # One way to create an Entrance is by calling the Entrance constructor.
    #   overworld_to_bottom_right_room = Entrance(world.player, "Overworld to Bottom Right Room", parent=overworld)
    #   overworld.exits.append(overworld_to_bottom_right_room)

    #   # You can then connect the Entrance to the target region.
    #   overworld_to_bottom_right_room.connect(bottom_right_room)

    # An even easier way is to use the region.connect helper.
    lobby.connect(storeroom, "Lobby to Storeroom")

    lobby.connect(dining_room, "Lobby to Dining Room")
    dining_room.connect(kitchen, "Dining Room to Kitchen")

    lobby.connect(laundry, "Lobby to Laundry")
    
    lobby.connect(hallways, "Lobby to Hallways")
    hallways.connect(room_1, "Hallways to Room 1")
    hallways.connect(room_2, "Hallways to Room 2")
    hallways.connect(room_3, "Hallways to Room 3")

    #   # The region.connect helper even allows adding a rule immediately.
    #   # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #   overworld.connect(top_left_room, "Overworld to Top Left Room", lambda state: state.has("Key", world.player))

    #   # Some Entrances may only exist if the player enables certain options.
    #   # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    #   # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    #   if world.options.hammer:
    #       top_middle_room = world.get_region("Top Middle Room")
    #       overworld.connect(top_middle_room, "Overworld to Top Middle Room")
