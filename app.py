import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import streamlit as st
# Hide PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)


# dashboard title
st.title("Payment type and review distribution")

#=-=-=-=-=-=-=-=-=-==-
#mengambil data yang dibutuhkan
order_reviews_df = pd.read_csv("data/order_reviews_dataset.csv", delimiter=",")
sellers_df = pd.read_csv("data/sellers_dataset.csv", delimiter=",")
orders_df = pd.read_csv("data/orders_dataset.csv", delimiter=",")
customers_df = pd.read_csv("data/customers_dataset.csv", delimiter=",")
orders_df.dropna(subset=['order_delivered_carrier_date', 'order_delivered_customer_date','order_approved_at'], inplace=True)


customers_df.rename(columns={'customer_state': 'state'}, inplace=True)
sellers_df.rename(columns={'seller_state': 'state'}, inplace=True)

customers_state_counts = customers_df.groupby('state').customer_id.nunique()
sellers_state_counts = sellers_df.groupby('state').seller_id.nunique()
merged_counts = pd.concat([customers_state_counts, sellers_state_counts], axis=1, keys=['Customers', 'Sellers'])

datetime_or = ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
for column in datetime_or:
  orders_df[column] = pd.to_datetime(orders_df[column])
  orders_df.info()


delivery_time = orders_df["order_delivered_customer_date"] - orders_df["order_delivered_carrier_date"]
delivery_time = round(delivery_time.apply(lambda x: x.total_seconds())/86400,1)
orders_df["delivery_time"] = delivery_time



# select the type of users
selected_feature = st.selectbox('Select type of data', ['Customers vs Sellers', 'Review and Score Dist.'])


if selected_feature == 'Review and Score Dist.':
    merged_df = pd.merge(orders_df, order_reviews_df, on='order_id')
    selected_plot = st.selectbox('Select Plot', ['Scatter Plot', 'Box Plot', 'Violin Plot'])
    if selected_plot == 'Scatter Plot':
        # Plotting the scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(merged_df['delivery_time'], merged_df['review_score'], alpha=0.5)
        plt.title('Scatter Plot of Delivery Time vs Review Score')
        plt.xlabel('Delivery Time (days)')
        plt.ylabel('Review Score')
        plt.grid(True)
        plt.show()
    elif selected_feature == 'Box Plot':
        plt.figure(figsize=(12, 8))
        sns.boxplot(x=pd.cut(merged_df['delivery_time'], bins=[0, 10, 20, 30, 40, 50, 100, float('inf')], labels=['0-10', '11-20', '21-30', '31-40', '41-50', '51-100', '100+']), y=merged_df['review_score'])
        plt.title('Box Plot of Review Score vs Delivery Time')
        plt.xlabel('Delivery Time (days)')
        plt.ylabel('Review Score')
        plt.show()
    elif selected_feature == 'Violin Plot':
        plt.figure(figsize=(12, 8))
        sns.violinplot(x=pd.cut(merged_df['delivery_time'], bins=[0, 10, 20, 30, 40, 50, 100, float('inf')], labels=['0-10', '11-20', '21-30', '31-40', '41-50', '51-100', '100+']), y=merged_df['review_score'])
        plt.title('Violin Plot of Review Score vs Delivery Time')
        plt.xlabel('Delivery Time (days)')
        plt.ylabel('Review Score')
        plt.show()



    
elif selected_feature == 'Customers vs Sellers':
    merged_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Number of Customers and Sellers by State')
    plt.xlabel('State')
    plt.ylabel('Count')
    plt.show()
