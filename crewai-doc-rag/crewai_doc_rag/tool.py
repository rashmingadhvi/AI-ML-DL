from crewai_tools import PDFSearchTool
from dotenv import load_dotenv

pdf_tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemma3:1b",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="granite-embedding",
                
                # title="Embeddings",
            ),
        ),
        
        # chunk_size=1000,
        # chunk_overlap=200,
        # k=5,
        # max_tokens=1000,
        # verbose=True,
        # num_processes=1,
        # num_threads=1,
        # max_depth=1,
        # allowagent=True,
        # async_mode=True,
        # memory=MemoryType.LongTerm,
        # long_term_memory_collection_name="long_term_memory",
        # access_kws=["search", "query", "read", "load", "index", "embed", "memory", "long_term_memory"],
        # deny_kws=["deny", "reject", "refuse", "forbid", "block", "ignore"],
    ),
    pdf="./docs/Belair.pdf"
)