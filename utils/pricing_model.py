A = 1.35
B = 0.11282


def price_model(lp: float) -> float:
    return (lp ** A) * B
