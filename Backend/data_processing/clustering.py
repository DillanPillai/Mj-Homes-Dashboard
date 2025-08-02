# Clusters property data using KMeans based on latitude, longitude, and price, therefore returns list of properties with assigned cluster labels
from sklearn.cluster import KMeans
import pandas as pd

def cluster_properties(data: list[dict], n_clusters: int = 3):
    df = pd.DataFrame(data)

    if df.empty or len(df) < n_clusters:
        return []

    X = df[["latitude", "longitude", "price"]]

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df["cluster"] = kmeans.fit_predict(X)

    return df[["id", "latitude", "longitude", "price", "cluster"]].to_dict(orient="records")
