
class StudentDashboardLogic:
    def __init__(self, student_name="Maria", student_level=2, student_class="2º ano - Turma A"):
        self._student_name = student_name
        self._student_level = student_level
        self._student_class = student_class

        self._activities = [
            {"title": "Associação de Formas", "icon": "fa5s.puzzle-piece", "status": "Concluído", "color": "#4CAF50"},
            {"title": "Percepção Cromática", "icon": "fa5s.palette", "status": "Disponível", "color": "#2196F3"},
            {"title": "Reconhecimento Simbólico", "icon": "fa5s.lightbulb", "status": "Bloqueado", "color": "#9E9E9E"},
            {"title": "Jogo da Memória", "icon": "fa5s.brain", "status": "Disponível", "color": "#FFC107"}
        ]

        self._recent_activities = [
            {"title": "Associação de Formas", "icon": "fa5s.puzzle-piece", "score": "85%", "date": "Hoje, 10:30"},
            {"title": "Percepção Cromática", "icon": "fa5s.palette", "score": "92%", "date": "Ontem, 14:15"}
        ]

    def get_student_info(self):
        return {
            "name": self._student_name,
            "level": self._student_level,
            "class": self._student_class
        }

    def get_greeting_message(self):
        return f"Olá, {self._student_name}!"

    def get_available_activities(self):
        return self._activities

    def get_recent_activities(self):
        return self._recent_activities

    def get_available_activities_title(self):
        return "Atividades Disponíveis"

    def get_recent_activities_title(self):
        return "Atividades Recentes"

    def logout(self):
        # In a real application, this would handle session termination, etc.
        print(f"Student {self._student_name} logged out.")
        return True # Simulate successful logout

if __name__ == '__main__':
    logic = StudentDashboardLogic()
    print("Student Info:", logic.get_student_info())
    print("Greeting:", logic.get_greeting_message())
    print("Available Activities:", logic.get_available_activities())
    print("Recent Activities:", logic.get_recent_activities())
    logic.logout()

