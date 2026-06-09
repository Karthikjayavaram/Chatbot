import streamlit as st 
from langraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

def generate_unique_id():
    unique_id = uuid.uuid4()
    return unique_id

def add_thread(unique_id):
    st.session_state['chat_thread'].append(unique_id)
    
def reset_chat():
    thread_id = generate_unique_id()
    st.session_state['unique_id'] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def load_conversation(unique_id):
    return chatbot.get_state(config={'configurable':{'thread_id':unique_id}}).values.get('messages',[])

if 'message_history' not in st.session_state:
     st.session_state['message_history'] = []
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] = generate_unique_id()
if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = [
        st.session_state['unique_id']
    ]



# SideBar_UI
st.sidebar.title("Karthiks Chatbot")
if st.sidebar.button("Add New Conversation",key="add"):
    reset_chat()
st.sidebar.header("My Conversations")

for thread in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thread),key=f"thread_{thread}"):
        st.session_state['unique_id'] = thread
        msgs = load_conversation(thread)
        temp_msgs = []
        for msg in msgs:
            if isinstance(msg,HumanMessage):
                role = "user"
            else:
               role = "ai"
            temp_msgs.append({ "role" : role,'content':msg.content})
        st.session_state['message_history'] = temp_msgs
     
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
         st.text(message['content'])


CONFIG = {'configurable':{'thread_id':st.session_state['unique_id']}}

user_input = st.chat_input("Please place your query")

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    with st.chat_message("ai"):
        ai_response = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
               {'messages' : [HumanMessage(content=user_input)]},
               config=CONFIG,
               stream_mode='messages'
            )
        )
        st.session_state['message_history'].append({'role':'ai','content':ai_response})