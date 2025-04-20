from bs4 import BeautifulSoup
from collections import Counter
import statistics

# Step 1: Load the downloaded HTML file
with open("python_class_question.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "lxml")

# Step 2: Extract the shirt colors from the second <td> in each row
shirt_colors = []

rows = soup.find_all('tr')

for row in rows:
    tds = row.find_all('td')
    if len(tds) > 1:
        # Split the string in td[1] by comma and strip whitespaces
        colors = [color.strip().upper() for color in tds[1].text.split(',')]
        shirt_colors.extend(colors)  # Add each color individually

# Step 3: Analyze the shirt colors
color_counts = Counter(shirt_colors)

# Most common color (mode)
most_common_color = color_counts.most_common(1)[0][0]

# Median color (based on frequency)
sorted_colors = sorted(shirt_colors)
n = len(sorted_colors)
if n % 2 == 1:
    median_color = sorted_colors[n // 2]
else:
    median_color = sorted_colors[n // 2 - 1]  # or take average if numeric

# Mean frequency of color appearances (not a "mean color", just mean of counts)
mean_frequency = statistics.mean(color_counts.values())

# Print results
print("Shirt Colors:", shirt_colors)
print("Most Common Color:", most_common_color)
print("Median Color:", median_color)
print("Mean Frequency of Colors:", mean_frequency)

# BONUS: Variance of color frequencies
try:
    color_frequencies = list(Counter(shirt_colors).values())
    variance = statistics.variance(color_frequencies)
    print(f"Variance of color frequencies: {variance}")
except statistics.StatisticsError:
    print("Not enough data to compute variance.")

# BONUS: Probability that a randomly chosen color is red
total_colors = len(shirt_colors)
red_count = shirt_colors.count("RED")
probability_red = red_count / total_colors if total_colors > 0 else 0

print(f"Probability of choosing red: {probability_red:.4f}")


import psycopg2

# Count the color frequencies
color_counter = Counter(shirt_colors)

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="shirt_colors_db",
        user="postgres",
        password="Hayo24434078",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    # Insert color and frequency data
    for color, freq in color_counter.items():
        cursor.execute("INSERT INTO shirt_colors (color, frequency) VALUES (%s, %s)", (color, freq))

    conn.commit()
    print("✅ Data inserted into PostgreSQL successfully!")

except Exception as e:
    print("❌ Error:", e)

finally:
    if conn:
        cursor.close()
        conn.close()


#a recursive searching algorithm to search for a number entered by user in a list of numbers.
def recursive_linear_search(arr, target, index=0):
    # Base case: If index is beyond the list length, the target is not found
    if index == len(arr):
        return -1  # target not found

    # If the target is found, return the index
    if arr[index] == target:
        return index

    # Recursively call the function with the next index
    return recursive_linear_search(arr, target, index + 1)

# Example usage
if __name__ == "__main__":
    numbers = [3, 6, 2, 9, 5, 10, 1]  # Example unsorted list
    target = int(input("Enter a number to search: "))
    result = recursive_linear_search(numbers, target)

    if result != -1:
        print(f"Number {target} found at index {result}.")
    else:
        print(f"Number {target} not found in the list.")


#A program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10. 
import random

# Generate a random 4-digit binary number
binary_number = ''.join(random.choice('01') for _ in range(4))

# Convert the binary number to base-10
decimal_number = int(binary_number, 2)

# Display the results
print(f"Generated 4-digit binary number: {binary_number}")
print(f"Converted to base-10: {decimal_number}")


# Function to sum the first n Fibonacci numbers
def fibonacci_sum(n):
    a, b = 0, 1  # Starting values for Fibonacci sequence
    total = 0

    for _ in range(n):
        total += a  # Add the current number to the total
        a, b = b, a + b  # Update the values of a and b for the next Fibonacci number

    return total

# Summing the first 50 Fibonacci numbers
n = 50
result = fibonacci_sum(n)
print(f"The sum of the first {n} Fibonacci numbers is: {result}")
9