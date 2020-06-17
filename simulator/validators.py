def require_int_inclusive_range(subject: int, lower_bound: int, upper_bound: int, msg: str):
    if not (lower_bound <= subject <= upper_bound):
        raise ValueError(
            f"Value, {subject} must be between {lower_bound} and {upper_bound}. Additional details: {msg}"
        )
