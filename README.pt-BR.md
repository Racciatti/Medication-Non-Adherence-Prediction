# PAM: Predição de Não Adesão a Medicamentos com NHANES 2013-2014

[English version](README.md)


## Problema

É possível sinalizar adultos com 50+ anos com maior chance de **não aderir ao medicamento
prescrito para uma condição crônica**, usando apenas informações demográficas, funcionais e de
quantidade de medicamentos?

- **Unidade de análise:** uma linha por par *(paciente, condição)*, para quatro condições crônicas:
  diabetes, osteoporose, hipertensão e colesterol alto.
- **Alvo (`target`, binário):** proxy de não adesão, construído com respostas da NHANES:
  - `1` (não aderente): tem a condição e o médico prescreveu medicação, mas o paciente **diz que
    não toma**, ou **diz que toma mas nenhum medicamento correspondente foi visto** pelo entrevistador
    (RXQ_RX_H, associado por códigos ICD do motivo de uso).
  - `0` (aderente): diz que toma e um medicamento correspondente foi visto.
  - Prevalência da classe 1: cerca de 36% (35,6% no treino, 39,6% no teste).
- As variáveis usadas só para construir o alvo **não** entram como features do modelo.

## Dados

[NHANES](https://www.cdc.gov/nchs/nhanes/), ciclo 2013-2014 ("H"), publicado pelo National Center
for Health Statistics (CDC), domínio público. 18 módulos são unidos pela chave `SEQN`.
Documentação: [NHANES 2013-2014](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2013).

**Citação:** Centers for Disease Control and Prevention (CDC), National Center for Health
Statistics (NCHS). *National Health and Nutrition Examination Survey Data, 2013-2014.* Hyattsville, MD:
U.S. Department of Health and Human Services, CDC.

**Como obter os dados brutos** (não redistribuídos aqui, ~75 MB):

```bash
python data/download.py
```

Os CSVs intermediários em `data/` (de `filtered_data.csv` a `final_selection_with_target.csv`, ~5 MB) e a
divisão final treino/teste (`data/final/`) estão incluídos, então o treino e boa parte do `data.ipynb` rodam sem os arquivos
brutos. Dicionário: [`docs/data_dictionary.md`](docs/data_dictionary.md); linhagem:
[`docs/data_lineage.md`](docs/data_lineage.md).

## Pipeline

```
Módulos NHANES .xpt (18)
        |  utils.load_and_verify
        v
  união por SEQN -> idade >= 50 -> ~30 variáveis selecionadas
        |
        v
  tratamento de nulos -> remoção de códigos inválidos (7/9: 0,4% das linhas)
        |
        v
  codificação / normalização -> uma linha por (paciente, condição)
        |
        v
  construção do alvo -> data/final/{X,y}_{train,test}.csv  (80/20, divisão sequencial)
        |
        v
  training.ipynb: benchmark de árvores -> poda por SHAP -> análise de threshold e ROI
```

## Metodologia

1. **Preparação (`data.ipynb`)**: carga e validação dos módulos, análise de nulos, recodificação,
   seleção de variáveis, construção do alvo e divisão.
2. **Features (16)**: sexo, idade normalizada, escolaridade, estado civil, indicadores de dificuldade
   (audição, visão, concentração, locomoção, memória), confusão, flags e tipo de condição e
   número de medicamentos (`RXDCOUNT`).
3. **Benchmark v1**: LightGBM, Random Forest e XGBoost com `GridSearchCV` (5 folds estratificados, ROC-AUC).
4. **v2/v3**: LightGBM com poda de features baseada em SHAP (limiares 0,1 a 0,5).
5. **v4**: varredura do threshold de decisão (F2) e análise ilustrativa de valor esperado (ROI) com
   **premissas hipotéticas** (custo de internação 15.000, eficácia da intervenção 30%, 5 internações
   por 1.000 não aderentes, prevalência 36%, custo de 0 a 30 por falso positivo), resultando em
   cerca de 62,5 de valor por verdadeiro positivo.

## Resultados

Teste: 659 linhas (261 positivos). Métricas de `results/*.csv` (threshold 0,5, salvo indicação).

| Modelo (benchmark v1) | ROC-AUC | F1 | Precisão | Recall | Brier |
|---|---|---|---|---|---|
| LightGBM | 0,750 | 0,559 | 0,753 | 0,444 | 0,229 |
| Random Forest | 0,747 | 0,536 | 0,837 | 0,395 | 0,201 |
| XGBoost | 0,731 | 0,541 | 0,732 | 0,429 | 0,221 |

LightGBM com poda por SHAP (`results/threshold_metrics.csv`):

| Limiar SHAP | ROC-AUC | F1 | Precisão | Recall |
|---|---|---|---|---|
| 0,1 | 0,749 | 0,545 | 0,714 | 0,441 |
| 0,2 | 0,720 | 0,520 | 0,690 | 0,418 |
| 0,3 | 0,739 | 0,532 | 0,632 | 0,460 |
| 0,4 | 0,779 | 0,478 | 0,869 | 0,330 |
| 0,5 | 0,779 | 0,499 | 0,900 | 0,345 |

Análise de threshold / valor esperado (`results/roi_threshold_optimal.csv`): com custo de alerta
zero ou baixo, o melhor threshold é muito baixo (0,01 a 0,02, ou seja, sinalizar quase todos); com
custo 30 por alerta sobe para 0,10 (181 VP, 129 FP). O threshold que maximiza F2 também é 0,01
(F2 = 0,742, recall 0,866, precisão 0,473).

De modo geral os modelos são modestos (ROC-AUC de 0,72 a 0,78): o sinal nessas features é limitado.

## Como reproduzir

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.11+
pip install -r requirements.txt
python data/download.py          # opcional: só para reexecutar o data.ipynb
jupyter lab                      # data.ipynb (opcional) e depois training.ipynb
pytest                           # testes de utils.py
```

O `training.ipynb` só precisa de `data/final/`. Reexecutar os notebooks sobrescreve arquivos em
`data/` e `results/`.

## Estrutura

```
data.ipynb          preparação dos dados, alvo e divisão
training.ipynb      modelos, poda por SHAP, threshold e ROI
training.py         TreeModelBenchmarker (GridSearchCV + métricas de teste)
utils.py            carga dos módulos NHANES / verificação de variáveis
data/download.py    baixa os .xpt brutos do CDC
data/*.csv           tabelas intermediárias (docs/data_lineage.md)
data/final/         divisão treino/teste
docs/               dicionário de dados e linhagem
results/            CSVs de benchmark, threshold e ROI
tests/              testes pytest de utils
```

## Limitações

- **Alvo proxy:** baseado em autorrelato e no que o entrevistador viu; não mede adesão real nem usa biomarcadores.
- **Amostra pequena e transversal** (3.295 linhas): um único ciclo, apenas 50+, grande incerteza; pesos
  amostrais da NHANES não foram usados (não é representativa nacionalmente da forma como foi usada).
- **Divisão:** sequencial 80/20 (não aleatória); balanceamento difere (35,6% vs 39,6%) e o mesmo
  paciente pode aparecer em mais de uma linha.
- **Threshold/ROI ajustados no próprio conjunto de teste**, portanto otimistas; custos são ilustrativos.

## Licença

MIT, veja [LICENSE](LICENSE). Os dados da NHANES são de domínio público (governo dos EUA).
