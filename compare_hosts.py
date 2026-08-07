# -*- coding: utf-8 -*-

"""
HostList Comparator
Autor: Marcelo Soares
Descrição: Ferramenta CLI para comparação de listas de hosts e auditoria de ativos/cobertura.
"""

import csv
import os
import sys
from typing import List, Dict, Set
from prettytable import PrettyTable
from colorama import init, Fore, Style

# Inicializa o colorama para suporte cross-platform no terminal
init(autoreset=True)

def carregar_hosts_por_arquivo(arquivos: List[str]) -> Dict[str, Set[str]]:
    """Lê os arquivos fornecidos e retorna um dicionário mapeando
    o nome de cada arquivo para o conjunto (set) de hosts encontrados.
    """
    hosts_por_arquivo = {}
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            print(f"{Fore.RED}[ERRO] O arquivo '{arquivo}' não existe ou não pode ser acessado.{Style.RESET_ALL}")
            return {}
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                # Remove linhas em branco e espaços extras
                hosts = {line.strip() for line in f if line.strip()}
                hosts_por_arquivo[arquivo] = hosts
        except Exception as e:
            print(f"{Fore.RED}[ERRO] Falha ao ler o arquivo '{arquivo}': {str(e)}{Style.RESET_ALL}")
            return {}
    return hosts_por_arquivo


def gerar_relatorio(arquivos: List[str], nome_arquivo_saida: str = "resultado.csv") -> None:
    """Compara os hosts dos arquivos fornecidos, gera um arquivo CSV de auditoria
    e exibe uma tabela formatada no terminal.
    """
    if not arquivos:
        print(f"{Fore.YELLOW}[!] Nenhum arquivo foi informado. Finalizando...{Style.RESET_ALL}")
        return

    hosts_por_arquivo = carregar_hosts_por_arquivo(arquivos)
    if not hosts_por_arquivo:
        return

    # Converte caminhos para nomes de exibição (ex: hosts.txt -> HOSTS)
    nomes_colunas = [os.path.splitext(os.path.basename(arq))[0].upper() for arq in arquivos]
    cabecalho = ['TODOS', 'VALIDAR'] + nomes_colunas

    # Configuração da PrettyTable para visualização de terminal
    tabela = PrettyTable()
    tabela.field_names = cabecalho
    tabela.align = 'c'
    tabela.hrules = True

    # União de todos os hosts únicos encontrados em todos os arquivos
    todos_hosts = sorted(set.union(*hosts_por_arquivo.values())) if hosts_por_arquivo else []

    if not todos_hosts:
        print(f"{Fore.YELLOW}[!] Nenhum host encontrado nos arquivos informados.{Style.RESET_ALL}")
        return

    try:
        with open(nome_arquivo_saida, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(cabecalho)

            for host in todos_hosts:
                validado = all(host in hosts_por_arquivo[arq] for arq in arquivos)
                status_validacao = 'VERDADEIRO' if validado else 'FALSO'

                # Linha para salvar no CSV
                linha_csv = [host, status_validacao]
                # Linha formatada com cores para o terminal
                linha_terminal = [host, status_validacao]

                for arq in arquivos:
                    presente = host in hosts_por_arquivo[arq]
                    linha_csv.append('OK' if presente else '*')
                    linha_terminal.append('OK' if presente else f"{Fore.RED}*{Style.RESET_ALL}")

                writer.writerow(linha_csv)
                tabela.add_row(linha_terminal)

        print(f"\n{tabela.get_string()}")
        print(f"\n{Fore.GREEN}[✓] Relatório salvo com sucesso em: {nome_arquivo_saida}{Style.RESET_ALL}\n")

    except PermissionError:
        print(f"{Fore.RED}[ERRO] Falha na gravação do arquivo '{nome_arquivo_saida}': Permissão negada.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERRO] Ocorreu um erro ao salvar o relatório: {str(e)}{Style.RESET_ALL}")


def menu_interativo() -> List[str]:
    """Exibe o menu interativo no terminal para coleta dos arquivos."""
    lista_arquivos = []
    print(f"{Style.BRIGHT}Digite os caminhos dos arquivos para comparar (ou 'f' para finalizar e processar):{Style.RESET_ALL}\n")
    
    while True:
        entrada = input("Caminho do arquivo: ").strip()
        if entrada.lower() == 'f':
            break
        if not entrada:
            continue
        if os.path.exists(entrada):
            lista_arquivos.append(entrada)
            print(f"  {Fore.GREEN}└─ Adicionado:{Style.RESET_ALL} {entrada}")
        else:
            print(f"  {Fore.RED}└─ [ERRO] Arquivo não encontrado ou inacessível.{Style.RESET_ALL}")

    return lista_arquivos


def main() -> None:
    print(f"{Style.BRIGHT}{Fore.CYAN}##########################################################")
    print(f"########### AUDITORIA & COMPARAÇÃO DE HOSTS ##############")
    print(f"################ AUTOR: MARCELO SOARES ###################")
    print(f"##########################################################{Style.RESET_ALL}\n")

    # Suporte para passar arquivos via linha de comando ou menu interativo
    if len(sys.argv) > 1:
        arquivos = sys.argv[1:]
        print(f"[+] Arquivos recebidos via CLI: {', '.join(arquivos)}\n")
    else:
        arquivos = menu_interativo()

    if arquivos:
        print(f"\n[+] Processando {len(arquivos)} arquivo(s)...")
        gerar_relatorio(arquivos)


if __name__ == "__main__":
    main()