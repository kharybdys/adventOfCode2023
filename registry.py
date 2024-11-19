import importlib
import pkgutil
from collections import defaultdict
from types import ModuleType

import advent
from utils import SolverFunction

_REGISTERED_SOLVERS: dict[str, dict[str, dict[str, SolverFunction]]] = defaultdict(lambda: defaultdict(dict))


def register_solver(year: str, key: str, variation: str):
    def _decorate(solver_func: SolverFunction):
        if _ := get_solver(year, key, variation):
            raise ValueError(f"Duplicate key triplet, cannot register: {year}, {key}, {variation} for {solver_func}")
        _REGISTERED_SOLVERS[year][key][variation] = solver_func
        return solver_func
    return _decorate


def get_solver(year: str, key: str, variation: str) -> SolverFunction:
    solver = _REGISTERED_SOLVERS.get(year, {}).get(key, {}).get(variation, None)
    return solver


def _import_submodules(package: str | ModuleType, recursive=True) -> dict[str, ModuleType]:
    """ Import all submodules of a module, recursively, including subpackages
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if recursive and is_pkg:
            results.update(_import_submodules(full_name))
    return results


def import_all_solvers():
    _import_submodules(advent)
