#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openai import OpenAI
import requests
import os

client = OpenAI()
# client.models.list()

# response = client.responses.create(
#     model="gpt-5",
#     input="Write a three line story about a unicorn."
# )

# print(response.output_text)

#%%
prompt = "What is the CAS Regsitery Number for Ethyl maltol?"
response = client.responses.create(
    model="gpt-5-mini",
    input=prompt,
    text = {
            "verbosity": None, 
            "format": {
                        "type": "json_schema", 
                        "name": "CAS_number", 
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "CAS_number": {"type": "string"}
                            },
                        "additionalProperties": False,
                        "required": ["CAS_number"]
                       }
            }},
    # max_output_tokens = 16,
    reasoning = {
            "effort": 'low'
            }
)

print(prompt)
print(response.output_text)

#%%

# payload = {
#     "model": "gpt-5-mini",
#     "instructions": "You are Kai, the always-helpful AI.",  # dynamic injection, before server-side chat
#     "input": [
#         {
#             "role": "scientist",
#             "content": [
#                 {"type": "input_text", "text": "What's your 'Juice' setting currently?"},
#             ]
#         }
#     ],
#     "tools": [],
#     "parallel_tool_calls": False,   # if reasoning: 500 error with empty tools, even False
#     "tool_choice": "none",          # 500 error with empty tools, even "none"
#     "temperature": 1, "top_p": 1,   # denied on "o" reasoning models unless exactly 1
#     "text": {"format": {"type": "text"}},  # or {"type": "json_schema",...}
#     "max_output_tokens": 10_000,
#     "reasoning": {
#         "effort": None,        # low | medium | high
#         "summary": "detailed",  # reasoning models only supports "detailed"
#     },
#     "text": {"verbosity": None},
#     "stream": False,
#     "include": [
#         #"web_search_call.action.sources",  # seems to run ok whenever
#         #"file_search_call.results",  # 500 error without file_search tool
#         #"message.input_image.image_url",  # ok with no images sent
#         #"computer_call_output.output.image_url", # 500 error without codex model
#         #"code_interpreter_call.outputs",  # will fail if code interpreter tool not on
#         #"reasoning.encrypted_content"  # only if store:False, encrypted because proprietary, optional reuse for chat history resending
#     ],
#     "store": False,
#     "metadata": {},
#     "previous_response_id": None,
#     "truncation": "auto",   
#     "service_tier": "priority",  # "flex": o4-mini & o3 only; "priority":  more models allowed
# }




