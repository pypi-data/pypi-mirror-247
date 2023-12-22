from logging import Logger
from multiprocessing import Pool
from os import getpid
from typing import Any, Callable, Iterable, ParamSpec, TypeVar

P = ParamSpec("P")
OType = TypeVar("OType")


def logged_child_process(
    func: Callable[P, OType], input_dict: dict[str, Any], logger: Logger
) -> OType:
    # Use the parent logger and create a child logger with the process ID
    child_logger = logger.getChild(str(getpid()))
    return func(logger=child_logger, **input_dict)


def run_parallel(
    func: Callable[P, OType],
    inputs: Iterable[dict[str, Any]],
    n_threads: int,
    logger: Logger,
) -> Iterable[OType]:
    pool = Pool(processes=n_threads)

    results = [
        pool.apply_async(
            logged_child_process,
            kwds={"func": func, "input_dict": input_dict, "logger": logger},
        )
        for input_dict in inputs
    ]

    pool.close()
    pool.join()
    logger.info("Ran all child processes")

    return tuple(result.get() for result in results)
