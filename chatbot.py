import streamlit as st
import time
import requests
from io import BytesIO
import json

def chat_stream(prompt):
    print(type(prompt['files'][0]))
    transactions = BytesIO(prompt['files'][0].read())
    with open("output.txt","wb") as f:
        f.write(transactions.getbuffer())
    
    
    response = requests.post('http://127.0.0.1:8000/process-text',file={"file":transactions},headers= {
                    'Accept': 'application/json',
                })
    statusbar =  st.sidebar.status("Calculating risk...")
    print(response.json())
    statusbar.write("Preprocessing the data")
    
    for char in response:
        yield char
        #time.sleep(0.02)
        statusbar.write("Learning about the entities")
        #time.sleep(139)
        statusbar.write("Calculating the risk")
        #time.sleep(45)
        statusbar.write("Publishing the report")
        #time.sleep(37)


def upload_file(file):
    try:
        downloadable_file = None
        files = {"file":file.getvalue()}
        response = requests.post("http://127.0.0.1:8000//generate-report",files=files)

        if(response.status_code==200):
            return response.json()
        else:
            st.error(f"Error while uploading file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None


def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]


if "history" not in st.session_state:
    st.session_state.history = []

st.logo(("./deep_peek.jpg"),size="medium")
st.write("DEEP PEEK")

for i, message in enumerate(st.session_state.history):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            feedback = message.get("feedback", None)
            st.session_state[f"feedback_{i}"] = feedback
            st.feedback(
                "thumbs",
                key=f"feedback_{i}",
                disabled=feedback is not None,
                on_change=save_feedback,
                args=[i],
            )

downloadable_file = None

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt","csv"])
if uploaded_file and st.sidebar.button("Upload"):
    with st.spinner("Uploading..."):
        upload_response = upload_file(uploaded_file)
        upload_response = json.loads(upload_response['results'])
        print("RESULTSSSSS"+str(upload_response.keys()))

        if upload_response:
            if(upload_response['pdf']!= None):
                downloadable_file = upload_response['pdf']
            st.sidebar.success(f"File uploaded successfully .")
            st.write((upload_response['results']))

if(downloadable_file!=None):
    st.sidebar.download_button('Download Report',downloadable_file,file_name='Risk Report',mime='application/pdf')

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.write(prompt.files)
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = st.write_stream(chat_stream(prompt))
        st.feedback(
            "thumbs",
            key=f"feedback_{len(st.session_state.history)}",
            on_change=save_feedback,
            args=[len(st.session_state.history)],
        )
    st.session_state.history.append({"role": "assistant", "content": response})