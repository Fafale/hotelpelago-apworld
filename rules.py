from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAny, Rule

from .options import HardMode

if TYPE_CHECKING:
    from .world import HotelpelagoWorld

CAN_ACCESS_STOREROOM = Has("Storeroom Key")
CAN_ACCESS_DINING_ROOM = Has("Dining Room Key")
CAN_ACCESS_KITCHEN = CAN_ACCESS_DINING_ROOM & Has("Kitchen Key")
CAN_ACCESS_LAUNDRY = Has("Laundry Key")
CAN_ACCESS_HALLWAYS = HasAny("Elevator Pass", "Staircase Pass")
CAN_ACCESS_ROOM_1 = CAN_ACCESS_HALLWAYS & Has("Room 1 Key")
CAN_ACCESS_ROOM_2 = CAN_ACCESS_HALLWAYS & Has("Room 2 Key")
CAN_ACCESS_ROOM_3 = CAN_ACCESS_HALLWAYS & Has("Room 3 Key")

CAN_CLEAN_FLOOR = Has("Mop & Bucket") & CAN_ACCESS_STOREROOM


def set_all_rules(world: HotelpelagoWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: HotelpelagoWorld) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    lobby_to_storeroom = world.get_entrance("Lobby to Storeroom")
    lobby_to_dining_room = world.get_entrance("Lobby to Dining Room")
    dining_room_to_kitchen = world.get_entrance("Dining Room to Kitchen")
    lobby_to_laundry = world.get_entrance("Lobby to Laundry")
    lobby_to_hallways = world.get_entrance("Lobby to Hallways")
    hallways_to_room_1 = world.get_entrance("Hallways to Room 1")
    hallways_to_room_2 = world.get_entrance("Hallways to Room 2")
    hallways_to_room_3 = world.get_entrance("Hallways to Room 3")

    world.set_rule(lobby_to_storeroom, CAN_ACCESS_STOREROOM)
    world.set_rule(lobby_to_dining_room, CAN_ACCESS_DINING_ROOM)
    world.set_rule(dining_room_to_kitchen, CAN_ACCESS_KITCHEN)
    world.set_rule(lobby_to_laundry, CAN_ACCESS_LAUNDRY)
    world.set_rule(lobby_to_hallways, CAN_ACCESS_HALLWAYS)
    world.set_rule(hallways_to_room_1, CAN_ACCESS_ROOM_1)
    world.set_rule(hallways_to_room_2, CAN_ACCESS_ROOM_2)
    world.set_rule(hallways_to_room_3, CAN_ACCESS_ROOM_3)

    #   # Now we can set our "can_destroy_bush" rule to the entrance which requires slashing a bush to clear the path.
    #   # The easiest way to do this is by calling world.set_rule, which works for both Locations and Entrances.
    #   world.set_rule(overworld_to_bottom_right_room, can_destroy_bush)
    #   
    #   # Conditions can also depend on event items.
    #   button_pressed = Has("Top Left Room Button Pressed")
    #   world.set_rule(right_room_to_final_boss_room, button_pressed)
    # 
    #   # Some entrance rules may only apply if the player enabled certain options.
    #   # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    #   # Overworld to the Top Middle Room.
    #   if world.options.hammer:
    #       overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
    #       can_smash_brick = Has("Hammer")
    #       world.set_rule(overworld_to_top_middle_room, can_smash_brick)

    # Beyond these structural advantages,
    # Rule Builder also allows the core AP code to do a lot of under-the-hood optimizations.
    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.


def set_all_location_rules(world: HotelpelagoWorld) -> None:
    # Removed all comments, need to read again from original apworld

    can_deliver_order: Rule = CAN_ACCESS_KITCHEN

    deliver_order_1 = world.get_location("Dining Room - Deliver order 1")
    deliver_order_2 = world.get_location("Dining Room - Deliver order 2")
    deliver_order_3 = world.get_location("Dining Room - Deliver order 3")

    world.set_rule(deliver_order_1, can_deliver_order)
    world.set_rule(deliver_order_2, can_deliver_order)
    world.set_rule(deliver_order_3, can_deliver_order)

    clean_floor_lobby = world.get_location("Lobby - Clean the floor")
    clean_floor_storeroom = world.get_location("Storeroom - Clean the floor")
    clean_floor_dining_room = world.get_location("Dining Room - Clean the floor")
    clean_floor_kitchen = world.get_location("Kitchen - Clean the floor")
    clean_floor_hallways = world.get_location("Hallways - Clean the floor")
    clean_floor_room_1 = world.get_location("Room 1 - Clean the floor")
    clean_floor_room_2 = world.get_location("Room 2 - Clean the floor")
    clean_floor_room_3 = world.get_location("Room 3 - Clean the floor")
    clean_floor_laundry = world.get_location("Laundry - Clean the floor")

    world.set_rule(clean_floor_lobby, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_storeroom, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_dining_room, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_kitchen, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_hallways, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_room_1, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_room_2, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_room_3, CAN_CLEAN_FLOOR)
    world.set_rule(clean_floor_laundry, CAN_CLEAN_FLOOR)


def set_completion_condition(world: HotelpelagoWorld) -> None:
    # For the time being, just have all available to do
    world.set_completion_rule(
        CAN_ACCESS_STOREROOM &
        CAN_ACCESS_DINING_ROOM &
        CAN_ACCESS_KITCHEN &
        CAN_ACCESS_LAUNDRY &
        CAN_ACCESS_HALLWAYS &
        CAN_ACCESS_ROOM_1 &
        CAN_ACCESS_ROOM_2 &
        CAN_ACCESS_ROOM_3 &
        CAN_CLEAN_FLOOR
    )

    #   # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    #   # For this, we can use world.set_completion_rule.
    #   # You can just set a completion condition directly like any other condition, referencing items the player receives:
    #   world.set_completion_rule(HasAll("Sword", "Shield"))
    #
    #   # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    #   # So lets undo what we just did, and instead set the completion condition to:
    #   world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class HotelpelagoWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
