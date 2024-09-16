from project.lms.training.training_course import TrainingCourse
from project.lms.training.training_system import TrainingSystem
from project.report.training.training_ddl import TrainingDDL
from project.report.training.training_sql import TrainingSQL
from project.cskh.training.training import TrainingChatbot

class TrainingFactory:
    def create_training(self,training_type):
        if training_type == 'course':
            return TrainingCourse()
        elif training_type == 'system':
            return TrainingSystem()
        elif training_type == 'training_sql':
            return TrainingSQL()
        elif training_type == 'training_ddl':
            return TrainingDDL()
        elif training_type == 'chatbot':
            return TrainingChatbot()