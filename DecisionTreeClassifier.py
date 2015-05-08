from Classifier import *
import math
import random

class DecisionTreeClassifier(Classifier): 

    def learn(self, X, y):
        """
        Constructs a decision tree.

        Args:
           X: A list of feature arrays where each feature array corresponds to feature values
        of one observation in the training set.
           y: A list of ints where 1s correspond to a positive instance of the class and 0s correspond
        to a negative instance of the class at said 0 or 1s index in featuresList.
        """
        DT = TreeNode(X, y, 0)
        DT.makeTree()
        self.DT = DT

    def getLogProbClassAndLogProbNotClass(self, x):
        """Returns log probabilities that a given observation is a positive sample or negative sample"""
        return self.DT.getLogProbClassAndLogProbNotClass(x)

class TreeNode: 

    def __init__(self, X, y, depth):
        self.X = X  # set of featurized observations
        self.y = y  # set of labels associated with the observations 
        self.depth = depth
        self.depthLimit = 10  # limits the depth of your tree for the sake of performance; feel free to adjust
        self.n = len(X)
        self.splitFeature, self.children = None, None  # these attributes should be assigned in splitNode()
        self.entropySplitThreshold = 0.7219 # node splitting threshold for 80%/20% split; feel free to adjust

    def splitNode(self, splitFeature):
        ''' Creates child nodes, splitting the featurized data in the current node on splitFeature. 
        Must set self.splitFeature and self.children to the appropriate values.

        Args: splitFeature, the feature on which this node should split on (this should be the feature you obtain from
            the bestFeature() function)
        Returns: returns True if split is performed, False if not.
        '''
        if len(set(self.y)) < 2: # fewer than 2 labels in this node, so no split is performed (node is a leaf)
            return False

        # YOU IMPLEMENT

        # build traits of children
        if splitFeature == None:
            return False
        self.splitFeature = splitFeature

        posX = []
        posY = []
        negX = []
        negY = []
        for i in range(self.n):
            obs = self.X[i]
            val = self.y[i]
            if obs[splitFeature] > 0:
                posX.append(obs)
                posY.append(val)
            else:
                negX.append(obs)
                negY.append(val)

        childPos = TreeNode(posX, posY, self.depth+1)
        childNeg = TreeNode(negX, negY, self.depth+1)

        self.children = (childPos, childNeg)

        return True

    def bestFeature(self):
        ''' Identifies and returns the feature that maximizes the information gain.
        You should calculate entropy values for each feature, and then return the feature with highest entropy.
        Consider thresholding on an entropy value -- that is, select a target entropy value, and if no feature 
        has entropy above that value, return None as the bestFeature 

        Returns: the index of the best feature based on entropy
        '''

        # YOU IMPLEMENT
        bestEntropy = 0
        bestFeature = None

        # iterate through each feature
        features = len(self.X[0])
        for i in range(features):
            sumv = 0
            for observation in self.X:
                # make into 1 and 0
                if observation[i] > 0:
                    sumv += 1

            p_pos = sumv/float(self.n)
            p_neg = 1 - p_pos

            if p_pos == 0:
                p_pos = 0.00001
            if p_neg == 0:
                p_neg = 0.00001

            # calculate entropy
            entropy = (-1)*p_pos*math.log(p_pos,2) + (-1)*p_neg*math.log(p_neg,2)

            # determine best entropy
            if entropy >= self.entropySplitThreshold and entropy > bestEntropy:
                bestEntropy = entropy
                bestFeature = i

        return bestFeature

    def makeTree(self):
        '''Splits the root node on the best feature (if applicable),
        then recursively calls makeTree() on the children of the root.
        If there is no best feature, you should not perform a split, and this
        node will become a leaf'''
        bestFeature = self.bestFeature()

        # YOU IMPLEMENT
        if (self.depth != self.depthLimit):
            val = self.splitNode(bestFeature)
            if val:
                left, right = self.children
                left.makeTree()
                right.makeTree()

    def getLogProbClassAndLogProbNotClass(self, x):
        """
        Args:
            x: A numpy array that corresponds to the feature values for a single observation.

        Returns:
            A tuple containing the log probability that the observation is a member of the class
                and the log probability that the observation is NOT a member of the class
        """

        # YOU IMPLEMENT

        node = self
        while node.depth < node.depthLimit and node.children != None:
            index = node.splitFeature
            if node.children != None:
                if x[index] > 0:
                    node = node.children[0]
                else:
                    node = node.children[1]

        sumv = 0
        for val in node.y:
            sumv += val;

        probClass = sumv / float(len(node.y))
        probNotClass = 1 - probClass

        if probClass == 0:
            probClass = 0.00001
        if probNotClass == 0:
            probNotClass = 0.00001

        logProbClass = math.log(probClass)
        logProbNotClass = math.log(probNotClass)

        return (logProbClass, logProbNotClass)
