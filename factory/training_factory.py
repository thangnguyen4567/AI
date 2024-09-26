from project.lms.training.training_course import TrainingCourse
from project.lms.training.training_resource import TrainingResource
from project.report.training.training_ddl import TrainingDDL
from project.report.training.training_sql import TrainingSQL

class TrainingFactory:
    def create_training(self,training_type):
        if training_type == 'course':
            return TrainingCourse()
        elif training_type == 'resource':
            return TrainingResource()
        elif training_type == 'training_sql':
            return TrainingSQL()
        elif training_type == 'training_ddl':
            return TrainingDDL()