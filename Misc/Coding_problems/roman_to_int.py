def roman_to_int(roman):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    num = 0
    prev_value = 0
    for char in roman:
        value = roman_dict[char]
        if value > prev_value:
            num += value - 2 * prev_value
        else:
            num += value
        prev_value = value
    return num

# Test the function
print(roman_to_int('CCXLIV'))  # Output: 244