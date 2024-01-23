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
        kmeans.fit(RFM_Table_scaled)        
        silhouette = silhouette_score(RFM_Table_scaled, kmeans.labels_)
        scores.append(silhouette)
        #st.caption("Nilai Cluster : ", n ,'Nilai Silhoutte : ' , silhouette )
        
    #scores
        
    st.write("Silhouette Scores for Different Numbers of Clusters")
    st.line_chart(scores)


       
