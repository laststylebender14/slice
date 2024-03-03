from random import sample

from core.storage.node import Node
from core.logger.logger import get_logger


def expire_sample(dictionary: dict[str, Node]) -> float:
    """Picks a random sample of keys from a dictionary and calculates the expiration rate.

    Args:
        dictionary: The dictionary containing Nodes as values.

    Returns:
        float: The ratio of deleted keys to the sample size (0 if no keys to sample).
    """

    sample_key_size = 20

    # Check if there are enough keys for sampling
    if len(dictionary) < sample_key_size:
        return 0.0

    # Sample a random set of keys
    sample_keys = sample(list(dictionary.keys()), sample_key_size)

    # Track deleted keys and iterate over the sample
    delete_key_cnt = 0
    for key in sample_keys:
        val = dictionary.get(key)  # Use get to avoid potential KeyError
        if val and val.is_node_expired():
            delete_key_cnt += 1
            del dictionary[key]

    # Calculate and return the expiration rate
    return delete_key_cnt / sample_key_size


def delete_expired_keys(storage):
    while True:
        deletion_to_sample_ratio = expire_sample(storage)

        get_logger().info(
            f"eviction ratio : {deletion_to_sample_ratio}",
        )
        if deletion_to_sample_ratio < 0.25:
            break
