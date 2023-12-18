from __future__ import annotations

from typing import Dict, List, Literal, Optional, Union

import jijmodeling as jm
import jijmodeling_transpiler as jmt
import mip

from jijzeptlab.compile import CompiledInstance
from jijzeptlab.utils.baseclass import Option, ResultWithDualVariables
from pydantic import Field


class MipModelOption(Option):
    """Option for MipModel

    Attributes:
        ignore_constraint_names (List[str]): constraint names to be ignored
        relaxed_variable_names (List[str]): variable names to be relaxed to continuous ones
        relax_all_variables (bool): if True, all variables are relaxed to continuous ones
        ignore_constraint_indices (Dict[str, List[List[int]]]): constraint indices to be ignored
        solver_name (Optional[Literal["CBC", "GUROBI"]]): Solver name to select. Defaults to None.
        emphasis (Optional[Literal["DEFAULT", "FEASIBILITY", "OPTIMALITY"]]): Emphasis. Defaults to None.
        infeas_tol (Optional[float]): Infeasibility tolerance. Defaults to None.
        integer_tol (Optional[float]): Integer tolerance. Defaults to None.
        max_mip_gap (Optional[float]): Maximum MIP gap. Defaults to None.
        max_mip_gap_abs (Optional[float]): Maximum MIP gap absolute. Defaults to None.
    """

    ignore_constraint_names: List[str] = Field(default_factory=list)
    relaxed_variable_names: List[str] = Field(default_factory=list)
    relax_all_variables: bool = False
    ignore_constraint_indices: Dict[str, List[List[int]]] = Field(default_factory=dict)
    solver_name: Literal["CBC", "GUROBI"] = "CBC"
    emphasis: Optional[Literal["DEFAULT", "FEASIBILITY", "OPTIMALITY"]] = None
    infeas_tol: Optional[float] = None
    integer_tol: Optional[float] = None
    max_mip_gap: Optional[float] = None
    max_mip_gap_abs: Optional[float] = None


class MipSolveOption(Option):
    """Options to solve mip problem

    Attributs:
        max_seconds (Union[int, float]): Maximum number of nodes. Defaults to mip.INF.
        max_nodes (int): Maximum number of solutions. Defaults to mip.INT_MAX.
        max_solutions (int): Maximum number of solutions. Defaults to mip.INT_MAX.
        max_seconds_same_incumbent (Union[int, float]): Maximum time in seconds that the search can go on
            if a feasible solution is available and it is not being improved. Defaults to mip.INF.
        max_nodes_same_incumbent (int): Maximum number of nodes that the search can go on
            if a feasible solution is available and it is not being improved. Defaults to mip.INT_MAX
        relax (bool): if true only the linear programming relaxation will be solved,
            i.e. integrality constraints will be temporarily discarded. Defaults to False
    """

    max_seconds: Union[int, float] = mip.INF
    max_nodes: int = mip.INT_MAX
    max_solutions: int = mip.INT_MAX
    max_seconds_same_incumbent: Union[int, float] = mip.INF
    max_nodes_same_incumbent: int = mip.INT_MAX
    relax: bool = False


class MipModel:
    """MIP model class for JijZeptLab"""

    def __init__(self, mip_model, mip_decoder) -> None:
        self.mip_model = mip_model
        self._mip_decoder = mip_decoder


class MipResult(ResultWithDualVariables):
    """Result class for MIP solver"""

    def __init__(self, mip_model: mip.Model, mip_decoder, status = None) -> None:
        self.mip_model = mip_model
        self._mip_decoder = mip_decoder
        self._status = status

    def to_sample_set(self) -> jm.SampleSet | None:
        """Convert to SampleSet"""
        if self._status is None:
            return None
        decoded_result = self._mip_decoder.decode_from_mip(self._status, self.mip_model)
        return decoded_result

    def _get_dual_variables(self) -> dict[str, dict[tuple[int], float]] | None:
        """Returns the dual variables of the constraints.
        If the result is trivially infeasible, None is returned.

        Returns:
            dict[str, dict[tuple[int], float]] | None: The dual variables of the constraints.
        """
        raise NotImplementedError("_get_dual_variables is not implemented")


def create_model(
    compiled_instance: CompiledInstance, option: Optional[MipModelOption] = None
) -> MipModel:
    """Create MIP model from compiled instance

    Args:
        compiled_instance (CompiledInstance): compiled instance
        option (Optional[MipModelOption]): option for MIP model

    Returns:
        MipModel: MIP model

    Examples:
        ```python
        import jijzeptlab as jzl
        import jijzeptlab.solver.mip as mip

        compiled_model = jzl.compile_model(problem, jzl.InstanceData.from_dict(instance_data))
        # initialize MIP instance
        mip_model = mip.create_model(compiled_model)
        # solve
        mip_result = mip.solve(mip_model)
        # convert the solution to `jm.SampleSet`。
        final_solution = mip_result.to_sample_set()
        ```
    """

    if option is None:
        option = MipModelOption()

    jmt_instance = compiled_instance._instance
    if option.relax_all_variables:
        relax_all_vars = list(jmt_instance.var_map.var_map.keys())
    else:
        relax_all_vars = []
    mip_builder = jmt.core.mip.transpile_to_mip(
        compiled_instance._instance, relax_list=relax_all_vars
    )
    pymip_model = mip_builder.get_model()
    return MipModel(pymip_model, mip_builder)


def solve(mip_model: MipModel) -> MipResult:
    status = mip_model.mip_model.optimize()
    return MipResult(mip_model.mip_model, mip_model._mip_decoder, status)
