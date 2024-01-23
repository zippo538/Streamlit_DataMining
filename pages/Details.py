from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="Information e commerce", layout="wide")

st.title("information e commerce")
st.divider()


@st.cache_data
def load_data():
    return pd.read_csv("data/data_e-commerse.csv")
    
data = load_data()
tab1,tab2 = st.tabs(['Pemesanan','Pendapatan'])

with tab1 :
    # Per Jam
    st.header('Pembelian Pelanggan Per Jam')
    data["order_purchase_timestamp"] = pd.to_datetime(data["order_purchase_timestamp"])
    orderbyhour = data.groupby(data["order_purchase_timestamp"].dt.hour)["order_id"].count().reset_index().sort_values(by="order_purchase_timestamp", ascending=False)
    orderbyhour.rename(columns={"order_id":"Total Orders", "order_purchase_timestamp": "Hour of Day"}, inplace=True)

    # Per Hari
    orderbydow = data.groupby(data["order_purchase_timestamp"].dt.day_name())["order_id"].count().reset_index()
    orderbydow.rename(columns={"order_id":"Total Orders", "order_purchase_timestamp": "Weekday Name"}, inplace=True)
    orderbydow = orderbydow.sort_values(by="Total Orders", ascending=False)

    col1, col2 = st.columns([3, 3])

    col1.subheader("Per Jam")
    col1.bar_chart(orderbyhour,x='Hour of Day',y='Total Orders')

    col2.subheader("Per Hari")
    col2.bar_chart(orderbydow,x='Weekday Name',y='Total Orders')


with tab2 :
    top_customers = data.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    top_customers.rename(columns={"payment_value":"total_paid"}, inplace=True)

    # ganti nama
    name = ['Dwight Stout','Consuelo Stewart','Karin Conrad','Bud Skinner','Ruth Farley','Ronda Ortiz','Deann Kramer','Nathanial Woodward','Milo Edwards','Diego Marquez']
    #for i in range(1,10):
    #    top_customers[:10]['customer_unique_id'] = top_customers[:10]['customer_unique_id'].str.replace(top_customers['customer_unique_id'][i],name[i])    

    st.subheader("Top 10 Customer")
    st.bar_chart(top_customers[:10],x="customer_unique_id",y="total_paid")



