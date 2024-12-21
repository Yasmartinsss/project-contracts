import sqlite3
import shutil

DB_PATH = "data/tasks.db"

def create_task(title, description):
    """Cria uma nova tarefa no banco de dados."""
    if not title or not description:
        print("Título e descrição são obrigatórios!")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
            conn.commit()
            print(f"Tarefa '{title}' criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tarefa: {e}")

def get_tasks():
    """Obtém todas as tarefas do banco de dados."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao obter as tarefas: {e}")
        return []

def update_task(task_id, title, description, status):
    """Atualiza uma tarefa existente no banco de dados."""
    if not title or not description:
        print("Título e descrição são obrigatórios!")
        return

    # Validação de status
    valid_statuses = ["Pendente", "Em andamento", "Concluído"]
    if status not in valid_statuses:
        print(f"Status inválido! Os status válidos são: {', '.join(valid_statuses)}")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, status = ?
            WHERE id = ?
            ''', (title, description, status, task_id))

            # Verificando se a tarefa foi encontrada e atualizada
            if cursor.rowcount == 0:
                print(f"Tarefa com ID {task_id} não encontrada!")
                return

            conn.commit()
            print(f"Tarefa {task_id} atualizada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar a tarefa: {e}")

def delete_task(task_id):
    """Deleta uma tarefa com base no ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

            if cursor.rowcount == 0:
                print(f"Tarefa com ID {task_id} não encontrada!")
                return

            print(f"Tarefa {task_id} deletada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar a tarefa: {e}")

def backup_database():
    """Faz um backup do banco de dados para um arquivo separado."""
    try:
        shutil.copy(DB_PATH, "data/tasks_backup.db")
        print("Backup do banco de dados realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar o backup do banco de dados: {e}")

def initialize_db():
    """Cria a tabela de tarefas no banco de dados, caso não exista."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL
            )
            ''')
            conn.commit()
            print("Tabela de tarefas criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

# Exemplo de uso
if __name__ == "__main__":
    initialize_db()  # Cria a tabela de tarefas no banco de dados se não existir

    # Adicionando uma nova tarefa
    create_task("Estudar Python", "Estudar SQLite e Tkinter para o projeto.")

    # Listando todas as tarefas
    tasks = get_tasks()
    print("Tarefas:", tasks)

    # Atualizando uma tarefa
    update_task(1, "Estudar Python Avançado", "Estudar SQLite e customtkinter.", "Em andamento")

    # Deletando uma tarefa
    delete_task(1)

    # Realizando backup do banco de dados
    backup_database()
