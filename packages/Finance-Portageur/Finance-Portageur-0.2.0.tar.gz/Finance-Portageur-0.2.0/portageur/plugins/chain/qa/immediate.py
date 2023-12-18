import weaviate, os, asyncio,pdb
from typing import Any, Dict, List, Optional, Union

from langchain.schema import BaseMessage, AgentFinish, AgentAction

from portageur.plugins.agents import BaseCallbackHandler
from portageur.plugins.splitter import RecursiveCharacterTextSplitter
from portageur.plugins.auth.azure import OpenAIEmbeddings
from portageur.plugins.auth.azure import AzureChatOpenAI
from portageur.plugins.loader.hybrid_weaviate import HybridWeaviate
from portageur.plugins.retrievers.retriever import create_selfquery,create_chain
from portageur.plugins.agents.agent import create_executor
from portageur.plugins.prompt.qa import QAHint

text_mapping = {
    "content_description":"text and table snippets relating to a company's Environmental, Social, Governance, and sustainability",
    "agent_system_prefix":"Answer the following questions as best you can. Please put numbers in markdown table if possible. You have access to the following tools:"
}


## 逻辑业务
class QACallbackHandler(BaseCallbackHandler):
    citation_list: List[str] = []

    def on_tool_start(
            self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Run when tool starts running."""

    def on_tool_end(
        self,
        output: str,
        **kwargs: Any,
    ) -> None:
        split_output = output.split(' [ref]: ')
        if len(split_output) > 1:
            citations = split_output[1].strip().split(',')
            for x in citations:
                self.citation_list.append(x.strip(' \n)'))
        super().on_tool_end(output,  **kwargs)

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""

    def on_chat_model_start(
            self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""


class Immediate(object):
    def __init__(self, index_name='ESG', text_content_description=None,
                 agent_system_prefix=None, metadata=None, trans_name=None):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name='cl100k_base', chunk_size=500, chunk_overlap=20)
        
        self.init_model()
        self.init_weaviate(index_name=index_name)
        self.init_variable(text_content_description=text_content_description,
                           agent_system_prefix=agent_system_prefix,
                           metadata=metadata)
        self.trans_name = 'weaviate' if trans_name is None else trans_name
        self.loop = asyncio.get_event_loop()

    def init_variable(self,text_content_description, agent_system_prefix, metadata):
        self.text_content_description = text_mapping["content_description"] if text_content_description is None else text_content_description
        self.agent_system_prefix = text_mapping["agent_system_prefix"] if agent_system_prefix is None else agent_system_prefix
        self.metadata = [
            {'name':'source','description':'the source reference of the snippet','type':'string'},
            {'name':'code','description':'the company code which the snippet relates to','type':'string'},
            {'name': 'industry', 'description': 'the codified industry of the company which the snippet relates to', 'type': 'string'},
            {'name': 'sector', 'description': 'the codified sector of the company which the snippet relates to', 'type': 'string'},
            ] if metadata is None else metadata
        

        self.tools = [
            {'name':f"documents_qa",
             'func':self.doc_qa_run,
             'description':f"A tool to answer questions based on company sustainability documents."
                        "Usually used to answer qualitative questions. "
                        "Can also be used to answer quantitative questions."
                        "Input should be a complete sentence containing the keywords AND the company code."
                        "EXAMPLE: 'the employee health policy of [code:BP.L]'"}]
        
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

        
        self.gpt4_short_ = AzureChatOpenAI(temperature=0, max_tokens=700, deployment_name="gpt-4",
                                          model_name="gpt-4", request_timeout=60, max_retries=2,
                                          streaming=True)

        # self.gpt4_short = self.gpt4_short_.with_fallbacks([self.gpt4])
        self.gpt4_short = self.gpt4_short_

        

    def init_weaviate(self, index_name="ESG"):
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

    def run(self, message, callback=None):
        chain_type_kwargs={'prompt': QAHint.research_text()}
        retriever = create_selfquery(
            model=self.gpt35_short, 
            vectorstore=self.master_vs, 
            content=self.text_content_description, 
            metadata=self.metadata, 
            trans_name=self.trans_name)
        
        self.chain = create_chain(model=self.gpt4_short, retriever=retriever, 
             chain_type_kwargs=chain_type_kwargs)
        
        self.agent_executor = create_executor(model=self.gpt4_short, 
                                              tools=self.tools, 
                                              agent_kwargs={'system_message_prefix': self.agent_system_prefix})
        
        cb = callback#(mongodb=1, task_id=10001)
        #cb.citation_list = []

        loop = asyncio.get_event_loop()
        answer = loop.run_until_complete(
            self.agent_executor.arun(message, callbacks=[cb]))
        
        text_elements, source_names = self.format_citation(answer, cb.citation_list)
        return answer, text_elements, source_names