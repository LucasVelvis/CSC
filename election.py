import time

import matplotlib.pyplot as plt
import numpy as np

# from visualize import visualize
import pandas as pd
from pabutools.election import (
    parse_pabulib,
    Cost_Sat,
    Cost_Sqrt_Sat,
    Effort_Sat,
    Cardinality_Sat,
)
from pabutools.rules import greedy_utilitarian_welfare, method_of_equal_shares
from visualize import visualize_data

paths = [
    "2024-03-23_10-28-29_pabulib/netherlands_amsterdam_252_.pb",
    "2024-03-23_10-28-29_pabulib/netherlands_amsterdam_285_.pb",
    "2024-03-23_10-28-29_pabulib/netherlands_amsterdam_309_.pb",
    "2024-03-23_10-28-29_pabulib/netherlands_amsterdam_523_.pb",
]


def print_outcome(outcome, name, instance):
    """
    Print the outcome of the algorithm.
    """
    print("Outcome of " + name + ":")
    cost = 0
    for projects in outcome:
        # print("Name: " + str(projects.name) + ", Cost: " + str(projects.cost))
        cost += projects.cost

    print(
        "Total cost: "
        + str(cost)
        + ". Budget left: "
        + str(instance.budget_limit - cost)
    )


def print_profile_info(instance, profile):
    """
    Print the information about the profile.
    """
    print(
        "Minimum Length of Ballots: " + str(profile.legal_min_length)
    )  # Imposed minimum length of the ballots in the profile
    print(
        "Maximum Length of Ballots: " + str(profile.legal_max_length)
    )  # Imposed maximum length of the ballots in the profile

    print(
        "Minimum Total Cost of Ballots: " + str(profile.legal_min_cost)
    )  # Imposed minimum total cost of the ballots in the profile
    print(
        "Maximum Total Cost of Ballots: " + str(profile.legal_max_cost)
    )  # Imposed maximum total cost of the ballots in the profile

    print("Budget limit is: " + str(instance.budget_limit))

    return


def perform_election(path, algorithm, algorithm_name, sat_class):

    instance, profile = parse_pabulib(path)
    # print_profile_info(instance, profile)

    start = time.time()
    outcome = algorithm(instance, profile, sat_class=sat_class)
    end = time.time()

    print_outcome(outcome, algorithm_name, instance)
    print(f"Time taken {algorithm_name}: {end - start:.2f} seconds")

    return outcome


def get_shares(outcome, profile, instance):
    """
    Shares based on Definition (and Example) 1 from the paper.
    Fair shares based on Definition 2 from the paper.
    """
    shares = []
    fair_shares = []

    # Dict for projects + their costs
    selected_projects = {project.name: float(project.cost) for project in outcome}

    # Dict for projects + their voters
    total_voters_per_project = {
        project.name: sum(project.name in ballot for ballot in profile)
        for project in outcome
    }

    # Get shares and fair shares for each voter
    for ballot in profile:
        agent_share = sum(
            selected_projects[project] / total_voters_per_project[project]
            for project in ballot
            if project in selected_projects
        )
        shares.append(agent_share)
        b_over_n = float(instance.budget_limit) / len(profile)
        fair_shares.append(min(b_over_n, agent_share))

    return shares, fair_shares


def get_average_capped_fair_share_ratio(shares, fair_shares):
    """
    Average capped fair share ratio based on page 17 from the paper.
    """
    # TODO: take into account the case where the denominator is 0

    num_agents = len(shares)
    sum_fair_shares = 0
    for i in range(num_agents):
        if shares[i] == 0:
            sum_fair_shares += 1
        else:
            sum_fair_shares += min(1, fair_shares[i] / shares[i])

    return sum_fair_shares / num_agents


def get_average_l1_distance(shares, fair_shares):
    """
    Average L1 distance also based on page 17 from the paper.
    """
    num_agents = len(shares)
    return sum(abs(shares[i] - fair_shares[i]) for i in range(num_agents)) / num_agents


if __name__ == "__main__":
    start = time.time()

    # Bins of no. of projects: 2 - 7, 8 - 13, 14 - 19 20 - 30, 31 - 6
    bins = {
        "2 - 7": {},
        "8 - 13": {},
        "14 - 19": {},
        "20 - 30": {},
        "31 - 65": {},
    }
    outcomes = {
        "Greedy": {},
        "MES Cost_Sat": {},
        "MES Cost_Sqrt_Sat": {},
        "MES Effort_Sat": {},
        "MES Cardinality_Sat": {},
    }

    for measure in outcomes:
        outcomes[measure] = {
            "projects": [],
            "avg_capped": [],
            "avg_l1": [],
        }
        
    for bin in bins:
        bins[bin] = outcomes.copy()

    for path in paths:
        # path = "2024-03-23_10-28-29_pabulib/netherlands_amsterdam_252_.pb"  # set this variable
        instance, profile = parse_pabulib(path)

        # Greedy
        outcomes["Greedy"]["projects"].append(
            perform_election(path, greedy_utilitarian_welfare, "Greedy", Cost_Sat)
        )

        # MES Cost_Sat
        outcomes["MES Cost_Sat"]["projects"].append(
            perform_election(path, method_of_equal_shares, "MES Cost_Sat", Cost_Sat)
        )

        # MES Cost_Sqrt_Sat
        outcomes["MES Cost_Sqrt_Sat"]["projects"].append(
            perform_election(
                path, method_of_equal_shares, "MES Cost_Sqrt_Sat", Cost_Sqrt_Sat
            )
        )

        # MES Effort_Sat
        # outcomes["MES Effort_Sat"]["outcome"].append(
        #     perform_election(
        #         path, method_of_equal_shares, "MES Effort_Sat", Effort_Sat
        #     )
        # )

        # MES Cardinality_Sat
        outcomes["MES Cardinality_Sat"]["projects"].append(
            perform_election(
                path, method_of_equal_shares, "MES Cardinality_Sat", Cardinality_Sat
            )
        )

        # Add shares and fair shares to the outcomes, as well as project ranges
        for measure in outcomes:
            try:
                outcome = outcomes[measure]["projects"][-1]
            except IndexError:
                print(f"---- ! Skipping {measure} ----")
                continue

            shares, fair_shares = get_shares(outcome, profile, instance)

            # Save the data to the right bin
            num_projects = len(outcome)
            if num_projects < 8:
                bin = "2 - 7"
            elif num_projects < 14:
                bin = "8 - 13"
            elif num_projects < 20:
                bin = "14 - 19"
            elif num_projects < 31:
                bin = "20 - 30"
            else:
                bin = "31 - 65"

            bins[bin][measure]["projects"].append(outcome)
            bins[bin][measure]["avg_capped"].append(
                get_average_capped_fair_share_ratio(shares, fair_shares)
            )
            bins[bin][measure]["avg_l1"].append(
                get_average_l1_distance(shares, fair_shares)
            )

    # Visualize the data
    # print(outcomes)           

    for name in ["avg_capped", "avg_l1"]:
        visualize_data(bins, outcomes, name)

    end = time.time()
