# Import the required libraries and modules
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json

from dotenv import load_dotenv
load_dotenv() 




# Define the query text
text = """
The healthcare space is buzzing with innovation.
BrightLabs, co-founded by Dr. Jane Foster and Dr. Thor Odinson, specializes in nanotech for early cancer detection. Jane, an MIT alumna, is passionate about making healthcare accessible. You can reach her team via jane@brightlabs.com.
Meanwhile, BioDynamics, a cutting-edge startup led by Dr. Bruce Banner, focuses on bioinformatics solutions for genetic disorders. Dr. Banner, a noted Harvard geneticist, frequently shares his thoughts on @BruceBannerBio.  
"""

# Define the Founder class to represent a founder of a startup
class Founder(BaseModel):
    name: str = Field(..., example="Bill Gates")  # The name of the founder
    contact: Optional[str] = Field(None, example="billgates@microsoft.com, @BillGates")  # The contact information for the founder, which is optional

# Define the Startup class to represent a startup
class Startup(BaseModel):
    name: str = Field(..., example="Microsoft")  # The name of the startup
    description: str = Field(..., example="operating systems and software")  # The description of the startup
    founders: Optional[List[Founder]] = None  # The list of founders of the startup, which is optional

# Define the Startups class to represent a list of startups
class Startups(BaseModel):
    startups: List[Startup]  # The list of startups




# Prepare the query
query = HumanMessage(content=text)

# Initialize the ChatOpenAI instance
llm = ChatOpenAI()

# Define the functions
functions = [
    {"name": "get_startup_info", "description": "extract startup name and basic info from text", "parameters": Startups.schema()}
]


# Perform the function call
response = llm([query], functions=functions, function_call="auto")

# Extract the function call arguments from the response
result = response.additional_kwargs['function_call']['arguments']

# Load the result as JSON
data = json.loads(result)

# Loop over the startups in the data
for startup in data['startups']:
    print(f'Startup Name: {startup["name"]}')  # Print the name of the startup
    print(f'Description: {startup["description"]}')  # Print the description of the startup
    print('Founders:')  # Print the founders header

    # Loop over the founders of the startup
    for founder in startup['founders']:
        # If the founder has contact information, print their name and contact
        if founder["contact"]:
            print(f'\t{founder["name"]}, {founder["contact"]}')
        # If the founder does not have contact information, print just their name
        else:
            print(f'\t{founder["name"]}')
    print('')  # Print a blank line between startups