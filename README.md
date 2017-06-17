# MalPiles
This is project i started for educational purpouse mostly, to dive into machine learning. I will try to frequently update the project with faster and more accurate features and algorithms to be able to identify different packers.
The machine learning algorithm that is currently used is the kNN implementation from [Dr. Jason Brownlee tutorial](http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/)

Right now i use my own PE features collection script that collects the following features out of PE files:

```
Code section entropy
Entire PE entropy
Overlay data entropy
Longest ASCII string length
Longest ASCII string entropy (entropy is lower if it contains spaces)
```

Training samples must be named like this:

```
PackerFamily.A (1).exe
PackerFamily.A (2).exe
PackerFamily.A (3).exe
....
PackerFamily.B (1).exe
PackerFamily.B (2).exe
PackerFamily.B (3).exe
```

Example usage with very few sets:

```
python generate_dataset.py C:\Samples output.csv
python malpiles.py output.csv

Train set: 8
Test set: 10
> predicted='CrypterFamily.A', actual='CrypterFamily.A'
> predicted='WindowsSystemExe', actual='CrypterFamily.A'
> predicted='CrypterFamily.A', actual='CrypterFamily.A'
> predicted='WindowsSystemExe', actual='CrypterFamily.A'
> predicted='WindowsSystemExe', actual='WindowsSystemExe'
> predicted='WindowsSystemExe', actual='WindowsSystemExe'
> predicted='WindowsSystemExe', actual='WindowsSystemExe'
> predicted='WindowsSystemExe', actual='WindowsSystemExe'
> predicted='WindowsSystemExe', actual='WindowsSystemExe'
> predicted='UPX', actual='UPX'
Accuracy: 80.0%
```
