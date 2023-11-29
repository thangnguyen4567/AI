from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from flask import current_app
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
load_dotenv('.env')
def reportControllerV2(request):
    requestJson = request.get_json()
    userQuestion = requestJson["question"]
    with current_app.app_context():
        app = current_app
    questions = []
    docs = app.vector_db.similarity_search(query=userQuestion)
    for value in docs:
        question = {}
        question['question'] = value.page_content
        question['answer'] = value.metadata['query']
        questions.append(question)
    example_prompt = PromptTemplate(input_variables=["question", "answer"], 
                                    template=
                                    """
                                        When query compare name add N'' 
                                        Some examples of SQL queries that correspond to questions are:
                                        {question}\n{answer}
                                    """
                                    )
    prompt = FewShotPromptTemplate(
        examples=questions,
        example_prompt=example_prompt,
        suffix="Question: {input}",
        input_variables=["input"]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0)
    chain = create_sql_query_chain(llm, app.sql_db)
    query = chain.invoke({"question": prompt.format(input=userQuestion)})
    answer = query.replace("\n", " ")
    result = {'question': userQuestion, 'answer': answer}
    return result