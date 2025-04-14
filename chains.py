from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()

#####################
#### ENRICHMENT #####
#####################

class EnrichedQuery(BaseModel):
    enriched_query: str = Field(description="this is the enriched query")

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=EnrichedQuery)

normalize_prompt = PromptTemplate(
    template="You role is to enrich the provided user query about event planning to make sure it's clear.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

enrich_chain = (
    normalize_prompt
    | ChatOpenAI(model="gpt-4o", temperature=0)
    | parser
)

    
###################
##### ROUTING #####
###################
routing_chain = (
    PromptTemplate.from_template(
        """Given the user question below, you need to decide where to route it. These are the possible routes:

    - EventPlan: Generate a detailed event plan using available venues and vendors.
    - VendorInfo: Provide information about specific vendors or venues in the database.
    - NotSupported: Any other request.

Just respond with one word, the name of the route you selected.

<question>
{question}
</question>

Classification:"""
    )
    | ChatOpenAI(model="gpt-4o", temperature=0)
    | StrOutputParser()
)


########################
##### EVENT PLAN #####
########################
event_plan_prompt = PromptTemplate(
    template="""
    You are an event planner. Your task is to create personalized event plans for users based on their requests.

    User profile:
    {user_profile}

    User query: {query}

    Use the following venues and vendors for the plan. You don't necessarily have to use all of them, but you can only choose from this list:
    {resources}

    The output must be in the following JSON format:
    {{
        "type": "event_plan",
        "plan": [
            {{"day": "Day 1", "activities": [
                {{"venue_id": 1, "time": "09:00", "description": "Welcome breakfast"}},
                {{"venue_id": 2, "time": "14:00", "description": "Team building activities"}}
            ]}},
            {{"day": "Day 2", "activities": [
                {{"venue_id": 3, "time": "10:00", "description": "Conference sessions"}},
                {{"venue_id": 4, "time": "19:00", "description": "Gala dinner"}}
            ]}}
            ...
        ]
    }}
    """,
    input_variables=["user_profile", "query", "resources"]
)

event_plan_chain = (
    event_plan_prompt
    | ChatOpenAI(model="gpt-4o", temperature=0)
    | JsonOutputParser()
)

########################
##### SUMMARY #####
########################
summary_prompt = PromptTemplate(
    template="""
    You are an event planner. Your task is to provide a user with a short paragraph to complement the provided event plan. The plan is in JSON format, with all the activities scheduled for each day.

    User profile:
    {user_profile}

    Event plan:
    {event_plan}
    
    Just respond with the paragraph for the user, remember they can see the plan so you want to provide short tailored advice and information to complement the plan, do not regurgitate the plan to them.
    """,
    input_variables=["user_profile", "event_plan"]
)


summary_chain = (
    summary_prompt
    | ChatOpenAI(model="gpt-4o", temperature=0)
    | StrOutputParser()
)


#########################
##### VENDOR INFO #####
#########################

vendor_info_prompt = PromptTemplate(
    template="""
    You are an event planner. Your task is to provide the user with a list of venues and vendors that match their query.

    User query: {query}

    Choose from the following list of venues and vendors an appropriate subset that matches the user's query:
    {resources}

    The output must be in the following JSON format, containing an array of just resource IDs, nothing else:
    {{
        "type": "resources",
        "resource_ids": [1,15,20]
    }}
    """,
    input_variables=["query", "resources"]
)

vendor_info_chain = (
    vendor_info_prompt
    | ChatOpenAI(model="gpt-4o", temperature=0)
    | JsonOutputParser()
)

