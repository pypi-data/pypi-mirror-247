import argparse
import os
import sys
from typing import Any, cast

import yaml

from . import logger
from .loading import load_repr1, parse_yaml_value
from .nameddps import NamedDP
from .primitivedps import PrimitiveDP
from .mcdp_solution_interface import MCDPSolverInterface
from .utils import import_from_string

__all__ = [
    "solve_mcdp_main",
]


def solve_mcdp_main() -> None:
    queries = ["FixFunMinRes", "FixResMaxFun"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model source (file or URL)", required=True)
    parser.add_argument("--query", help="query", default="FixFunMinRes", required=False)
    parser.add_argument("--data", help="data (YAML Format)", required=True)
    parser.add_argument("--solver", help="Model source (file or URL)", required=True)

    args = parser.parse_args()

    model_source = args.model
    try:
        solver0 = import_from_string(args.solver)
    except Exception as e:
        logger.error("Could not import solver %r", args.solver, exc_info=e)
        sys.exit(1)

    solver: MCDPSolverInterface

    if isinstance(solver0, MCDPSolverInterface):
        solver = solver0
    else:
        # noinspection PyCallingNonCallable
        solver = solver0()  # type: ignore
    if not isinstance(solver, MCDPSolverInterface):
        msg = f"Expected a MCDPSolverInterface, got {solver!r}"
        raise ValueError(msg)

    query = args.query

    if query not in queries:
        logger.error("Unknown query %r. Known: %r", query, queries)
        sys.exit(1)

    query_data = args.data
    if model_source.startswith("http"):
        import requests

        r = requests.get(model_source)
        if r.status_code != 200:
            logger.error("Cannot download model from %r", model_source)
            sys.exit(1)

        model_source = r.text
        data = yaml.load(model_source, Loader=yaml.SafeLoader)
    else:
        if os.path.exists(model_source):
            model_source = open(model_source).read()
            data = yaml.load(model_source, Loader=yaml.SafeLoader)
        else:
            logger.error("Cannot open file: %r", model_source)
            sys.exit(1)

    model: NamedDP[Any, Any] = load_repr1(data, NamedDP)
    if not isinstance(model, NamedDP):  # type: ignore
        if isinstance(model, PrimitiveDP):
            msg = f"Expected a NamedDP, got a PrimitiveDP. Did you mean to use 'act4e-mcdp-solve-dp'?"
            raise ValueError(msg)

        msg = f"Expected a NamedDP, got {model!r}"
        raise ValueError(msg)
    logger.info("model: %s", model)

    yaml_query0 = yaml.load(query_data, Loader=yaml.SafeLoader)
    if not isinstance(yaml_query0, dict):
        raise ValueError(f"Expected dict, got {yaml_query0!r}")
    yaml_query = cast(dict[str, Any], yaml_query0)

    if query == "FixFunMinRes":
        found = set(yaml_query)
        expected = set(model.functionalities)
        if found != expected:
            msg = f"Expected {expected}, got {found}"
            raise ValueError(msg)

        value = {}
        for k, v in model.functionalities.items():
            value[k] = parse_yaml_value(v, yaml_query[k])

        logger.info("query: %s", value)

        solution = solver.solve_mcdp_FixFunMinRes(model, value)

        logger.info("solution: %s", solution)

    elif query == "FixResMaxFun":
        found = set(yaml_query)
        expected = set(model.resources)
        if found != expected:
            msg = f"Expected {expected}, got {found}"
            raise ValueError(msg)

        value = {}
        for k, v in model.resources.items():
            value[k] = parse_yaml_value(v, yaml_query[k])

        logger.info("query: %s", value)

        solution = solver.solve_mcdp_FixFunMinRes(model, value)

        logger.info("solution: %s", solution)

    else:
        raise ValueError(f"Unknown query {query}")
