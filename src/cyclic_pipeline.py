from email import header
from job_interface import JobInterface
from typing import TypeVar, Callable
from copy import deepcopy
import time

A = TypeVar("A")  # the variable name must coincide with the string

# cyclic pipeline: stops when stop_condition is verified or when the input is unchanged after an iteration


class CyclicPipeline():


    def __init__(self, jobs: list[JobInterface] = [], max_iterations = 1000) -> None:
        self.jobs: list = jobs
        self.head: int = 0 if len(jobs) > 0 else None
        self.max_iterations = max_iterations

    def add_job(self, job: JobInterface) -> None:
        self.jobs.append(job)
        if self.head < 0:
            self.head = 0

    def start(self, input: A, stop_condition: Callable):
        last_job_index = len(self.jobs)-1

        iteration_input = None
        num_iterations = 0

        while num_iterations < self.max_iterations:
            if self.head == 0:
                iteration_input = deepcopy(input)

            output = self._run_next_job(input)
            num_iterations += 1

            # compare if input has changed after a complete pipeline iteration
            if self.head == last_job_index and iteration_input == output:
                print("- CyclicPipeline: input unchanged after completed iteration")
                print("#Iterations: " + str(num_iterations))
                return output  # input unchanged after iteration

            if stop_condition(output):
                print("- CyclicPipeline: stop condition verified")
                print("#Iterations: " + str(num_iterations))
                return output  # stop condition verified

            self._increment_head()

    # TODO: print -> abstract methods with custom messages

    def _run_next_job(self, input: A) -> A:
        output = self.jobs[self.head].run(input)
        return output

    def _increment_head(self):
        self.head = (self.head+1) % len(self.jobs)
