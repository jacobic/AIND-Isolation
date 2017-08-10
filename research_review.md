### Silver - "Mastering the Game of {Go} with Deep Neural Networks and Tree Search" ###

#### Abstract ####

* AlphaGo uses **value networks** to evaluate board positions and **policy networks** to select moves. 

* These deep neural networks are trained by a novel combination of supervised learning from human expert games, and **reinforcement learning** from games of self-play. 

* Without any lookahead search, the neural networks play Go at the level of state-of-the-art Monte-Carlo tree search programs that simulate thousands of random games of self-play. 

* AlphaGo also introduce a new search algorithm that combines Monte-Carlo simulation with value and policy networks. 

* Using this search algorithm, AlphaGo achieved a 99.8% winning rate against other Go programs, and defeated the European Go champion, 5 - 0. 

* This is the first time that a computer program has defeated a human pro player in the full-sized game (this feat was thought to be at least a decade away).   
[Page 1](sk://SilverHuangEtAl16nature#1)

#### Alternatives to exhaustive search in Go ####

Go has an average branching factor and depth of $b \sim 250$ and $d \sim 150$ respectively therefore exhaustive search is infeasible but the effective search space can be reduced:

* The depth of the search may be reduced by position evaluation: truncating the search tree at state s and replacing the subtree below $s$ by an approximate value function $v(s)$ approx $v*(s)$ that predicts the outcome from state $s$. This approach has led to super-human performance in chess, checkers and othello, but it was believed to be intractable in Go due to the complexity of the game. 

* The breadth of the search may be reduced by sampling actions from a policy $p(a|s)$ that is a probability distribution over possible moves a in position $s$. For example, Monte-Carlo rollouts search to maximum depth without branching at all, by sampling long sequences of actions for both players from $a$ policy $p$. Averaging over such rollouts can provide an effective position evaluation, achieving super-human performance in backgammon and Scrabble, and weak amateur level play in Go.   
[Page 2](sk://SilverHuangEtAl16nature#2)

#### Monte-Carlo tree search (MCTS) ####

Monte-Carlo tree search uses Monte-Carlo rollouts to estimate the value of each state in a search tree: 

* More simulations -> larger search tree -> the relevant values become more accurate. 

* The policy used to select actions during search is also improved over time, by selecting children with higher values. 

* Asymptotically, this policy converges to optimal play, and the evaluations converge to the optimal value function. 

* The strongest current Go programs are based on MCTS, enhanced by policies that are trained to predict human expert moves. 

* These policies are used to narrow the search to a beam of high probability actions, and to sample actions during rollouts. 

* This approach has achieved strong amateur play. However, prior work has been limited to shallow policies  or value functions based on a linear combination of input features.   
[Page 2](sk://SilverHuangEtAl16nature#2)

#### Deep Convolutional Neural Networks (CNNs) ####

AlphaGo also uses deep convolutional neural networks:

* CNNs reduce the effective depth and breadth of the search tree: evaluating positions using a **value network**, and sampling actions using a **policy network**.

* Board positions are processed as a 19 × 19 image (CNNs are great for computer vision and image classification)

* Convolutional layers are used to construct a representation of the position. 

Training:

* Neural networks are trained using a pipeline consisting of several stages of machine learning. 

1. Training a supervised learning (SL) policy network, $p_\sigma$, directly from expert human moves. This provides fast, efficient learning updates with immediate feedback and high quality gradients. 

2. Similar to prior work, we also train a fast policy $p_\pi$that can rapidly sample actions during rollouts. 

3. Train a reinforcement learning (RL) policy network, $p_p$, that improves the SL policy network by optimising the final outcome of games of self-play. This adjusts the policy towards the correct goal of winning games, rather than maximizing predictive accuracy. 

4. Finally, we train a value network $v_	heta$ that predicts the winner of games played by the RL policy network against itself. Our program AlphaGo efficiently combines the policy and value networks with MCTS.   
[Page 2](sk://SilverHuangEtAl16nature#2)

#### Summary ####

* based on a combination of deep neural networks and tree search

* plays at the level of the strongest human players, thereby achieving one of artificial intelligence’s “grand challenges” 

* effective move selection and position evaluation functions based on deep neural networks that are trained by combining supervised and reinforcement learning. 

* introduced new search algorithm that successfully combines neural network evaluations with Monte-Carlo rollouts. 

* Our program AlphaGo integrates these components together, at scale, in a high-performance tree search engine.

* AlphaGo evaluates thousands of times fewer positions than Deep Blue did
- it compensates by selecting those positions more intelligently, using the policy network, and evaluating them more precisely, using the value network (perhaps closer to how humans play). 

- Deep Blue relied on a handcrafted evaluation function but AlphaGo’s neural networks are trained directly from game-play purely through general-purpose supervised and reinforcement learning methods.

* Go is exemplary of the difficulties faced by artificial intelligence a challenging decision-making task:
- an intractable search space
- an optimal solution so complex it appears infeasible to directly approximate using a policy or value function. 

* Previous major breakthrough in computer Go involved the introduction of Monte-Carlo tree search,  which have led to corresponding advances in many other domains.  

* By combining tree search with policy and value networks, AlphaGo has finally reached a professional level in Go, providing hope that human-level performance can now be achieved in other seemingly intractable artificial intelligence domains.

   
[Page 13](sk://SilverHuangEtAl16nature#13)


