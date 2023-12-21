from opendatagen.template import Template, TemplateManager, TemplateName, Variable
from opendatagen.data_generator import DataGenerator
from opendatagen.model import OpenAIChatModel, OpenAIInstructModel, OpenAIEmbeddingModel, ModelName, MistralChatModel
from mistralai.models.chat_completion import ChatMessage
from opendatagen.anonymizer import Anonymizer
from opendatagen.utils import function_to_call
from opendatagen.agent import DataAgent
import warnings
import json 
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pandas as pd

def anonymize_text(): 

    text_to_anonymize = """
            My name is Thomas, Call me at 0601010129 or email me at john.doe@example.com. 
            My SSN is 123-45-6789 and 4242 4242 8605 2607 is my credit card number. 
            Living in the best city in the world: Melbourne.
            New York & Co is a restaurant.
            It is 10 am.
            I have 10€ in my pocket. Oh my god.
            I have park my Tesla next to your house.
            My id is 0//1//2//2//2//2
    """
    
    completion_model = OpenAIChatModel(model_name="gpt-3.5-turbo-1106")

    anonymizer = Anonymizer(completion_model=completion_model)

    anonymized_text = anonymizer.anonymize(text=text_to_anonymize)
    
    print(anonymized_text)

def generate_data_from_predefined_template(template_file_path:str, template_name:str, output_path:str): 
    
    manager = TemplateManager(template_file_path=template_file_path)
    template = manager.get_template(template_name=template_name)

    if template:
        
        generator = DataGenerator(template=template)
        
        data = generator.generate_data(output_path=output_path)
        
        print(data)

def check_text(result: dict):

    relevant_sentence = result["relevant_sentence"].value.lower().replace("\n", " ").replace("'''", "")
    wikipedia_content = result["wikipedia_content"].value.lower().replace("\n", " ").replace("'''", "")

    if relevant_sentence in wikipedia_content:
        return True, "All ok."
    else:
        return False, "The sentence must be contained in the given text, please correct."


if __name__ == "__main__":

    #agent = DataAgent(model_name="gpt-4")
    #agent.run()
    #anonymize_text()
    '''
    generate_data_from_predefined_template(template_file_path="opendatagen/template.json", 
                                           template_name="factuality", 
                                           output_path="factuality.csv"
                                           )
    
    
    '''

    # Assuming 'factuality.csv' is in the same folder and has columns 'question' and 'answer'
    df = pd.read_csv('factuality.csv')

    # Initialize counters for each model
    true_counts = {'mistral7b': 0, 'mistra8x7b': 0, 'mistraX': 0, 'GPT35': 0}
    total_counts = {'mistral7b': 0, 'mistra8x7b': 0, 'mistraX': 0, 'GPT35': 0}

    for index, row in df.iterrows():
    
        print(f"Processing {index + 1}/{len(df)}")

        question = row['question']
        reference_answer = row['answer']

        mistral7b = MistralChatModel(name="mistral-tiny", max_tokens=64, temperature=[0])
        mistra8x7b = MistralChatModel(name="mistral-small", max_tokens=64, temperature=[0])
        mistraX = MistralChatModel(name="mistral-medium", max_tokens=64, temperature=[0])
        gpt35 = OpenAIChatModel(name="gpt-3.5-turbo-1106", max_tokens=64, temperature=[0])

        system_prompt_evaluator = "You are EvaluatorGPT, given the question and the reference answer please determine if the new answer is True or False. Only answer with 'True' or 'False'. No verbose."

        messages = [ChatMessage(role="user", content=f"Answer accurately and consicely to the following question:\n{question}")]

        gpt_messages = [
                {"role":"system", "content": "Answer to the question consicely."},
                {"role":"system", "content": f"Question:\n{question}"}
            ]

        answer7b = mistral7b.ask(messages=messages)
        answer8x7b = mistra8x7b.ask(messages=messages)
        answerX = mistraX.ask(messages=messages)
        answergpt35 = gpt35.ask(messages=gpt_messages)

        # For each model, evaluate the answer
        for model_name, model_answer in [('mistral7b', answer7b), ('mistra8x7b', answer8x7b), ('mistraX', answerX), ('GPT35', answergpt35)]:

            evaluator = OpenAIChatModel(name="gpt-4-1106-preview", max_tokens=5, system_prompt=system_prompt_evaluator)

            evaluator_messages = [
                {"role":"system", "content": system_prompt_evaluator},
                {"role":"system", "content": f"Question:\n{question}\nReference answer:\n{reference_answer}\nNew answer:\n{model_answer}"}
            ]
    
            evaluator_answer = evaluator.ask(messages=evaluator_messages)
            
            if evaluator_answer.lower() == "true":
                true_counts[model_name] += 1
            total_counts[model_name] += 1

    # Calculate and display the results
    for model_name in true_counts:
        accuracy = (true_counts[model_name] / total_counts[model_name]) * 100
        print(f"Model {model_name}: {accuracy:.2f}% True answers")

 