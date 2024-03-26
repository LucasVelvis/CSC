import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def visualize_data(bins, outcomes, name):
    # Attempt to make it look like the plot in the paper
    style_dict = {
        'Greedy': {'color': 'blue', 'marker': 'o', 'linestyle': '-'},
        'MES Cost_Sat': {'color': 'green', 'marker': 'X', 'linestyle': '--'},
        'MES Cost_Sqrt_Sat': {'color': 'red', 'marker': 's', 'linestyle': '-.'},
        'MES Effort_Sat': {'color': 'purple', 'marker': 'D', 'linestyle': ':'},
        'MES Cardinality_Sat': {'color': 'orange', 'marker': '^', 'linestyle': '-'}
    }

    # This should be plotted
    plot_data = {measure: {'x': [], 'y': [], 'yerr': []} for measure in outcomes}

    for bin_label, measures in bins.items():
        for measure, data in measures.items():
            if data[name]: # Check if the data is not empty
                avg = np.mean(data[name])
                std = np.std(data[name])
            else:
                avg = 0
                std = 0
            
            plot_data[measure]['x'].append(bin_label)
            plot_data[measure]['y'].append(avg)
            plot_data[measure]['yerr'].append(std)
    
    plt.figure(figsize=(12, 6))
    for measure, style in style_dict.items():
        plt.errorbar(plot_data[measure]['x'], plot_data[measure]['y'], yerr=plot_data[measure]['yerr'], 
                    label=measure, fmt=style['marker'], color=style['color'], linestyle=style['linestyle'], capsize=3)

    plt.xlabel('Number of Projects Range')
    plt.ylabel(f'Average {name}')
    plt.title(f'Average {name} by Project Range')
    plt.legend(title='Rule')
    plt.grid(True)

    plt.tight_layout()
    plt.show()



# def visualize(instance, outcomes, amount_of_outcomes):
#     instance.
#     df_outcomes = pd.DataFrame(columns=['Project', 'Cost', 'Algorithm'])
#     for outcome in outcomes:
#         addOutcome
#     return


# def createPlot():
#     # Preparing the plot
#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Colors for each algorithm
#     colors = {'Algorithm A': 'blue', 'Algorithm B': 'red', 'Algorithm C': 'green'}

#     # Plotting
#     for algorithm, group in df_outcomes.groupby('Algorithm'):
#         ax.barh(group['Project'], group['Cost'], label=algorithm, color=colors[algorithm], alpha=0.6)

#     plt.xlabel('Cost of Chosen Projects', fontweight='bold')
#     plt.ylabel('Projects', fontweight='bold')
#     plt.title('Chosen Projects by Participatory Budgeting Algorithms')
#     plt.legend()

#     # Show plot
#     plt.show()
#     return plot


# def addOutcome(plot, outcome):
#     # Populating the dataframe with the outcomes
#     for algorithm, projects in outcomes.items():
#         for project in projects:
#             df_outcomes = df_outcomes.append({'Project': project[0], 'Cost': project[1], 'Algorithm': algorithm}, ignore_index=True)