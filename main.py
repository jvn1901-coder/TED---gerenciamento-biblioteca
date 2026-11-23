"""
João Vitor Neto Rodrigues - 252-000673

Sistema de Gerenciamento de Biblioteca (CLI)

"""

from collections import deque

ARQUIVO = "dados_sistema.txt"
SEP = "|"  # delimitador do arquivo

# Estado do sistema (inicia vazio)
usuarios = []              # LISTA: {"id": int, "nome": str, "contato": str}
fila_reservas = deque()    # FILA:  {"id_usuario": int, "titulo": str}
pilha_devolucoes = []      # PILHA: {"codigo": str, "titulo": str}
acervo = {}                # ÁRVORE: {"Área": "Subárea": "Livro": {}}



# Funções utilitárias de entrada
def limpar(texto):
    """Remove espaços das pontas e troca o delimitador '|' para não quebrar o arquivo."""
    return texto.strip().replace(SEP, "-")


def ler_texto(mensagem):
    """Lê um texto obrigatório (repete até o usuário digitar algo)."""
    while True:
        valor = limpar(input(mensagem))
        if valor:
            return valor
        print("  Valor não pode ser vazio.")


def ler_inteiro(mensagem):
    """Lê um número inteiro (repete até ser válido)."""
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("  Digite um número inteiro válido.")



# LISTA: usuários (acesso por chave/índice)

def proximo_id_usuario():
    """Gera o próximo ID: maior ID existente + 1 (ou 1 se a lista estiver vazia)."""
    return max((u["id"] for u in usuarios), default=0) + 1


def buscar_usuario(id_usuario):
    """Busca linear pela chave 'id'. Retorna o usuário ou None."""
    for u in usuarios:
        if u["id"] == id_usuario:
            return u
    return None


def cadastrar_usuario():
    nome = ler_texto("Nome: ")
    contato = ler_texto("Contato (telefone/e-mail): ")
    novo = {"id": proximo_id_usuario(), "nome": nome, "contato": contato}
    usuarios.append(novo)  # inserção no fim da lista
    print(f"  Usuário cadastrado com ID {novo['id']}.")


def listar_usuarios():
    if not usuarios:
        print("  Nenhum usuário cadastrado.")
        return
    for posicao, u in enumerate(usuarios):
        print(f"  [{posicao}] ID {u['id']} | {u['nome']} | {u['contato']}")


def consultar_usuario():
    u = buscar_usuario(ler_inteiro("ID do usuário: "))
    if u:
        print(f"  ID {u['id']} | {u['nome']} | {u['contato']}")
    else:
        print("  Usuário não encontrado.")


def atualizar_usuario():
    u = buscar_usuario(ler_inteiro("ID do usuário a atualizar: "))
    if not u:
        print("  Usuário não encontrado.")
        return
    u["nome"] = ler_texto(f"Novo nome (atual: {u['nome']}): ")
    u["contato"] = ler_texto(f"Novo contato (atual: {u['contato']}): ")
    print("  Usuário atualizado.")


def remover_usuario():
    u = buscar_usuario(ler_inteiro("ID do usuário a remover: "))
    if not u:
        print("  Usuário não encontrado.")
        return
    usuarios.remove(u)
    print("  Usuário removido.")


def menu_usuarios():
    opcoes = {
        "1": ("Cadastrar usuário", cadastrar_usuario),
        "2": ("Listar usuários", listar_usuarios),
        "3": ("Consultar usuário por ID", consultar_usuario),
        "4": ("Atualizar usuário", atualizar_usuario),
        "5": ("Remover usuário", remover_usuario),
    }
    executar_submenu("USUÁRIOS (LISTA)", opcoes)



# FILA: reservas (FIFO: entra no fim, sai do início)
def reservar_livro():
    id_usuario = ler_inteiro("ID do usuário: ")
    if not buscar_usuario(id_usuario):
        print("  Usuário não cadastrado. Cadastre-o primeiro.")
        return
    titulo = ler_texto("Título do livro: ")
    fila_reservas.append({"id_usuario": id_usuario, "titulo": titulo})  # fim da fila
    print(f"  Reserva criada. Posição na fila: {len(fila_reservas)}.")


def listar_reservas():
    if not fila_reservas:
        print("  Fila de reservas vazia.")
        return
    for posicao, r in enumerate(fila_reservas, start=1):
        print(f"  {posicao}º | Usuário {r['id_usuario']} | {r['titulo']}")


def proxima_reserva():
    if not fila_reservas:
        print("  Fila de reservas vazia.")
        return
    r = fila_reservas[0]  # apenas consulta, sem remover
    print(f"  Próximo da fila: usuário {r['id_usuario']} -> {r['titulo']}")


def atender_reserva():
    if not fila_reservas:
        print("  Fila de reservas vazia.")
        return
    r = fila_reservas.popleft()  # remoção no início da fila
    print(f"  Reserva atendida: usuário {r['id_usuario']} -> {r['titulo']}")


def atualizar_reserva():
    """Altera o título de uma reserva sem mudar sua posição na fila."""
    if not fila_reservas:
        print("  Fila de reservas vazia.")
        return
    listar_reservas()
    posicao = ler_inteiro("Posição da reserva a atualizar: ")
    if not 1 <= posicao <= len(fila_reservas):
        print("  Posição inválida.")
        return
    fila_reservas[posicao - 1]["titulo"] = ler_texto("Novo título: ")
    print("  Reserva atualizada.")


def menu_fila():
    opcoes = {
        "1": ("Reservar livro (entrar no fim da fila)", reservar_livro),
        "2": ("Listar reservas", listar_reservas),
        "3": ("Ver próximo da fila", proxima_reserva),
        "4": ("Atualizar reserva", atualizar_reserva),
        "5": ("Atender reserva (remover do início)", atender_reserva),
    }
    executar_submenu("RESERVAS (FILA)", opcoes)


# PILHA: livros devolvidos (LIFO: entra e sai pelo topo)
def registrar_devolucao():
    codigo = ler_texto("Código do exemplar: ")
    titulo = ler_texto("Título do livro: ")
    pilha_devolucoes.append({"codigo": codigo, "titulo": titulo})  # push no topo
    print("  Livro empilhado no balcão.")


def listar_devolucoes():
    if not pilha_devolucoes:
        print("  Pilha de devoluções vazia.")
        return
    # Exibe do topo (último inserido) para a base
    for i, d in enumerate(reversed(pilha_devolucoes)):
        marca = "TOPO" if i == 0 else "    "
        print(f"  {marca} | {d['codigo']} | {d['titulo']}")


def ver_topo():
    if not pilha_devolucoes:
        print("  Pilha de devoluções vazia.")
        return
    d = pilha_devolucoes[-1]
    print(f"  Topo: {d['codigo']} | {d['titulo']}")


def atualizar_topo():
    if not pilha_devolucoes:
        print("  Pilha de devoluções vazia.")
        return
    topo = pilha_devolucoes[-1]
    topo["titulo"] = ler_texto(f"Novo título (atual: {topo['titulo']}): ")
    print("  Livro do topo atualizado.")


def triar_livro():
    if not pilha_devolucoes:
        print("  Pilha de devoluções vazia.")
        return
    d = pilha_devolucoes.pop()  # pop no topo
    print(f"  Livro triado e enviado à estante: {d['codigo']} | {d['titulo']}")


def menu_pilha():
    opcoes = {
        "1": ("Registrar devolução (push)", registrar_devolucao),
        "2": ("Listar pilha (topo -> base)", listar_devolucoes),
        "3": ("Ver livro do topo", ver_topo),
        "4": ("Atualizar livro do topo", atualizar_topo),
        "5": ("Triar livro do topo (pop)", triar_livro),
    }
    executar_submenu("DEVOLUÇÕES (PILHA)", opcoes)



# ÁRVORE: acervo (dicionários aninhados; cada nó é um dict com seus filhos)
def ler_caminho(mensagem):
    """Lê um caminho como 'Ciencias/Computacao'. Vazio = raiz. Retorna lista de nomes."""
    texto = input(mensagem).strip()
    return [limpar(parte) for parte in texto.split("/") if parte.strip()]


def navegar(caminho):
    """Desce na árvore seguindo o caminho. Retorna o nó (dict) ou None se não existir."""
    no = acervo
    for nome in caminho:
        if nome not in no:
            return None
        no = no[nome]
    return no


def inserir_no():
    pai = ler_caminho("Caminho do nó pai (vazio = raiz, ex: Ciencias/Computacao): ")
    no_pai = navegar(pai)
    if no_pai is None:
        print("  Caminho do pai não existe.")
        return
    nome = ler_texto("Nome do novo nó (área, subárea ou livro): ")
    if nome in no_pai:
        print("  Já existe um nó com esse nome neste local.")
        return
    no_pai[nome] = {}  # novo nó sem filhos
    print("  Nó inserido.")


def imprimir_arvore(no, nivel=0):
    """Percorre a árvore recursivamente (pré-ordem) indentando por nível."""
    for nome, filhos in no.items():
        print("  " + "    " * nivel + "- " + nome)
        imprimir_arvore(filhos, nivel + 1)


def listar_acervo():
    if not acervo:
        print("  Acervo vazio.")
        return
    print("  ACERVO")
    imprimir_arvore(acervo)


def consultar_no():
    caminho = ler_caminho("Caminho do nó (ex: Ciencias/Computacao): ")
    no = navegar(caminho)
    if no is None or not caminho:
        print("  Nó não encontrado.")
        return
    print(f"  Nó '{caminho[-1]}' encontrado com {len(no)} filho(s).")
    imprimir_arvore(no, 1)


def renomear_no():
    caminho = ler_caminho("Caminho do nó a renomear: ")
    if not caminho:
        print("  Informe um caminho.")
        return
    no_pai = navegar(caminho[:-1])
    antigo = caminho[-1]
    if no_pai is None or antigo not in no_pai:
        print("  Nó não encontrado.")
        return
    novo = ler_texto("Novo nome: ")
    if novo in no_pai:
        print("  Já existe um nó com esse nome neste local.")
        return
    # Reconstrói o dicionário para manter a ordem original das chaves
    itens = [(novo if k == antigo else k, v) for k, v in no_pai.items()]
    no_pai.clear()
    no_pai.update(itens)
    print("  Nó renomeado.")


def remover_no():
    caminho = ler_caminho("Caminho do nó a remover (remove também os filhos): ")
    if not caminho:
        print("  Informe um caminho.")
        return
    no_pai = navegar(caminho[:-1])
    if no_pai is None or caminho[-1] not in no_pai:
        print("  Nó não encontrado.")
        return
    del no_pai[caminho[-1]]
    print("  Nó removido.")


def menu_acervo():
    opcoes = {
        "1": ("Inserir nó (área/subárea/livro)", inserir_no),
        "2": ("Listar acervo completo", listar_acervo),
        "3": ("Consultar nó e seus filhos", consultar_no),
        "4": ("Renomear nó", renomear_no),
        "5": ("Remover nó", remover_no),
    }
    executar_submenu("ACERVO (ÁRVORE)", opcoes)


# PERSISTÊNCIA em arquivo texto único
def caminhos_folhas(no, prefixo=()):
    """Gera o caminho completo de cada folha da árvore (um por linha ARVORE)."""
    for nome, filhos in no.items():
        caminho = prefixo + (nome,)
        if filhos:
            yield from caminhos_folhas(filhos, caminho)
        else:
            yield caminho


def salvar_dados():
    """Grava o estado atual das 4 estruturas, uma linha por registro."""
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            for u in usuarios:
                f.write(SEP.join(["LISTA", str(u["id"]), u["nome"], u["contato"]]) + "\n")
            for r in fila_reservas:  # do início ao fim da fila
                f.write(SEP.join(["FILA", str(r["id_usuario"]), r["titulo"]]) + "\n")
            for d in pilha_devolucoes:  # da base ao topo (para recarregar na mesma ordem)
                f.write(SEP.join(["PILHA", d["codigo"], d["titulo"]]) + "\n")
            for caminho in caminhos_folhas(acervo):
                f.write(SEP.join(["ARVORE", *caminho]) + "\n")
        print(f"  Dados salvos em '{ARQUIVO}'.")
    except OSError as erro:
        print(f"  Erro ao salvar: {erro}")


def carregar_dados():
    """Reconstrói as estruturas em memória a partir do arquivo."""
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        print(f"  Arquivo '{ARQUIVO}' não encontrado. Salve dados primeiro.")
        return
    except OSError as erro:
        print(f"  Erro ao carregar: {erro}")
        return

    # Limpa o estado atual antes de reconstruir
    usuarios.clear()
    fila_reservas.clear()
    pilha_devolucoes.clear()
    acervo.clear()

    ignoradas = 0
    for linha in linhas:
        if not linha.strip():
            continue
        partes = linha.split(SEP)
        tipo, campos = partes[0], partes[1:]
        try:
            if tipo == "LISTA":
                usuarios.append({"id": int(campos[0]), "nome": campos[1], "contato": campos[2]})
            elif tipo == "FILA":
                fila_reservas.append({"id_usuario": int(campos[0]), "titulo": campos[1]})
            elif tipo == "PILHA":
                pilha_devolucoes.append({"codigo": campos[0], "titulo": campos[1]})
            elif tipo == "ARVORE":
                no = acervo
                for nome in campos:
                    no = no.setdefault(nome, {})  # cria o nó se ainda não existir
            else:
                ignoradas += 1
        except (IndexError, ValueError):
            ignoradas += 1  # linha mal formatada

    print(f"  Dados carregados de '{ARQUIVO}'.")
    if ignoradas:
        print(f"  Atenção: {ignoradas} linha(s) inválida(s) ignorada(s).")

# MENUS
def executar_submenu(titulo, opcoes):
    """Mostra um submenu numérico e executa a função da opção escolhida."""
    while True:
        print(f"\n=== {titulo} ===")
        for numero, (descricao, _) in opcoes.items():
            print(f"{numero} - {descricao}")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("  Opção inválida.")


def menu_principal():
    while True:
        print("\n===== BIBLIOTECA =====")
        print("1 - Usuários (Lista)")
        print("2 - Reservas (Fila)")
        print("3 - Devoluções (Pilha)")
        print("4 - Acervo (Árvore)")
        print("5 - Salvar dados")
        print("6 - Carregar dados")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == "1":
            menu_usuarios()
        elif escolha == "2":
            menu_fila()
        elif escolha == "3":
            menu_pilha()
        elif escolha == "4":
            menu_acervo()
        elif escolha == "5":
            salvar_dados()
        elif escolha == "6":
            carregar_dados()
        elif escolha == "0":
            print("Encerrando. Dados não salvos serão perdidos.")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    menu_principal()
