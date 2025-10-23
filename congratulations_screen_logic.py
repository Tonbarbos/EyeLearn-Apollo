
class CongratulationsScreenLogic:
    def __init__(self, score, time_elapsed, errors):
        self._score = score
        self._time_elapsed = time_elapsed
        self._errors = errors

    def get_formatted_score(self):
        # Assuming score is a percentage or needs to be displayed as such
        return f"{self._score}%"

    def get_formatted_time(self):
        minutes = self._time_elapsed // 60
        seconds = self._time_elapsed % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_errors(self):
        return str(self._errors)

    def get_star_rating(self):
        # Simple example: 1 star for every 20% score
        return self._score // 20

    def get_activity_results(self):
        # This could be expanded to include results from multiple activities
        return {
            "activity_name": "Jogo da Memória",
            "score": self.get_formatted_score(),
            "time": self.get_formatted_time(),
            "errors": self.get_errors()
        }

    def get_congratulations_message(self, student_name="Maria"):
        return f"Parabéns, {student_name}!"

    def get_subtitle_message(self):
        return "Você completou todas as atividades"

    def get_general_score_title(self):
        return "Pontuação Geral"

    def get_results_by_activity_title(self):
        return "Resultados por Atividade"

    def get_activity_star_rating(self):
        # Pode ser a mesma lógica do get_star_rating geral ou uma lógica específica para a atividade
        return self._score // 20

if __name__ == '__main__':
    # Example usage
    logic = CongratulationsScreenLogic(score=85, time_elapsed=150, errors=3)
    print("Formatted Score:", logic.get_formatted_score())
    print("Formatted Time:", logic.get_formatted_time())
    print("Errors:", logic.get_errors())
    print("Star Rating:", logic.get_star_rating())
    print("Activity Results:", logic.get_activity_results())
    print("Congratulations Message:", logic.get_congratulations_message())

