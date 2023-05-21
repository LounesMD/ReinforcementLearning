# (AlphaZero) Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm

Auteur: DeepMind
Lien: https://arxiv.org/pdf/1712.01815.pdf
Note sur 5: ⭐️⭐️⭐️
Statut: Terminé
Type: Article

# (AlphaZero) Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm

![Untitled]((AlphaZero)%20Mastering%20Chess%20and%20Shogi%20by%20Self-Play%206460966613664c28af351340322afdce/Untitled.png)

# Introduction:

The goal of this paper is to present a generalization of the AlphaGoZero algorithm. This generalization aims to not use handcrafted knowledge and domain-specific information, as was done in the previous paper.

Here, the goal is to train a function to predict action probabilities and scalar value, similar to the previous AlphaGoZero algorithm.

The selection of the action is based on the value of the new state, action probability, and visit count.

# Novelties:

The main novelty of the algorithm is its simplified version, which does not use handcrafted knowledge or domain-specific information, and only the rules are given to the model. Additionally, the number of simulations used is reduced from 1600 to 800.

In this paper, data augmentation is mentioned as a technique where winning policies are reused but with the symmetry of the board taken into consideration. However, this technique is not used in AlphaZero training (if equals to AlphaZero does not augment the training data and does not transform the board position during MCTS).

# Questions:

1. The paper mentions adding noise to the prior policy to ensure exploration, but it does not specify when, how, or how much noise is added.
2. The paper does not mention any handcrafted features.
3. The paper does not mention any pruning algorithm or threshold of probabilities.
4. The paper does not mention when the learning rate was dropped or what scheduler was used.