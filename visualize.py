import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def visualize(instance, outcomes, amount_of_outcomes):
    instance.
    df_outcomes = pd.DataFrame(columns=['Project', 'Cost', 'Algorithm'])
    for outcome in outcomes:
        addOutcome
    return


def createPlot():
    # Preparing the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Colors for each algorithm
    colors = {'Algorithm A': 'blue', 'Algorithm B': 'red', 'Algorithm C': 'green'}

    # Plotting
    for algorithm, group in df_outcomes.groupby('Algorithm'):
        ax.barh(group['Project'], group['Cost'], label=algorithm, color=colors[algorithm], alpha=0.6)

    plt.xlabel('Cost of Chosen Projects', fontweight='bold')
    plt.ylabel('Projects', fontweight='bold')
    plt.title('Chosen Projects by Participatory Budgeting Algorithms')
    plt.legend()

    # Show plot
    plt.show()
    return plot


def addOutcome(plot, outcome):
    # Populating the dataframe with the outcomes
    for algorithm, projects in outcomes.items():
        for project in projects:
            df_outcomes = df_outcomes.append({'Project': project[0], 'Cost': project[1], 'Algorithm': algorithm}, ignore_index=True)