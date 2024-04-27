from llm.factory.context.context_course import ContextCourse
from llm.factory.context.context_system import ContextSystem
from llm.factory.context.context_report import ContextReport

class ContextFactory:
    def create_context(self,context_type):
        if context_type == 'course':
            return ContextCourse()
        elif context_type == 'system':
            return ContextSystem()
        elif context_type == 'report':
            return ContextReport()