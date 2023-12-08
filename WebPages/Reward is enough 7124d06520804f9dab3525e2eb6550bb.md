# Reward is enough

Type: Paper
Link: https://www.sciencedirect.com/science/article/pii/S0004370221000862
Date: 2021/10/01

![Untitled](Reward%20is%20enough%207124d06520804f9dab3525e2eb6550bb/Untitled.png)

# Reward is enough

**Statement:** Intelligence can be conceptualized as serving the purpose of maximizing reward. This maximization encompasses all goals of intelligence. For example, a squirrel, to maximize its satiation (i.e., to reduce hunger), must identify and understand food. Moreover, having a composite reward system, rather than individual rewards, renders an agent more rational and deepens its understanding by explaining the *why* of an ability, not just the *what*.

The authors argue that the most effective method for maximizing reward is learning through trial and error. Placed in a rich environment, this approach facilitates the emergence of sophisticated general intelligence. They reference AZ, noting that a reward system of 0 during gameplay, +1 for winning, and -1 for losing, enabled AZ to learn complex tactics.

**Knowledge and Learning:**

- **Definition of Knowledge:** Information internal to the agent.
- **Innate Knowledge:** Some knowledge, not derived from environmental experiences, is immediately accessible in new situations. This concept is particularly relevant in RL, as RL can allows for repeated exposure to specific scenarios to understand/learn innate knowledge, although this is not always applicable.
- **Learned Knowledge:** The nature of the environment dictates the need for specific skills. This seems akin to Ilya Sutskever's notion of LMs finetuning (see: [Ilya Sutskever Discussion](https://github.com/LounesMD/ReinforcementLearning/blob/main/WebPages/Discussion%20Ilya%20x%20Jensen%2073db3112e6e34b4896dc9b97cc9ae961.md)).

**Perception:**
The authors also discuss the enhancement of perception through unified perceptual abilities in addressing supervised learning problems.

**Social Intelligence:**

- **Definition:** The capability to effectively understand and interact with other agents, resembling an equilibrium solution in a multi-agent game.

This is advantageous when agents are rational, as they have no incentive to deviate. An example of learning a Nash equilibrium with RL is detailed in [Mastering Stratego](https://github.com/LounesMD/ReinforcementLearning/blob/main/WebPages/(DeepNash)%20Mastering%20the%20game%20of%20Stratego%20with%20mod%20b064bddef212485db6f72bd3c67afd49.md). Agents must anticipate others' behaviour even when they are not predictable/adaptative, necessitating robustness, especially when multiple RL agents seek to maximise their rewards, often requiring stochastic (mixed strategy) approaches.

**Language/Imitation/General Intelligence:**
Further arguments support the idea of reward maximization.

**Constructing Such an Agent:**
The process involves utilizing reward maximization and learning through trial and error within environment(s?).

**Discussion:**

Which reward signal: ****It doesn’t really matter as the learning quality should be robust to to the nature of the reward.

Online tends to be better to learn a more useful behaviour than offline.

## References:

1. G. Debreu, "Representation of a Preference Ordering by a Numerical Function," 1954.
2. J. Perolat et al., "Mastering the Game of Stratego with Model-Free Multiagent Reinforcement Learning," 2022.