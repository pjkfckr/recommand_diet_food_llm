import os

import streamlit as st
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model=os.environ['OPENAI_API_MODEL'], temperature=float(os.environ['OPENAI_API_TEMPERATURE']))

output_parser = StrOutputParser()
# 다음 context에 기반해 답변해주세요. 적당한 답변이 없다면 만들어서 답변해주세요
prompt = ChatPromptTemplate.from_template(
    """
    성인 남자의 경우 평균 2500kcal, 성인 여성의 경우 2000kcal이 권장량입니다.
    한끼에 20g이상 35g이하의 단백질을 포함해주세요.
    식물성과 동물성을 섞어서 답변해주세요.
    식물성은 두부, 유부, 두유, 낫또, 청국장, 된장, 콩가루, 콩비지 만 포함시켜서 답변해주세요.
    최대 5끼 먹을 수 있지만, 3끼를 제일 먼저 권장해주세요.
    닭가슴살, 두부 등 간편식은 5끼에 전부 포함될 수 있지만, 다른음식은 겹치지않게 해주세요.
    다이어트때 먹기 좋은 음식 레시피가 있다면 자세히 추천 해주세요.

    질문: {input}

    Tool 사용 로그: {agent_scratchpad}
    """
)
tools = load_tools(["ddg-search"])


def create_chain(history_chat):
    memory = ConversationBufferMemory(
        chat_memory=history_chat, memory_key="chat_history", return_messages=True
    )

    agent = create_openai_tools_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, memory=memory)


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
            print(response)
            # Save assistant message to history
            history.add_ai_message(response["output"])

            st.markdown(response["output"])
        except Exception as e:
            st.error(f"An error occurred: {e}")

