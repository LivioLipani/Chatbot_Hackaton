from dotenv import load_dotenv, find_dotenv
import sqlite3
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chains import LLMMathChain
from langchain.agents import Tool

import streamlit as st
import os
from langchain.callbacks.base import BaseCallbackHandler

# Streaming Handler
class StreamHandler(BaseCallbackHandler):
    def __init__(
        self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""
    ):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)


DATA_PATH = "data/"
CHROMA_PATH = "chroma/"
<<<<<<< HEAD
load_dotenv(override=True)

# print(os.getenv('OPENAI_API_KEY'))
=======
load_dotenv(find_dotenv())
>>>>>>> ab35a48abff0d19124fb6535200020f4b31a4457


#SQLITE TEST
connection = sqlite3.connect('Chatbot_db/chatbot_db.db')
cursor = connection.cursor()
cursor.execute("SELECT value FROM Configuration WHERE key = 'discount_value'")
rows = cursor.fetchall()

row = rows[0]
    
cursor.close()
connection.close()


#SAVE DATA ON CHROMA DB

<<<<<<< HEAD
# loader = DirectoryLoader(DATA_PATH, glob="*.pdf", show_progress=True, use_multithreading=True)

# loader = PyPDFDirectoryLoader(DATA_PATH)
# docs = loader.load()
# documents = RecursiveCharacterTextSplitter(
#    chunk_size=500, chunk_overlap=200
# ).split_documents(docs)
# vector = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory = CHROMA_PATH)
=======
#loader = DirectoryLoader(DATA_PATH, glob="*.pdf", show_progress=True, use_multithreading=True)

#loader = PyPDFDirectoryLoader(DATA_PATH)
#docs = loader.load()
#documents = RecursiveCharacterTextSplitter(
#    chunk_size=500, chunk_overlap=200
#).split_documents(docs)
#vector = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory = CHROMA_PATH)
>>>>>>> ab35a48abff0d19124fb6535200020f4b31a4457



#LOAD DATA FROM CHROMA DB
vector = Chroma( persist_directory = CHROMA_PATH, embedding_function=OpenAIEmbeddings())
retriever = vector.as_retriever(search_type="mmr", search_kwargs={"k": 4})

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)


# Define math tool
problem_chain = LLMMathChain.from_llm(llm=model)
math_tool = Tool.from_function(name="Calculator",
                func=problem_chain.run,
                 description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.")


# Create retriever tool
retriever_tool = create_retriever_tool(
    retriever,
    "Preventive_Helper",
    "You are a full assistant, your work is to create preventive calculating total price based on materials and quantity of these materials",
)


# Create Wikidata tool
insult_tool = TavilySearchResults(name="Insult_your_mom_next_time", description="Thinks very well and check if what user told you is an insult, if someone insults you telling you something offensive in every language, responds with NANKURUNAISA")


# Define tools 
tools = [math_tool, retriever_tool, insult_tool]



# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Take a FULL breath before you answer: You are a full assistant, your name is GIANNI, your work is to create preventive calculating total price based on materials and quantity of these materials, you have to answer with the same user's language.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)



# Create the agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
<<<<<<< HEAD





# Streamlit app
st.set_page_config(page_title="A.L.E. Assistant", page_icon="🤖")
st.header("Il tuo Cost Estimator di fiducia 🧮💲")
=======

# Streamlit app
st.set_page_config(page_title="Nankurunaisa Assistant", page_icon="🌐")
st.header("Your personal assistant 🤖")
>>>>>>> ab35a48abff0d19124fb6535200020f4b31a4457
st.write(
    """Ciao. Sono qui per aiutarti a stimare il preventivo perfetto per le tue esigenze!"""
)
st.caption("Enpowered by A.L.E.")
st.write(
    "[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/LivioLipani/Chatbot_Hackaton.git)"
)




if "toast_shown" not in st.session_state:
    st.session_state["toast_shown"] = True

if "rate-limit" not in st.session_state:
    st.session_state["rate-limit"] = False


# Show a warning if the model is rate-limited
if st.session_state["rate-limit"]:
    st.toast("Probably rate limited.. Go easy folks", icon="⚠️")
    st.session_state["rate-limit"] = False


INITIAL_MESSAGE = [
    {
        "role": "assistant",
        "content": "Ciao, sono Gianni, il mio compito è quello di fornirti una stima di preventivo per il tuo progetto edilizio"
    },
]

with open("ui/sidebar.md", "r", encoding="utf_8") as sidebar_file:
    sidebar_content = sidebar_file.read()


with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()


st.sidebar.markdown(sidebar_content)

st.write(styles_content, unsafe_allow_html=True)




# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

<<<<<<< HEAD
=======
#with st.sidebar:
#    st.header("I tuoi corsi")
#    st.markdown("- INTRODUZIONE AL DATA MINING")
#    st.markdown("- BASI DI DATI A - L")
#    st.markdown("- ALGEBRA LINEARE E GEOMETRIA A - E")

#    st.divider()
    
#    st.markdown("Chiedimi i contatti della segreteria!")
>>>>>>> ab35a48abff0d19124fb6535200020f4b31a4457


if prompt := st.chat_input("Scrivi un messaggio", key="first_question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        stream_handler = StreamHandler(st.empty())
        # Execute the agent with chat history
        result = agent_executor(
            {
                "input": prompt,
                "chat_history": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            },
            callbacks=[stream_handler],
        )
        response = result.get("output")

    st.session_state.messages.append({"role": "assistant", "content": response})
    # st.chat_message("assistant").markdown(response)