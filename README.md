# Reinforcement Learning Intership
## Overview
This repository provides an implementation of several reinforcement learning algorithms made during my summer internship in 2021.

<p align="center">
  <img src="Images/GIF.gif" width="300" title="Qlearning applied to find the shortest way in a maze">
</p>

## Report
My report (available in [french](https://github.com/LounesMD/Stage2021_RL/blob/main/CompteRendu.pdf) or in [english](https://www.google.com)) proposed an in-dept study of the algorithms used. Note that the algorithms are not written because they are easily found on the internet. For my part, my work was based on this document : [Reinforcement Learning](https://philippe-preux.github.io/Documents/digest-ar.pdf).

## To come
Monte-Carlo algorithm to estimate the Q function.  <br>
non-exhaustive list of what's coming soon : 
+ Algorithms :
  1. Monte Carlo
  2. Fitted Q-Iteration
  3. Deep Q-Network
  4. REINFORCE
  5. PPO
  6. Model-based
+ Environment :
  1. car-in-the-hill.

## Questions / Answers
### Questions
In this part, I will keep track of the questions I ask myself and publish their answers when I have the answer. <br>
1. If we want to learn the optimal policy from the environnement (environnement we discover during exploration), why initialize the Quality function to 0 for each (state, action) at the beginning ? Should not we just add a value to (state,action) when we discover it ? (Generaly you'll see something like `Initialize Q(s,a) arbitrarily`)


2. A new way to encourage the exploration of the environnement is to give extra-rewards to the agent during its exploration*.
However, for various application, when the agent does something wrong and gets a negative reward, this negative reward is  exactly the same for the next epochs. My question is so : Why don't we just increase the negative reward ? (I don't say to get it to -inf, but make the agent thinks before doing the same errors several times). Maybe, by increasing the negative reward, in a non-linear way, with a strong increase close to the initial state can help. <br>
This is, from my point of view, different from the current approach wich is : The agent learns to don't do errors several times because it will learn to do no errors (by choosing the action that maximize its total reward). <br>
I'll try to implement this idea with the CarInTheHill problem and publish my results. <br>
*I'm still looking for the first article about this.

### Answers
