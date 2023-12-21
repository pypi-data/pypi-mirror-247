
import random
from pathlib import Path
from statistics import mean
from tqdm import tqdm

import mesa
import networkx as nx
import mesa_geo as mg

from scicom.utilities.statistics import prune
from scicom.historicalletters.utils import createData

from scicom.historicalletters.agents import SenderAgent, RegionAgent
from scicom.historicalletters.space import Nuts2Eu


def getPrunedLedger(model):
    """Model reporter for simulation of archiving.
    
    Returns statistics of ledger network of model run
    and various iterations of statistics of pruned networks. 
    """
    # TODO: Add all model params
    if model.runPruning is True:
        ledgerColumns= ['sender', 'receiver', 'sender_location', 'receiver_location', 'topic', 'step']
        modelparams = {
            "population": model.population,
            "moveRange": model.moveRange,
            "letterRange": model.letterRange,
            "useActivation": model.useActivation,
            "useSocialNetwork": model.useSocialNetwork,
        }
        result = prune(
            modelparameters=modelparams,
            network=model.letterLedger,
            columns=ledgerColumns
        )
    else:
        result = model.letterLedger
    return result


class HistoricalLetters(mesa.Model):
    """A letter sending model with historical informed initital positions.
    
    Each agent has an initial topic vector, expressed as a RGB value. The 
    initial positions of the agents is based on a weighted random draw
    based on data from [1]
    
    Each step, agents generate two neighbourhoods for sending letters and 
    potential targets to move towards. The probability to send letters is 
    a self-reinforcing process. During each sending the internal topic of 
    the sender is updated as a random rotation towards the receivers topic.

    [1] J. Lobo et al, Population-Area Relationship for Medieval European Cities,
        PLoS ONE 11(10): e0162678.
    """
    def __init__(
        self,
        population=100,
        moveRange=0.5,
        letterRange=0.5,
        similarityThreshold=0.5,
        updateTopic=0.1,
        useActivation=False,
        useSocialNetwork=False,
        longRangeNetworkFactor=0.3,
        shortRangeNetworkFactor=0.8,
        runPruning=False,
        datafolder: str = Path(__file__).parent.parent.resolve(),
        tempfolder: str = "./",
        debug=False
    ):
        super().__init__()

        self.schedule = mesa.time.RandomActivation(self)
        self.space = Nuts2Eu()
        self.population = population
        self.letterLedger = []
        # Initialize social network
        self.useSocialNetwork = useSocialNetwork
        self.G = nx.DiGraph()
        self.longRangeNetworkFactor = longRangeNetworkFactor
        self.shortRangeNetworkFactor = shortRangeNetworkFactor
        # 
        self.moveRange = moveRange
        self.letterRange = letterRange
        self.useActivation = useActivation
        self.runPruning = runPruning
        self.movements = 0
        self.updatedTopic = 0
        self.personRegionMap = {}
        self.datafolder = datafolder
        self.tempfolder = tempfolder
        self.debug = debug

        initSenderFile, _, _ = createData(
            population,
            outputfolder=self.tempfolder,
            datafolder=self.datafolder
        )

        self.factors = dict(
            updateTopic=updateTopic,
            similarityThreshold=similarityThreshold,
            moveRange=moveRange,
            letterRange=letterRange,
        )

        # Set up the grid with patches for every NUTS region
        ac = mg.AgentCreator(RegionAgent, model=self)
        self.regions = ac.from_file(
            Path(self.datafolder, "data/nuts_rg_60M_2013_lvl_2.geojson"),
            unique_id="NUTS_ID"
        )
        self.space.add_regions(self.regions)

        # Set up agent creator for senders
        ac_senders = mg.AgentCreator(
            SenderAgent,
            model=self,
            agent_kwargs=self.factors
        )

        # Create agents based on random coordinates generated 
        # in the createData step above, see util.py file.
        senders = ac_senders.from_file(
            initSenderFile,
            unique_id="unique_id"
        )

        Path.unlink(initSenderFile)

        # Create random set of initial topic vectors.
        topics = [
            tuple(
                [random.random() for x in range(3)]
            ) for x in range(self.population)
        ]

        # Attach topic and activationWeight to each agent,
        # connect to social network graph.
        for idx, sender in enumerate(senders):
            self.G.add_node(
                sender.unique_id,
                numLettersSend=0,
                numLettersReceived=0    
            )
            sender.topicVec = topics[idx]
            if useActivation is True:
                sender.activationWeight = random.random()

        for agent in senders:
            self.space.add_sender(agent)
            self.schedule.add(agent)

        # Add graph to network grid for potential visualization.
        self.grid = mesa.space.NetworkGrid(self.G)

        # Calculate mean of mean distances for each agent. 
        # This is used as a measure for the range of exchanges.
        borderAgent = self.population - 1
        agentsp = self.space.get_agents_as_GeoDataFrame()[-borderAgent:]
        distances = []
        for source in agentsp.geometry.values:
            agentdistances = [source.distance(x) for x in agentsp.geometry.values]
            meanDist = mean(agentdistances)
            distances.append(meanDist)
        self.meandistance = mean(distances)

        # Create social network
        if useSocialNetwork is True:
            for agent in self.schedule.agents:
                if isinstance(agent, SenderAgent):
                    self._createSocialEdges(agent, self.G)

        # TODO: What comparitive values are useful for visualizations?
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Ledger": getPrunedLedger
            },
        )

    def _createSocialEdges(self, agent, graph):
        closerange = [x for x in self.space.get_neighbors_within_distance(
            agent,
            distance=self.moveRange * self.meandistance,
            center=False
        ) if isinstance(x, SenderAgent)]
        for neighbor in closerange:
            if neighbor.unique_id != agent.unique_id:
                connect = random.choices(
                    population=[True, False],
                    weights=[self.shortRangeNetworkFactor, 1 - self.shortRangeNetworkFactor],
                    k=1
                )
                if connect[0] is True:
                    graph.add_edge(agent.unique_id, neighbor.unique_id)
                    graph.add_edge(neighbor.unique_id, agent.unique_id)
        longrange = [x for x in self.schedule.agents if x not in closerange and isinstance(x, SenderAgent)]
        for neighbor in longrange:
            if neighbor.unique_id != agent.unique_id:
                connect = random.choices(
                    population=[True, False],
                    weights=[self.longRangeNetworkFactor, 1 - self.longRangeNetworkFactor],
                    k=1
                )
                if connect[0] is True:
                    graph.add_edge(agent.unique_id, neighbor.unique_id)
                    graph.add_edge(neighbor.unique_id, agent.unique_id)

    def step(self):
        self.schedule.step()
        #if self.useSocialNetwork is True:
        #    nx.spring_layout(self.G)
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        if self.debug is True:
            for _ in tqdm(range(n)):
                self.step()
        else:
            for _ in range(n):
                self.step()
