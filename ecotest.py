import logging
import os
import openai
from llama_index.llms import OpenAI
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from llama_index import OpenAIEmbedding, StorageContext, load_index_from_storage
from llama_index import PromptTemplate
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from dotenv import load_dotenv
from llama_index.vector_stores import SimpleVectorStore
import PyPDF2
import json


# Load environment variables and set API key
load_dotenv()
DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')
os.environ["OPENAI_API_KEY"] = SECRET_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create an OpenAI instance with the correct model and temperature
llm = OpenAI(model='gpt-4-1106-preview', temperature=0)
embed_model = OpenAIEmbedding()


service_context = ServiceContext.from_defaults(
    llm=llm, embed_model=embed_model
)

# Define base directory and path for extracted data
Base_dir = os.path.dirname(os.getcwd())
custom_path = os.path.join(Base_dir, "Data_extracted", "GNR_PDD", "Goldstd_verified", "Goldstd_verified")

# Define query templates for different types of information extraction
proponent_query_template = """
 #####INSTRUCTIONS
        -Act like an extraction system which looks for the field(s) in the document and find their value(s)
        -Make sure to check extensively for each field and find a value.
        -If you do not find a value for a field, assign it as None.
        -If the input is 'project proponents', then go and extract the 'project proponents' section. 
        -Remember for each field, return its value.
        -below are the fields to look for in the document:
        #### FIELDS
    Fields =    "role": 
                "name": 
                "title": 
                "address": 
                "organization": 
                "contact": 
                "email": 
                
                
            
    -MAKE SURE to Look for the values for each of the above fields and extract them in the document.
   
        """ # Your detailed instructions for proponents
other_entities_query_template = """
 #####INSTRUCTIONS
        -Act like an extraction system which looks for the field(s) in the given document and find their value(s)
        -Make sure to check extensively for each field and find a value.
        -If you do not find a value for a field, assign it as None.
        -If the input is 'other entities involved in the project', then go and extract the 'other entities involved in the project' section. 
        -Remember for each field, return its value.
        -below are the fields to look for in each document:
        #### FIELDS
    Fields =    "role": 
                "name": 
                "title": 
                "address": 
                "organization": 
                "contact": 
                "email": 
                 
                
            
        MAKE SURE to Look for the values for each of the above fields and extract them in each document.
        
        """ # Your detailed instructions for other entities
location_query_template = """
 #####INSTRUCTIONS
        -Act like an extraction system which looks for the location of the project in the document.
        -Make sure to check extensively.
        -If you do not find a value for a field, assign it as None.
        -Remember for each field, return its value.
      
        """ # Your detailed instructions for location
query_engines=[]
tools = []
# proponent_engines=[]
# entities_engines=[]
# location_engines=[]

#first=True

# Create tools for each subdirectory
for folder_name in os.listdir(custom_path):
    # if not first:
    #     break
    folder_path = os.path.join(custom_path, folder_name)
    #print(folder_name)
    if os.path.isdir(folder_path):
        print(folder_path)
        storage_path=os.path.join(folder_path, "storage")
        storage_context = StorageContext.from_defaults(persist_dir=storage_path)
        index = load_index_from_storage(storage_context=storage_context)
       
        
        query_engine = index.as_query_engine(similarity_top_k=3, service_context=service_context)
        query_engines.extend([query_engine])
        #print(folder_path)
        # proponent_engine = index.as_query_engine(similarity_top_k=3, service_context=service_context, simple_template=PromptTemplate(template=proponent_query_template))
        # other_entities_engine = index.as_query_engine(similarity_top_k=3, service_context=service_context, simple_template=PromptTemplate(other_entities_query_template))
        # location_engine = index.as_query_engine(similarity_top_k=3, service_context=service_context, simple_template=PromptTemplate(location_query_template))
        # proponent_engines.extend([proponent_engine])
        # entities_engines.extend([other_entities_engine])
        # location_engines.extend([location_engine])

        
        # proponent_tool = QueryEngineTool(query_engine=proponent_engine, metadata=ToolMetadata(name=f'{folder_name}_proponents', description=f'Project {folder_name} - Proponents'))
        # other_entities_tool = QueryEngineTool(query_engine=other_entities_engine, metadata=ToolMetadata(name=f'{folder_name}_other_entities', description=f'Project {folder_name} - Other Entities'))
        # location_tool = QueryEngineTool(query_engine=location_engine, metadata=ToolMetadata(name=f'{folder_name}_location', description=f'Project {folder_name} - Location'))

        #tools.extend([proponent_tool, other_entities_tool, location_tool])
        # if first:
        #     first=False

print("query engine length: ",len(query_engines))
# proponent_tool1=query_engines[5]
# #proponent_tool1.query(proponent_query_template)
# response=proponent_tool1.query("who is the project proponent and what are their details? ")
# print(response)
# print(response.source_nodes)

# entities_tool1=query_engines[5]
# #proponent_tool1.query(proponent_query_template)
# response=entities_tool1.query("who are the other entities involved in the project and what are their details?")
# print(response)
# print(response.source_nodes)


# location_tool1=query_engines[0]
# #proponent_tool1.query(proponent_query_template)
# response=location_tool1.query("who is the project proponent and what are their details? ")
# #print(response)
# print(response.response)

# location_responses=[]
# proponent_responses=[]
# entities_responses=[]
for query_engine in query_engines:
    location_response=query_engine.query(location_query_template)
    proponent_response=query_engine.query(proponent_query_template)
    entities_response=query_engine.query(other_entities_query_template)
    print(f"project_location: {location_response}")
    print("/n")
    print(f"project_proponent: {proponent_response}")
    print("/n")
    print(f"other_entities: {entities_response}")
    print("/n")
    # location_responses.append(location_response)
    # proponent_responses.append(proponent_response)
    # entities_responses.append(entities_response)




#json formatter for my output
# Create dictionaries to store the extracted data
# extracted_data = []

# # Loop through the responses and extract relevant information
# for location_response, proponent_response, entities_response in zip(location_responses, proponent_responses, entities_responses):
#     project_data = {
#         "location": location_response.response if location_response else None,
#         "proponent": proponent_response.response if proponent_response else None,
#         "other_entities": entities_response.response if entities_response else None,
#     }
#     extracted_data.append(project_data)

# # Define the path for the output JSON file
# output_json_file = os.path.join(Base_dir, "extracted_data.json")

# # Check if the JSON file already exists
# if os.path.exists(output_json_file):
#     # Load the existing data from the JSON file
#     with open(output_json_file, 'r') as json_file:
#         existing_data = json.load(json_file)
    
#     # Append the new data to the existing data
#     existing_data.extend(extracted_data)
#     extracted_data = existing_data

# # Write the updated extracted data to the JSON file
# with open(output_json_file, 'w') as json_file:
#     json.dump(extracted_data, json_file, indent=4)

# print(f"Extracted data has been saved to {output_json_file}")




