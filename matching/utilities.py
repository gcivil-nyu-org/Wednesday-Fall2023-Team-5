# Import required libraries
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors


# Function for data pre-processing: Convert categorical to numerical attributes
def pre_process_data(data):
    # one hot encode interests column with multi-label Binarizer as it a multi-label column
    mlb = MultiLabelBinarizer()
    data_encoded = data.join(
        pd.DataFrame(
            mlb.fit_transform(data["userprofile__interests"]), columns=mlb.classes_
        )
    )

    # one hot encode remaining categorical columns
    data_encoded = pd.get_dummies(
        data_encoded,
        columns=[
            "userprofile__drink_pref",
            "userprofile__smoke_pref",
            "userprofile__edu_level",
        ],
    )
    # drop interests column post encoding
    data_encoded = data_encoded.drop("userprofile__interests", axis=1)

    return data_encoded


def create_knn_model(data):
    # Create a KNN model
    knn = NearestNeighbors(n_neighbors=3, metric="cosine")  # n_neighbors set to 3

    # Fit the KNN model on the feature matrix
    knn.fit(data)

    return knn


# Function to get recommendations for a user based on their attributes
def get_recommendations(knn, data, user_attributes, num_recommendations=5):
    user_attributes = [user_attributes]
    distances, indices = knn.kneighbors(user_attributes)
    recommended_users = data.iloc[indices[0]].drop(
        columns=[col for col in data.columns if col != "userprofile__user"]
    )
    return recommended_users.head(num_recommendations), distances


def get_knn_recommendations(data, curr_user):
    # perform data preprocessing on match pool
    data_encoded = pre_process_data(data)

    # create KNN model:
    knn = create_knn_model(data_encoded)

    # Get Recommendations:
    # index of the user you want recommendations for
    user_index = data_encoded[
        data_encoded["userprofile__user"] == curr_user
    ].index.values.astype(int)[0]
    print("user_index:", user_index)
    user_attributes = data_encoded.iloc[user_index]
    # print(user_attributes)
    recommendations, distances = get_recommendations(
        knn, data_encoded, user_attributes, num_recommendations=3
    )
    recommendations = recommendations["userprofile__user"].tolist()
    print("Recommended people:")
    print(recommendations)
    print(distances)

    return recommendations
