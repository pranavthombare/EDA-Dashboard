import os
# Keep it clean
import warnings
# Timer
from timeit import default_timer as timer
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit
import streamlit as st

def show_data(data, dictionary, indicator):
    query = ' & '.join(['`{}`=="{}"'.format(k, str(v)) for k, v in dictionary.items()])
    df = data.copy()
    df = df.query(query)
    return df


def main():
    st.header("Project Vulcan")
    st.subheader("Filter Selection")
    st.sidebar.title("Settings")

    uploaded_file = st.sidebar.file_uploader("Choose a csv file...", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        fp = st.sidebar.selectbox("Select shapefile ", os.listdir("shape_files/"))

        map_df = st.cache(gpd.read_file)("shape_files/" + str(fp))

        filters = st.multiselect("Select columns", data.columns)

        filter_list = []
        for item in filters:
            filter_list.append(st.sidebar.selectbox("Choose one", data[item].unique()))
        indicator = st.sidebar.selectbox("Choose indicator", list(data.columns))

        dictionary = dict(zip(filters, filter_list))
        st.write("Dictionary of selected items", dictionary)
        if st.checkbox("Show Selected Data"):
            test = show_data(data, dictionary, indicator)
            test = test[filters + [str(indicator)]]
            st.write(test)

        if st.checkbox("Show Raw Data"):
            st.write("Raw Data", data)
    else:
        st.write("Upload a file to be Checked")


start = timer()
main()
end = timer()
print("time taken = ", (end - start))
