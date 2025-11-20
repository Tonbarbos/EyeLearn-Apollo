from database import DatabaseManager


class TeacherDashboardLogic:
    def __init__(self):
        self.db = DatabaseManager()

    def get_students(self):
        """Busca lista de alunos para o painel."""
        query = """
            SELECT 
                id,
                nomeCompleto as nome,
                TIMESTAMPDIFF(YEAR, dataNascimento, CURDATE()) as idade,
                CONCAT(serieEscola, ' - ', turma) as turma
            FROM Alunos
        """
        return self.db.fetch_all(query)

    def delete_student(self, student_id):
        """Remove um aluno do banco."""
        query = "DELETE FROM Alunos WHERE id = %s"
        self.db.execute_query(query, (student_id,))
        return True

    def get_student_details(self, student_id):
        """Busca detalhes completos de um aluno pelo ID."""
        # 1. Dados Pessoais
        query_info = """
            SELECT *, TIMESTAMPDIFF(YEAR, dataNascimento, CURDATE()) as idade 
            FROM Alunos WHERE id = %s
        """
        student = self.db.fetch_one(query_info, (student_id,))

        if not student:
            return None

        # 2. Dados Agregados (Médias)
        query_stats = """
            SELECT 
                COUNT(*) as total_sessoes,
                COALESCE(AVG(pontuacao_final), 0) as media_pontuacao,
                COALESCE(SUM(erros_count), 0) as total_erros
            FROM Sessoes 
            WHERE aluno_id = %s
        """
        stats = self.db.fetch_one(query_stats, (student_id,))
        if not stats:
            stats = {"total_sessoes": 0, "media_pontuacao": 0, "total_erros": 0}

        # 3. --- NOVO: Buscar o Heatmap da ÚLTIMA sessão ---
        query_heatmap = """
            SELECT caminhoMapaCalor 
            FROM Sessoes 
            WHERE aluno_id = %s 
            ORDER BY data_sessao DESC 
            LIMIT 1
        """
        last_session = self.db.fetch_one(query_heatmap, (student_id,))

        heatmap_path = last_session['caminhoMapaCalor'] if last_session else None

        # Mescla tudo e adiciona o caminho do heatmap
        result = {**student, **stats}
        result['heatmap_path'] = heatmap_path

        return result

    def get_dashboard_title(self):
        return "Painel do Professor"

    def get_students_list_title(self):
        return "Meus Alunos"

    def logout(self):
        print("Teacher logged out.")
        return True # Simulate successful logout

if __name__ == '__main__':
    logic = TeacherDashboardLogic()
    print("Alunos encontrados:", logic.get_students())

