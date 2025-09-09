import datetime
import json
import random
from pathlib import Path


class TooManyTipsException(Exception):
    """Exception raised for more than 20 tips demanded."""
    pass


def menu():
    """ Presents a menu to the user """
    global choice
    print("========LOTTERY MENU==========")
    print("==============================")
    print("1: Generating Swisslos tips")
    print("2: Generating EuroMillions tips")
    print("3: Loading past tips (if present)")
    print("Everything else: Quit")
    print("Please make your choice: ")
    choice = str(input())
    return choice


def quit_program():
    """ Quitting the program """
    print("Bye ...")
    exit()


def generate_tip():
    """
    Generate one tip for Swisslos or EuroMillions
    Swisslos: 6 numbers in the range 1 - 42
    EuroMillions: 5 numbers in the range 1 - 50
    """
    if choice == "1":
        return tuple(sorted(random.sample(range(1, 43), 6)))
    else:
        return tuple(sorted(random.sample(range(1, 50), 5)))


def generate_unique_tips(n):
    """
    Generate n unique tips (no two identical tips).
    """
    tips = set()
    while len(tips) < n:
        tips.add(generate_tip())
    # return tips as lists (easier to print later)
    return [list(t) for t in tips]


def has_identical_tips(list_of_tips):
    """
    Checks if any two lists in a collection have the same elements, regardless of order.
    """
    seen = set()

    for current_list in list_of_tips:
        # Sort the list to handle different element orders
        sorted_tuple = tuple(sorted(current_list))

        # Check if this normalized version has been seen before
        if sorted_tuple in seen:
            return True

        # Add the normalized version to the set
        seen.add(sorted_tuple)

    return False


def print_tips(list_of_tips):
    """
    Pretty-print tips, one per line.
    """
    if choice == "1":
        print("Your Swisslos tips: Good luck")
        print("=============================")
    else:
        print("Your EuroMillions tips: Good luck")
        print("=================================")
    for i, tip in enumerate(list_of_tips, start=1):
        print(f"Tip {i}: {tip}")
    # Convert the list of tips to a dictionary with numbered keys (as preparation of export)
    tips_dict = {f"Tip {i}": tip for i, tip in enumerate(list_of_tips, start=1)}
    export_to_file(tips_dict)


def distribution_analysis(list_of_tips):
    """ Checks potential problems in the distribution
        Issue 1: A tip has only odd or even numbers
        Issue 2: three or more consecutive numbers
    """
    print("Summary of distribution analysis for tips:")
    # Issue 1
    all_numbers = [number for tip in list_of_tips for number in tip]
    odd_numbers = [number for number in all_numbers if number % 2 != 0]
    even_numbers = [number for number in all_numbers if number % 2 == 0]

    if len(odd_numbers) == 0 or len(even_numbers) == 0:
        print("Problem: List of tips has only odd or even numbers.")
    else:
        print("No problem regarding distribution of odd / even numbers")

    # Issue 2
    for i, tip in enumerate(list_of_tips, start=1):
        consecutive_count = 1
        has_consecutive = False

        # The tips are already sorted, so we can directly iterate
        for j in range(len(tip) - 1):
            if tip[j + 1] == tip[j] + 1:
                consecutive_count += 1
            else:
                consecutive_count = 1

            if consecutive_count >= 3:
                print(f"Warning: Tip {i} has 3 or more consecutive numbers.")
                has_consecutive = True
                break  # Exit the inner loop once found

    if not has_consecutive:
        print("No tip has 3 or more consecutive numbers. Great!")


def user_input():
    """
    Ask the user for number of tips, up to 10 attempts.
    """
    number_attempts = 0
    while number_attempts < 10:
        try:
            number_tips = int(input("Please enter number of tips: "))
            if number_tips <= 0:
                raise ValueError("Number must be positive!")
            if number_tips > 20:
                raise ValueError("Not more than 20 tips possible!")

            list_of_tips = generate_unique_tips(number_tips)
            print_tips(list_of_tips)

            if has_identical_tips(list_of_tips):
                print("Validation: At least two lists are identical!")
                print("New generation of numbers necessary!")
            else:
                print("Validation: Valid tip set!")
                distribution_analysis(list_of_tips)
            break
        except ValueError as e:
            number_attempts += 1
            print(f"Invalid input ({e}). Please enter a valid integer. "
                  f"You have overall 10 attempts.")
            print(f"Attempt number: {number_attempts}")
        except TooManyTipsException as e:
            print(f"Invalid input ({e}). Please enter a positive integer with a value not more than 20. "
                  f"You have overall 10 attempts.")
            print(f"Attempt number: {number_attempts}")


def export_to_file(tips_export):
    # Add a timestamp to the data
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tips_export['timestamp'] = timestamp
    # Write the data to a JSON file
    with open('tips.json', 'w') as file:
        json.dump(tips_export, file, indent=4)
        print("Tips written to a file in JSON format ...")


def has_json_file():
    """Checks if a JSON file exists in the current directory."""
    # Create a Path object for the current directory
    current_directory = Path('.')

    # Use the glob() method to search for files matching a pattern.
    # The '*' in '*.json' is a wildcard for any filename.
    # By default, glob() is non-recursive, so it will not search subdirectories.
    for file_path in current_directory.glob('*.json'):
        # If the loop finds even one file, it returns True immediately.
        print("A JSON file with tips was found! Great!")
        pprint_json_file()
        return True

    # If the loop finishes without finding any matching file, return False.
    print("No JSON file with tips was found! Sorry!")
    return False


def pprint_json_file():
    with open('tips.json') as f:
        dict_tips = json.load(f)
    tip_size = len(dict_tips["Tip 1"])  # At least one tip must be present
    if tip_size == 5:
        print("Here come the EuroMillions tips:")
    else:
        print("Here come the Swisslos tips:")

    for key, value in dict_tips.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    choice = menu()
    if choice in ("1", "2"):
        user_input()
    elif choice == "3":
        has_json_file()
    else:
        quit_program()
