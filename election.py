from pabutools.election import *
from pabutools.rules import *
import time
#from visualize import visualize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def print_outcome(outcome, name):
    print("Outcome of " + name + ":")
    cost = 0
    for projects in outcome:
        print("Name: " + str(projects.name) + ", Cost: " + str(projects.cost))
        cost += projects.cost

    print("Total cost: " + str(cost) + ". Budget left: " + str(instance.budget_limit - cost)) 


def visualize(instance, outcomes, amount_of_outcomes):
    df_projects = pd.DataFrame(columns=['Project', 'Cost', 'Algorithm'])
    all_projects = instance.init()
    for project in all_projects:
        df_projects.append({'Project': str(project.name), 'Cost': str(project.cost)}, ignore_index=True)


    
    for outcome in outcomes:
        addOutcome
    return


def createPlot(df_projects, df_outcomes):
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
    return plt


def addOutcome(plot, outcome):
    # Populating the dataframe with the outcomes
    for algorithm, projects in outcomes.items():
        for project in projects:
            df_outcomes = df_outcomes.append({'Project': project[0], 'Cost': project[1], 'Algorithm': algorithm}, ignore_index=True)


def budgetFeasability(instance):
    for b in instance.budget_allocations():
        print(str(b) + " is a feasible budget allocation")


if __name__ == '__main__':
    start = time.time()

    path = "2024-03-23_10-28-29_pabulib\\netherlands_amsterdam_252_.pb"  # set this variable
    instance, profile = parse_pabulib(path)

    print("Minimum Length of Ballots: " + str(profile.legal_min_length))   # Imposed minimum length of the ballots in the profile
    print("Maximum Length of Ballots: " + str(profile.legal_max_length))   # Imposed maximum length of the ballots in the profile

    print("Minimum Total Cost of Ballots: " + str(profile.legal_min_cost))   # Imposed minimum total cost of the ballots in the profile
    print("Maximum Total Cost of Ballots: " + str(profile.legal_max_cost))   # Imposed maximum total cost of the ballots in the profile

    print("Budget limit is: " + str(instance.budget_limit))
    
    #outcomes = list(BudgetAllocation)

    start2 = time.time()

    outcome = greedy_utilitarian_welfare(
    instance,
    profile,
    sat_class=Cost_Sat
    )

    print_outcome(outcome, "Greedy")

    start3 = time.time()

    outcome = method_of_equal_shares(
    instance,
    profile,
    sat_class=Cost_Sat
    )

    print_outcome(outcome, "MES Cost_Sat")

    outcome = method_of_equal_shares(
    instance,
    profile,
    sat_class=Cost_Sqrt_Sat
    )

    print_outcome(outcome, "MES Cost_Sqrt_Sat")


    # outcome = method_of_equal_shares(
    # instance,
    # profile,
    # sat_class=Effort_Sat
    # )


    # effort = time.time()
    # print_outcome(outcome, "MES  Effort_Sat")
    # outcomes.append(outcome)
    # effort_e = time.time()

    outcome = method_of_equal_shares(
    instance,
    profile,
    sat_class=Cardinality_Sat
    )

    print_outcome(outcome, "MES  Cardinality_Sat")

    #visualize(instance, outcomes, range(outcomes))

    end = time.time()
    print(f"Time taken to load: {start2 - start:.2f} seconds")
    print(f"Time taken Greedy: {start3 - start2:.2f} seconds")
    #print(f"Time taken Effort: {effort_e - effort:.2f} seconds")
    print(f"Time taken MES Total: {end - start3:.2f} seconds")
    print(f"Total time taken: {end - start:.2f} seconds") 
