import pickle


full_path = r'C:\Users\Ben\Desktop\Dropbox\maths\names\first_names.pickle'
with open(full_path, 'rb') as f:
    names = pickle.load(f)
    print (names)
