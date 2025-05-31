import os 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score


dataPath = 'data.csv' # path of the data file 

if not os.path.exists(dataPath): 
    # to check if the data file exists in the current directory
    raise FileNotFoundError(f"The file {dataPath} does not exist in the current directory.")

data= pd.read_csv(dataPath, sep=r'\s+', header=None) # to read the data file
# "sep=r'\s+'" is used to read the data file with space as a separator 
# "header=None" is used to read the data file without header 

extractedNumericalData= data.iloc[:, 0:2].values 
# to extract the numerical data from the data file
# for unsupervised learning, we do not need the labels(column 3)

# we will run KMeans multiple times with different values of random seeds 

bestKMeansModel= None 
# we will use this variable to store the best KMeans model
# and choose the model with best compactness score

bestInertiaScore= np.inf  # to store the inertia score
# therefore, we will use np.inf to initialize the lowest inertia score

for randomSeed in range(10): # to run KMeans 10 times with different random seeds
    kMeansModel=KMeans(n_clusters=3, n_init=10, random_state=randomSeed) 
    # to create a KMeans model with 3 clusters
    # "n_init=10" is used to run KMeans 10 times with different initializations
    # "random_state=randomSeed" is used to set the random seed for reproducibility
    kMeansModel.fit(extractedNumericalData) 
    # to fit the KMeans model to the data
    if kMeansModel.inertia_ < bestInertiaScore:
        # to check if the current model has a lowest inertia score
        # because inertia_ is the sum of squared distances of samples to their closest cluster center
        # we want to minimize this value
        bestInertiaScore= kMeansModel.inertia_ 
        # to update the best compactness score
        bestKMeansModel= kMeansModel 
        # to update the best KMeans model

labelsOfBestKMeansModel= bestKMeansModel.labels_
# to get the labels of the best KMeans model
# labels_ is the labels of each sample

# we will use the labels to plot the data points
plt.figure(figsize=(10, 6))
plt.scatter(extractedNumericalData[:, 0], extractedNumericalData[:, 1], c=labelsOfBestKMeansModel, cmap='viridis', marker='o', edgecolor='k', s=50)
# to plot the KMeans clusters
# "c=labelsOfBestKMeansModel" is used to color the data points according to their labels
# "cmap='viridis'" is used to set the color map
# "marker='o'" is used to set the marker style
# "edgecolor='k'" is used to set the edge color of the markers
# "s=50" is used to set the size of the markers
plt.title('KMeans Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.grid(True, linestyle='--', alpha=0.7)
# to add grid lines to the plot
# "linestyle='--'" is used to set the line style of the grid lines
# "alpha=0.7" is used to set the transparency of the grid lines
plt.tight_layout()
# to adjust the plot layout
plt.show()

# ============== Gaussian Mixture Model ==============
# we will run Gaussian Mixture Model multiple times with different values of random seeds
# and we will use the best model with the highest log likelihood score

GaussianMixtureModel= GaussianMixture(n_components=3, n_init=10, random_state=0)
# to create a Gaussian Mixture Model with 3 components
# "n_init=10" is used to run Gaussian Mixture Model 10 times with different initializations
GaussianMixtureModel.fit(extractedNumericalData)
# to fit the Gaussian Mixture Model to the data
labelsOfGaussianMixtureModel= GaussianMixtureModel.predict(extractedNumericalData)
# to get the labels of the Gaussian Mixture Model
# "predict" is used to predict the labels of each sample
# we will use the labels to plot the data points
GaussianMixtureModelMeans= GaussianMixtureModel.means_
# to get the means of the Gaussian Mixture Model
# "means_" is the means of each component
print("Means of the Gaussian Mixture Model: ", GaussianMixtureModelMeans)
plt.figure(figsize=(10, 6))
# to plot the Gaussian Mixture Model clusters
plt.scatter(extractedNumericalData[:, 0], extractedNumericalData[:, 1], c=labelsOfGaussianMixtureModel, cmap='viridis', marker='o', edgecolor='k', s=50, alpha=0.5)
# to plot the data points
# "alpha=0.5" is used to set the transparency of the data points
# "c=labelsOfGaussianMixtureModel" is used to color the data points according to their labels
# "cmap='viridis'" is used to set the color map
plt.scatter(GaussianMixtureModelMeans[:, 0], GaussianMixtureModelMeans[:, 1], c='red', marker='X', s=200, label='Means', linewidths=3, edgecolor='white')
# to plot the means of the Gaussian Mixture Model
# "c='red'" is used to set the color of the means
# "marker='X'" is used to set the marker style of the means
# "s=200" is used to set the size of the means
# "label='Means'" is used to set the label of the means
plt.title('Gaussian Mixture Model Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
# to add a legend to the plot
plt.grid(True, linestyle='--', alpha=0.7)
# to add grid lines to the plot
plt.tight_layout()
# to adjust the plot layout
plt.show()
# ============== Silhouette Score ==============
# we will use silhouette score to evaluate the clustering performance for KMeans when k=2,3,4

silhouetteScores= {}
# to store the silhouette scores for each value of k
for k in [2,3,4]:
    kMeansModel= KMeans(n_clusters=k, n_init=10, random_state=0)
    labelsForCluster= kMeansModel.fit_predict(extractedNumericalData)
    # to fit the KMeans model to the data and get the labels
    silhouetteScore= silhouette_score(extractedNumericalData, labelsForCluster)
    # to calculate the silhouette score
    silhouetteScores[k]= silhouetteScore
    # to store the silhouette score for each value of k
    # to print the silhouette scores
    print("Silhouette Scores: ", silhouetteScores)

bestKMeansScore= max(silhouetteScores, key=silhouetteScores.get)
# to get the best KMeans score
bestSilhouetteScore= silhouetteScores[bestKMeansScore]
# to get the best silhouette score
print(f"Best Silhouette Score: {bestSilhouetteScore}")
# to print the best silhouette score
git push -u origin main







