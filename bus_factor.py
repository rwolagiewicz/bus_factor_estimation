#!/usr/bin/env python3

import argparse
from bus_factor_estimator import BusFactorEstimator

parser = argparse.ArgumentParser()
parser.add_argument('--language', required=True)
parser.add_argument('--project_count', required=True, type=int)
parser.add_argument('--sort', default='stars')
parser.add_argument('--sorting_order', default='desc')

args = parser.parse_args()

estimator = BusFactorEstimator(args.language, args.project_count, args.sort, args.sorting_order)
repositories = estimator.bus_factor_repositories()
for repository in repositories:
    repository['percentage'] = f"{repository['percentage']:.2f}"
    project, user, percentage = [f'{key}: {val}' for key, val in repository.items()]
    print(f'  {project: <30} {user: <30} {percentage: <30}')
