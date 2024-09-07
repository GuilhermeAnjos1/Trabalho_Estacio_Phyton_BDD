import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Conectando ao banco de dados SQLite3 (ou criando-o)
conn = sqlite3.connect('usf_vila_independencia.db')
cursor = conn.cursor()

# Criando tabelas se não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    genero TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    motivo TEXT NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

conn.commit()

# Função para cadastrar um novo usuário
def cadastrar_usuario():
    username = simpledialog.askstring("Cadastrar Usuário", "Nome de usuário:")
    senha = simpledialog.askstring("Cadastrar Usuário", "Senha:", show="*")

    if username and senha:
        try:
            cursor.execute('''
            INSERT INTO usuarios (username, senha)
            VALUES (?, ?)
            ''', (username, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já existe. Tente outro nome.")
    else:
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios.")

# Função para autenticar o usuário
def autenticar_usuario():
    username = simpledialog.askstring("Login", "Nome de usuário:")
    senha = simpledialog.askstring("Login", "Senha:", show="*")

    cursor.execute('''
    SELECT * FROM usuarios WHERE username = ? AND senha = ?
    ''', (username, senha))

    usuario = cursor.fetchone()
    if usuario:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        abrir_menu_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        tela_inicial()

# Função para abrir o menu principal após login bem-sucedido
def abrir_menu_principal():
    esconder_janelas()  # Esconder a janela atual
    global menu_window
    menu_window = tk.Toplevel(root)
    menu_window.title("Sistema de Gestão da USF Vila Independência")
    menu_window.geometry('400x400')
    menu_window.minsize(400, 400)

    # Botões de funcionalidades
    btn_cadastrar_paciente = tk.Button(menu_window, text="Cadastrar Paciente", command=cadastrar_paciente)
    btn_cadastrar_paciente.pack(pady=5)

    btn_agendar_consulta = tk.Button(menu_window, text="Agendar Consulta", command=agendar_consulta)
    btn_agendar_consulta.pack(pady=5)

    btn_listar_consultas = tk.Button(menu_window, text="Listar Consultas", command=mostrar_consultas)
    btn_listar_consultas.pack(pady=5)

    btn_editar_consulta = tk.Button(menu_window, text="Editar Consulta", command=editar_consulta)
    btn_editar_consulta.pack(pady=5)

    btn_cancelar_consulta = tk.Button(menu_window, text="Cancelar Consulta", command=cancelar_consulta)
    btn_cancelar_consulta.pack(pady=5)

    btn_relatorio_consultas = tk.Button(menu_window, text="Gerar Relatório de Consultas", command=gerar_relatorio_consultas)
    btn_relatorio_consultas.pack(pady=5)

    btn_relatorio_pacientes = tk.Button(menu_window, text="Gerar Relatório de Pacientes", command=gerar_relatorio_pacientes)
    btn_relatorio_pacientes.pack(pady=5)

    btn_sair = tk.Button(menu_window, text="Sair", command=sair_para_tela_inicial)
    btn_sair.pack(pady=10)

# Função para cadastrar novo paciente
def cadastrar_paciente():
    esconder_janelas()  # Esconder a janela atual
    global cadastro_window
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastrar Paciente")

    nome = simpledialog.askstring("Cadastrar Paciente", "Nome do Paciente:")
    if not nome:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    data_nascimento = simpledialog.askstring("Cadastrar Paciente", "Data de Nascimento (dd/mm/aaaa):")
    if not data_nascimento:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    genero = simpledialog.askstring("Cadastrar Paciente", "Gênero:")
    if not genero:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    endereco = simpledialog.askstring("Cadastrar Paciente", "Endereço:")
    if not endereco:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    telefone = simpledialog.askstring("Cadastrar Paciente", "Telefone:")
    if not telefone:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    cursor.execute('''
    INSERT INTO pacientes (nome, data_nascimento, genero, endereco, telefone)
    VALUES (?, ?, ?, ?, ?)
    ''', (nome, data_nascimento, genero, endereco, telefone))

    conn.commit()
    messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    abrir_menu_principal()

# Função para agendar uma consulta
def agendar_consulta():
    esconder_janelas()  # Esconder a janela atual
    global agendamento_window
    agendamento_window = tk.Toplevel(root)
    agendamento_window.title("Agendar Consulta")

    paciente_id = simpledialog.askinteger("Agendar Consulta", "ID do Paciente:")
    if not paciente_id:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    data = simpledialog.askstring("Agendar Consulta", "Data da Consulta (dd/mm/aaaa):")
    if not data:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    horario = simpledialog.askstring("Agendar Consulta", "Horário da Consulta (hh:mm):")
    if not horario:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    motivo = simpledialog.askstring("Agendar Consulta", "Motivo da Consulta:")
    if not motivo:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    try:
        cursor.execute('''
        INSERT INTO consultas (paciente_id, data, horario, motivo)
        VALUES (?, ?, ?, ?)
        ''', (paciente_id, data, horario, motivo))
        conn.commit()
        messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "ID do Paciente não encontrado.")

    abrir_menu_principal()

# Função para mostrar consultas em uma nova tela
def mostrar_consultas():
    esconder_janelas()  # Esconder a janela atual
    global consulta_window
    consulta_window = tk.Toplevel(root)
    consulta_window.title("Consultas Agendadas")
    consulta_window.geometry('600x400')

    scrollbar = tk.Scrollbar(consulta_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    consulta_listbox = tk.Listbox(consulta_window, yscrollcommand=scrollbar.set, width=100, height=20)
    consulta_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    cursor.execute('''
    SELECT consultas.id, pacientes.nome, consultas.data, consultas.horario, consultas.motivo
    FROM consultas
    JOIN pacientes ON consultas.paciente_id = pacientes.id
    ''')

    consultas = cursor.fetchall()

    if consultas:
        for consulta in consultas:
            consulta_listbox.insert(tk.END, f"ID: {consulta[0]}, Paciente: {consulta[1]}, Data: {consulta[2]}, Horário: {consulta[3]}, Motivo: {consulta[4]}")
    else:
        consulta_listbox.insert(tk.END, "Nenhuma consulta agendada.")

    scrollbar.config(command=consulta_listbox.yview)

    btn_voltar = tk.Button(consulta_window, text="Voltar", command=abrir_menu_principal)
    btn_voltar.pack(pady=10)

        # Função para retornar ao menu principal ao fechar a janela de consultas
    def fechar_janela_consultas():
        consulta_window.destroy()
        abrir_menu_principal()  # Reabre o menu principal após fechar a janela de consultas

    # Vincular a função fechar_janela_consultas ao fechamento da janela
    consulta_window.protocol("WM_DELETE_WINDOW", fechar_janela_consultas)

# Função para editar uma consulta existente
def editar_consulta():
    esconder_janelas()  # Esconder a janela atual
    global editar_window
    editar_window = tk.Toplevel(root)
    editar_window.title("Editar Consulta")

    consulta_id = simpledialog.askinteger("Editar Consulta", "ID da Consulta:")
    if not consulta_id:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    cursor.execute('''
    SELECT * FROM consultas WHERE id = ?
    ''', (consulta_id,))

    consulta = cursor.fetchone()

    if consulta:
        novo_data = simpledialog.askstring("Editar Consulta", "Nova Data (dd/mm/aaaa):", initialvalue=consulta[2])
        if not novo_data:  # Cancelado ou vazio
            abrir_menu_principal()
            return

        novo_horario = simpledialog.askstring("Editar Consulta", "Novo Horário (hh:mm):", initialvalue=consulta[3])
        if not novo_horario:  # Cancelado ou vazio
            abrir_menu_principal()
            return

        novo_motivo = simpledialog.askstring("Editar Consulta", "Novo Motivo:", initialvalue=consulta[4])
        if not novo_motivo:  # Cancelado ou vazio
            abrir_menu_principal()
            return

        cursor.execute('''
        UPDATE consultas
        SET data = ?, horario = ?, motivo = ?
        WHERE id = ?
        ''', (novo_data, novo_horario, novo_motivo, consulta_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Consulta não encontrada.")

    abrir_menu_principal()

# Função para cancelar uma consulta existente
def cancelar_consulta():
    esconder_janelas()  # Esconder a janela atual
    global cancelar_window
    cancelar_window = tk.Toplevel(root)
    cancelar_window.title("Cancelar Consulta")

    consulta_id = simpledialog.askinteger("Cancelar Consulta", "ID da Consulta:")
    if not consulta_id:  # Cancelado ou vazio
        abrir_menu_principal()
        return

    cursor.execute('DELETE FROM consultas WHERE id = ?', (consulta_id,))
    conn.commit()

    if cursor.rowcount:
        messagebox.showinfo("Sucesso", "Consulta cancelada com sucesso!")
    else:
        messagebox.showerror("Erro", "Consulta não encontrada.")

    abrir_menu_principal()

# Função para gerar relatório de consultas
def gerar_relatorio_consultas():
    esconder_janelas()  # Esconder a janela atual
    with open("relatorio_consultas.txt", "w") as file:
        cursor.execute('''
        SELECT consultas.id, pacientes.nome, consultas.data, consultas.horario, consultas.motivo
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        ''')

        consultas = cursor.fetchall()

        if consultas:
            for consulta in consultas:
                file.write(f"ID: {consulta[0]}, Paciente: {consulta[1]}, Data: {consulta[2]}, Horário: {consulta[3]}, Motivo: {consulta[4]}\n")
            messagebox.showinfo("Sucesso", "Relatório de consultas gerado com sucesso!")
        else:
            file.write("Nenhuma consulta agendada.\n")
            messagebox.showinfo("Aviso", "Nenhuma consulta agendada para gerar o relatório.")
    abrir_menu_principal()

# Função para gerar relatório de pacientes
def gerar_relatorio_pacientes():
    esconder_janelas()  # Esconder a janela atual
    with open("relatorio_pacientes.txt", "w") as file:
        cursor.execute('SELECT * FROM pacientes')
        pacientes = cursor.fetchall()

        if pacientes:
            for paciente in pacientes:
                file.write(f"ID: {paciente[0]}, Nome: {paciente[1]}, Data de Nascimento: {paciente[2]}, Gênero: {paciente[3]}, Endereço: {paciente[4]}, Telefone: {paciente[5]}\n")
            messagebox.showinfo("Sucesso", "Relatório de pacientes gerado com sucesso!")
        else:
            file.write("Nenhum paciente cadastrado.\n")
            messagebox.showinfo("Aviso", "Nenhum paciente cadastrado para gerar o relatório.")
    abrir_menu_principal()

# Função para sair para a tela inicial
def sair_para_tela_inicial():
    menu_window.destroy()
    tela_inicial()

# Função para esconder janelas abertas
def esconder_janelas():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) or isinstance(widget, tk.Frame):
            widget.withdraw()

# Função para criar a tela inicial com opções de Login ou Cadastro
def tela_inicial():
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry('400x300')
    root.minsize(400, 300)

    btn_cadastrar_usuario = tk.Button(root, text="Cadastrar Usuário", command=cadastrar_usuario, width=20)
    btn_cadastrar_usuario.pack(pady=10)

    btn_login = tk.Button(root, text="Realizar Login", command=autenticar_usuario, width=20)
    btn_login.pack(pady=10)

# Função principal para inicializar o sistema
def main():
    global root
    root = tk.Tk()
    root.title("Sistema de Gestão da USF Vila Independência")
    tela_inicial()
    root.mainloop()

# Executa a interface gráfica
main()

# Fechando a conexão com o banco de dados
conn.close()
