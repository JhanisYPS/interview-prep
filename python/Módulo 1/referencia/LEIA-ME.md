# Referência de estudo: relatório de vendas com OO

Uma solução de alta qualidade depende do escopo. Este exemplo prioriza regras
explícitas, resultados verificáveis e separação de responsabilidades. Não é um
sistema de produção completo. Seu notebook original foi preservado.

## Como executar

No terminal, nesta pasta, use um ambiente virtual e instale as dependências:

```powershell
python -m pip install pandas openpyxl gdown
python sales_report.py --file "C:\caminho\Vendas.xlsx"
python -m unittest discover -s . -p 'test_*.py' -v
```

O primeiro comando instala dependências. O segundo só lê o Excel e exibe o
relatório. O terceiro testa regras usando dados sintéticos e um Excel temporário;
não acessa Drive nem envia e-mail.

Para baixar de uma pasta pública, informe também o nome exato da base:

```powershell
python sales_report.py --drive-url "URL_DA_PASTA" --filename "Vendas.xlsx"
```

Para enviar, configure `GMAIL_USER` e `GMAIL_APP_PASSWORD` no ambiente do processo
e acrescente `--send-to destinatario@example.com`. Não salve uma senha real nos
arquivos do projeto. Sem `--send-to`, não há conexão SMTP. Repetir esse comando
com a opção de envio envia novamente; não existe prevenção de duplicidade.

## Comparação com seu notebook

| Sua abordagem | Referência | Benefício |
|---|---|---|
| Código executado no corpo de `class main` | Função `main()` e guarda de execução | Importar o módulo não baixa arquivos nem envia mensagens. |
| Downloads repetidos entre células | Uma aquisição por execução | Fluxo e origem dos dados ficam claros. |
| Primeiro caminho retornado pelo Drive | Nome explícito com exatamente um candidato | Evita analisar outro arquivo pela posição. |
| Leitura dentro da normalização | `ExcelSource` lê; `SalesAnalyzer` transforma | Cálculo pode ser testado em memória. |
| Soma de todas as colunas numéricas | Duas colunas de negócio explícitas | IDs não entram na agregação; coluna ausente gera erro. |
| `sum().to_frame().T` e extração da primeira célula | `SalesSummary` com dois campos | O resultado expressa diretamente os indicadores. |
| Caracteres trocados antes do `strip()` | Normalização seguida de remoção de `_` nas extremidades | Espaços e pontuação não deixam separadores soltos. |
| Sem detecção de colisão dos headers | Nomes duplicados rejeitados | Duas colunas não são confundidas após normalização. |
| `locale.setlocale` | Formatação explícita brasileira | Não depende de uma localidade instalada no Windows. |
| Senha no notebook | Variável de ambiente | Segredo fica fora do código de referência. |
| `send_email` altera a mensagem recebida | `GmailSender` cria sua própria mensagem | Evita modificar objetos do chamador e duplicar headers. |

## Contratos e escolhas que você deve saber explicar

- A base deve ser `.xlsx`, com dados na primeira aba e headers na primeira linha.
- Exigimos `VALOR_FINAL` e `QUANTIDADE` após normalização. Outras colunas são ignoradas.
- Valores ausentes, não finitos, quantidades fracionárias e frações de centavo
  são rejeitados. Uma base vazia também é rejeitada; não representa receita zero.
- Negativos são aceitos como estornos. Se o negócio não permitir isso, a regra
  deve mudar explicitamente, com teste correspondente.
- Textos numéricos usam ponto decimal, sem símbolo monetário ou milhar. Não
  adivinhamos se `1.234` representa milhar ou fração. `R$ 1.234,50` é apresentação.
- `Decimal` evita a soma binária de valores como `0.1` e `0.2`. A leitura do Excel
  pode já trazer floats: converter sua representação textual não recupera precisão
  perdida na origem. Não há política implícita para arredondar dados inválidos.
- Pandas lê, seleciona e organiza a tabela. A soma percorre duas colunas para
  validar cada registro e usar `Decimal`; isso prioriza clareza e exatidão para
  uma base didática. Grandes volumes exigiriam medir desempenho e outra estratégia.
- Download usa uma pasta temporária isolada e a remove ao terminar. Não há arquivo
  persistente de saída. A seleção de nome é exata, inclusive maiúsculas/minúsculas.
- Erros de rede e leitura propagam a exceção. Não há `except Exception` que imprime
  sucesso ou mascara a falha. Uma aplicação final poderia traduzi-los na interface.
- O SMTP usa timeout e não faz retentativas automáticas. Aceite pelo servidor não
  comprova entrega na caixa do destinatário.

As classes são concretas e pequenas. Não há interfaces, herança ou factories sem
necessidade. `SalesSummary` representa dados; as demais encapsulam operações.
É uma escolha para seu treino obrigatório de OO, não uma regra de que projetos
Python não possam usar funções independentes.

O exemplo mantém sua decisão de baixar diretamente com `gdown`. Ele **não atende
ao requisito de usar `pyautogui`**, caso o professor exija essa biblioteca. Nesse
caso, substitua a aquisição de dados, preservando análise e apresentação.

## Exercícios para comparar ativamente

1. Rode os testes e localize qual problema do notebook cada um previne.
2. Acrescente um cenário com estorno e defina o total esperado manualmente.
3. Acrescente um teste de arquivo com duas colunas que normalizam para o mesmo nome.
4. Crie uma apresentação HTML sem mudar `SalesAnalyzer`.
5. Teste o envio com `unittest.mock`, verificando destinatário e corpo sem rede.

Os testes entregues cobrem o cálculo e a leitura de Excel. Download e SMTP não
foram exercitados contra serviços reais; credenciais e permissões variam por conta.
