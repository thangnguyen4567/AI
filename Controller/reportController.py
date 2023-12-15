from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from flask import current_app
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from config.config_vectordb import connect_vectordb
load_dotenv('.env')

def reportController(request):
    requestJson = request.get_json()
    userQuestion = requestJson["question"]
    with current_app.app_context():
        app = current_app
    prompt = get_training_prompt(userQuestion)
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    chain = create_sql_query_chain(llm, app.sql_db)
    query = chain.invoke({"question": prompt.format(input=userQuestion)})
    answer = query.replace("\n", " ")
    result = {'question': userQuestion, 'answer': answer}
    return result

def get_training_prompt(userQuestion):
    vectordb = connect_vectordb()
    docs = vectordb.similarity_search(query=userQuestion,k=3)
    questions = []
    for value in docs:
        question = {}
        question['question'] = value.page_content
        question['answer'] = value.metadata['query']
        questions.append(question)
    example_prompt = PromptTemplate(input_variables=["question", "answer"], 
                                    template=
                                    """
                                        When query compare name add N'' 
                                        'Danh sách' and 'Báo cáo' and 'Thống kê' have the same meaning
                                        Some examples of SQL queries that correspond to questions are:
                                        {question}\n answer:{answer}
                                    """
                                    )
    prompt = FewShotPromptTemplate(
        examples=questions,
        example_prompt=example_prompt,
        suffix="Question: {input}",
        input_variables=["input"]
    )
    return prompt