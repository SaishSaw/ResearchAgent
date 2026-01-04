from openai import OpenAI
from environs import Env
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import ToolMessage,AIMessage,HumanMessage
from tavily import TavilyClient

import chainlit as cl
import regex as re
import json

# load env
env = Env()
env.read_env()



# setup OpenAI client for Deepseek model
client = ChatNVIDIA(
  model="deepseek-ai/deepseek-v3.1-terminus",
  api_key=env.str('LLM_API_KEY'), 
  temperature=0.2,
  top_p=0.7,
  max_tokens=2048,
  )


# helper function

def json_parser(text:str):
  """Return the json from LLM response"""
  pattern = r"```json\s*([\s\S]*?)\s*```"
  match = re.search(pattern,text)
  if not match:
    return None
  if match:
    try:
      return json.loads(match.group(1))
    except JSONDecodeError:
      return None



# expansion for user query.
query_agent = create_agent(
  model = client,
  system_prompt = """
      Given the research topic from user, generate 2 different search queries suitable for finding academic papers.
      Return a json response exactly in the format mentioned
      ```json{{
        "query" : <your_response>
      }}```
    """)


#query_response = query_agent.invoke({"messages":[{"role":"user","content":"Tell me about ML models in biotechnology."}]})
#print(query_response)
#query_result = json_parser(query_response['messages'][1].content)
#print(query_result)


tavily = TavilyClient(api_key=env.str("TAVILY_API"))
# tavily search function
@tool("research_search",description="Use this tool for searching academic research papers, survey papers, arXiv articles")
def research_search(query:str):
  """Returns the search results"""
  return tavily.search(
        query=query,
        max_results=5,
        search_depth="advanced"
    )




# searching agent
search_agent = create_agent(
  model = client,
  tools = [research_search],
  system_prompt = """You are a helpful AI assistant. For user queries shared fetch the web search results."""
)

# final response agent
conversational_agent = create_agent(
  model = client,
  system_prompt = """You are a expert recommender agent. Use search results shared and recommend the research papers to the user. Ensure the tone is professional and polite.
  Return the response in markdown format."""
)


#  main function
@cl.on_message
async def research_agent(message: cl.Message):
  """Runs the entire workflow"""

  user_query = message.content
  
  query_response = await query_agent.ainvoke({"messages":[{"role":"user","content":user_query}]})
  query_result = json_parser(query_response['messages'][-1].content)
  print(f"Query result: {query_result}")

  query_expansions = [[r for r in results] for results in query_result.values()]

  tool_results = []
  for query in query_expansions:
    search_response = await search_agent.ainvoke({'messages':[{'role':'user','content':query}]})
    print(f"Search response fetched")
    

    for msg in search_response['messages']:
      if isinstance(msg,ToolMessage):
        tool_response = json.loads(msg.content)['results']
        tool_results.append(tool_response)

  print(f"Tool response: {tool_results}")
  context = json.dumps(tool_results[:3], indent=2)
  conversational_response = await conversational_agent.ainvoke({'messages':[{'role':'user','content':f"Summarize these research papers {context}"}]})    # passing only the top 5 results
  final_response = conversational_response['messages'][-1].content
  print(f'Final response : {final_response}')
  
  await cl.Message(content=final_response).send()


#print(research_agent("Tell me about ML in biotech"))
