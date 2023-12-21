import os
from tqdm import tqdm
import pandas as pd

from semanticlayertools.metric.prune import PruneNetwork

def prune(
    modelparameters: dict,
    network: tuple,
    columns: list,
    iterations=10,
    delAmounts=(0.1, 0.25, 0.5, 0.75, 0.9),
    delTypes=("degree", "unif")
):
    """Generate pruned networks from input.
    
    Assumes existence of columns "sender", "receiver", and "step".
    """
    runDf = pd.DataFrame(network, columns = columns)
    pruning = PruneNetwork(runDf)
    result = pruning.deleteFromNetwork(
        iterations=iterations,
        delAmounts=delAmounts,
        delTypes=delTypes
    )
    result = result.assign(**modelparameters)
    return result
    