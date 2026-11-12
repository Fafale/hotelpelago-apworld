from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle
# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class ChallengesGoalAmount(Range):
    """
    How many challenges are required to be beaten
    in order to goal your game.
    """

    display_name = "Challenges Goal Amount"

    range_start = 3
    range_end = 6
    default = 6

class ChallengeHelpers(Range):
    """
    How many final challenge helpers will be added to the item pool.
    They give extra time, score or lifes, depending on the challenge.
    """

    display_name = "Challenge Helpers"

    range_start = 0
    range_end = 2
    default = 1

class UsefulFillerPercentage(Range):
    """
    How many of the filler items will be actually useful filler.
    The remaining filler will be either "Nothing" or traps.
    """

    display_name = "Useful Filler Percentage"

    range_start = 0
    range_end = 100
    default = 70

class TrapPercentage(Range):
    """
    How many of the remaining filler will be turned into traps.
    They'll become "Nothing" otherwise.
    """

    display_name = "Trap Percentage"

    range_start = 0
    range_end = 100
    default = 5
    
# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class HotelpelagoOptions(PerGameCommonOptions):
    challenges_goal_amount: ChallengesGoalAmount

    challenge_helpers: ChallengeHelpers
    useful_filler_percentage: UsefulFillerPercentage
    trap_percentage: TrapPercentage


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Goal Options",
        [ChallengesGoalAmount]
    ),
    OptionGroup(
        "Filler Options",
        [ChallengeHelpers, UsefulFillerPercentage, TrapPercentage],
    )
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {}
