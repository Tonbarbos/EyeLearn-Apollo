
class TeacherDashboardLogic:
    def __init__(self):
        self._students = [
            {"nome": "Maria Silva", "idade": 8, "turma": "2º ano - Turma A", "pontuacao": 90},
            {"nome": "João Santos", "idade": 9, "turma": "3º ano - Turma B", "pontuacao": 75},
            {"nome": "Ana Oliveira", "idade": 7, "turma": "1º ano - Turma C", "pontuacao": 95},
        ]

    def get_students(self):
        return self._students

    def get_student_details(self, student_name):
        for student in self._students:
            if student["nome"] == student_name:
                return student
        return None

    def get_dashboard_title(self):
        return "Painel do Professor"

    def get_students_list_title(self):
        return "Meus Alunos"

    def logout(self):
        # In a real application, this would handle session termination, etc.
        print("Teacher logged out.")
        return True # Simulate successful logout

if __name__ == '__main__':
    logic = TeacherDashboardLogic()
    print("Students:", logic.get_students())
    print("Details for Maria Silva:", logic.get_student_details("Maria Silva"))
    print("Dashboard Title:", logic.get_dashboard_title())
    logic.logout()

