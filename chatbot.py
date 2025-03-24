import streamlit as st
import time
import requests
from io import BytesIO

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


def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]


if "history" not in st.session_state:
    st.session_state.history = []

st.logo(("./deep-peek-ui/deep_peek.jpg"),size="medium")
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

if prompt := st.chat_input("Say something",accept_file=True,
    file_type=["txt","csv"],
):
    print(prompt)
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