import pickle
import os


first_names_path = r'C:\Users\Ben\Desktop\Dropbox\maths\names\first_names.pickle'
with open(first_names_path, 'r') as f:
    names = pickle.load(f)
