# kMeans w/ Purity using Python
By: Taylor Brazelton

## Data Points File:
    python main.py -d iris.txt -k 2

  This forces the program to start out with the points from iris.txt and 2 random centroids.

## Specific Initial Centroids:
    python main.py -d toy.txt -c centroid.txt

  This forces the program to initialize with the points from toy.txt and the centroids defined in centroid.txt.

## Class Labels:
    python main.py -d iris.txt -k 2 -l labels.txt

  Forces the program to use the data points in iris.txt with 2 random centroids and run the purity algorithm with the labels defined in labels.txt.
