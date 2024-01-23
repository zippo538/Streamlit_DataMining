from matplotlib import pyplot as plt
from scipy import stats
import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Recency Monetary Frequency", layout="wide")

st.title("Recency Monetary Frequency")
st.divider()

@st.cache_data
def load_data():
    return pd.read_csv("data/data_e-commerse.csv")

data = load_data()

tab1,tab2 = st.tabs(['Before','After'])

df_recency = data.groupby(by='customer_unique_id', as_index=False)['order_purchase_timestamp'].max()
df_recency.rename(columns={"order_purchase_timestamp":"LastPurchaseDate"}, inplace=True)
df_recency["LastPurchaseDate"] = pd.to_datetime(df_recency["LastPurchaseDate"],errors='coerce')
# Get recent invoice date and use it to calculate recency
recent_date = pd.to_datetime(data["order_purchase_timestamp"],errors='coerce').max()

df_recency['Recency'] = df_recency['LastPurchaseDate'].apply(lambda x: (recent_date - x).days)

frequency_df = data.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index()
frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)

monetary_df = data.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
monetary_df.columns = ['customer_unique_id', 'Monetary']

rf_df = df_recency.merge(frequency_df, on='customer_unique_id')
rfm_df = rf_df.merge(monetary_df, on='customer_unique_id').drop(columns='LastPurchaseDate')

rfm_df[rfm_df.columns[1:]] = rfm_df[rfm_df.columns[1:]].applymap(lambda x: 1 if x ==0 else x)

skew = stats.skew(rfm_df['Recency'])
skewtest = stats.skewtest(rfm_df['Recency'])

def check_skew(df_skew, column):
    skew = stats.skew(df_skew[column])
    skewtest = stats.skewtest(df_skew[column])
    plt.title('Distribution of ' + column)
    sns.distplot(df_skew[column])
    plt.show()
    st.pyplot(plt)
    st.caption("{}'s: Skew: {}, : {}".format(column, skew, skewtest))
    return

with tab1 :
    for col in rfm_df.columns[1:]:
        check_skew(rfm_df, col)
        
with tab2 :
    # standarkan data
    rfm_df_log = rfm_df.copy()
    for c in rfm_df.columns[2:]:
        rfm_df_log[c] = np.log10(rfm_df_log[c])
    
    for col in rfm_df.columns[1:]:
        check_skew(rfm_df_log, col)