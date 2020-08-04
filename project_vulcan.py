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
    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.sidebar.file_uploader("Choose a csv file...", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        fp = st.sidebar.selectbox("Select shapefile ", os.listdir("shape_files/"))

        map_df = st.cache(gpd.read_file)("shape_files/" + str(fp))

        keys = st.multiselect("Select columns", data.columns)
        fix = st.selectbox("Set index column",data.columns)

        values = []
        for item in keys:
            values.append(st.sidebar.selectbox("Choose one", data[item].unique()))
        indicator = st.sidebar.selectbox("Choose indicator", list(data.columns))

        dictionary = dict(zip(keys, values))
        st.write("Dictionary of selected items", dictionary)
        if st.checkbox("Show Selected Data and stats"):
            test = show_data(data, dictionary, indicator)
            test = test[[fix] + keys + [str(indicator)]]
            st.write(test)
            st.write(
                "% of NA values in the given column",
                (test[indicator].isna().sum() / test[indicator].count()) * 100,
            )
            st.write("Min value of indicator", test[indicator].min())
            st.write("Max value of indicator", test[indicator].max())
            st.write("Column data type", test[indicator].dtype)
        # sns.boxplot(y = indicator,data = df)
        # st.write('Outliers')
        # st.pyplot()   
        if st.checkbox("Show Raw Data"):
            st.write("Raw Data", data)
    else:
        st.write("Upload a file to be Checked")


start = timer()
main()
end = timer()
print("time taken = ", (end - start))
