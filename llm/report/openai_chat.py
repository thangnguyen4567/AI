from abc import abstractmethod

from openai import OpenAI
import google.generativeai as genai
from llm.report.base import LLMBase
from dotenv import load_dotenv
import os

class OpenAI_Chat(LLMBase):
    def __init__(self, config=None):
        LLMBase.__init__(self, config=config)

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def system_message(message: str) -> dict:
        return {"role": "system", "content": message}

    @staticmethod
    def user_message(message: str) -> dict:
        return {"role": "user", "content": message}

    @staticmethod
    def assistant_message(message: str) -> dict:
        return {"role": "assistant", "content": message}

    @staticmethod
    def str_to_approx_token_count(string: str) -> int:
        return len(string) / 4

    @staticmethod
    def add_ddl_to_prompt(initial_prompt: str, ddl_list: list[str], max_tokens: int = 14000) -> str:
        if len(ddl_list) > 0:
            initial_prompt += f"\nYou may use the following DDL statements as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for ddl in ddl_list:
                if OpenAI_Chat.str_to_approx_token_count(initial_prompt) + OpenAI_Chat.str_to_approx_token_count(ddl) < max_tokens:
                    initial_prompt += f"{ddl}\n\n"

        return initial_prompt

    @staticmethod
    def add_documentation_to_prompt(initial_prompt: str, documentation_list: list[str], max_tokens: int = 14000) -> str:
        if len(documentation_list) > 0:
            initial_prompt += f"\nYou may use the following documentation as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for documentation in documentation_list:
                if OpenAI_Chat.str_to_approx_token_count(initial_prompt) + OpenAI_Chat.str_to_approx_token_count(documentation) < max_tokens:
                    initial_prompt += f"{documentation}\n\n"

        return initial_prompt

    @staticmethod
    def add_sql_to_prompt(initial_prompt: str, sql_list: list[str], max_tokens: int = 14000) -> str:
        if len(sql_list) > 0:
            initial_prompt += f"\nYou may use the following SQL statements as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for question in sql_list:
                if OpenAI_Chat.str_to_approx_token_count(initial_prompt) + OpenAI_Chat.str_to_approx_token_count(question["sql"]) < max_tokens:
                    initial_prompt += f"{question['question']}\n{question['sql']}\n\n"

        return initial_prompt

    def get_sql_prompt(
        self,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs,
    ):
        initial_prompt = "The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.\n\nRespond with only SQL code. Do not answer with any explanations -- just the code.\n"

        initial_prompt = OpenAI_Chat.add_ddl_to_prompt(initial_prompt, ddl_list, max_tokens=14000)

        initial_prompt = OpenAI_Chat.add_documentation_to_prompt(initial_prompt, doc_list, max_tokens=14000)

        message_log = [OpenAI_Chat.system_message(initial_prompt)]

        for example in question_sql_list:
            if example is None:
                print("example is None")
            else:
                if example is not None and "question" in example and "sql" in example:
                    message_log.append(OpenAI_Chat.user_message(example["question"]))
                    message_log.append(OpenAI_Chat.assistant_message(example["sql"]))
    
        message_log.append({"role": "user", "content": question})

        return message_log

    def submit_prompt(self, prompt, **kwargs) -> str:

        response = self.client.chat.completions.create(
            model='gpt-4o', messages=prompt, max_tokens=500, stop=None, temperature=0.7
        )

        for (
            choice
        ) in (
            response.choices
        ):  # Find the first response from the chatbot that has text in it (some responses may not have text)
            if "text" in choice:
                return choice.text

        return response.choices[
            0
        ].message.content  # If no response with text is found, return the first response's content (which may be empty)