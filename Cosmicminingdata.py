import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


print("Karan Dahyea's tbl_file_to_spectra graph converter for cosmic mining")

while True:  # Start infinite loop :D

    root = tk.Tk()
    root.withdraw()

    # Open file explorer and ask for the .tbl file
    file_path = filedialog.askopenfilename(
        title="Pick your .tbl file please.",
        filetypes=(("Text files", "*.tbl"), ("All files", "*.*"))
    )

    if file_path:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Get the data (skip first 3 lines)
            data = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    data.append(line.split())

            x = []  # Wavelengths
            y = []  # Flux values

            # Try to turn the data into numbers
            for row in data:
                try:
                    x.append(float(row[0]))  # Wavelength
                    y.append(float(row[1]))  # Flux
                except:
                    continue  # Skip if it can't be converted to a number

            if x and y:
                y_smooth = np.convolve(y, np.ones(2)/2, mode='same')  # Smooth the flux data

                # Ask the user for how "big" an anomaly should be (percentage)
                threshold_percentage = float(input("How much of a difference do you want it to be a feature? Enter a number for example 30 for 30%: ")) / 100

                weird_x = []  # Points that are a weird difference
                weird_y = []  # Flux values for the weird points

                # Check every point to see if it's weird (bigger than threshold)
                for i in range(len(y)):
                    if abs(y[i] - y_smooth[i]) > threshold_percentage * y_smooth[i]:
                        weird_x.append(x[i])
                        weird_y.append(y[i])
                
                # Plot everything
                plt.scatter(x, y, color='blue')  # Normal points (blue)
                plt.plot(x, y_smooth, color='black', linewidth=2)  # The smooth line (black)
                plt.scatter(weird_x, weird_y, color='red')  # The weird points (red)

                # Show the graph
                plt.show()
            else:
                print("No data found")

        except:
            print("something broke.")
    else:
        print("No file picked")

    # Ask the user if they want to continue or quit
    restarter = input("Woulds you like to pick another file? (yes/no): ").lower()
    if restarter := 'yes':   
        print("Exiting program, thanks for trying it out <3")
        break  # Exit the loop if the user says no