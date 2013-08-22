import pickle


with open('first_names.csv', 'r') as f:
    names = pickle.load(f)
