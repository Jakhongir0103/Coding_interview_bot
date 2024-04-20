import os
import sys

from langchain_openai import ChatOpenAI
# from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


import keys

os.environ["OPENAI_API_KEY"] = keys.opai_key

# true answer classifier
next_answer_classifier = ChatOpenAI(model="gpt-4-turbo")

# python code classifier
chat_classifier = ChatOpenAI(model="gpt-4-turbo")

# create a chain with chat history
chat = ChatOpenAI(model="gpt-4-turbo")
system_prompt = """You are a senior recruiter in Google with years of experience with having a coding interview with the candidates.
Right now you are doing an coding interview from an candidate who is applying to a position in Google.
Throughout the interview act just like a human interviewer, and not like a chatbot nor an assistant.
You Ask medium level leetcode questions."""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
chain = prompt | chat
demo_ephemeral_chat_history_for_chain = ChatMessageHistory()
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# create an agent with code execution
tools = [PythonREPLTool()]
instructions = """You are an agent designed to execute python code.
You have access to a python REPL, which you can use to execute python code.
You are given a python function with some examples.
Execute the function with the given examples, and return both the examples and the output of the execution.
If the given python code is only a function, think of an example to use that function, and return both the example you have used and the output of the execution.
If the function returns an error, return the error statement directly, without trying to correct it.
NEVER modify the python code you are given.
"""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_openai_functions_agent(ChatOpenAI(temperature=0, model="gpt-4-turbo"), tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


# functions
def get_answer(prompt_text):
  response = chain_with_message_history.invoke(
    {"input": prompt_text},
    {"configurable": {"session_id": "unused"}},
  )
  return response.content

def execute_code(input):
  output = agent_executor.invoke({"input": input})
  return output['output']

def contains_python(text, prompt_text="""You are given a text. 
Return YES if the text includes an executable python code.
Return NO if the text does not include any executable python code, even if the text mentions the python.
Return only YES or NO with no additional information.
### text
{text}

### YES or NO
"""):
  response = chat_classifier.invoke(
      [
          HumanMessage(
              content=prompt_text.format(text=text)
          )
      ]
  )
  return response.content

def is_correct(text, prompt_text="""You are given a feedback on an answer to a coding question.
Read the feedback and determine if the feedback suggests that they have moved to a new question.
Return YES if the feedback suggest that they have moved on to a new question, whether the given answer is correct or wrong.
Return NO if the feedback suggest that they have not moved on to a new question, but the feedback asks to rethink.
Return only YES or NO with no additional information.
### text
{text}

### YES or NO
"""):
  response = next_answer_classifier.invoke(
      [
          HumanMessage(
              content=prompt_text.format(text=text)
          )
      ]
  )
  return response.content

def clear_history():
  demo_ephemeral_chat_history_for_chain.clear()
