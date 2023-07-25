import pickle

fruits = ("apple", "orange", "banana", "pineapple", "strawberry", ((1, 'tomato'), (2, 'beans')))


with open(r"D:\workspace\fruits.pickle", "wb") as fout:
    pickle.dump(fruits, fout)


with open(r"D:\workspace\fruits.pickle", "rb") as fin:
    data = pickle.load(fin)
    print(data)
