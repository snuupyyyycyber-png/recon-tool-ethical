# recon-tool-ethical

**Ferramenta ética de reconhecimento passivo para Bug Bounty**

---

## 🎯 Objetivo

ReconTool é uma ferramenta simples, segura e ética para enumeração passiva de subdomínios.  
Foi desenvolvida especialmente para programas de Bug Bounty rigorosos, como o **Meta Bug Bounty**.

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
```

## Usando arquivo de escopo (altamente recomendado):
```bash
python3 recontool.py -d meta.com --scope-file scope.txt --passive-only```
```
Exemplo de arquivo ```scope.txt:```
```txt
exemplo.com
*.exemplo.com
api.exemplo.com
test.exemplo.com
```

# Opções Principais

## Opção Descrição
```-d, --domainDomínio alvo``` (obrigatório)
``` --passive-onlyExecuta``` apenas enumeração passiva (modo mais seguro)
```--activeAtiva``` scans leves (use somente se o programa permitir)
```--scope-fileArquivo``` com lista de domínios/subdomínios permitidos
```--threads``` Número de threads (padrão: 25)-o,
```--outputDiretório``` onde os resultados serão salvos

## Instalação
```bash
git clone https://github.com/snuupyyyycyber-png/recon-tool-ethical
cd recon-tool-ethical
chmod +x recontool.py
```

## Recomendações
Sempre leia as regras do programa de Bug Bounty antes de usar
Prefira o modo ```--passive-only```
Sempre utilize ```--scope-file``` para evitar subdomínios fora do escopo
Não use o modo ```--active``` em programas que proíbem automação pesada


# Aviso Legal
O autor desta ferramenta não se responsabiliza por qualquer uso indevido.
Use com responsabilidade e ética.
