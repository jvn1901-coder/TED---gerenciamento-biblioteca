# Sistema de Gerenciamento de Biblioteca (CLI)

Projeto final de Estruturas de Dados em Python. O sistema roda no terminal, por menu numérico, e integra **Lista, Pilha, Fila e Árvore** com persistência em um único arquivo texto.

## Como executar

Requisito: Python 3.8 ou superior (somente biblioteca padrão, nenhuma instalação extra).

```bash
python main.py
```

(Em alguns sistemas: `python3 main.py`.)

O sistema inicia **vazio**. Use as opções **5 - Salvar dados** e **6 - Carregar dados** do menu principal para gravar/ler o arquivo `dados_sistema.txt`, criado na pasta onde o programa é executado.

### Menu principal

| Opção | Estrutura | Operações |
|-------|-----------|-----------|
| 1 | Usuários (Lista) | cadastrar, listar, consultar por ID, atualizar, remover |
| 2 | Reservas (Fila) | reservar (fim), listar, ver próximo, atualizar, atender (início) |
| 3 | Devoluções (Pilha) | empilhar, listar, ver topo, atualizar topo, triar (desempilhar) |
| 4 | Acervo (Árvore) | inserir nó, listar, consultar, renomear, remover |
| 5 | Salvar dados | grava o estado em `dados_sistema.txt` |
| 6 | Carregar dados | reconstrói tudo a partir de `dados_sistema.txt` |
| 0 | Sair | encerra (dados não salvos são perdidos) |

### Exemplo de uso (caminho feliz)

1. `1` → `1`: cadastre um usuário (ele recebe o ID 1).
2. `2` → `1`: reserve um livro para o ID 1; `5` atende a reserva.
3. `3` → `1`: registre uma devolução; `5` faz a triagem do livro do topo.
4. `4` → `1`: crie a área `Ciencias`; depois `Computacao` com pai `Ciencias`; depois o livro `Algoritmos` com pai `Ciencias/Computacao` (caminhos usam `/`).
5. Volte ao menu principal e escolha `5` para salvar.

## Formato do arquivo `dados_sistema.txt`

Uma linha por registro: identificador da estrutura + campos separados por `|`.

```
LISTA|1|Ana Lima|ana@email.com
FILA|1|Dom Casmurro
PILHA|EX-010|Algoritmos
ARVORE|Ciencias|Computacao|Algoritmos
```

- `LISTA|id|nome|contato`
- `FILA|id_usuario|titulo` (primeira linha = início da fila)
- `PILHA|codigo|titulo` (última linha = topo da pilha)
- `ARVORE|nó1|nó2|...|folha` (caminho da raiz até uma folha)

## Justificativa técnica das estruturas

**Lista (`list`) – cadastro de usuários.** O cadastro precisa de acesso e manipulação por posição ou chave (consultar, atualizar e remover qualquer leitor, não apenas o primeiro ou o último). A `list` do Python permite inserção no fim em tempo O(1) amortizado, percorre os registros na ordem de cadastro e permite remover um elemento qualquer. Como o volume de usuários de uma biblioteca é moderado, a busca linear por ID é suficiente e simples.

**Fila (`collections.deque`) – reservas.** Reservas de exemplares disputados devem ser atendidas por ordem de chegada (FIFO): quem reservou primeiro é atendido primeiro. O `deque` oferece `append` (entrada no fim) e `popleft` (saída no início) em O(1). Usar uma `list` com `pop(0)` custaria O(n), pois deslocaria todos os elementos.

**Pilha (`list`) – livros devolvidos.** No balcão, os livros devolvidos são empilhados e o último a chegar é o primeiro a ser triado (LIFO), exatamente como uma pilha física. `append` (push) e `pop` (pop) operam no fim da `list` em O(1), e o "topo" é o último elemento.

**Árvore (dicionários aninhados) – acervo.** O acervo é naturalmente hierárquico: área do conhecimento → subárea → livro. Cada nó é um dicionário cujas chaves são os nomes dos filhos e cujos valores são os dicionários dos filhos. Isso permite navegar por caminho (`Ciencias/Computacao`), inserir em qualquer nível, listar recursivamente e remover um ramo inteiro de uma vez, algo que uma estrutura linear representaria mal.

## Persistência

Os dados são gravados apenas em `dados_sistema.txt`, sem banco de dados, JSON, CSV ou `pickle`. Ao carregar, as estruturas em memória são limpas e reconstruídas linha a linha; linhas mal formatadas são ignoradas com aviso. O caractere `|` digitado pelo usuário é substituído por `-` para não corromper o formato.
