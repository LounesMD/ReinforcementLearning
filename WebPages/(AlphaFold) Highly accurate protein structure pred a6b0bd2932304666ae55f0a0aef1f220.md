# (AlphaFold)  Highly accurate protein structure prediction with AlphaFold

Auteur: Deepmin
Lien: https://sci-hub.hkvisa.net/10.1038/s41586-021-03819-2
Note sur 5: ⭐️⭐️⭐️⭐️
Statut: Terminé
Type: Article

# (AlphaFold)  Highly accurate protein structure prediction with AlphaFold

![Untitled]((AlphaFold)%20Highly%20accurate%20protein%20structure%20pred%20a6b0bd2932304666ae55f0a0aef1f220/Untitled.png)

## Idea :

This paper is to present AlphaFold, a model that can predicts the structure of proteins.

This idea of AlphaFold, which is different from AlfaZero/MuZero is to predict the 3D coordinates of all heavy atoms for a given protein.

## Model :

![Untitled]((AlphaFold)%20Highly%20accurate%20protein%20structure%20pred%20a6b0bd2932304666ae55f0a0aef1f220/Untitled%201.png)

The model is in 2 parts.

The first one is the trunk of network as it processes the input through repeated layers of Evoformer. Evoformer is composed of blocks that contain attention-based and non-attention-based components in order to  enable direct reasoning about the spatial and evolutionary relationships.

The second part of the network is the structure module that introduces an explicit 3D structure in the form of a rotation and translation for each residue of the protein.

By repeatedly using the network with previous outputs, step call *recycling*, they aim to refine a highly accurate protein structure with precise atomic details

![Untitled]((AlphaFold)%20Highly%20accurate%20protein%20structure%20pred%20a6b0bd2932304666ae55f0a0aef1f220/Untitled%202.png)

## Interesting :

The most interesting things in this paper : 

1. The use of recycling for the training in order to refine the protein structure prediction
2. The use of a combination of attention-based/non-attention-based components (We have more information in AlphaTensor ^^)
3. Evoformer is an Encoder like model for protein structure that tries to capture dependencies and relationships between amino acids in the protein sequence
4. One “big” model for encoding a smaller one for prediction 
5. Wow, they use an approach similar to noisy student self-distillation to enhance accuracy 
6. Protein structures can be represented as graphs, where the nodes represent amino acids and the edges represent interactions between them. Graph-based methods leverage the spatial relationships and dependencies between amino acids to infer the protein's three-dimensional structure. This is particularly important for capturing long-range interactions between amino acids that may not be adjacent in the primary sequence.
7. Supplementary section : [https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-021-03819-2/MediaObjects/41586_2021_3819_MOESM1_ESM.pdf](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-021-03819-2/MediaObjects/41586_2021_3819_MOESM1_ESM.pdf)

## Questions :

1. What is a logit bias ?
2. How do they eliminate impossible case ?
    1. “the elimination of impossible cases is achieved through a combination of several techniques during the protein structure prediction process” : Constraint satisfaction, Spatial consistency, Confidence estimation, Energy minimization