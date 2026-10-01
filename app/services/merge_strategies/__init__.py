from app.domain.models import MergeStrategy

from app.services.merge_strategies.rrf import RRFMergeStrategy
from app.services.merge_strategies.score_normalization import ScoreNormalizationMergeStrategy

def get_merge_strategy(merge_strategy: MergeStrategy):
    """
    Get the merge strategy class based on the strategy name.

    Args:
        strategy_name (str): The name of the merge strategy.

    Returns:
        Type[MergeStrategy]: The merge strategy class.

    Raises:
        ValueError: If the strategy name is not found.
    """

    strategies = {
        "score_normalization": ScoreNormalizationMergeStrategy,
        "rrf": RRFMergeStrategy,
    }

    if merge_strategy not in strategies:
        raise ValueError(f"Merge strategy '{merge_strategy}' not found.")

    return strategies[merge_strategy]
