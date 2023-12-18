import typing as tp

from enum import Enum, auto

import jijmodeling as jm
import numpy as np

from google.protobuf.text_encoding import CUnescape

from jijzeptlab.exception import JijZeptLabDeserializeError


class JijZeptLabDataType(Enum):
    NDARRAY = auto()
    QUBO = auto()
    SAMPLESET = auto()
    SERIALIZABLEOBJECT = auto()


def deserialize_qubo(seri):
    """Deserializes QUBO.

    Args:
        seri (List[[index,...], [value,...]]): serialized QUBO
    Returns:
        dict[tuple[int, ...], float]: deserialized QUBO
    """
    qubo = {}
    for index, value in zip(seri[0], seri[1]):
        qubo[tuple(index)] = value

    return qubo


def recursive_deserialize(seri: tp.Any) -> tp.Any:
    """
    Function to restore JSON serializable result values.

    Args:
        seri (Any): JSON serializable result values.

    Returns:
        Any: Restored result values.

    Raises:
        JijZeptLabDeserializeError: If failed to restore result values.
    """
    if seri is None:
        return None
    elif isinstance(seri, (int, float, str, bool)):
        return seri
    elif isinstance(seri, dict):
        if len(seri) == 0:
            return seri
        elif "JijZeptLabDataType" in seri:
            if seri["JijZeptLabDataType"] == JijZeptLabDataType.QUBO.name:
                return deserialize_qubo(seri["data"])
            elif seri["JijZeptLabDataType"] == JijZeptLabDataType.NDARRAY.name:
                return np.array(seri["data"])
            elif seri["JijZeptLabDataType"] == JijZeptLabDataType.SAMPLESET.name:
                return jm.SampleSet.from_json(seri["data"])
            elif seri["JijZeptLabDataType"] == JijZeptLabDataType.SERIALIZABLEOBJECT.name:
                return jm.from_protobuf(CUnescape(seri["data"]))
            else:
                raise JijZeptLabDeserializeError(
                    f"Failed to deserialize: {str(seri)}"
                )
        else:
            return {k: recursive_deserialize(v) for k, v in seri.items()}
    elif isinstance(seri, (list, tuple)):
        return [recursive_deserialize(elem) for elem in seri]
    else:
        raise JijZeptLabDeserializeError(
            f"Failed to deserialize: {str(seri)}"
        )