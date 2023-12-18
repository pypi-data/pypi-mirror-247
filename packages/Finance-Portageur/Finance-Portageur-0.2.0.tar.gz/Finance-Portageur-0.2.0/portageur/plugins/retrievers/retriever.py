import importlib,pdb
from langchain.retrievers import SelfQueryRetriever
from portageur.plugins.retrievers.attribute import create_attribute
from langchain.retrievers.self_query.weaviate import WeaviateTranslator
from langchain.chains import RetrievalQAWithSourcesChain

def create_selfquery(model, vectorstore, content, metadata, trans_name):
    inst_module = importlib.import_module(
        'langchain.retrievers.self_query.{0}'.format(trans_name))
    translator = getattr(inst_module,"{}Translator".format(trans_name.title()))
    retriever = SelfQueryRetriever.from_llm(
        llm=model.instance(), 
        vectorstore=vectorstore,
        document_contents=content,
        metadata_field_info=[att.to_atrribute() for att in create_attribute(metadata)],
        verbose=True,
        use_original_query=False,
        structured_query_translator=translator()
        )
    return retriever

def create_chain(model, retriever, chain_type_kwargs, chain_type='stuff'):
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=model.instance(), chain_type=chain_type,
        retriever=retriever,
        reduce_k_below_max_tokens=True,
        max_tokens_limit=6000,
        chain_type_kwargs=chain_type_kwargs)
    return chain