# (AlphaTensor) Discovering faster matrix multiplication algorithms with reinforcement learning

Auteur: DeepMind
Lien: https://www.nature.com/articles/s41586-022-05172-4
Note sur 5: ⭐️⭐️⭐️⭐️ 
Statut: Terminé
Type: Article

# (AlphaTensor) Discovering faster matrix multiplication algorithms with reinforcement learning

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled.png)

## Introduction :

The goal of AlphaTensor was to use AlphaZero to find algorithms, within a finite factor space, for discovering efficient and provably correct algorithms for the multiplication of arbitrary matrices.

Instead of trying to characterize the complexity of the asymptotically optimal algorithm, they focused on practical matrix multiplication algorithms, which correspond to explicit low-rank decompositions of the matrix multiplication tensor. Moreover, the previous algorithms used have been discovered by attacking this tensor decomposition problem using human search, continuous optimization and combinatorial search (relying on sub-optimal human-designed heuristics). That's why they use DRL to learn to recognize and generalize over patterns in tensors, and use the learned agent to predict efficient decompositions.

## The TensorGame :

Their agent, the AlphaTensor, played the single-player game called TensorGame. At each step of TensorGame, the player selects how to combine different entries of the matrices to multiply. A score is assigned based on the number of selected operations required to reach the correct multiplication result (10^12 actions for some situations). Because their agent was trained on tensors of various sizes, it led to the transfer of learned decomposition techniques across various tensors.

## DRL for algorithm discovery :

The goal of the agent is to find at each time step ***t*** a triplet (**u**(*t*), **v**(*t*), **w**(*t*)) such as :

$$
T_t \leftarrow T_{t-1} - \bold{u}^t \otimes  \bold{v}^t \otimes \bold{w}^t
$$

With the goal of getting :

$$
T_t = 0
$$

When the player reaches the zero tensor, the sequence of selected factors satisfies :

$$
T_n = \sum_{t=1}^R \bold{u}^t \otimes  \bold{v}^t \otimes \bold{w}^t, with\ R\ the\ number\ of\ moves
$$

The reward is -1 at step to encourage to find the shortest path and is -γ(T_R) at the end if it didn’t find a zero tensor with γ(T_R) an upper bound on the rank of the terminal tensor.

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled%201.png)

## **Neural network architecture :**

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled%202.png)

First of all, it is a transformer-based architecture that incorporates inductive biases for tensor inputs.

When they have their input, they project the *S* × *S* × *S* input tensor into three *S* × *S* grids of feature vectors, and then apply their model, which is a sequence of attention operators (no more information).

### Torso :

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled%203.png)

The torso of the AlphaTensor model is a crucial component responsible for processing input data, consisting of scalars and tensors, and generating a meaningful representation for both the policy head and the value head. It leverages a modified transformers architecture, operating on three S × S grids projected from the S × S × S input tensors. Each grid represents two modes of the tensor, and its elements are initialized with input tensor values along the missing mode. Enrichment of these feature vectors is achieved through concatenating a linear projection from the scalars, followed by a linear layer for dimensionality reduction. The torso further utilizes attention-based blocks to propagate information across the grids, employing axial attention to capture relationships between the elements. The resulting representation, comprising 3S^2 512-dimensional feature vectors, is then forwarded to the policy head.

### Policy head :

It uses as input the state produiced by the Torso (which is supposed to be a representation of the relevent features of the T+1 tensors).

In summary, the policy head uses a transformer to generate an autoregressive policy. During training, it uses teacher-forcing with the ground truth actions. The transformer is fed with tokens and attends to features generated by the "torso". During inference, actions are sampled from the policy head, and the feature representation from the initial step (before the last linear layer) is used as input to the value head.

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled%204.png)

### Value head :

In summary, the value head of the AlphaTensor model uses a multilayer perceptron to predict a distribution of possible returns from a given state. It does this by predicting the value of each quantile of the return distribution. During inference, the model promotes risk-taking by considering the upper quartile of the predicted return distribution.

![Untitled]((AlphaTensor)%20Discovering%20faster%20matrix%20multiplica%206e5d564f0366440697a1de1fa4b2d2f6/Untitled%205.png)

## Questions :

1. What is their model trained to guide a planning procedure searching for efficient matrix multiplication algorithms.
2. What is their inductive biases for tensor inputs
3. They mention “teacher-forcing”, but when is it done ?

## Note :

Wow, that’s what we call ***Supplementary*** Information : [https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-022-05172-4/MediaObjects/41586_2022_5172_MOESM1_ESM.pdf](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-022-05172-4/MediaObjects/41586_2022_5172_MOESM1_ESM.pdf)