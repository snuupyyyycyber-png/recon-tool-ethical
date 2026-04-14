# recon-tool-ethical
Ferramenta ética de reconhecimento passivo para Bug Bounty

# ReconTool - Reconhecimento Ético para Bug Bounty

Uma ferramenta simples, segura e ética para enumeração passiva de subdomínios, ideal para programas de Bug Bounty rigorosos como o **Meta Bug Bounty**.

## 🎯 Objetivo

Fornecer um reconhecimento passivo leve, organizado e respeitoso, ajudando hunters a descobrir subdomínios **dentro do escopo autorizado**, sem causar impacto nos alvos.

## ⚠️ Uso Ético (Muito Importante)

Esta ferramenta deve ser usada **apenas** em:
- Seus próprios laboratórios ou ambientes de teste
- Programas de Bug Bounty com **autorização explícita**
- Alvos nos quais você tem permissão por escrito

**Nunca use em sistemas sem permissão.** Respeite sempre as regras do programa.

## 🚀 Como Usar

### Comando básico (recomendado):

```bash
python3 recontool.py -d exemplo.com --passive-only
