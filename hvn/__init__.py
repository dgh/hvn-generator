import random
import json
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- #

# The one time Lua beats out Python. Wish I had a rawset(_G, k, v)
with open(os.path.join(module_dir, "data/classes.json")) as f:
    classes = json.load(f)

with open(os.path.join(module_dir, "data/names.json")) as f:
    names = json.load(f)

with open(os.path.join(module_dir, "data/professions.json")) as f:
    professions = json.load(f)

with open(os.path.join(module_dir, "data/races.json")) as f:
    races = json.load(f)


def set_seed(seed: int) -> None:
    random.seed(seed)
    return


def roll(d: int, n: int, sort: bool = False, reverse: bool = False) -> list:
    """
    Return a list of random numbers generated by the dice-notation. Such as
    "AdX" where A is the number of rolls, and X is the number of faces on a
    dice. Additional parameters will sort the list in ascending or descending
    order.
    """

    rolls = [random.randint(1, n) for x in range(d)]

    if sort:
        rolls.sort(reverse=reverse)

    return rolls

# --------------------------------------------------------------------------- #


def generate_power_score() -> int:
    """
    Creates the character's internal power score [1, 100]. Power score is used
    to determine how interesting a character information will be. Higher score
    means a character that has a higher potential
    """
    rolls = roll(3, 100, True)

    return rolls[0]


def generate_race() -> str:
    """
    From the JSON file make two lists. One for the population and the weights
    associated. Use random.choices to make a weighted choice.
    """

    population = []
    weights = []

    for race in races.items():
        population.append(race[0])
        weights.append(race[1]["weight"])

    # Subscripted to pull out from returned list
    race = random.choices(population, weights)[0]

    return race


def generate_gender() -> str:
    """
    Pick a random string from the genders list. Only "male" and "female".
    Uncertain if that will change. Good enough for now.
    """

    genders = ["male", "female"]
    gender = genders[random.randrange(len(genders))]

    return gender


def generate_first_name(race, gender) -> str:
    """
    Pick a random first name. There is a chance that the name will be from the
    race-neutral name set defined by `chance_of_neutral_name`.
    """

    # chance_of_neutral_name = 0.25

    # if random.random() <= chance_of_neutral_name:
    #     race = "neutral"

    # valid_names = data["names"].get(race)["first_names"].get(gender)
    # first_name = random.choice(valid_names)

    valid_names = names["genericFirst"].get(gender)
    first_name = random.choice(valid_names)

    return first_name


def generate_last_name(race) -> str:
    """
    Pick a random last name. There is a chance that the name will be from the
    race-neutral name set defined by `chance_of_neutral_name`.
    """

    # chance_of_neutral_name = 0.25

    # if random.random() <= chance_of_neutral_name:
    #     race = "neutral"

    # valid_names = data["names"].get(race)["last_names"]
    # last_name = random.choice(valid_names)

    valid_names = names["genericLast"]
    last_name = random.choice(valid_names)

    return last_name


def generate_full_name(race, gender) -> tuple:
    """
    Does what it do
    """

    first_name = generate_first_name(race, gender)
    last_name = generate_last_name(race)

    return (first_name, last_name)


def generate_class() -> str:
    """
    Same code as generate_races for now. See that for details.
    """
    population = []
    weights = []

    for class_name in classes.items():
        population.append(class_name[0])
        weights.append(class_name[1]["weight"])

    # Subscripted to pull out from returned list
    class_name = random.choices(population, weights)[0]

    return class_name


def generate_profession(power_score) -> str:
    """
    Takes power score translates that into a "profession bracket". High power
    score means a rarer profession. Check "professions.json" for the minimum
    threshold for each bracket.
    """
    bracket = "low"
    thresholds = professions["thresholds"]

    # Get the profession bracket
    for level in thresholds:
        if power_score >= thresholds.get(level):
            bracket = level
            break

    # From the bracket get the valid professions and pick a random one
    valid_professions = professions.get(bracket)
    profession = random.choice(valid_professions)

    return profession


def generate_ability_scores(race, class_name) -> dict:
    """
    Generate the ability scores based off of race modifiers and proper class
    distributions
    """

    ability_scores = {
        "str": 0, "dex": 0, "con": 0,
        "int": 0, "wis": 0, "cha": 0,
    }

    A = 4
    X = 6
    # Grabs the three highest rolls from a AdX roll six times
    rolls = [sum(roll(A, X, True)[-3:]) for i in range(6)]
    # To ensure randomness for non distributed classes we do NOT sort rolls

    # Apply the class distribution
    distribution = classes.get(class_name)["distribution"]
    for ability in distribution:
        # Pop the largest roll
        largest = rolls.pop(rolls.index(max(rolls)))
        ability_scores[ability] += largest

    # Apply non-specified ability scores
    for ability in set(ability_scores) - set(distribution):
        score = rolls.pop()
        ability_scores[ability] += score

    # Adjust for race modifiers
    race_modifiers = races.get(race)["modifiers"]
    for ability in race_modifiers:
        ability_scores[ability] += race_modifiers[ability]

    return ability_scores

# --------------------------------------------------------------------------- #


# if __name__ == "__main__":
#     race = generate_race()
#     print(race)

#     gender = generate_gender()
#     print(gender)

#     full_name = generate_full_name(race, gender)
#     print(full_name[0], full_name[1])

#     char_class = generate_class()
#     print(char_class)

#     ability_scores = generate_ability_scores(race, char_class)
#     for k, v in ability_scores.items():
#         print(k + ": ", v)

#     power_score = generate_power_score()
#     print("power score:", power_score)

#     profession = generate_profession(power_score)
#     print("profession:", profession)
