import random
import uuid
from pathlib import Path
from datetime import datetime

import pandas as pd
from convert2geojson import Convert2GeoJson


def createData(population, outputfolder, datafolder=Path(__file__).parent.parent.resolve()):
    """Create random coordinates of historically motivated choices.
    Each coordinate additionally gets a random topic consisting of
    three numbers between 0 and 1.
    """

    initial_population_choices = pd.read_csv(
        Path(datafolder, "data/relPop_plosOne.csv")
    )

    loc_probabilities = []
    loc_values = []
    for idx, row in initial_population_choices.iterrows():
        loc_probabilities.append(row["relPop"])
        loc_values.append(
            (row["longitude"], row["latitude"])
        )

    coordinates = random.choices(
        loc_values,
        loc_probabilities,
        k=population
    )

    data = pd.DataFrame(
        coordinates,
        columns=["longitude", "latitude"]
    )

    data.insert(
        0,
        'unique_id',
        [
            "P" + str(x) for x in list(range(population))
        ]
    )
    convert = Convert2GeoJson(
        data,
        properties=["unique_id"]
    )
    convert.convert()
    # Take note of initial conditions creation time
    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y-%H_%M_%S")
    
    # Prevent reuse of initial condition in parallel thread
    uid = uuid.uuid4()
    filename = Path(outputfolder, f"initCond_pop_{population}_datetime_{date_time}_fileid_{uid}.geojson")

    convert.save(
        filename
    )
    return filename, data, True
