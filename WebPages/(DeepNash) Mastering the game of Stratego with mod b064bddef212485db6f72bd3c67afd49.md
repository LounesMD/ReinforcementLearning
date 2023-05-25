# (DeepNash) Mastering the game of Stratego with model-free multiagent reinforcement learning

Auteur: DeepMind
Lien: https://arxiv.org/pdf/2206.15378.pdf
Statut: En cours
Type: Article

# (DeepNash) ****Mastering the game of Stratego with model-free multiagent reinforcement learning****

![Untitled]((DeepNash)%20Mastering%20the%20game%20of%20Stratego%20with%20mod%20b064bddef212485db6f72bd3c67afd49/Untitled.png)

## Introduction :

This paper is to introduice DeepNash, a new RL algorithm/agent that can works with an imperfect information environnement and a with a huge number of existing states.

Like the previous AlphaX algorithms, it learns by selfplay. However, unlike the AlphaX algorithms, it is not based on MCTS but on Regularized Nash Dynamics (R-NaD). The agent’s purpose is to learn an approximate Nash equilibrium through self-play so the agent will perform well, even against a worst case opponent. Designing a strategy to be robust in the worst case is typically a good choice to play well against humans in two-player zero-sum games, as a Nash equilibrium guarantees an unexploitable agent, and thus the best possible worst-case performance. And this justifies why DeepNash and not AlphaX.

## Main contribution :

The main contribution of DeepNash is the use of a loss whose minimization would converge to a Nash equilibrium without introducing prohibitive computational obstacles at large scale. For this purpose, they minimized the exploitability (known for quantity that measures the distance to a Nash equilibrium) by defining a learning update rule that induces a dynamical system for which there exists a so-called Lyapunov function.

Algorithm :

![Untitled]((DeepNash)%20Mastering%20the%20game%20of%20Stratego%20with%20mod%20b064bddef212485db6f72bd3c67afd49/Untitled%201.png)

The algorithm is easy to understand. At each iteration, the reward is updated, as described by the formula below, while guaranteeing to converge towards a nash equilibrium.

$$
Reward\ update : r^{i}(\pi^{i},\pi^{-i},a^{i},a^{-i}) = r^{i}(a^{i},a^{-i}) - \eta log(\frac{\pi^{i}(a^{i}) }{\pi_{reg}^{i}(a^{i})}) + \eta log(\frac{\pi^{-i}(a^{-i}) }{\pi_{reg}^{-i}(a^{-i})})
$$

$$
\eta > 0\ and\ i\in\{1,2\}
$$

### Steps :

1. Model Free RL algorithm (above)
2. fine-tuning of the learnt policy to reduce the residual probabilities of taking highly improbable actions
3. test-time post-processing to filter out low probability actions and clear mistakes

## Model / Observation:

![Untitled]((DeepNash)%20Mastering%20the%20game%20of%20Stratego%20with%20mod%20b064bddef212485db6f72bd3c67afd49/Untitled%202.png)

![Untitled]((DeepNash)%20Mastering%20the%20game%20of%20Stratego%20with%20mod%20b064bddef212485db6f72bd3c67afd49/Untitled%203.png)

## Question :

1. What is a “learning update” ? 
    1. It’s juste the update of the parameters
2. Each time they use post-processing to remove the less possible actions, illegal moves, etc. but how exactly do they do it ?