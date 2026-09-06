# Referência de estudo: strings com OO

Esta é uma proposta de solução de alta qualidade **para o escopo destes exercícios**.
“10/10” não é uma propriedade universal do código: requisitos diferentes mudam as escolhas.
Seu notebook foi preservado. A referência não exige substituir OO por funções.

## Execute e compare

No terminal, nesta pasta:

```powershell
python strings_oo.py
python -m unittest discover -s . -p 'test_*.py' -v
```

Não há dependências externas. Os exemplos usam valores fixos, como seu notebook.
Se o professor exigir leitura interativa, capture `input()` na função `main()` e
passe os valores às classes; a lógica de comparação não precisa mudar.

## Seu código e a referência

| No notebook revisado | Na referência | Por quê |
|---|---|---|
| `_init_` em `AppCompareStrings` | `@dataclass` gera `__init__` | `_init_` é método comum; não inicializa automaticamente o objeto. |
| `len_str_1` e `len_str_2` armazenados | `len()` calculado quando necessário | Evita representar a mesma informação de duas formas. |
| `if comparação: return True` | Retorno direto da comparação | A comparação já produz um booleano. |
| Métodos auxiliares que só consultam o estado | Propriedades `same_content` e `same_length` | São consultas baratas, sem efeitos externos, legíveis como atributos. |
| Método imprime o relatório | `report()` retorna texto; `main()` imprime | Permite testar e reutilizar a apresentação. |
| Dois blocos de relatório telefônico quase iguais | Um relatório com mensagem condicional | Corrigir layout não exige alterar dois lugares. |
| `_verify_len()` retorna string ou `False` | `corrected` sempre retorna string | O objeto rejeita entrada inválida na criação; seus resultados têm contrato estável. |
| `re.sub` remove qualquer não dígito | Remove apenas hífen | Não transforma letras inválidas em um telefone aparentemente válido. |

## O que estudar em OO

1. `@dataclass` gera inicialização, representação e igualdade baseadas nos campos.
2. `frozen=True` bloqueia atribuições comuns aos campos. Não é uma barreira de segurança
   nem torna objetos mutáveis aninhados imutáveis; aqui os campos são strings.
3. `@property` executa uma consulta ao acessar `objeto.same_length`, sem `()`.
   Não é um cache. As propriedades do telefone recalculam pequenas strings; para
   sete ou oito dígitos, isso é preferível a estado extra ou otimização prematura.
4. `__post_init__` executa após a inicialização gerada. No telefone, estabelece
   a condição que todos os métodos seguintes podem pressupor.
5. Os dois underscores de `__init__` e `__post_init__` pertencem ao protocolo
   do Python. Não devem ser trocados por um underscore como métodos auxiliares.

A validação extra do telefone é uma escolha didática para mostrar consistência
do objeto, não um requisito omitido pelo seu exercício. Não validamos posição
do hífen nem regras reais de telefonia. Comparar strings é literal: maiúsculas,
espaços e acentos contam. `len()` segue a definição de comprimento do Python.

A função `main()` apenas coordena a execução. As responsabilidades dos exercícios
continuam nas classes; uma função de entrada é compatível com programação OO.

## Roteiro de estudo

- Preveja os resultados dos testes antes de rodá-los.
- Tente alterar `comparison.first` e observe `FrozenInstanceError`.
- Remova temporariamente `frozen=True`: os tamanhos continuam coerentes porque
  não foram armazenados, mas o telefone pode passar a aceitar estado inválido
  após a construção. São responsabilidades diferentes.
- Acrescente um teste para strings diferentes com o mesmo tamanho.
- Reimplemente uma classe sem `dataclass`, escrevendo `__init__` manualmente.
  Isso ajuda a entender o que o decorador faz, em vez de apenas memorizá-lo.
