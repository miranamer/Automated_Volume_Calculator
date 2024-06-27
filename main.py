import matplotlib.pyplot as plt
import random

mySubstances = []
solution_volume = None

def plot_volume_distribution(volumes, labels):
    # Generate random colors
    random.seed(42)  # for reproducibility
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in volumes]

    # Create a stacked bar plot
    fig, ax = plt.subplots(figsize=(2, 6))

    # Plot the stacked bars
    bottom = 0
    for volume, label, color in zip(volumes, labels, colors):
        ax.bar(1, volume, bottom=bottom, color=color, edgecolor='black', label=label)
        bottom += volume

    # Add the volume labels inside the bars
    bottom = 0
    for volume, label in zip(volumes, labels):
        ax.text(1, bottom + volume / 2, f'{volume} µL\n{label}', ha='center', va='center', color='black')
        bottom += volume

    # Remove the x axis for a cleaner look
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set the limit for the y-axis to fit all volumes
    ax.set_ylim(0, sum(volumes))

    # Add titles
    plt.title('Volume Distribution for Final Solution', pad=20)

    # Show the plot
    plt.tight_layout()
    plt.show()

def find_relative_conc_factor(conc_factor_desired, volume_to_add, volume_adding_into, volume_old = 0, initial_conc_of_substance = 0):
    volume_total = volume_to_add + volume_adding_into

    resultant_conc_factor = ((conc_factor_desired * volume_total) - volume_old) / volume_to_add

    if volume_old == 0:
        print(f'You need to add {volume_to_add} uL of substance with a conc of {resultant_conc_factor}X')
        return (0, resultant_conc_factor) # 0 means it's relative to initial conc. => ?X
    else:
        if(initial_conc_of_substance <= 0):
            return('Error! - You need to mention what the initial conc. of the substance was in the old volume.')
        else:
            print(f'You need to add {volume_to_add}uL of substance with a conc of {resultant_conc_factor * initial_conc_of_substance} uL')
            return (1, resultant_conc_factor * initial_conc_of_substance) # 1 means it's the actual value of the conc needed to be added


def find_volume_to_extract_from_stock(desired_conc_in_solution, total_volume_in_solution, conc_of_base_stock):
    volume_to_extract_from_stock = (desired_conc_in_solution * total_volume_in_solution) / conc_of_base_stock
    return volume_to_extract_from_stock * 1000 # vol in μL
    #print(f'You need to extract {volume_to_extract_from_stock * 1000} uL of substance from stock | substance_vol:total_vol ratio => {volume_to_extract_from_stock * 1000}:{total_volume_in_solution * 1000}') # * 1000 to get into uL

while True:
    start = input("Add Subtance? (y/n): ")

    if start != 'y':
        break
    else:
        substance_name = input('Name of substance: ')
        conc_factor_desired = float(input('Desired Conc. Factor (e.g. 1X, 2X, 10X, etc.): '))
        volume_to_add = float(input('What is the volume of the solution you would like to add? - [μL]: ')) # Should enter same value all the time as you want to mix these substances all into this given volume
        volume_adding_into = float(input(f'What volume are you adding this {volume_to_add} into? - [μL]: '))
            
        volume_old = float(input('Is there any initial volume with this substance in it? If yes, how much else enter 0 - [μL]: '))
        if volume_old > 0:
            initial_conc_of_substance = float(input('What was the initial conc. of substance in the old volume - [μL]: '))
        else:
            initial_conc_of_substance = 0
        
        mySubstances.append([substance_name, conc_factor_desired, volume_to_add, volume_adding_into, volume_old, initial_conc_of_substance])
        if solution_volume == None:
            solution_volume = volume_to_add

#print(mySubstances)

step_1_results = []

for i in mySubstances:
    res = find_relative_conc_factor(i[1], i[2], i[3], i[4], i[5]) # res[1] = actual value, res[0] tells you if its relative X or value
    step_1_results.append([i[0], res[1], res[0]])

print(step_1_results)

step_2_results = []
total_vol_added_so_far = 0

for i in step_1_results:
    name, val, val_type = i[0], i[1], i[2]

    if val_type == 0:
        what_is_X = float(input(f'What is your X for {name} (conc. of substance you want in the final total vol)? - [μg/mL]: '))
        val *= what_is_X
    
    base_stock_conc = float(input(f'What is the base stock conc. for {name}? - [μg/mL]: '))

    res = find_volume_to_extract_from_stock(val, solution_volume / 1000, base_stock_conc)
    total_vol_added_so_far += round(res, 2)

    step_2_results.append([name, round(res, 2)])

if total_vol_added_so_far < solution_volume:
    step_2_results.append(['Diluent', solution_volume - total_vol_added_so_far])


volumes = [i[1] for i in step_2_results]
labels = [i[0] for i in step_2_results]

plot_volume_distribution(volumes, labels)