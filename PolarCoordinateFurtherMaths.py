import time
import sys
import math

while True:
    print("Welcome to Karan's Polar Co-ordinate converter!")
    x_value = float(input("Enter the x value: "))
    y_value = float(input("Enter the y value: "))

    r = (x_value**2 + y_value**2)**0.5
    theta = 0
    if x_value > 0:
        theta = math.atan(y_value / x_value)
    elif x_value < 0 and y_value >= 0:
        theta = math.atan(y_value / x_value) + math.pi
    elif x_value < 0 and y_value < 0:
        theta = math.atan(y_value / x_value) - math.pi
    elif x_value == 0 and y_value > 0:
        theta = math.pi / 2
    elif x_value == 0 and y_value < 0:
        theta = -math.pi / 2
    print(f"The polar coordinates are: r = {r}, θ = {theta} radians")
    play_again = input("Do you want to convert another point? (yes/no): ").strip().lower()
    if play_again != "yes":
        print("Thank you for using the Polar Co-ordinate converter")
        break
    time.sleep(1)  # Wait before the next iteration
    print("Invalid input, please type 'yes' or 'no'.")
    time.sleep(1)  # Wait before the next iteration
    if play_again == "no":
        print("Thank you for using the Polar Co-ordinate converter")
        break
    else:
        print("Invalid input, please type 'yes' or 'no'.")
        time.sleep(1) # Wait before the next iteration