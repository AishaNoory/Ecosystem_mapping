import os
from llama_index.llms import OpenAI
from llama_index import LLMPredictor, OpenAIEmbedding, PromptHelper, ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index.node_parser import SentenceSplitter
from llama_index import Document
from llama_index.vector_stores import SimpleVectorStore
from llama_index import VectorStoreIndex


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')
os.environ["OPENAI_API_KEY"] = SECRET_KEY

Base_dir = os.path.dirname(os.getcwd())
custom_path = os.path.join(Base_dir, "GNR_PDD", "Goldstd_unverified")

llm = OpenAI(model='gpt-3.5-turbo', temperature=0, streaming=True)
#llm_predictor = LLMPredictor(llm=llm)
#node_parser = SimpleNodeParser.from_defaults()
node_parser=SentenceSplitter()
# prompt_helper = PromptHelper(
#     context_window=3900,
#     num_output=256,
#     chunk_overlap_ratio=0.1,
#     chunk_size_limit=None
# )

service_context = ServiceContext.from_defaults(
    llm=llm,
    node_parser=node_parser,
    #prompt_helper=prompt_helper
    embed_model=OpenAIEmbedding()
)

# Constructing the indices
def construct_index(root_directory):
    isFirstLoop=True
    for dir_path, dir_directories, dir_files in os.walk(root_directory):
        
        if isFirstLoop:
            isFirstLoop= False
            continue
        print(dir_path)
        documents = SimpleDirectoryReader(input_dir=dir_path).load_data()
        nodes=node_parser.get_nodes_from_documents(documents)
        index=VectorStoreIndex(nodes=nodes, service_context=service_context, show_progress=True)
        storage_path=os.path.join(dir_path, "storage")
        if os.path.isdir(storage_path):
            continue
        #os.makedirs(name=storage_path)
        
      
        index.storage_context.persist(persist_dir=storage_path)

            #print(dir)
           # documents = SimpleDirectoryReader(input_dir=dir)

            # # Check if the path is a file
            # if os.path.isfile(file_path):
            #     # Read the content of the file
            #     # Read the content of the file with a more permissive encoding
            #   with open(file_path, 'r', encoding='ISO-8859-1') as f:
            #    content = f.read()


            #     # Create a document from the file content
            # document = Document(content=content, metadata={'file_path': file_path})

            #     # Process the document and create an index
            # nodes = node_parser.get_nodes_from_documents([document])
            # index = VectorStoreIndex(nodes, service_context=service_context, show_progress=True)
            # parent_dir = os.path.abspath(os.path.join(file_path, os.pardir))
            # index.storage_context.persist(persist_dir=parent_dir)

            # if index is not None:
            #         print(f"Index created for {file_path}")
            # else:
            #         print(f"Failed to create index for {file_path}")

# Specify the root directory containing subdirectories with files
root_directory = r"C:\Users\user\Downloads\stakeholder_mapping\stakeholder_mapping\Data_extracted\GNR_PDD\verra_verified\verra_verified"
construct_index(root_directory)
