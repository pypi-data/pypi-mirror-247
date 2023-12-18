class JijZeptLabError(Exception):
    """Base class for exceptions in jijzeptlab."""

    pass


class JijZeptLabSolverError(JijZeptLabError):
    """Exception raised for errors in the solver."""

    pass


class JijZeptLabDeserializeError(JijZeptLabError):
    """Exception raised for errors in recursive_deserialize."""

    pass