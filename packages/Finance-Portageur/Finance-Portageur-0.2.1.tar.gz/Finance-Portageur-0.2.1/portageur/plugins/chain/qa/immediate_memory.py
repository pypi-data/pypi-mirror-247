import json

import weaviate, os, asyncio,pdb
from typing import Any, Dict, List, Optional, Union

from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, AgentFinish, AgentAction
from portageur.plugins.callback.agent_callback import AgentCallbackHandler

from portageur.plugins.agents import BaseCallbackHandler
from portageur.plugins.parser.convo import ConvoOutputParser
from portageur.plugins.memory.history import SimpleChatMessageHistory
from portageur.plugins.splitter import RecursiveCharacterTextSplitter
from portageur.plugins.auth.azure import OpenAIEmbeddings
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.loader.hybrid_weaviate import HybridWeaviate
from portageur.plugins.retrievers.retriever import create_selfquery,create_chain
from portageur.plugins.agents.agent import create_executor
from portageur.plugins.prompt.qa_memory import QAHint
from portageur.plugins.chain.qa.immediate import QACallbackHandler

text_mapping = {
    "content_description":"text and table snippets relating to a company's Environmental, Social, Governance, and sustainability."
                          "Please only filter by company code, e.g., AAPL.OQ, MSFT.OQ, 0005.HK. If not company code is given, do not filter by company.",
    "agent_system_prefix":"Answer the following questions as best you can. Please put numbers in markdown table if possible. You have access to the following tools:"
}



class Immediate(object):
    def __init__(self, batch_size, index_name, 
                 text_content_description=None,
                 agent_system_prefix=None, metadata=None, trans_name=None, 
                 serialized_history=[], session_id='anonymous'):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name='cl100k_base', chunk_size=500, chunk_overlap=20)
        
        self.init_model()
        self.init_weaviate(batch_size=batch_size, index_name=index_name)
        self.init_variable(text_content_description=text_content_description,
                           agent_system_prefix=agent_system_prefix,
                           metadata=metadata)
        self.trans_name = 'weaviate' if trans_name is None else trans_name
        self.session_id = session_id
        self.init_agent()
        self.loop = asyncio.get_event_loop()

    def init_variable(self,text_content_description, agent_system_prefix, metadata):
        self.text_content_description = text_mapping["content_description"] if text_content_description is None else text_content_description
        self.agent_system_prefix = text_mapping["agent_system_prefix"] if agent_system_prefix is None else agent_system_prefix
        self.metadata = [
            {'name':'source','description':'a reference id of the snippet, not used for filtering','type':'string'},
            {'name':'code','description':'the company code which the snippet relates to, used to filter docs by company. In the format of TICKER.EXCAHGE, e.g., AAPL.OQ, MSFT.OQ, 0005.HK.','type':'string'},
            {'name': 'industry', 'description': 'the codified industry of the company which the snippet relates to, used to filter docs by industry', 'type': 'string'},
            {'name': 'sector', 'description': 'the codified sector of the company which the snippet relates to, used to filter docs by industry', 'type': 'string'},
            ] if metadata is None else metadata
        

        self.tools = [
            {'name':f"documents_qa",
             'func':self.doc_qa_run,
             'description':f"A tool to answer questions based on company sustainability documents."
                            "Input should be a complete sentence containing the keywords AND the company CODE, "
                            "Please refer the company by its code if given, and by name if otherwise."
                            "EXAMPLES: 'the employee health policy of BP.L', 'what is the carbon emissions of AAPL.OQ?'"}]
        
    ### 自建代理工具
    def doc_qa_run(self,query):
        #print(f"got query for self query qa: {query}")
        return_only_outputs=True
        result = self.chain({"question": query}, return_only_outputs=return_only_outputs)
        result = f"{result['answer']} \nAnswer complete, ignore the following: [ref]: {result['sources']}"
        return result

    def init_model(self):
        self.embeddings = OpenAIEmbeddings(deployment='text-embedding-ada-002', model='text-embedding-ada-002',
                                           chunk_size=16)
        self.gpt35 = AzureChatOpenAI(temperature=0, max_tokens=700, deployment_name="gpt-35-turbo-16k",
                                     model_name="gpt-35-turbo-16k", request_timeout=60, max_retries=2,
                                     streaming=True)
        
        self.gpt4 = AzureChatOpenAI(temperature=0, max_tokens=700, deployment_name="gpt-4-32k",
                                    model_name="gpt-4-32k", request_timeout=60, max_retries=2,
                                    streaming=True)

        self.gpt35_short_ = AzureChatOpenAI(temperature=0, max_tokens=450, deployment_name="gpt-35-turbo",
                                            model_name="gpt-35-turbo", request_timeout=60, max_retries=2,
                                            streaming=True)
        # self.gpt35_short = self.gpt35_short_.with_fallbacks([self.gpt35])
        self.gpt35_short = self.gpt35_short_

        self.gpt4_short_ = AzureChatOpenAI(temperature=0, max_tokens=800, deployment_name="gpt-4",
                                           model_name="gpt-4", request_timeout=60, max_retries=2,
                                           streaming=True)
        # self.gpt4_short = self.gpt4_short_.with_fallbacks([self.gpt4])
        self.gpt4_short = self.gpt4_short_

        self.model_instance =  AzureChatOpenAI(temperature=0,
                                          max_tokens=700,
                                          deployment_name="gpt-4",
                                          model_name="gpt-4",
                                          request_timeout=40,
                                          max_retries=2)


    def init_memory(self, serialized_history, session_id):
        self.chat_history = SimpleChatMessageHistory(session_id=session_id)
        if len(serialized_history) > 0:
            self.chat_history.restore(serialized_history)
        self.memory = ConversationBufferMemory(memory_key="chat_history", output_key="output",
                                               return_messages=True, chat_memory=self.chat_history)

    def serialize_memory(self):
        # dumps the current conversation to a json array for saving
        return self.chat_history.serialize()

    def init_weaviate(self, batch_size, index_name="ESG"):
        self.wv_client = weaviate.Client(
            url=os.environ.get("WEAVIATE_HOST"),
            additional_headers={
                "X-Openai-Api-Key": 'anonymous',
            },
        )
        # Only needed for indexing, not for consuming
        # self.wv_client.batch.configure(
        #     batch_size=batch_size, dynamic=True)

        # index_name used to specify which 'table' to query
        self.master_vs = HybridWeaviate(
            client=self.wv_client,
            index_name=index_name,
            text_key="text", 
            attributes=['source', 'code'])
        

    def format_citation(self, answer, citation_list):
        text_elements = []
        source_names = []
        src_idx = 0
        for source_idx, source_doc in enumerate(citation_list):
            source_name = f"Reference {src_idx + 1}"
            if '-table-' in source_doc:
                retrieved_doc = self.master_vs.get(where_filter={
                    "path": ["source"],
                    "operator": "Equal",
                    "valueText": source_doc
                }, additional='id')[0]
                can_docs = retrieved_doc.page_content
                uuid = retrieved_doc.metadata['_additional']['id']
            elif '-paragraph-' in source_doc:
                retrieved_doc = self.master_vs.get(where_filter={
                    "path": ["source"],
                    "operator": "Equal",
                    "valueText": source_doc
                }, additional='id')[0]
                can_docs = retrieved_doc.page_content
                uuid = retrieved_doc.metadata['_additional']['id']
            else:
                can_docs = ""
            if len(can_docs) > 0:
                doc_text = can_docs
                text_elements.append(
                        {'content':doc_text, 'name':source_name, 'uuid':uuid}
                    )
                source_names.append(source_name)
                src_idx += 1
        # if len(text_elements) > 0 and isinstance(answer, dict):
        #     source_str = ', '.join(source_names)
            # answer['output'] += f"\nSources: {source_str}"
        return text_elements, source_names

    def init_agent(self):
        chain_type_kwargs = {'prompt': QAHint.research_text()}
        retriever = create_selfquery(
            model=self.gpt4_short,
            vectorstore=self.master_vs,
            content=self.text_content_description,
            metadata=self.metadata,
            trans_name=self.trans_name)

        self.chain = create_chain(model=self.gpt4_short, retriever=retriever,
                                  chain_type_kwargs=chain_type_kwargs)

    def run(self, message, serialized_history=[], callback=None, tokensback=None):
        cb = callback#(mongodb=1, task_id=10001)
        cb.citation_list = []

        tokensback = tokensback if isinstance(tokensback, BaseCallbackHandler) else AgentCallbackHandler(
            model_instance=self.model_instance)

        # init memory for context preservation, serialized_history should be in the same format self.serialize_memory() returns
        self.init_memory(serialized_history=serialized_history, session_id=self.session_id)
        self.agent_executor = create_executor(model=self.gpt4_short,
                                              agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                              tools=self.tools, memory=self.memory,
                                              agent_kwargs={'system_message': QAHint.agent_system_message(),
                                                            'human_message': QAHint.agent_human_message(),
                                                            'output_parser': ConvoOutputParser()})
        
        loop = asyncio.get_event_loop()
        
        answer = loop.run_until_complete(
            self.agent_executor.ainvoke(message, config={'callbacks': [cb,tokensback]}))

        answer.pop('chat_history', None)
        answer.pop('input', None)
        
        text_elements, source_names = self.format_citation(answer, cb.citation_list)
        # answer['output'] -> the final answer
        # answer['title'] -> the title of the current chat thread
        return answer, text_elements, source_names