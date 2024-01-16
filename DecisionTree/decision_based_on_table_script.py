def read_text_document(file_path):  # read given amount of lines (lines of 8 integers)
    string_array = []

    try:
        with open(file_path, 'r') as file:
            # Read each line of the document
            for line in file:
                # Remove trailing newline characters and append to the array
                string_array.append(line.rstrip('\n'))
    except FileNotFoundError:
        print("File not found.")

    return string_array # returns array of lines from the file


def gen_output(array, second_array):    # transcribes line of integers into elemental decisions of shelf "g" and "d"
    if array[0] == 0 or array[0] == 1:
        second_array[0] = "g"
    else:
        second_array[0] = "d"
    if array[1] == 1 or array[1] == 2:
        second_array[1] = "d"
    else:
        second_array[1] = "g"
    if array[2] == 0:
        second_array[2] = "g"
    else:
        second_array[2] = "d"
    if array[3] == 0:
        second_array[3] = "g"
    else:
        second_array[3] = "d"
    if array[4] == 0:
        second_array[4] = "d"
    else:
        second_array[4] = "g"
    if array[5] == 0:
        second_array[5] = "g"
    else:
        second_array[5] = "d"
    if array[6] == 0:
        second_array[6] = "d"
    else:
        second_array[6] = "g"
    if array[7] == 0:
        second_array[7] = "d"
    else:
        second_array[7] = "g"

def count(array):   #   count number of g and d and make decision, if same number return 2 instead
    d = 0
    g = 0
    for digit in array:
        if digit == "g":
            g += 1
        else:
            d += 1
    if d > g:
        return 0    # lower shelf
    elif g > d:
        return 1    # upper shelf
    else:
        return 2    # optimisation of space, goes to more empty shelf overall

file_path = 'file/path/to/input/lines/of/integers'
examples = read_text_document(file_path)  # array of given number of examples from file

for input in examples:
    digit_array = []

    for char in input:
        # Convert the character to an integer and add it to the array
        digit_array.append(int(char))

    output_array = [None] * 8
    gen_output(digit_array, output_array)

    decision_output = count(output_array)
    if decision_output == 2:    # in case d == g, check which shelf is more empty
        if output_array[7] == "g":
            decision_output = 1
        elif output_array[7] == "d":
            decision_output = 0
    print(decision_output)  # final decision