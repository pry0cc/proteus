#!/usr/bin/env python3
import streamlit as st
import pymongo
from pymongo import MongoClient
import pandas as pd
import string
import io
import re
import lxml

st.set_page_config(
     page_title="ASM Viewer",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded"
     
 )

st.title("ASM Viewer")
st.sidebar.header('ASM Viewer')
scans = st.sidebar.text_input('Scan Search')
st.sidebar.info('Please start by typing the target id.')

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient("mongodb://127.0.0.1:27017")

client = init_connection()

# pipeline for subs


def query(scans,keywords):

    subspipeline = [
    {
        "$match": {
            'target_id': '%s' % (scans)
        }
    }, 
    {
        "$sort": {
            "scan_id": pymongo.ASCENDING
        }
    },
    {
        "$project": {
        "_id": 0, # Change to 0 if you wish to ignore "_id" field.
        "name": 1,
        "host": 1,
        "source": 1,
        "scan_id": 1
    }
  }]

    result = client['asm']['subs'].aggregate(subspipeline)

    results_as_dataframe = pd.DataFrame(list(result))

    return results_as_dataframe



if st.sidebar.button('Search'):
    df = query(scans,scans)
    if df.empty:
        st.error("No matches found!")
    else:
        st.write(df)
