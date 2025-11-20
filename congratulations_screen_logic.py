from database import DatabaseManager

class CongratulationsScreenLogic:

    def __init__(self, score, time_elapsed, errors, student_id=None):
        self.db = DatabaseManager()
        self._score = score
        self._time_elapsed = time_elapsed
        self._errors = errors
        self.student_name = self._get_student_name(student_id)

    def _get_student_name(self, student_id):
        if not student_id:
            return "Visitante"

        try:
            # Busca apenas o primeiro nome para ser mais amigável
            query = "SELECT nomeCompleto FROM Alunos WHERE id = %s"
            result = self.db.fetch_one(query, (student_id,))
            if result:
                return result['nomeCompleto'].split()[0]
        except Exception as e:
            print(f"Erro ao buscar nome do aluno: {e}")

        return "Visitante"

    def get_formatted_score(self):
        return f"{self._score}%"

    def get_formatted_time(self):
        minutes = self._time_elapsed // 60
        seconds = self._time_elapsed % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_errors(self):
        return str(self._errors)

    def get_star_rating(self):
        if self._score >= 80: return 5
        if self._score >= 60: return 4
        if self._score >= 40: return 3
        if self._score >= 20: return 2
        return 1

    def get_activity_results(self):
        return {
            "activity_name": "Jogo da Memória",
            "score": self.get_formatted_score(),
            "time": self.get_formatted_time(),
            "errors": self.get_errors()
        }

    def get_congratulations_message(self):
        return f"Parabéns, {self.student_name}!"

    def get_subtitle_message(self):
        return "Você completou a atividade com sucesso!"

    def get_general_score_title(self):
        return "Pontuação Geral"

    def get_results_by_activity_title(self):
        return "Resultados por Atividade"

    def get_activity_star_rating(self):
        return self.get_star_rating()