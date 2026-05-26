import networkx
import pickle 


def graphgenerator(parameters, k):
    megadictionary = {} 
    for (n,p) in parameters:
        collection = [] 
        for i in range(1, k):
            collection.append(networkx.to_dict_of_lists(networkx.erdos_renyi_graph(n,p)))
        megadictionary.update({(n,p):collection})
    return megadictionary



def parametergenerator(start, step, count, probs):
    parameters = [] 
    for i in range(1, count): 
        for p in probs: 
           parameters.append((start,p))
        start = start+step 
    return parameters 


def main() :
    pmtr = parametergenerator(10, 10, 10, [0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8, 1])
    g = graphgenerator(pmtr, 3)
    print(g)
    with open("megadictionary.pkl", "wb") as file:
        pickle.dump(g, file)

main() 