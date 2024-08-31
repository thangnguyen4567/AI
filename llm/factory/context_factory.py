from llm.factory.context.context_course import ContextCourse
from llm.factory.context.context_system import ContextSystem
from llm.factory.context.context_report import ContextReport
from llm.factory.context.context_trungnguyen import ContextTrungNguyen
from llm.factory.context.context_highlands import ContextHighlands

class ContextFactory:
    def create_context(self,context_type):
        if context_type == 'course':
            return ContextCourse()
        elif context_type == 'system':
            return ContextSystem()
        elif context_type == 'report':
            return ContextReport()
        elif context_type == 'webcafe':
            return ContextTrungNguyen()
        elif context_type == 'highlands':
            return ContextHighlands()
