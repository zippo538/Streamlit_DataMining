from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import silhouette_score
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np

@st.cache_data
def load_data():
    return  pd.read_csv("data/RFM_set-standar.csv")

data = load_data()

tab1,tab2 = st.tabs(['Elbow Method','Silhoutte Coeficiency'])

scaler = StandardScaler()
scaler.fit(data.drop("customer_unique_id", axis=1))
RFM_Table_scaled = scaler.transform(data.drop("customer_unique_id", axis=1))
RFM_Table_scaled = pd.DataFrame(RFM_Table_scaled, columns=data.columns[1:])



with tab1:
        distortions = []
        K = range(1,10)
        disc_log= pd.DataFrame(data=distortions)
        for k in K:
            kmeanModel = KMeans(n_clusters=k)
            kmeanModel.fit(RFM_Table_scaled)
            distortions.append(kmeanModel.inertia_)
        plt.figure(figsize=(5,6))
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()
        st.pyplot(plt)
        st.caption("Terlihat pada cluster 4 mulai mendatar")
        disc_log
        
with tab2 :
     
     # Evaluation with metric silhoutte score
    scores= []
    for n in range(2,10) :
        kmeans = KMeans(n_clusters=n)
        y_pred_kmeans = kmeans.fit_predict(RFM_Table_scaled)

        scores.append(silhouette_score(RFM_Table_scaled,y_pred_kmeans))
        
    plt.plot(range(2,10),scores)
    plt.title('number of cluster vs silhouette_score')
    plt.xlabel('number of cluster')
    plt.ylabel('silhouette_score')
    st.pyplot(plt)


       
