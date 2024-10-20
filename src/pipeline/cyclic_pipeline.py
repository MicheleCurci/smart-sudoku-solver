from src.pipeline.abstract_job import AbstractJob
from typing import TypeVar, Callable
from copy import deepcopy

A = TypeVar("A")

# cyclic pipeline stops if:
#   - stop_condition is verified
#   - input is unchanged after an iteration


class CyclicPipeline:
    def __init__(self, jobs: list[AbstractJob] = [], max_iterations=1000) -> None:
        self.jobs: list[AbstractJob] = jobs
        self.head: int = 0 if len(jobs) > 0 else -1
        self.max_iterations = max_iterations

    def add_job(self, job: AbstractJob) -> None:
        self.jobs.append(job)
        self.head = max(self.head, 0)

    def start(self, input: A, stop_condition: Callable) -> A:
        last_job_index = len(self.jobs) - 1
        iteration_input = None
        num_iterations = 0
        output = input

        while num_iterations < self.max_iterations:
            if self.head == 0:
                iteration_input = deepcopy(input)

            output: A = self._run_next_job(input)
            num_iterations += 1

            # Compare if input has changed after a complete pipeline iteration
            # Pipeline is stopped if input is unchanged after iteration
            if self.head == last_job_index and iteration_input == output:
                print(
                    f"> CyclicPipeline: input unchanged after completed iteration. {str(num_iterations)} iterations."
                )
                break

            if stop_condition(output):
                print(
                    f"> CyclicPipeline: stop condition verified. {str(num_iterations)} iterations."
                )
                break

            self._increment_head()

        if num_iterations == self.max_iterations:
            raise Exception("Reached the maximum limit of pipeline iterations.")

        return output

    # TODO: print -> abstract methods with custom messages

    def _run_next_job(self, input: A) -> A:
        output = self.jobs[self.head].run(input)
        return output

    def _increment_head(self):
        self.head = (self.head + 1) % len(self.jobs)
