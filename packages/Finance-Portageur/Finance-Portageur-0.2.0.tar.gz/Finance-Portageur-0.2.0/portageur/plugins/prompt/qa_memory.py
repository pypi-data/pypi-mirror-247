# -*- coding: utf-8 -*
from portageur.plugins.prompt.base import transformer, PromptsMessage

class QAHint(object):

    @classmethod
    def table_prefix(cls):
        return  """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Your answer should be in the format of a markdown table if there are more than one numerical values in the answer.
ALWAYS return a "SOURCES" part in your answer, unless the extracted parts are all irrelevant.
Only cite the relevant parts in the "SOURCES" part.
"""
    
    @classmethod
    def text_prefix(cls):
        return """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Please include complementary information in your answer, besides the direct answer.
For answers containing numerical values, you should answer in markdown table format.
For other answers please use itemized list for text answers, with key phrases in bold.
Please still reply with relevant information if you can't find direct answer to the question.
ALWAYS return a "SOURCES" part in your answer, unless the extracted parts are all irrelevant.
ONLY cite the USED parts in you answer in the "SOURCES" part.
"""
    @classmethod
    def qa_example(cls):
        return """
        QUESTION: Which state/country's law governs the interpretation of the contract?
        =========
        Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
        Source: 28-pl
        Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
        Source: 30-pl
        Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
        Source: 4-pl
        =========
        FINAL ANSWER: This Agreement is governed by *English law*.
        SOURCES: 28-pl

        QUESTION: What did the president say about Michael Jackson?
        =========
        Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
        Source: 0-pl
        Content: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
        Source: 24-pl
        Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
        Source: 5-pl
        Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
        Source: 34-pl
        =========
        FINAL ANSWER: The president did not mention Michael Jackson.
        SOURCES:

        QUESTION: {question}
        =========
        {summaries}
        =========
        FINAL ANSWER:"""
    
    @classmethod
    def research_table(cls):
        return transformer(cls.table_prefix() + cls.qa_example(), 
                            method=PromptsMessage.Template,
                            variables=["summaries", "question"]
                            )
    @classmethod
    def research_text(cls):
        return transformer(cls.text_prefix() + cls.qa_example(), 
                            method=PromptsMessage.Template,
                            variables=["summaries", "question"]
                            )
    
    @classmethod
    def research_example(cls):
        return transformer("Content: {page_content}\nSource: {source}",
                            method=PromptsMessage.Template,
                            variables=["page_content", "source"]
                            )

    @classmethod
    def agent_system_message(cls):
        return """Assistant is a large language model trained by PortageBay.

        Assistant is designed to be able to assist with a wide range of sustainable finance research tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
        
        Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
        If assistant cannot provide user with a satisfactory answer, please advise the user to check out PortageBay;s 'Sustainability Analyst' for broader research options
        Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist."""

    @classmethod
    def agent_human_message(cls):
        return """TOOLS
        ------
        Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:
        
        {{tools}}
        
        {format_instructions}
        
        USER'S INPUT
        --------------------
        Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):
        
        {{{{input}}}}"""

    @classmethod
    def output_parser_format_instruction(cls):
        return """RESPONSE FORMAT INSTRUCTIONS
        ----------------------------
        
        When responding to me, please output a response in one of two formats:
        
        **Option 1:**
        Use this if you want the human to use a tool.
        Markdown code snippet formatted in the following schema:
        
        ```json
        {{{{
            "action": string, \\ The action to take. Must be one of {tool_names}
            "action_input": string \\ The input to the action
        }}}}
        ```
        
        **Option #2:**
        Use this if you want to respond directly to the human. Please refer the companies ONLY by names in your outputs. 
        Please keep all the context from the tool outputs.
        Even if you don't have the direct answer, you should still provide the user with the relevant information.
        Markdown code snippet formatted in the following schema:
        
        ```json
        {{{{
            "action": "Final Answer",
            "chat_title": string, \\ A short title for the entire chat history, under 10 words
            "suggestions": List[string], \\ up to 2 suggested follow-up questions
            "action_input": string \\ You should put what you want to return to use here, preserve markdown tables and itemized lists to present the content, and bold key phrases
        }}}}
        ```"""


