import pydoc


def squares(number):
    """ Computes the square of a number"""
    return number ** 2


def put_number_to_list(number_list, number):
    """ Adds a number to a list """
    number_list.append(number)


def put_list_to_dictionary(number_list, number_dict):
    """ Makes a dictionary out of a list """
    for i in range(len(number_list)):
        number_dict[i] = number_list[i]
    return number_dict


def put_list_to_tuple(number_list):
    """ Returns a tuple made from a list """
    return tuple(number_list)


class NumberTooBigException(Exception):
    pass


if __name__ == "__main__":
    number_list = []
    number_dict = {}

    while True:  # Use an infinite loop and break on '0'
        try:
            number = int(input("Input a number? (enter 0 to end): "))
            if number == 0:
                break  # Exit the loop when 0 is entered

            if number <= 1000:
                squared_number = squares(number)
                print(f"The square of {number} is {squared_number}")
                put_number_to_list(number_list, squared_number)
            else:
                raise NumberTooBigException("Number is too big for computing squares")

        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")
        except NumberTooBigException as e:
            print(f"Error: {e}")

    print("\n--- Summary ---")
    print("All the square numbers as list are:", number_list)

    put_list_to_dictionary(number_list, number_dict)
    print("All the numbers as dictionary are:", number_dict)

    number_tuple = put_list_to_tuple(number_list)
    print("All the numbers as a tuple are:", number_tuple)

pydoc.writedoc('squares')
