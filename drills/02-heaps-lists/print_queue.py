"""Drill 02-7, debugging: the print queue.

This program is finished, and it has a fault. Find it, say in one sentence why it is a fault, and
fix it. Change as little as you can. Time box: 20 minutes.

The office printer takes jobs in priority order: a lower number prints first. Jobs with the same
priority print in the order they were sent. run_order returns the names of the jobs in the order
the printer prints them.

    jobs = [Job("report", 2), Job("photo", 1), Job("letter", 2)]
    run_order(jobs)  ->  ["photo", "report", "letter"]

Three tests in test_print_queue.py fail. Read the first message before you read the code.
"""

import heapq
from dataclasses import dataclass


@dataclass
class Job:
    name: str
    priority: int  # a lower number prints first


def run_order(jobs: list[Job]) -> list[str]:
    waiting = []
    for job in jobs:
        heapq.heappush(waiting, (job.priority, job))
    order = []
    while waiting:
        _, job = heapq.heappop(waiting)
        order.append(job.name)
    return order
