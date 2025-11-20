from database import DatabaseManager


class StudentDashboardLogic:
    def __init__(self):
        self.db = DatabaseManager()
        self.student_id = None
        # Dados padrão
        self.student_data = {"name": "Visitante", "level": "-", "class": "-"}

    def set_student_id(self, student_id):
        print(f"--- DEBUG: set_student_id chamado com ID: {student_id} ---")
        self.student_id = student_id
        self._load_student_data()

    def _load_student_data(self):
        if not self.student_id:
            print("--- DEBUG: ID é None ou inválido, cancelando busca ---")
            return

        print(f"--- DEBUG: Buscando aluno ID {self.student_id} no banco... ---")

        # Buscar dados do Aluno
        query_aluno = "SELECT nomeCompleto, serieEscola, turma FROM Alunos WHERE id = %s"

        try:
            aluno = self.db.fetch_one(query_aluno, (self.student_id,))
            print(f"--- DEBUG: Resultado do banco: {aluno} ---")

            if aluno:
                primeiro_nome = aluno['nomeCompleto'].split()[0]
                self.student_data = {
                    "name": primeiro_nome,
                    "level": aluno['serieEscola'],
                    "class": aluno['turma']
                }
                print(f"--- DEBUG: Dados atualizados: {self.student_data} ---")
            else:
                print("--- DEBUG: Aluno não encontrado no banco! ---")

        except Exception as e:
            print(f"--- DEBUG ERRO CRÍTICO: {e} ---")

    def get_student_info(self):
        return self.student_data

    def get_greeting_message(self):
        return f"Olá, {self.student_data['name']}!"

    def get_available_activities(self):
        # Por enquanto, mantemos fixo pois as atividades são do sistema, não do banco
        return [
            {"title": "Jogo da Memória", "icon": "fa5s.brain", "status": "Disponível", "color": "#FFC107"},
            {"title": "Associação de Formas", "icon": "fa5s.puzzle-piece", "status": "Em Breve", "color": "#9E9E9E"},
            {"title": "Percepção Cromática", "icon": "fa5s.palette", "status": "Em Breve", "color": "#9E9E9E"},
        ]

    def get_recent_activities(self):
        if not self.student_id:
            return []

        # 2. Buscar últimas sessões do aluno no banco
        query_sessoes = """
            SELECT 
                pontuacao_final as score, 
                DATE_FORMAT(data_sessao, '%d/%m %H:%i') as date
            FROM Sessoes 
            WHERE aluno_id = %s 
            ORDER BY data_sessao DESC 
            LIMIT 3
        """
        sessoes = self.db.fetch_all(query_sessoes, (self.student_id,))

        activities = []
        for s in sessoes:
            activities.append({
                "title": "Jogo da Memória",  # Por enquanto só temos esse jogo
                "icon": "fa5s.brain",
                "score": f"{s['score']} pts",
                "date": s['date']
            })

        return activities


