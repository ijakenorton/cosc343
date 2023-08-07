def average_from_file(filename):
    with open(filename, 'r') as f:
        numbers = f.readlines()
    
    # Convert each line to a float and sum them, ensuring the line isn't empty
    total = sum(float(num.strip()) for num in numbers if num.strip())
    
    # Divide by the number of non-empty lines to get the average
    average = total / len([num for num in numbers if num.strip()])
    
    return average

filename = 'random_seed_codes'  # Replace with your file name
print(f"The average of the numbers in {filename} is {average_from_file(filename)}")