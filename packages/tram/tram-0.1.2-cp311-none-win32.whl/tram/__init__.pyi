def linear_assign(
    from_: list[int],
    to_: list[int],
    arc_freqs: list[float],
    costs: list[float],
    demands: list[float],
    dsts: list[int],
) -> tuple[list[float], float]: ...
def mat_linear_assign(
    alignments: list[list[int]],
    freqs: list[float],
    travel_time_mat: list[list[float]],
    demands_mat: list[list[float]],
) -> tuple[list[list[float]], float]: ...
def linear_congested_assign(
    from_: list[int],
    to_: list[int],
    arc_freqs: list[float],
    costs: list[float],
    demands: list[float],
    dsts: list[int],
    capacity: float,
    average_decay_factor: float = 0.01,
    beta: float = 0.2,
    tol: float = 0.001,
    max_iters: int = 1000,
) -> tuple[list[float], float]: ...
def mat_linear_congested_assign(
    alignments: list[list[int]],
    freqs: list[float],
    travel_time_mat: list[list[float]],
    demands_mat: list[list[float]],
    capacity: float,
    average_decay_factor: float = 0.01,
    beta: float = 0.2,
    tol: float = 0.001,
    max_iters: int = 1000,
) -> tuple[list[list[float]], float]: ...
