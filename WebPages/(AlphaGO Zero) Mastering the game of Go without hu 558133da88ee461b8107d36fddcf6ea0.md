# (AlphaGO Zero) Mastering the game of Go without
human knowledge

Auteur: DeepMind
Lien: https://sci-hub.ru/10.1038/nature24270
Note sur 5: ⭐️⭐️⭐️⭐️
Statut: Terminé
Type: Article

# (AlphaGO Zero) Mastering the game of Go without human knowledge

![Untitled]((AlphaGO%20Zero)%20Mastering%20the%20game%20of%20Go%20without%20hu%20558133da88ee461b8107d36fddcf6ea0/Untitled.png)

## Introduction / Contribution:

This model is a self-play reinforcement learning algorithm. It uses only one neural network model (instead of four), and the board (black and white pawns) and its history are the only inputs. The history captures the velocity/strategy of the game. Additionally, there are no Monte Carlo rollouts because the model uses only the prediction made by the above model.

## Model:

The main contribution and difference from the previous paper is that now only one model is used. This model predicts, from the current state of the board and the history, a probability map for actions and a value. The value aims to know the relevance (i.e., chance of winning) of the current state. So, this model serves as both the value function and the policy function.

## Loss of the model:

The loss function of the model is mean-squared error plus cross-entropy.

## Training:

The model was trained using 4.9 million generated games (were all played/used?), and 1,600 simulations were run for each Monte Carlo Tree Search (MCTS) (0.4 seconds). The model was updated with 700,000 mini-batches of 2,048 positions. It is not clear whether the model was trained or not.