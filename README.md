# Reinforcement Learning
## Overview
This repository provides an implementation of several reinforcement learning algorithms, must read papers/books and questions (of any kind).

<p align="center">
  <img src="Images/Gif_Maze.gif" width="300" title="Qlearning applied to find the shortest way in a maze">
  <img src="Images/Mountain_Car.gif" width="400" height="300" title="Qlearning applied to find the shortest way in a maze">
</p>


In addition, I keep this repository updated with my thoughts and future work (mainly to answer the question: How to improve reinforcement learning for non-stationary environments).

## Report
My report (available in [french](https://github.com/LounesMD/Stage2021_RL/blob/main/CompteRendu.pdf) or in [english](https://www.google.com)) proposed an in-dept study of the algorithms used. Note that the algorithms are not written because they are easily found on the internet. For the first version of the report, my work was based on this document : [Reinforcement Learning](https://philippe-preux.github.io/Documents/digest-ar.pdf).

## To come
Fitted Q-Iteration.  <br>
Deep Q-Learning. <br>

non-exhaustive list of what's coming soon : 
+ Algorithms :
  1. Monte Carlo Search
  2. Fitted Q-Iteration
  3. Deep Q-Network
  4. REINFORCE
  5. PPO
  6. Model-based
+ Environment :
  1. Classic Control : Cart Pole and Acroboy.
  2. Mujoco : Ant, Hopper and Humanoid.
  3. My own environments !
 
Also, I would like to provide a script, based on Deep-Q Learning, that can be run on *every* video game website to find the best way to *maximize* a score. <br>
At the beginning of 2023, you will have an object-oriented implementation of my algorithms.
 
## To read
  - [x] [Complexity of Planning with Partial Observability](https://www.aaai.org/Papers/ICAPS/2004/ICAPS04-041.pdf)
  - [ ] [An introduction to Reinforcement Learning](http://incompleteideas.net/book/bookdraft2017nov5.pdf)
  - [x] [World Models](https://arxiv.org/pdf/1803.10122.pdf)
  - [x] [Gans](https://arxiv.org/pdf/1406.2661.pdf) and [its analysis](https://www.youtube.com/watch?v=eyxmSmjmNS0&ab_channel=YannicKilcher)
  - [ ] [MDPs]()
  - [ ] Offline Reinforcement Learning : [Paper1](https://arxiv.org/abs/2005.01643) & [Paper2](https://arxiv.org/abs/2203.01387)
  - [ ] [Online Reinforcement Learning](https://arxiv.org/abs/1612.03780)
  - [ ] More ...

  
## Questions / Answers
### Questions
In this part, I will keep track of the questions I ask myself and publish their answers when I have the answer. I will do my best to publish them soon on stackoverflow, Quora, ...<br>
1. If we want to learn the optimal policy from the environnement (environnement we discover during exploration), why initialize the Quality function to 0 for each (state, action) at the beginning ? Should not we just add a value to (state,action) when we discover it ? (Generaly you'll see something like `Initialize Q(s,a) arbitrarily`)


2. A new way to encourage the exploration of the environnement is to give extra-rewards to the agent during its exploration*.
However, for various application, when the agent does something wrong and gets a negative reward, this negative reward is  exactly the same for the next epochs. My question is so : Why don't we just increase the negative reward ? (I don't say to get it to -inf, but make the agent thinks before doing the same errors several times). Maybe, by increasing the negative reward, in a non-linear way, with a strong increase close to the initial state can help. <br>
This is, from my point of view, different from the current approach wich is : The agent learns to don't do errors several times because it will learn to do no errors (by choosing the action that maximize its total reward). <br>
I'll try to implement this idea with the CarInTheHill problem and publish my results. <br>
*I'm still looking for the first article about this.

3. When we use an algorithm to find the optimal policy, let's say in go, do we use the same policy for both player (= and so update it by the score of both players) ? If yes, why do we think that the optimal policy found is optimal for the black payer and the white player ? <br>
Also, is it interesting to use different algorithms for the two players?

4. What is the difference between a bandit and an agent ? When to choose which one and can we oppose an agent and a bandit ?


5. How important it is to be able to know the new state of the agent after doing an action ? (Check this [article](https://www.aaai.org/Papers/ICAPS/2004/ICAPS04-041.pdf))

### Answers
1. I have done such an implementation for the mountain car problem, and the performance is the same. I asked this question before I realized that you can discretize your environment if you use a classic Q-Learning tabular method.
