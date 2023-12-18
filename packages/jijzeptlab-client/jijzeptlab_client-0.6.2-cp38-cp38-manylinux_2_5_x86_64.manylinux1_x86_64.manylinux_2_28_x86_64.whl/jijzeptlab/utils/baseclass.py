import abc

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

import jijmodeling as jm

from pydantic import BaseModel, ConfigDict


class Option(BaseModel):
    """Base class for option"""
    model_config = ConfigDict(extra="forbid", frozen=True)


class Result(ABC, metaclass=abc.ABCMeta):
    """Base class for storing result"""

    @abstractmethod
    def to_sample_set(self) -> jm.SampleSet:
        """Convert to SampleSet"""
        ...


class ResultWithDualVariables(Result, metaclass=abc.ABCMeta):
    """Base class for storing result with dual variables"""

    @abstractmethod
    def _get_dual_variables(self) -> Optional[Dict[str, Dict[Tuple[int], float]]]:
        """Converts the result to a dictionary."""
        pass


class StateModel(metaclass=abc.ABCMeta):
    """Base class for model which has the state"""

    @abstractmethod
    def reset(self, *args, **kwargs) -> Any:
        """Reset the state"""
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        """Update the state"""
        ...
