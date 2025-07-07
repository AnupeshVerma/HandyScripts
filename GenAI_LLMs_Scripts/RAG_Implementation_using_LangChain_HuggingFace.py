from langchain_huggingface.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

PDF_URL = "https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"                 # "all-MiniLM-L6-v2"
LLM_MODEL_ID = "google/flan-t5-base"                                            # "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


# Load and split PDF into chunks
def loadAndSplitPDF():
    documents = PyPDFLoader(PDF_URL).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    return docs

# Create embeddings and store in FAISS vector store
def createStoreVectorEmbeddings():
    docs = loadAndSplitPDF()
    embeddings = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL_NAME)
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store


def loadLLM():
    pipe = pipeline(
        "text2text-generation",
        model=LLM_MODEL_ID,
        tokenizer=LLM_MODEL_ID,
        max_new_tokens=256,     # Reduced max_new_tokens for conciseness
        # temperature=0.1,       # Lower temperature for less randomness and more factual answers
        do_sample=False,
        device = -1             # set to -1 if no GPU available
    )
    rag_llm = HuggingFacePipeline(pipeline=pipe)
    return rag_llm

# Create a RetrievalQA chain combining the vector store retriever and the LLM
def createRetrievalQAChain():
    vector_store = createStoreVectorEmbeddings()
    rag_llm = loadLLM()

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    rag_chain = RetrievalQA.from_chain_type(
        llm=rag_llm,
        chain_type="stuff",  # simple concatenation of retrieved docs
        retriever=retriever,
        return_source_documents=True,
    )
    return rag_chain


def generateResponse(query):
    rag_chain = createRetrievalQAChain()
    response = rag_chain.invoke({"query": query})
    print(f"Question: {query}\nAnswer: {response["result"]}")

    # print("Sources:")
    # for doc in response["source_documents"]:
    #     print(f"- Content: {doc.page_content[:150]}... (Page: {doc.metadata.get('page')})") 

if __name__ == "__main__":
    query = "What types of leaves are covered in this policy?"
    generateResponse(query)
    query = "How many sick leaves are mentioned in this policy?"
    generateResponse(query)


 
