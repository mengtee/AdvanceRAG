from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.together import TogetherLLM
from llama_index.core.settings import Settings
from app.settings import init_settings
from app.tools.valuation_tool import calculate_intrinsic_value
# define sample Tool
init_settings()
calculate_intrinsic_value = FunctionTool.from_defaults(fn=calculate_intrinsic_value)

llm = Settings.llm 

# initialize ReAct agent
agent = ReActAgent.from_tools([calculate_intrinsic_value], llm=llm, verbose=True)
print("successfully run agent file")
response= agent.chat("how to calculate the gross margin")
# response = agent.chat(" can you calculate the intrinsic value of a company, The initial_fcf = 50000000, fcf_growth_rate = 0.05  wacc = 0.1  , terminal_growth_rate = 0.02, forecast_period = 10, company_debt = 100000000 ,outstanding_shares = 5000000 ")