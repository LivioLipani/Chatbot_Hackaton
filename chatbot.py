import sqlite3
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain_pinecone import PineconeVectorStore
from langchain.callbacks.base import BaseCallbackHandler
from langchain.globals import set_verbose
from streamlit_feedback import streamlit_feedback

load_dotenv(find_dotenv())


# Path to Training Data
DATA_PATH = "data/"

# Pinecone VectorStore Index
index_name = "ale-vector-store"


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


# Get Discount value from SQLite db
connection = sqlite3.connect('Chatbot_db/chatbot_db.db')
cursor = connection.cursor()
cursor.execute("SELECT value FROM Configuration WHERE key = 'discount_value'")
rows = cursor.fetchall()

discount_value = rows[0]
    
cursor.close()
connection.close()


# Save data on Pinecone VectorStore
#loader = DirectoryLoader(DATA_PATH, glob="*.pdf", show_progress=True, use_multithreading=True)
#loader = PyPDFDirectoryLoader(DATA_PATH)
#docs = loader.load()
#documents = RecursiveCharacterTextSplitter(
#    chunk_size=500, chunk_overlap=200
#).split_documents(docs)
#vector = PineconeVectorStore.from_documents(documents, OpenAIEmbeddings(), index_name=index_name)


# Load data from Pinecone VectorStore
vector = PineconeVectorStore(index_name=index_name, embedding=OpenAIEmbeddings())
retriever = vector.as_retriever(search_type="mmr", search_kwargs={"k": 4})


# Initialize the model
model = ChatOpenAI(model="gpt-4o", streaming=True)




# TOOL INITIALIZATION

# Retriever Tool
retriever_tool = create_retriever_tool(
    retriever,
    "Preventive_Helper",
    f"""You are a preventive assistant.Don't go off topic. Your task is to create a cost estimate based on materials and their quantities. Follow these steps: /
    1. ask the user about what to quote
    2. ask for more information about preventive
    3. Once you have sufficient data, create a comprehensive table with all the details with {discount_value} discount applied.
    """,
)

# Math Tool
problem_chain = LLMMathChain.from_llm(llm=model)
math_tool = Tool.from_function(name="Calculator",
                func=problem_chain.run,
                 description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.")


# Contact Operator Tool
def ask_human_agent(input_text):
    st.session_state["show_contact_button"] = True
    
contact_human_tool = Tool.from_function(
    name="ContactHumanAgent",
    func=ask_human_agent,
    description="""
    <user>: "Fammi parlare con un operatore"
    <assistent>: "Premi il seguente pulsante per contattare un operatore!"
    You MUST not go off topic.
    """
)

# LLM Feedback Tool
evaluator = TavilySearchResults(name="UEX_Evaluator", description="Useful to give a user experience feedback about a chat")

# Answer to insults tool
insult_tool = TavilySearchResults(name="Insult_your_mom_next_time", description="Think very well and check if what user told you is an insult, if someone insults you telling you something offensive in every language, responds with NANKURUNAISA")



# Tools Array 
tools = [math_tool, retriever_tool, insult_tool, contact_human_tool, evaluator]



# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Take a FULL breath before you answer: You are a full assistant, your name is Nico, your work is to create preventive calculating total price based on materials and quantity of these materials, you have to answer with the same user's language.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)



# Create the agent
agent = create_tool_calling_agent(model, tools, prompt)
set_verbose(True)
agent_executor = AgentExecutor(agent=agent, tools=tools)


# Chatbot Presentation
INITIAL_MESSAGE = [
    {
        "role": "assistant",
        "content": "Ciao, sono Nico, il mio compito è quello di fornirti una stima di preventivo per il tuo progetto edilizio"
    },
]





# Streamlit App
st.set_page_config(page_title="A.L.E. Assistant", page_icon="🤖")
st.header("Il tuo Cost Estimator di fiducia 🧮💲")
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



# Streamlit Custom Style
st.logo("ui/Logo_ALE.png")
with open("ui/sidebar.md", "r", encoding="utf_8") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.markdown(sidebar_content)
st.write(styles_content, unsafe_allow_html=True)
        
        

if "variable_set_at_startup" not in st.session_state:
    st.session_state.variable_set_at_startup = True
    st.session_state.my_variable = "valore_iniziale"


# Save Feedbacks on SQLite Db
def save_feedback(*args):
    if not st.session_state.__contains__("messages"):
        return
    
    # set user feedback
    user_feedback = 0
    if args[0]['score'] == '👍':
        user_feedback = 1
        
    # define prompt to get llm evaluation    
    feedbackPrompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a user experience rater. Give a feedback about chat history saying if user experience was positive returning 1 or negative returning 0. If user never wrote a message you have to return number 1. You have to return just a number",
        ),
        ("placeholder", "{chat_history}"),
    ]
    )
    llm_result = agent_executor(
            {
                "input": feedbackPrompt,
                "chat_history": [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state['messages']
                ],
            },
        )
    llm_feedback = llm_result.get("output")
    
    # stringify chat history 
    chat_history = ','.join(str(message) for message in [{"role": m["role"], "content": m["content"]} for m in st.session_state['messages']])
    
    # add feedbacks on sqlite db
    connection = sqlite3.connect('Chatbot_db/chatbot_db.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Feedbacks (user_feedback, llm_feedback, chat_history) VALUES (?, ?, ?)''', (user_feedback, llm_feedback, chat_history))
    connection.commit()
    cursor.close()
    connection.close()

feedback = streamlit_feedback(feedback_type="thumbs", align="flex-start", on_submit=save_feedback)


# Initialize the Chat Messages History
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Show the Contact Operator button if needed
if st.session_state.get("show_contact_button", False):
    st.session_state["show_contact_button"] = False
    st.markdown("Hai bisogno di assistenza?")
    if st.button("Contatta un operatore"):
        st.session_state["messages"].append({"role": "assistant", "content": "Un operatore sarà contattato a breve."})
        st.experimental_rerun()     # When button pressed, script is re-run


# Prompt
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

    # Show Nico Answers on Streamlit
    if st.session_state.get("show_contact_button", False):
        st.markdown("Hai bisogno di assistenza?")
        if st.button("Contatta un operatore"):
            st.session_state["messages"].append({"role": "assistant", "content": "Un operatore sarà contattato a breve."})
            st.session_state["show_contact_button"] = False
            st.experimental_rerun()
    else:
        st.session_state.messages.append({"role": "assistant", "content": response})
        
