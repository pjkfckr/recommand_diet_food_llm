import os

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

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


def create_chain(history):
    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True
    )

    agent = create_openai_tools_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, memory=memory)
