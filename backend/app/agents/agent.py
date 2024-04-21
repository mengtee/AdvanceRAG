from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.together import TogetherLLM
from llama_index.core.settings import Settings
from app.settings import init_settings
from app.tools.valuation_tool import calculate_intrinsic_value
# define sample Tool
calculate_intrinsic_value = FunctionTool.from_defaults(fn=calculate_intrinsic_value)

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_agent(vectara_response: str):
    llm = Settings.llm
    agent = ReActAgent.from_tools([calculate_intrinsic_value], llm=llm, verbose=True)
    logger.info("successfully run agent file")  # Use logger instead of print
    logger.info(response)
    response = agent.chat(vectara_response)
    
    return response
