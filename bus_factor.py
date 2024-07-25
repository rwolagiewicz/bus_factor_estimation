#!/usr/bin/env python3
import argparse

from bus_factor_estimator import BusFactorEstimator


def _get_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True)
    parser.add_argument("--project_count", required=True, type=int)
    parser.add_argument("--sort", default="stars")
    parser.add_argument("--sorting_order", default="desc")
    return parser.parse_args()


def run_bus_factor_estimator(args):
    estimator = BusFactorEstimator(
        args.language, args.project_count, args.sort, args.sorting_order
    )
    repositories = estimator.get_bus_factor_repositories()
    for repository in sorted(repositories, key=lambda x: x["percentage"], reverse=True):
        repository["percentage"] = f"{repository['percentage']:.2f}"
        project, user, percentage = [f"{key}: {val}" for key, val in repository.items()]
        print(f"  {project: <30} {user: <30} {percentage: <30}")


if __name__ == "__main__":
    args = _get_cmd_args()
    run_bus_factor_estimator(args)
