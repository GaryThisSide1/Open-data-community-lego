from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
le = LabelEncoder()
# Load your data into a pandas dataframe
data = pd.read_csv("climate-grant-votes/climate_grant_votes.csv")

# Define the features you want to use for anomaly detection
X = data[["source_wallet", "destination_wallet"]]
X['source_wallet'] = le.fit_transform(X['source_wallet'])
X['destination_wallet'] = le.fit_transform(X['destination_wallet'])
# Create an instance of the LocalOutlierFactor class
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)

# Fit the model to your data
lof.fit(X)

# Use the decision_function method to assign a score to each data point
scores = lof.negative_outlier_factor_

# Create a column in your dataframe to store the scores
data["anomaly_score"] = scores

# Identify the data points with the highest anomaly scores
anomalies = data[data["anomaly_score"] < -1]
# highest_score = round(anomalies["anomaly_score"].max(), 2)
# print(highest_score)
highest_index = round(anomalies["anomaly_score"].idxmax(),2)
highest_anomaly = anomalies.loc[highest_index]

#print the highest anomaly score and the corresponding data
print("highest anomaly score:",highest_anomaly["anomaly_score"])
print("highest anomaly data:",highest_anomaly)
import matplotlib.pyplot as plt

# Create a scatter plot of feature_1 vs feature_2
plt.scatter(data["source_wallet"], data[ "destination_wallet"], c=data["anomaly_score"], cmap='viridis')
plt.colorbar()
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Anomaly Score")
plt.show()
