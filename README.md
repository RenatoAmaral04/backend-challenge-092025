# MBRAS — Backend Challenge (Python/FastAPI)

API de análise de sentimentos em tempo real. O sistema processa feeds de mensagens aplicando regras determinísticas baseadas em léxico, cálculo de influência via hash e detecção de anomalias de postagem.

## Quickstart

Requisito: Python 3.11+

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
(Nota: Se estiver usando Linux/Mac, ative o ambiente com source .venv/bin/activate)

Testes
O projeto conta com cobertura total das regras de negócio e validação de performance.

Bash
# Rodar os 14 cenários de validação (regras, flags e anomalias):
python -m pytest tests/test_analyzer.py -v

# Rodar o teste de estresse e performance (< 200ms):
RUN_PERF=1 python -m pytest tests/test_performance.py -v

Arquitetura e Decisões Técnicas
Alta Performance O(1): Estruturação do léxico e contadores de trending topics utilizando Hash Maps (Sets e Dicionários) para garantir complexidade de tempo constante, batendo a meta de processamento de 1000 mensagens na casa dos milissegundos.

Determinismo de Influência: Lógica de engajamento encapsulada utilizando geração de hashlib.sha256 acoplada às regras matemáticas de Fibonacci (strings de 13 caracteres) e Proporção Áurea.

Normalização Segura: Utilização de NFKD para matching case-insensitive e remoção de diacríticos no léxico, operando de forma desacoplada do input original para não quebrar a contagem de caracteres em regras de edge cases (ex: user_café).

CI Pipeline: Workflow integrado via GitHub Actions contemplando 3 etapas obrigatórias: Linting de sintaxe (flake8), Testes Unitários e Testes de Performance.