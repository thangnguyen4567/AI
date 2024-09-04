from llm.factory.training.training_course import TrainingCourse
from llm.factory.training.training_system import TrainingSystem
from llm.factory.training.training_ddl import TrainingDDL
from llm.factory.training.training_sql import TrainingSQL
from llm.factory.training.training_chatbot import TrainingChatbot

class TrainingFactory:
    def create_training(self,training_type):
        if training_type == 'training_course':
            return TrainingCourse()
        elif training_type == 'training_system':
            return TrainingSystem()
        elif training_type == 'training_sql':
            return TrainingSQL()
        elif training_type == 'training_ddl':
            return TrainingDDL()
        elif training_type == 'chatbot':
            return TrainingChatbot()