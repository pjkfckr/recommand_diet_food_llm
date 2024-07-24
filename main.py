import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from nlp import create_chain

st.title("간단한 식단 추천")

# Initialize chat history
history = StreamlitChatMessageHistory()

# 채팅 메시지 히스토리 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# Display chat history
for message in history.messages:
    st.chat_message(message.type).write(message.content)

# User input
prompt = st.chat_input("섭취해야하는 영양성분과 식사분량을 입력해주세요")

if prompt:
    # Save user message to history
    history.add_user_message(prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        agent_chain = create_chain(history)
        try:
            response = agent_chain.invoke(
                {"input": prompt},
                {"callbacks": [callback]}
            )
            # Save assistant message to history
            history.add_ai_message(response["output"])

            st.markdown(response["output"])
        except Exception as e:
            st.error(f"An error occurred: {e}")

