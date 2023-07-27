import paramiko
import getpass
"""
#
# E-mail:     liralc@gmail.com
# Autor:      Anderson Lira
# Manutenção: Anderson Lira
#
# ************************************************************************** #
#  Conexão via ssh client.
#
# ************************************************************************** #
# Histórico:
#
#   v1.0.0 26/07/2023, =====> Anderson Lira:
#       - Início do programa.
#
# ************************************************************************** #
"""

def ssh_connect(host, user, passwd):
    """
    Estabelece uma conexão SSH com o servidor remoto.

    Parâmetros:
        host (str): Endereço IP ou nome do servidor remoto.
        user (str): Nome de usuário para autenticação SSH.
        passwd (str): Senha do usuário para autenticação SSH.

    Retorna:
        paramiko.SSHClient: Objeto cliente SSH estabelecido ou None em caso de falha na conexão.
        
        python -c "import pty;pty.spawn('/bin/bash')" Exemplo de comando para abrir o tty.
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=passwd)
        return client
    except paramiko.AuthenticationException:
        print("Erro: Falha na autenticação. Verifique o nome de usuário e senha.")
    except paramiko.SSHException as e:
        print(f"Erro ao estabelecer a conexão SSH: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    return None

def execute_command(client, command):
    """
    Executa um comando no servidor remoto e imprime a saída.

    Parâmetros:
        client (paramiko.SSHClient): Objeto cliente SSH estabelecido.
        command (str): Comando a ser executado no servidor remoto.
    """
    try:
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            print(line.strip())
        
        errors = stderr.read().decode()
        if errors:
            print(errors.strip())
    except paramiko.SSHException as e:
        print(f"Erro ao executar o comando SSH: {e}")
    except Exception as e:
        print(f"Erro inesperado ao executar o comando: {e}")

def get_password():
    """
    Solicita a senha do usuário de forma segura, sem exibi-la na tela enquanto é digitada.

    Retorna:
        str: Senha fornecida pelo usuário ou None em caso de erro.
    """
    try:
        return getpass.getpass("Senha: ")
    except Exception as e:
        print(f"Erro ao obter a senha: {e}")
    return None

def main():
    # Configurações do servidor remoto
    host = "127.0.0.1"
    user = "user"

    # Obter a senha do usuário de forma segura
    passwd = get_password()
    if not passwd:
        return

    print("Conectando ao servidor...")
    # Estabelecer a conexão SSH
    client = ssh_connect(host, user, passwd)
    if not client:
        return

    try:
        print(f"Conexão estabelecida com sucesso. Digite os comandos abaixo (exit para sair).\n")
        while True:
            command = input("Comando: ")
            if command.lower() in ["exit", "quit"]:
                break
            execute_command(client, command)
    finally:
        client.close()
        print("Conexão encerrada.")
    

if __name__ == "__main__":
    main()
