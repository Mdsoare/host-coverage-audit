# 🔍 HostList Comparator — Audit & Coverage Tool

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Domain](https://img.shields.io/badge/domain-SecOps%20%26%20IT%20Audit-red.svg)

Uma ferramenta em Python desenvolvida para **comparação automatizada de listas de ativos (hosts/IPs)** provenientes de múltiplos sistemas de inventário e ferramentas de segurança (ex: Active Directory, EDR/Antivírus, WSUS, Scanners de Vulnerabilidades).

A ferramenta cruza as listas de dados, identifica lacunas de cobertura de agentes/soluções, gera uma matriz visual de validação no terminal e exporta um relatório detalhado em formato `.csv`.

---

## 📌 Principais Recursos

- **Cruzamento Multiareas:** Compare ilimitadas listas de ativos de forma simultânea.
- **Validação Automática (`VERDADEIRO` / `FALSO`):** Identifica instantaneamente quais hosts estão presentes em **todos** os inventários selecionados.
- **Visualização CLI Amigável:** Tabela formatada no terminal com destaque visual colorido para itens ausentes (`*`).
- **Exportação CSV:** Matriz tabular pronta para auditorias, dashboards ou relatórios gerenciais.
- **Modo Flexível:** Suporta execução interativa via menu de terminal ou atalhos via argumentos de linha de comando (CLI).

---

## 🛠️ Pré-requisitos e Instalação

### Pré-requisitos
- **Python 3.8+** instalado.

### Instalação

#### 1. Clone o repositório:
```bash
# Clone o repositório:
git clone https://github.com/Mdsoare/host-coverage-audit.git
cd host-coverage-audit
```

---

#### 2. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

### 🚀 Como Utilizar

#### 1. Modo Interativo
Execute o script sem argumentos e digite o caminho dos arquivos individualmente:

```bash
python compare_hosts.py
```

---

#### 2. Modo CLI (Argumentos diretos)
Passe os arquivos desejados diretamente na execução:

```bash
python compare_hosts.py hosts_ad.txt agentes_edr.txt inventario_wsus.txt
```

---

### 📊 Exemplo de Saída

#### Matriz Gerada no Terminal / CSV

|     TODOS       | VALIDAR    | HOSTS_AD | AGENTES_EDR | INVENTARIO_WSUS|
| --------------- | ---------- | -------- | ----------- | -------------- |
| srv-db-01.corp  | VERDADEIRO |    OK	  |     OK	    |       OK       |
| srv-app-02.corp |   FALSO    |    OK	  |     *	    |       OK       |
| srv-web-01.corp |   FALSO    |    OK	  |     OK	    |        *       |


ℹ️ Legenda:

- OK: O ativo está presente na respectiva lista.
- *: O ativo NÃO foi encontrado nessa solução/inventário (destacado em vermelho no terminal).

---

## 📜 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.


Desenvolvido por Marcelo Soares | Especialista em Segurança da Informação.
