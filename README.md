# EyeLearn-Apollo 👁️🧠

**EyeLearn Apollo** é uma aplicação desktop desenvolvida para auxiliar na avaliação neurocognitiva de crianças (7 a 10 anos) através de atividades gamificadas. O sistema utiliza técnicas de **Rastreamento Ocular (Eye Tracking)** e geração de **Mapas de Calor (Heatmaps)** para identificar padrões de atenção que podem indicar neurodivergências, como TDAH ou Dislexia.

## 📋 Funcionalidades

* **Gamificação:** "Jogo da Memória" interativo para engajar o aluno.
* **Rastreamento Ocular (Híbrido):**
    * Simulação via Mouse (para testes e demonstração).
    * Integração com Webcam via OpenCV e Haar Cascades (para detecção facial e pupilar).
* **Análise de Dados:**
    * Geração automática de **Mapas de Calor (Heatmaps)** sobrepostos à tela do jogo.
    * Cálculo de métricas: Pontuação, Tempo de Conclusão e Erros.
* **Painéis de Usuário:**
    * **Aluno:** Interface amigável para realização das atividades.
    * **Professor:** Dashboard administrativo para cadastro de alunos, visualização de relatórios e análise dos mapas de calor.
* **Persistência de Dados:** Banco de dados MySQL para histórico de sessões e perfis.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Interface Gráfica:** PyQt6 (QtAwesome para ícones)
* **Visão Computacional:** OpenCV (cv2), NumPy
* **Banco de Dados:** MySQL (mysql-connector-python)

## 🚀 Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:
1.  **Python 3.11** ou superior.
2.  **MySQL Server** (rodando localmente).
3.  **Git** (opcional, para clonar o repositório).

## 📦 Instalação e Configuração

Siga os passos abaixo para rodar o projeto em seu ambiente local.

### 1. Clonar o Repositório
  // git clone [https://github.com/seu-usuario/EyeLearn-Apollo.git](https://github.com/seu-usuario/EyeLearn-Apollo.git)
  // cd EyeLearn-Apollo

### 2. Criar ambiente virtual
# Windows
  // python -m venv venv
  // venv\Scripts\activate

# Linux/Mac
  // python3 -m venv venv
  // source venv/bin/activate

### 3. Instalar dependências
  // pip install -r requirements.txt

### 4. Configurar banco de dados
O projeto possui um script automatizado para criar o banco e as tabelas necessárias.

Abra o arquivo database.py na raiz do projeto.

Verifique e altere as configurações de conexão no método setup() e __init__:

  self.config = {
    'host': 'localhost',
    'user': 'root',      # Seu usuário do MySQL
    'password': '',      # Sua senha do MySQL
    'database': 'EyeLearnDB'
}

Execute o script de configuração inicial:
  // python database.py
  
Isso criará o banco EyeLearnDB e as tabelas Alunos, Sessoes e Diagnosticos automaticamente.

OBS: Caso deseje configurar o seu banco de dados do MySQL conforme o padrão do sistema, utilise como usuario = 'admin', e como senha = '$enhaF0rt3'

### 5. Executar o programa principal
  // python main.py

## 📂 Estrutura do Projeto
* **main.py:** Gerenciador de janelas e fluxo principal.

* **database.py:** Gerenciador de conexão e setup do MySQL.

* **heatmap_generator.py:** Lógica de criação e processamento dos mapas de calor.

* **tela_*.py:** Arquivos de interface gráfica (Views).

* ***_logic.py:** Regras de negócio (Controllers).

* **project/capturers/:** Algoritmos de detecção facial/ocular (Haar Cascade).

* **assets/:** Imagens, ícones e onde os heatmaps são salvos.
