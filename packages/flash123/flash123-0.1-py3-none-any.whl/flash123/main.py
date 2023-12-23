def first():
    return """ 
    def heuristic(n):
        H_dist = {
            'A': 10,
            'B': 8,
            'C': 5,
            'D': 7,
            'E': 3,
            'F': 6,
            'G': 5,
            'H': 3,
            'I': 1,
            'J': 0
        }
        return H_dist[n]


    Graph_nodes = {
        'A': [('B', 6), ('F', 3)],
        'B': [('C', 3), ('D', 2)],
        'C': [('D', 1), ('E', 5)],
        'D': [('C', 1), ('E', 8)],
        'E': [('I', 5), ('J', 5)],
        'F': [('G', 1), ('H', 7)],
        'G': [('I', 3)],
        'H': [('I', 2)],
        'I': [('E', 5), ('J', 3)],
    }

    def aStarAlgo(start_node, stop_node):
        g = dict()
        open_set = set(start_node)
        closed_set = set()
        parents = {}
        g[start_node] = 0
        parents[start_node] = start_node

        while len(open_set) > 0:
            n = None
            for v in open_set:
                if n == None or g[v] + heuristic(v) < g[n] + heuristic(n):
                    n = v

            if n == stop_node or Graph_nodes[n] == None:
                pass
            else:
                for (m, weight) in get_neighbors(n):
                    if m not in open_set and m not in closed_set:
                        open_set.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n

                            if m in closed_set:
                                closed_set.remove(m)
                                open_set.add(m)

            if n == None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                path = []
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                path.append(start_node)
                path.reverse()
                print('Path found: {}'.format(path))
                return path

            open_set.remove(n)
            closed_set.add(n)

        print('Path does not exist!')
        return None


    def get_neighbors(v):
        if v in Graph_nodes:
            return Graph_nodes[v]
        else:
            return None




    aStarAlgo('A', 'J')
 """
def second():
    return """ 
    class Graph:
        def __init__(self, graph, heuristicNodeList, startNode):
            self.graph = graph
            self.H = heuristicNodeList
            self.start = startNode
            self.parents = {}
            self.status = {}
            self.solutionGraph = {}

        def computeMinCost(self, v):
            minCost = 0
            costToMin = {minCost: []}
            flag = True

            for node in self.graph.get(v, ''):
                cost = 0
                nodeList = []
                for c, weight in node:
                    cost += self.H.get(c, 0) + weight
                    nodeList.append(c)

                if flag:
                    minCost = cost
                    costToMin[minCost] = nodeList
                    flag = False

                else:
                    if minCost > cost:
                        minCost = cost
                        costToMin[minCost] = nodeList

            return minCost, costToMin[minCost]

        def aoStar(self, v, backtracking=False):
            print(f'Heuristic Values: {self.H}')
            print(f'Solution Graph: {self.solutionGraph}')
            print(f'Processing Node: {v}')

            if self.status.get(v, 0) >= 0:
                minCost, childNodeList = self.computeMinCost(v)
                self.H[v] = minCost
                self.status[v] = len(childNodeList)
                solved = True

                for childNode in childNodeList:
                    self.parents[childNode] = v
                    if self.status.get(childNode, 0) != -1:
                        solved = solved & False

                if solved:
                    self.status[v] = -1
                    self.solutionGraph[v] = childNodeList

                if v != self.start:
                    self.aoStar(self.parents[v], True)

                if not backtracking:
                    for childNode in childNodeList:
                        self.status[childNode] = 0
                        self.aoStar(childNode, False)

    h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J': 1}
    graph1 = {
        'A': [[('B', 1), ('C', 1)], [('D', 1)]],
        'B': [[('G', 1)], [('H', 1)]],
        'C': [[('J', 1)]],
        'D': [[('E', 1), ('F', 1)]],
        'G': [[('I', 1)]]
    }
    G1 = Graph(graph1, h1, 'A')
    G1.aoStar(G1.start)
    print(f'Solution starting from {G1.start}:\n{G1.solutionGraph}')
    """
def third():
    return """ 
    import numpy as np
    import pandas as pd

    data = pd.read_csv('enjoy.csv')
    print(data)

    concepts = np.array(data.iloc[:, 0:-1])
    print("\nInstances are:\n", concepts)

    target = np.array(data.iloc[:, -1])
    print("\nTarget Values are: ", target)

    def learn(concepts, target):
        specific_h = concepts[0].copy()
        print("\nInitialization of specific_h and generic_h")
        print("\nSpecific Boundary: ", specific_h)
        general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
        print("\nGeneric Boundary: ", general_h)
        
        for i, h in enumerate(concepts):
            print("\nStep", i + 1, ": ", h)
            if target[i] == "Yes":
                print("Instance is Positive ")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        specific_h[x] = '?'
                        general_h[x][x] = '?'
            
            if target[i] == "No":
                print("Instance is Negative ")
                for x in range(len(specific_h)):
                    if h[x] != specific_h[x]:
                        general_h[x][x] = specific_h[x]
                    else:
                        general_h[x][x] = '?'

            print("Specific Boundary ", specific_h)
            print("Generic Boundary", general_h)
            print("\n")
        
        indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
        for i in indices:
            general_h.remove(['?', '?', '?', '?', '?', '?'])
        
        return specific_h, general_h

    s_final, g_final = learn(concepts, target)
    print("Final Specific_h: ", s_final, sep="\n")
    print("Final General_h: ", g_final, sep="\n")
    """
def fourth():
    return """ 
    def find_entropy(df):
        Class = df.keys()[-1]  
        entropy = 0
        values = df[Class].unique()
        for value in values:
            fraction = df[Class].value_counts()[value]/len(df[Class]) 
            entropy += -fraction*np.log2(fraction)
        return entropy

    def find_entropy_attribute(df,attribute):
        Class = df.keys()[-1]  
        target_variables = df[Class].unique()  
        variables = df[attribute].unique()
        entropy2 = 0
        for variable in variables:
            entropy = 0
            for target_variable in target_variables:
                num = len(df[attribute][df[attribute]==variable][df[Class] ==target_variable])
                den = len(df[attribute][df[attribute]==variable])
                fraction = num/(den+eps)
                entropy += -fraction*log(fraction+eps)
            fraction2 = den/len(df)
            entropy2 += -fraction2*entropy
        return abs(entropy2)

    def find_winner(df):
        Entropy_att = []
        IG = []
        for key in df.keys()[:-1]:
            IG.append(find_entropy(df)-find_entropy_attribute(df,key))
        return df.keys()[:-1][np.argmax(IG)]  

    def get_subtable(df, node,value):
        return df[df[node] == value].reset_index(drop=True)

    def buildTree(df,tree=None):  
        Class = df.keys()[-1]   

        node = find_winner(df)
        attValue = np.unique(df[node])
        if tree is None:                    
            tree={}
            tree[node] = {}

        for value in attValue:
            subtable = get_subtable(df,node,value)
            clValue,counts = np.unique(subtable['PlayTennis'],return_counts=True)                        
            if len(counts)==1:
                tree[node][value] = clValue[0]                                                    
            else:        
                tree[node][value] = buildTree(subtable) 
        return tree

    import pandas as pd
    import numpy as np
    eps = np.finfo(float).eps
    from numpy import log2 as log
    df = pd.read_csv('id3.csv')
    print("\n Given Play Tennis Data Set:\n\n",df)
    tree= buildTree(df)
    import pprint
    print('The resultant decision tree  is')
    pprint.pprint(tree)

    test={'Outlook':'Sunny','Temperature':'Hot','Humidity':'High','Wind':'Weak'}
    def func(test, tree, default=None):
        attribute = next(iter(tree))  
        print(attribute)  
        if test[attribute] in tree[attribute].keys():
            print(tree[attribute].keys())
            print(test[attribute])
            result = tree[attribute][test[attribute]]
            if isinstance(result, dict):
                return func(test, result)
            else:
                return result
        else:
            return default
    ans = func(test, tree)
    print(ans)
 """
def fifth():
    return """ 
    import numpy as np

    X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    y = np.array(([92], [86], [89]), dtype=float)
    X = X / np.amax(X, axis=0)
    y = y / 100

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def derivatives_sigmoid(x):
        return x * (1 - x)

    epoch = 5000
    lr = 0.1
    inputlayer_neurons = 2
    hiddenlayer_neurons = 3
    output_neurons = 1

    wh = np.random.uniform(size=(inputlayer_neurons, hiddenlayer_neurons))
    bh = np.random.uniform(size=(1, hiddenlayer_neurons))
    wout = np.random.uniform(size=(hiddenlayer_neurons, output_neurons))
    bout = np.random.uniform(size=(1, output_neurons))

    for i in range(epoch):
        hinp1 = np.dot(X, wh)
        hinp = hinp1 + bh
        hlayer_act = sigmoid(hinp)

        outinp1 = np.dot(hlayer_act, wout)
        outinp = outinp1 + bout
        output = sigmoid(outinp)

        EO = y - output
        outgrad = derivatives_sigmoid(output)
        d_output = EO * outgrad

        EH = d_output.dot(wout.T)
        hiddengrad = derivatives_sigmoid(hlayer_act)
        d_hiddenlayer = EH * hiddengrad

        wout += hlayer_act.T.dot(d_output) * lr
        wh += X.T.dot(d_hiddenlayer) * lr

    print("Input:\n" + str(X))
    print()
    print("Actual Output:\n" + str(y))
    print()
    print("Predicted Output:\n", output)
 """
def sixth():
    return """ 
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.naive_bayes import GaussianNB

    data = pd.read_csv('p-tennis.csv')


    X = data.iloc[:, :-1]
    print('Dependent variables')
    print(X.head())

    y = data.iloc[:, -1]
    print('Independent variables')
    print(y.head())


    convert = LabelEncoder()

    for i in list(data.columns)[:-1]:
        X[i] = convert.fit_transform(X[i])


    print("\nNow the Train input is\n", X.head())

    y = convert.fit_transform(y)
    print("\nNow the Train output is\n",y)

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.20)

    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    print("Accuracy is:", accuracy_score(classifier.predict(X_test), y_test)) """
def seventh():
    return """ 
    from sklearn.cluster import KMeans
    from sklearn.mixture import GaussianMixture
    import sklearn.metrics as metrics
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    names = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width', 'Class']
    dataset = pd.read_csv("iris.csv", names=names)
    X = dataset.iloc[:, :-1] 
    label = {'Iris-setosa': 0,'Iris-versicolor': 1, 'Iris-virginica': 2} 
    y = [label[c] for c in dataset.iloc[:, -1]]
    plt.figure(figsize=(16,6))
    colormap=np.array(['red','lime','black'])
    # REAL PLOT
    plt.subplot(1,3,1)
    plt.title('Real')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y])

    # K-PLOT
    model=KMeans(n_clusters=3, random_state=0).fit(X)
    plt.subplot(1,3,2)
    plt.title('KMeans')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[model.labels_])
    print('The accuracy score of K-Mean: ',metrics.accuracy_score(y, model.labels_))

    # EM PLOT
    gmm=GaussianMixture(n_components=3, random_state=0).fit(X)
    y_cluster_gmm=gmm.predict(X)
    plt.subplot(1,3,3)
    plt.title('EM Clustering')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y_cluster_gmm])
    plt.show()
    print('The accuracy score of EM: ',metrics.accuracy_score(y, y_cluster_gmm))
    print('Observation: EM algorithm based clustering matched the true labels more closely than the Kmeans.') """
def eigth():
    return """ 
    from sklearn.model_selection import train_test_split 
    from sklearn.neighbors import KNeighborsClassifier 
    from sklearn import datasets

    iris=datasets.load_iris() 
    print("Iris Data set loaded...")

    x_train, x_test, y_train, y_test = train_test_split(iris.data,iris.target,test_size=0.1) #10% test 

    #random_state=0
    print("Data set is split into trainiong and testing")
    print("Size of training data and its label", x_train.shape,y_train.shape)
    print("size of testing data and its label",x_test.shape,y_test.shape)
    for i in range(len(iris.target_names)):
        print("Label", i , "-",str(iris.target_names[i]))

    classifier = KNeighborsClassifier(n_neighbors=2)

    classifier.fit(x_train, y_train)
    y_pred=classifier.predict(x_test) 

    print("Results of Classification using K-nn with K=1 ") 
    for r in range(0,len(x_test)):
        print(" Sample:", str(x_test[r]), " Actual-label:", str(y_test[r])," Predicted-label:", str(y_pred[r]))
    print("Classification Accuracy :" , classifier.score(x_test,y_test))
 """
def ninth():
    return """ 
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np


    def kernel(point, xmat, k):
        m, n = np.shape(xmat)
        weights = np.mat(np.eye(m))
        
        for j in range(m):
            diff = point - X[j]
            weights[j, j] = np.exp(diff * diff.T / (-2.0 * k**2))
        
        return weights

    def localWeight(point, xmat, ymat, k):
        wei = kernel(point, xmat, k)
        W = (X.T * (wei * X)).I * (X.T * (wei * ymat.T))
        return W

    def localWeightRegression(xmat, ymat, k):
        m, n = np.shape(xmat)
        ypred = np.zeros(m)
        
        for i in range(m):
            ypred[i] = xmat[i] * localWeight(xmat[i], xmat, ymat, k)
        
        return ypred


    data = pd.read_csv('10-dataset.csv')
    bill = np.array(data.total_bill)
    tip = np.array(data.tip)


    mbill = np.mat(bill)
    mtip = np.mat(tip)
    m = np.shape(mbill)[1]
    one = np.mat(np.ones(m))  
    X = np.hstack((one.T, mbill.T))


    ypred = localWeightRegression(X, mtip, 0.5)
    SortIndex = X[:, 1].argsort(0)
    xsort = X[SortIndex][:, 0]

    plt.scatter(bill, tip, color = 'green')
    plt.plot(xsort[:, 1], ypred[SortIndex], color='red', linewidth=5)
    plt.xlabel('Total bill')
    plt.ylabel('Tip')
    plt.show()  """