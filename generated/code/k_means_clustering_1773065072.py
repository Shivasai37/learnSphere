# Required libraries
# numpy: The NumPy library for efficient numerical computation
# matplotlib: The Matplotlib library for data visualization
# random: The random library for generating random numbers
# sklearn: The scikit-learn library for machine learning

import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.cluster import KMeans

class KMeansClustering:
    def __init__(self, k, max_iters=100):
        # Initialize the number of clusters (k) and the maximum number of iterations
        self.k = k
        self.max_iters = max_iters

    def _init_centroids(self, data):
        # Initialize the centroids by randomly selecting k data points
        indices = random.sample(range(data.shape[0]), self.k)
        return data[indices]

    def _assign_clusters(self, data, centroids):
        # Assign each data point to the nearest centroid
        distances = np.sqrt(np.sum((data[:, np.newaxis] - centroids) ** 2, axis=2))
        return np.argmin(distances, axis=1)

    def _update_centroids(self, data, cluster_assignments):
        # Update the centroids by taking the mean of all data points in each cluster
        centroids = np.array([data[cluster_assignments == i].mean(axis=0) for i in range(self.k)])
        return centroids

    def fit(self, data):
        # Initialize the centroids
        centroids = self._init_centroids(data)
        
        # Repeat the clustering process until convergence or the maximum number of iterations
        for _ in range(self.max_iters):
            # Assign each data point to the nearest centroid
            cluster_assignments = self._assign_clusters(data, centroids)
            
            # Update the centroids
            new_centroids = self._update_centroids(data, cluster_assignments)
            
            # Check for convergence
            if np.all(centroids == new_centroids):
                break
            
            # Update the centroids for the next iteration
            centroids = new_centroids
        
        return centroids, cluster_assignments

# Main execution block
if __name__ == "__main__":
    # Generate some sample data
    np.random.seed(0)
    data = np.random.rand(100, 2)

    # Create a KMeansClustering object with 3 clusters
    kmeans = KMeansClustering(k=3)

    # Run the K-means clustering algorithm
    centroids, cluster_assignments = kmeans.fit(data)

    # Print the centroids
    print("Centroids:")
    print(centroids)

    # Print the cluster assignments
    print("\nCluster Assignments:")
    print(cluster_assignments)

    # Visualize the clusters
    plt.scatter(data[:, 0], data[:, 1], c=cluster_assignments)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.5)
    plt.show()

    # Compare with scikit-learn's KMeans
    kmeans_sklearn = KMeans(n_clusters=3)
    kmeans_sklearn.fit(data)
    print("\nScikit-learn Centroids:")
    print(kmeans_sklearn.cluster_centers_)
    print("\nScikit-learn Cluster Assignments:")
    print(kmeans_sklearn.labels_)