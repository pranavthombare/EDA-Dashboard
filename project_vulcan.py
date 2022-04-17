import os
# Keep it clean
import warnings
# Timer
from timeit import default_timer as timer
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt

# Streamlit
import streamlit as st

def show_data(data, dictionary, indicator):
    query = ' & '.join(['`{}`=="{}"'.format(k, str(v)) for k, v in dictionary.items()])
    df = data.copy()
    df = df.query(query)
    return df


def main():
    st.header("EDA Dashboard")
    st.sidebar.title("Settings")
    st.set_option("deprecation.showfileUploaderEncoding", False)

    uploaded_file = st.sidebar.file_uploader("Choose a csv file...", type="csv")
    if uploaded_file is not None:
        # We load the csv file.
        data = pd.read_csv(uploaded_file)

        # Select a column to get the stats for.
        indicator = st.sidebar.selectbox("Choose a column", list(data.columns))
        st.subheader(f"Analysis of the column: {indicator}")

        # We need to fix a column to set it as an index.
        freeze = st.sidebar.selectbox("Choose a column to freeze", list(data.columns))
        
        # And now we print the stats of the column
        st.write("Column data type", data[indicator].dtype)
        st.write("The number of items in the selected columns = ",data[indicator].count())

        # More stats depending on the column type. 
        # Doesn't makes sense to calculate mean for "object" type column
        if (data[indicator].dtype == "int64" or data[indicator].dtype == "float64"):
            st.write("The max value in the selected column is = ",data[indicator].max())
            st.write("The min value in the selected column is = ",data[indicator].min())
            st.write("The mean of the selected column is = ",data[indicator].sum()/data[indicator].count())
            
            # Now we select only 2 rows: the index column and the column we need stats for
            subset = data[[freeze,indicator]]
            vis = alt.Chart(subset).mark_bar().encode(x=freeze, y=indicator)
            st.altair_chart(vis)
 
        if st.checkbox("Show Raw Data"):
            st.write("Raw Data", data)
    else:
        st.write("Upload a file to be Checked")


start = timer()
main()
end = timer()
print("time taken = ", (end - start))
