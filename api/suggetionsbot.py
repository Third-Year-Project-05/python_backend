# """suggetionsBot.ipynb

# Automatically generated by Colab.

# Original file is located at
#     https://colab.research.google.com/drive/1_7o8brYHWrAiZlPqyAzNNOjGh6L2YrVu
# """

import os
from dotenv import load_dotenv
import warnings
from langchain_openai import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import time
import json  
warnings.filterwarnings("ignore", category=DeprecationWarning)

class SuggestionsBot:
    def __init__(self):
        self.load_env_variables()
        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
        self.examples = self.get_examples()
        self.few_shot_prompt = self.create_few_shot_prompt()
        self.prompt = self.create_chat_prompt_template()

    def load_env_variables(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

    def get_examples(self):
        return [
            {"Question": "Did you eat ?", "Answer": ["Yes", "No"]},
            {"Question": "Do you have a car ?", "Answer": ["Yes", "No"]},
            {"Question": "Where are you now ?", "Answer": ["In the home", "In the school", "another place"]},
            {"Question": "There is a car", "Answer": ["yeah I see, man"]},
            {"Question": "What is your name ? who are you ?", "Answer": ["My Name is Dilum Induwara"]},
        ]

    def create_few_shot_prompt(self):
        example_prompt = PromptTemplate(
            input_variables=["Question", "Answer"],
            template="Question: {Question}\nAnswer: {Answer}"
        )
        return FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=example_prompt,
            suffix="Question: {input}",
            input_variables=["input"]
        )

    def create_chat_prompt_template(self):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="If some one ask some personal details from you. then if you have it please response with give that data. If you haven any that data then response for message is ('I am don't know it.'). Now your are not a chatbot. your are now human. Your name is Dilum Induwara. No need metion another parts."),
                MessagesPlaceholder(variable_name="history"),
                MessagesPlaceholder(variable_name="input")
            ]
        )

    def get_response(self, user_input, history=[]):
        final_prompt = [
            {"role": "system", "content": "If some one ask some personal details from you. then if you have it please response with give that data. If you haven any that data then response for message is ('I am don't know it.'). Now your are not a chatbot. your are now human. Your name is Dilum Induwara. No need metion another parts."},
            {"role": "system", "content": self.few_shot_prompt.format(input=user_input)},
            {"role": "user", "content": user_input}
        ]
        
        # Insert history messages after the first messages
        for item in history:
            final_prompt.insert(2, item) 

        start_time = time.time()

        response = self.llm(self.few_shot_prompt.format(input=user_input)).content
        
        end_time = time.time()

        # Calculate Time
        elapsed_time = end_time - start_time

        # Process response to extract the answer list
        try:
            # Assuming the response is in the format "Answer: ['I am doing well, thank you for asking']"
            answer_start = response.find("Answer: ") + len("Answer: ")
            answer = response[answer_start:].strip()
            answer_list = json.loads(answer)
        except (json.JSONDecodeError, ValueError):
            answer_list = response

        print(answer_list," Time:",elapsed_time)

        return answer

