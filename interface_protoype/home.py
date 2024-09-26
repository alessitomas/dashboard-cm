import shutil
import streamlit as st
import pandas as pd
import os
import requests
import json
from io import StringIO
from datetime import datetime


if 'cm' not in st.session_state:
    st.session_state.cm = False

if 'param' not in st.session_state:
    st.session_state.param = {}

st.title("CM Interface")

file_path = ""

file_select = st.sidebar.selectbox(
    'File Read Options',
    ('Relative Path', 'Upload','Default')
)

if file_select == "Relative Path":
    file_path = st.sidebar.text_input(
        "Enter the Relative Path Here! 👇"
    )

    if file_path:
        st.write("You entered: ", file_path)

elif file_select == 'Upload':

    uploaded_file = st.sidebar.file_uploader(
        'What is your input file?'
    )

    if uploaded_file is not None:

        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        date = "-".join(str(datetime.now()).split('.')[0].split(' '))

        print(date)

        with open(f'../api/data/file_{date}.tsv', 'w') as fd:
            stringio.seek(0)
            shutil.copyfileobj(stringio, fd)

        file_path = f'./data/file_{date}.tsv'


algorithm = st.sidebar.selectbox(
    'What is your clustering algorithm?',
    ('Leiden-CPM', 'Leiden-Mod', 'infomap','sbm')
)

if algorithm == 'Leiden-CPM':
    st.session_state.param = {}
    resolution = st.sidebar.number_input(label= "resolution", value= 0.001, format="%f")
    iteration = st.sidebar.number_input(label= "iterations", value= 2)
    st.session_state.param["res"] = float(resolution)
    st.session_state.param["i"] = int(iteration)
    clustering_algorithm = 'leiden'
elif algorithm == 'Leiden-Mod':
    st.session_state.param = {}
    iteration = st.sidebar.number_input(label= "iterations", min_value=1, max_value=100, step=1, value=1)
    clustering_algorithm = 'leiden_mod'
    if iteration is not None:
        print(iteration)
        st.session_state.param["i"] = int(iteration)
elif algorithm == 'infomap':
    st.session_state.param = {}
    clustering_algorithm = 'infomap'
elif algorithm == "sbm":
    st.session_state.param = {}
    
    block_state = st.sidebar.selectbox(
        "Select block state:",
        options=["non_nested_sbm", "planted_partition_model"]
    )

    degree_corrected = st.sidebar.checkbox(
        "Degree corrected", value=False
    )
    
    st.session_state.param["block_state"] = block_state 
    st.session_state.param["degree_corrected"] = degree_corrected 
    clustering_algorithm = 'sbm'

post_treatment = st.sidebar.selectbox(
    'What is your clustering Post Treatment?',
    ('None', 'CM-CC', 'CM-WCC')
)

if post_treatment == "CM-CC":
    st.session_state.post_treatment = "cc"
elif post_treatment == "CM-WCC":
    st.session_state.post_treatment = "wcc"
else:
    st.session_state.post_treatment = ""




if st.button("Run CM Pipeline"):
    
    data = {
        "algo_name" : clustering_algorithm,
        "params": st.session_state.param,
        "file_path": file_path,
        "post_treatment": st.session_state.post_treatment
    }
    res = requests.post('http://127.0.0.1:8000/pipeline', data= json.dumps(data))
    st.write(res)






