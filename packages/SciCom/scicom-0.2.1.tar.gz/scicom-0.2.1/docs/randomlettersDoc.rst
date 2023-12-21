Random letters documentation
============================

Variables and Scales
--------------------

Agent's variables
Each agent represents a scholar. They are heterogeneous and defined by a matrix of static and dynamic characteristics.
Among other traits, agents hold a geographical position and a vector of topics.

- Position [x, y]: Every agent has a time-varying position represented as a pair of x-y coordinates in a 2-D plane or map.
- Letters-sent [ai]: A vector where each element ai expresses the total number of letters sent from the scholar to agent i.
- Letters-received [aj ]: A vector where each element aj shows the total count of letters received from agent j
- Topics [ak]: A vector containing the interest of the agent among k topics.

Global variables
We position the agents in geographical space and give them topics.
So, beyond the agent's variables, we keep track of the global environment.

- Social Network [aij ]: A weighted directed graph measuring the number of letters sent from agent i to agent j
- Letters: A time-stamped ledger table that keeps track of every letter sent

Each entry includes information on senders and receivers, their locations, the topic of the letter, and the time.

Scheduling
----------

- Create N agents. Give them an initial position and a random topic of vectors.
- Start the simulation at time t = 0.
- At each step, the agents receive a list of neighbours within a threshold radius.
  We consider both social and spatial distance to make the list of neighbours.
- Each agent selects and writes a letter to one of their neighbours. 
  To pick the neighbour, we use a variation of the Polya Urn. We create a distribution of
  neighbours' ids based on their total letters received and past communication -
  both letters sent and received - with the focal agent. And we randomly pick
  one id from the distribution.
- After we match senders with potential receivers, we compare their topic interests. 
  We find the distance between their vector of topics. And if it falls within
  a predetermined threshold, we continue with the simulation.
- Every letter has at least one topic. And we repeat the urn process to select
  it. Thus we create a distribution of topics based on the intersection of interest
  between receiver and sender, and we randomly pick one.
- After selecting a receiver and topics, the agent can send their letters. And we
  need to update their global and agent variables.
- First, in the Letters table, we write the complete ”transaction” information.
  That is, we add a new line containing the ids of the sender and receiver, their
  respective locations, the topic, and the time.
- Then, we update the agents' vectors.
- Agents are updated sequentially and at random.
- A time-step is defined as the length of time it takes to update all agents
