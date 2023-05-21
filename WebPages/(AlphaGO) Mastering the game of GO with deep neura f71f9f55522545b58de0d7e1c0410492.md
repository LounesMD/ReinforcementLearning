# (AlphaGO) Mastering the game of GO with deep neural networks and tree search

Auteur: DeepMind
Lien: https://sci-hub.hkvisa.net/10.1038/nature16961
Note sur 5: ⭐️⭐️⭐️
Statut: Terminé
Type: Article

# (AlphaGO) Mastering the game of GO with deep neural networks and tree search

![Untitled]((AlphaGO)%20Mastering%20the%20game%20of%20GO%20with%20deep%20neura%20f71f9f55522545b58de0d7e1c0410492/Untitled.png)

## Ideas:

Instead of searching the full tree, they truncate the tree and replace the subtree with its value. This achieves better performance due to computational savings.

### 3 policies:

- Rollout policy to simulate self-play rollouts during the MCTS process.
- SL Policy Network trained on expert moves to guide early MCTS stages. This policy predicts the next board state when building the tree.
- RL Policy Network is the trained policy that predicts the action to take depending on the state.

### 1 Value network:

- The value network (computed with the action of the RL policy) is also a deep learning model that computes the classic value function (v: state -> value).

### 1 Reward function:

- The reward is computed only at the end of the game (either winning or end of the simulation). The winner receives +1, and the loser receives -1.

## Training:

- Training is a mix between Rollout and Value network.

## Questions:

1. What is the representation of their model, and what is the input of their model? 
    1. One hot encoding with az simple representation of the board (cf methods)
2. With their asynchronous multi-threaded search algorithm, how does one CPU know what the other is doing?
3. How does one achieve the "Parallel Computation of Policy and Value Networks" since they are deep learning models?
4. What about illegal moves ? 
    1. There is a post-processing step which removes the illefal moves
5. If we use NN models, what is the loss ? (cross-entropy i guess)
    1. The same as AlphaGo Zero