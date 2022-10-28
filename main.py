import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Streamlit 入門')

st.write('DataFrame')

df = pd.read_csv('Pstats_2019.csv')
df_columns = df.columns

df[1:4]
st.dataframe(df)

x = st.selectbox("X", df_columns)
y = st.selectbox("Y", df_columns)

fig = plt.figure(figsize = (12,8))
plt.scatter(df[x],df[y])
plt.xlabel(x, fontsize = 18)
plt.ylabel(y, fontsize = 18)
st.pyplot(fig)