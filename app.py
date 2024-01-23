import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.metrics import silhouette_score
import streamlit as st


@st.cache_data
def load_data_standar():
    return pd.read_csv("data/RFM_set-standar.csv")
def load_data():
    return pd.read_csv("data/RFM_set.csv")

rfm_df = load_data()
rfm_df_log= load_data_standar()


#standarkan data

scaler = StandardScaler()
scaler.fit(rfm_df_log.drop("customer_unique_id", axis=1))
RFM_Table_scaled = scaler.transform(rfm_df_log.drop("customer_unique_id", axis=1))
RFM_Table_scaled = pd.DataFrame(RFM_Table_scaled, columns=rfm_df_log.columns[1:])


# Cluster menggunakan method elbow
def elbw_mthd() :
        kmean_model = KMeans(n_clusters=4, random_state=5)
        kmean_y = kmean_model.fit(RFM_Table_scaled)
        centers = kmean_model.cluster_centers_

        rfm_df['Cluster'] = kmean_model.labels_
        st.header("Hasil Cluster menggunakan elbow method")

        df_new = rfm_df.groupby(['Cluster']).agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': ['mean', 'count']
                
        }).round(0)
        return df_new

df_elbw = elbw_mthd()
st.table(df_elbw)

# Cluster menggunakan Silhoutte Coeffieciency
def slht_mthd() :
    kmean_model = KMeans(n_clusters=2, random_state=5)
    kmean_y = kmean_model.fit_predict(RFM_Table_scaled)
    rfm_df['Cluster'] = kmean_model.labels_

    st.header("Hasil Cluster menggunakan Silhoutte Coeffiecieny method")


    df_new = rfm_df.groupby(['Cluster']).agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': ['mean', 'count']
    }).round(0)
    return df_new
df_slht = slht_mthd()

st.table(df_slht)