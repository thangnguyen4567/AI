from llm.factory.context.course import ContextCourse
from llm.factory.context.system import ContextSystem
class ContextFactory:
    def create_context(self,context_type):
        if context_type == 'course':
            return ContextCourse()
        elif context_type == 'system':
            return ContextSystem()