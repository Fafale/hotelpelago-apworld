from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAny, Rule, CanReachRegion, HasGroupUnique, HasGroup

from .data import ENTRANCE_RULES, LOCATION_RULES
from .helpers import CAN_ACCESS_GARDEN, CAN_ACCESS_DINING_ROOM, CAN_ACCESS_KITCHEN, CAN_ACCESS_POOL_AREA, CAN_ACCESS_SAUNA, CAN_ACCESS_STOREROOM, CAN_ACCESS_LAUNDRY, CAN_ACCESS_MECHANICAL_ROOM, CAN_ACCESS_HALLWAYS, CAN_ACCESS_ROOM_A1, CAN_ACCESS_ROOM_B3, CAN_ACCESS_ROOM_C2, CAN_USE_TOOLKIT, CAN_USE_PIPE_WRENCH, CAN_USE_PRUNING_SHEARS, CAN_USE_TOWELS, CAN_USE_SOAP_BAR, CAN_BEAT_CHALLENGE_GARDEN, CAN_BEAT_CHALLENGE_KITCHEN, CAN_BEAT_CHALLENGE_LOBBY, CAN_BEAT_CHALLENGE_POOL_AREA, CAN_BEAT_CHALLENGE_LAUNDRY, CAN_BEAT_CHALLENGE_HALLWAYS, CAN_CLEAN_FLOOR, CAN_CLEAN_STAINS, CAN_CLEAN_TRASH, CAN_COOK_FOOD, CAN_MOVE_PACKAGES, CAN_DELIVER_CLOTHES, CAN_DELIVER_LUGGAGES, CAN_DELIVER_FOOD, CAN_DELIVER_PACKAGES, CAN_DELIVER_DRINKS

if TYPE_CHECKING:
    from .world import HotelpelagoWorld


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
    for entrance_name in ENTRANCE_RULES.keys():
        entrance = world.get_entrance(entrance_name)
        world.set_rule(entrance, ENTRANCE_RULES[entrance_name])

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

    for location_name in LOCATION_RULES.keys():
        location = world.get_location(location_name)
        world.set_rule(location, LOCATION_RULES[location_name])

    victory_loc = world.get_location("5-Star Reviews Collected")
    world.set_rule(victory_loc, Has("5-Star Review", int(world.options.challenges_goal_amount)))


def set_completion_condition(world: HotelpelagoWorld) -> None:
    #   # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    #   # For this, we can use world.set_completion_rule.
    #   # You can just set a completion condition directly like any other condition, referencing items the player receives:
    #   world.set_completion_rule(HasAll("Sword", "Shield"))
    #
    #   # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    #   # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class HotelpelagoWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
