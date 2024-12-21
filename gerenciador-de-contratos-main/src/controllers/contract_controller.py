import os
import csv
import sqlite3

class ContractController:
    def __init__(self, file_path="data/contratos.csv", db_path="data/contracts.db"):
        self.file_path = file_path
        self.db_path = db_path
        self.ensure_data_directory_exists()

    def ensure_data_directory_exists(self):
        """Garante que o diretório para o arquivo CSV e banco de dados exista."""
        dir_path = os.path.dirname(self.file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def load_contracts(self):
        """Carrega contratos do arquivo CSV."""
        contracts = []
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                contracts = [row for row in reader]
        except FileNotFoundError:
            pass  # Usamos 'pass' aqui para não fazer nada se o arquivo não existir.
        return contracts

    def save_contracts(self, contracts):
        """Salva a lista de contratos no arquivo CSV."""
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ["Descrição do Contrato", "Categoria", "Data de Vencimento", "Fornecedor"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contracts)

    def add_contract(self, contract):
        """Adiciona um novo contrato ao CSV."""
        contracts = self.load_contracts()
        contracts.append(contract)
        self.save_contracts(contracts)

    def delete_contract(self, description):
        """Deleta um contrato com base na descrição."""
        contracts = self.load_contracts()
        contracts = [c for c in contracts if c["Descrição do Contrato"] != description]
        self.save_contracts(contracts)

    def update_contract(self, description, updated_contract):
        """Atualiza um contrato com base na descrição."""
        contracts = self.load_contracts()
        for i, contract in enumerate(contracts):
            if contract["Descrição do Contrato"] == description:
                contracts[i] = updated_contract
                break
        self.save_contracts(contracts)

    def import_csv_to_sqlite(self):
        """Importa os contratos do CSV para o banco de dados SQLite."""
        contracts = self.load_contracts()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT,
                    categoria TEXT,
                    vencimento TEXT,
                    fornecedor TEXT
                )
            ''')
            for contract in contracts:
                cursor.execute('''
                    INSERT INTO contracts (descricao, categoria, vencimento, fornecedor)
                    VALUES (?, ?, ?, ?)
                ''', (
                    contract["Descrição do Contrato"],
                    contract["Categoria"],
                    contract["Data de Vencimento"],
                    contract["Fornecedor"]
                ))
            conn.commit()

    def export_sqlite_to_csv(self):
        """Exporta os contratos do banco de dados SQLite para o arquivo CSV."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT descricao, categoria, vencimento, fornecedor FROM contracts")
            rows = cursor.fetchall()
            contracts = [
                {
                    "Descrição do Contrato": row[0],
                    "Categoria": row[1],
                    "Data de Vencimento": row[2],
                    "Fornecedor": row[3]
                } for row in rows
            ]
            self.save_contracts(contracts)

# Exemplo de uso
if __name__ == "__main__":
    controller = ContractController()

    # Adicionando um contrato
    new_contract = {
        "Descrição do Contrato": "Serviço de TI",
        "Categoria": "Tecnologia",
        "Data de Vencimento": "2024-12-31",
        "Fornecedor": "Empresa XYZ"
    }
    controller.add_contract(new_contract)

    # Listando contratos
    contracts = controller.load_contracts()
    print("Contratos:", contracts)

    # Atualizando um contrato
    updated_contract = {
        "Descrição do Contrato": "Serviço de TI",
        "Categoria": "Tecnologia Atualizada",
        "Data de Vencimento": "2025-01-01",
        "Fornecedor": "Empresa XYZ"
    }
    controller.update_contract("Serviço de TI", updated_contract)

    # Deletando um contrato
    controller.delete_contract("Serviço de TI")

    # Importando contratos do CSV para o SQLite
    controller.import_csv_to_sqlite()

    # Exportando contratos do SQLite para o CSV
    controller.export_sqlite_to_csv()