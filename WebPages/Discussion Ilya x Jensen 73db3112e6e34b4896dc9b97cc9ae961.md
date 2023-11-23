# Discussion: Ilya x Jensen

Type: Video
Link: https://www.youtube.com/watch?v=ZZ0atq2yYJw&ab_channel=MindCathedral
Date: 2023/05/17

# Discussion between Jensen HUANG (NVIDIA) and Ilya SUTSKEVER (OpenAI)

**Why Computer Vision:**

1. The shift towards deep learning in computer vision was driven by supervised learning methods. These methods require deep AND large neural networks to solve complex tasks. [1]
2. Initially, the focus was primarily on deepening the networks, but the significant role of network size was later recognized.
3. Classical methods, such as kernel-based or Bayesian approaches, were found to be inadequate in representing complex solutions that deep learning could achieve.

**On Compute Power:**

1. The discussion omitted initial considerations of compute power. It highlighted the pivotal role of GPUs in handling large datasets and complex computations, which, combined with Convolutional Neural Networks (CNNs), proved to be highly effective.

**The Inception of OAI:**

1. The foundation of OpenAI (OAI) was based on several innovative ideas, with a notable focus on unsupervised learning through data compression techniques.
2. A key development was the 'Sentiment Neuron'[2] where successfully predicting the next character in an Amazon review led to identifying a neuron in the LSTM[3] network that correlated with the review's sentiment. This demonstrated the network's ability to learn meaningful interpretations of data.

**On Scaling:**

1. Scaling, encompassing bigger models, deeper networks, and bigger datasets, was recognized as a vital factor in improving performance.
2. A significant paper from OAI discussed scaling laws, elaborating on the relationships between loss, model size, and dataset size.[4]
3. At OAI, the emphasis was on understanding how to utilize scale effectively and purposefully.

**ChatGPT:**

1. ChatGPT combines foundational aspects of GPTs with Reinforcement Learning from Human Feedback (RLHF), drawing on experience from projects like DoTA.
2. The process of predicting the next word in a sequence is not just learning statistical correlations in text, the neural network develops a compressed representation of both the text and the underlying processes that generated it and its meaning (the world).
3. There is a distinction between an assistant and a language model. An assistant, such as ChatGPT, must be trustworthy, employing techniques like RLHF, fine-tuning, and human-AI collaboration. In contrast, a language model focuses on completing given internet prompts (learns as much as you can of the world from its projection, words). Going from a LM to an ALM means teaching how to behave and not new knowledge.

**Deep Learning and Reasoning:**

1. Ilya posited a link between prediction accuracy and understanding, drawing an analogy to gathering clues in a crime investigation to predict the perpetrator: “The one who commited the crime is …”.
2. Reasoning is defined as the process of finding better solutions through various means, akin to thinking.
3. A limitation in reasoning is addressed by explicitly asking the neural network to 'think out loud,' although true boundaries of this approach have yet to be fully explored.
4. The primary challenge for neural networks to be more useful is their reliability, as they can hallucinate and make errors, often struggling to explicitly acknowledge what they do or do not know.

**GPT and Information Retrieval:**

1. While GPT excels at word prediction, it could significantly benefit from enhanced capabilities in information retrieval.

**Multi-Modality:**

1. Incorporating multiple modalities is beneficial for neural networks, as it enables them to 'see' and thus better understand context.
2. Learning from combined text and images is more effective than from text alone.
3. Videos contribute to understanding the dynamics of the world, while audio aids in grasping the meaning of words.

## References:

[1] A. Krizhevsky, I. Sutskever and G.E. Hinton, Imagenet classification with deep convolutional neural networks, 2012

[2] A. Radford et al., Learning to Generate Reviews and Discovering Sentiment, 2017

[3] S. Hochreiter and J. Schmidhuber, Long Short-term Memory, 1997

[4] J. Kaplan et al., Scaling Laws for Neural Language Models, 2020