# -*- coding: utf-8 -*-
"""Falcon7b_Langchain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Anil-matcha/langchain-tutorials/blob/main/Falcon7b_Langchain.ipynb

This is incredible

Chat privately with an LLM in few lines of code

Without the need for ChatGPT
"""

!nvidia-smi

# Commented out IPython magic to ensure Python compatibility.
# %pip install transformers accelerate einops langchain xformers

from transformers import AutoTokenizer

model = "tiiuae/falcon-7b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model)

import torch
import transformers

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_new_tokens=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)

from langchain import HuggingFacePipeline

llm = HuggingFacePipeline(pipeline=pipeline)

from langchain import PromptTemplate, LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory,ConversationSummaryMemory
from langchain.llms import HuggingFacePipeline
template = """You are an informative assistant chatting with a human.
{chat_history}
Human:{input}
Assistant:"""
#creating the prompt
prompt = PromptTemplate(
    input_variables=["chat_history","input"],
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm = HuggingFacePipeline(pipeline=pipeline)
#adding memory to the llm chain
llm_chain = LLMChain(llm=llm,prompt=prompt,memory=memory)

llm_chain.predict(input='make a REGIX to extract emails')

llm_chain.predict(input="Create a tweet from above content")