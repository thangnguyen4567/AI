from llm.factory.training.course import TrainingCourse
from llm.factory.training.system import TrainingSystem
class TrainingFactory:
    def create_training(self,training_type):
        if training_type == 'training_course':
            return TrainingCourse()
        elif training_type == 'training_system':
            return TrainingSystem()