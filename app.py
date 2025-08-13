import os
from flask import Flask, render_template, request, jsonify
import psycopg2

# --- Configuração do Flask ---
app = Flask(__name__)

# --- Configuração do Banco de Dados ---
# ATENÇÃO: Substitua 'SUA_SENHA_DO_POSTGRES' pela senha que você criou
# na instalação do PostgreSQL.
DB_HOST = "localhost"
DB_NAME = "gerenciamento_clientes"
DB_USER = "postgres"
DB_PASS = "postgres"

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# --- ROTAS DO SERVIDOR WEB ---

# Rota para servir a página de gerenciamento (cadastro)
@app.route('/')
def gerenciamento():
    # render_template busca o arquivo na pasta 'templates'
    return render_template('gerenciamento.html')

# Rota para servir a página de listagem
@app.route('/listagem')
def listagem():
    return render_template('listagem.html')

# Rota para servir a página de edição
@app.route('/edicao')
def edicao():
    return render_template('edicao.html')

# Rota para servir a página de financiamento
@app.route('/financiamento')
def financiamento():
    return render_template('financiamento.html')

# Rota para servir a página de listagem de empréstimos
@app.route('/listagem-emprestimos')
def listagem_emprestimos():
    return render_template('listagem-emprestimos.html')

# Rota para receber os dados do formulário de cadastro de clientes
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    data = request.json  # Esperamos dados no formato JSON
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')

    # Validação básica dos campos obrigatórios
    if not nome or not telefone:
        return jsonify({"message": "Nome e Telefone são campos obrigatórios."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s) RETURNING telefone;",
            (nome, email, telefone)
        )
        cliente_telefone = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Cliente cadastrado com sucesso!", "telefone": cliente_telefone}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"message": "Erro: Telefone já cadastrado. O telefone deve ser único."}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao cadastrar o cliente.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para buscar e listar todos os clientes
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, telefone FROM clientes;")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    # Formatar os resultados para JSON
    clientes_formatados = []
    for cliente in clientes:
        clientes_formatados.append({ 
            "nome": cliente[0],
            "email": cliente[1],
            "telefone": cliente[2]
        })
    return jsonify(clientes_formatados)

# Rota para deletar um cliente por telefone
@app.route('/clientes/<string:telefone>', methods=['DELETE'])
def deletar_cliente(telefone):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM clientes WHERE telefone = %s", (telefone,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Cliente não encontrado."}), 404
        return jsonify({"message": "Cliente excluído com sucesso!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao excluir o cliente.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
    # Rota para deletar um empréstimo por ID
@app.route('/emprestimos/<int:id>', methods=['DELETE'])
def deletar_emprestimo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM emprestimos WHERE id = %s", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Empréstimo não encontrado."}), 404

        return jsonify({"message": "Empréstimo excluído com sucesso!"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao excluir o empréstimo.", "error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
    
    
# Rota para buscar os dados de um único cliente por telefone
@app.route('/clientes/<string:telefone>', methods=['GET'])
def buscar_cliente(telefone):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT nome, email, telefone FROM clientes WHERE telefone = %s", (telefone,))
        cliente = cursor.fetchone()

        if cliente is None:
            return jsonify({"message": "Cliente não encontrado."}), 404

        cliente_formatado = {
            "nome": cliente[0],
            "email": cliente[1],
            "telefone": cliente[2]
        }
        
        return jsonify(cliente_formatado), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao buscar o cliente.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para atualizar os dados de um cliente por telefone
@app.route('/clientes/<string:telefone>', methods=['PUT'])
def atualizar_cliente(telefone):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    
    if not nome:
        return jsonify({"message": "Nome é um campo obrigatório."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE clientes SET nome = %s, email = %s WHERE telefone = %s",
            (nome, email, telefone)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Cliente não encontrado ou dados não alterados."}), 404

        return jsonify({"message": "Cliente atualizado com sucesso!"}), 200
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"message": "Erro: Telefone já cadastrado. O telefone deve ser único."}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao atualizar o cliente.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
# Rota para cadastrar um novo empréstimo
@app.route('/emprestimos', methods=['POST'])
def cadastrar_emprestimo():
    data = request.json
    valor_emprestado = data.get('valor_emprestado')
    juros_mensal = data.get('juros_mensal')
    num_meses = data.get('num_meses')
    detalhes = data.get('detalhes')
    cliente_telefone = data.get('cliente_telefone')

    if not all([valor_emprestado, juros_mensal, num_meses, cliente_telefone]):
        return jsonify({"message": "Campos obrigatórios faltando."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO emprestimos (valor_emprestado, juros_mensal, num_meses, detalhes, cliente_telefone) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (valor_emprestado, juros_mensal, num_meses, detalhes, cliente_telefone)
        )
        emprestimo_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Empréstimo cadastrado com sucesso!", "id": emprestimo_id}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"message": "Erro: Telefone do cliente não existe."}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao cadastrar o empréstimo.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota para listar os empréstimos de um cliente específico por telefone
@app.route('/emprestimos/<string:telefone>', methods=['GET'])
def listar_emprestimos_cliente(telefone):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, valor_emprestado, juros_mensal, num_meses, detalhes FROM emprestimos WHERE cliente_telefone = %s",
            (telefone,)
        )
        emprestimos = cursor.fetchall()

        emprestimos_formatados = []
        for emprestimo in emprestimos:
            emprestimos_formatados.append({
                "id": emprestimo[0],
                "valor_emprestado": str(emprestimo[1]),
                "juros_mensal": str(emprestimo[2]),
                "num_meses": emprestimo[3],
                "detalhes": emprestimo[4]
            })
        return jsonify(emprestimos_formatados), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Ocorreu um erro ao buscar os empréstimos.", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Criar uma pasta para as páginas HTML, se não existir
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Você precisa mover seus arquivos HTML para dentro desta pasta 'templates'
    print("Por favor, mova seus arquivos gerenciamento.html, listagem.html e financiamento.html para a nova pasta 'templates'.")
    
    app.run(debug=True, port=5000)