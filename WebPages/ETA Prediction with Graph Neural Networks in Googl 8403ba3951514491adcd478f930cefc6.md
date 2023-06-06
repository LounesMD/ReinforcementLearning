# ETA Prediction with Graph Neural Networks in Google Maps

Author: DeepMind <br>
Link: https://arxiv.org/pdf/2108.11482.pdf and https://youtube.com/watch?v=a6WCZn7kOhk&ab_channel=AleksaGordić-TheAIEpiphanyand

# ****ETA Prediction with Graph Neural Networks in Google Maps****

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled.png)

From a point A to B, google map computes feasible path, computes the ETA for each path  and returns the shortest/smaller one.

To build the graph, they cut/segment roads in segments so not only intersections are nodes. With this approach, long roads are not only one long edges in the graph (probably justifying the better results of this approach in some countries and not others) .

## Graph featues

The labels for prediction in node-level and graph-level are the time (in second) to traverse the segments and supersegments.

The features of the nodes are :

- The average real-time and historical segment travel speeds and times
- segment length
- segement priority (road classifications such as highway)
- Additionaly, they provide learnable segment and supersegment-level embedding vectors. (size 16 and 64)

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled%201.png)

## Model Architecture :

### [Graph Network blocks (GN) :](https://arxiv.org/pdf/1806.01261.pdf)

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled%202.png)

Where :

- **e’_k** is the new edge features
- **e_k** is the current edge features
- **v_sk** source node features
- **v_tk** target node features
- **u** global graph features vector
- **v’_i** is the new node features
- **v_i** is the current node features
- **ρ** sums the incoming/outgoing edges (if E’) or nodes (if V’) features
- **u’** is the new global features vector

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled%203.png)

They apply the GN processor 2 times. And they learn a separate model for each horizon h (traverse rn, in 10mins, 30mins, etc). Why ? Because they had better results.

## Loss

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled%204.png)

Here, as we can see we have :

- a sum of weighted losses
- Losses with Hubert loss in order to prevent destabilizing the training
- Flow, f^i, to know how long does it take to traverse the supersegment i when the route is almost empty. To counterbalance the errors introduced by y and ŷ.

### Reduice the variance :

To prevent the prediction to dump, they use :

- **MetaGradients** : Instead of picking a learning rate and a schedule, you treat the learning rate a learning parameter
- **Exponential Moving Average** (EMA) : To update the weights, you don’t just use the new weights, you also use the previous ones

![Untitled](ETA%20Prediction%20with%20Graph%20Neural%20Networks%20in%20Googl%208403ba3951514491adcd478f930cefc6/Untitled%205.png)