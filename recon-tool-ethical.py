#!/usr/bin/env python3

import subprocess
import argparse
import logging
import time
from datetime import datetime
from pathlib import Path

# ==============================================================================
# RECONTOOL CTF - Versão Melhorada e Organizada
# ==============================================================================

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

def print_banner():
    print(f"{Colors.BLUE}{'='*70}")
    print("                  RECONTOOL CTF - VERSÃO MELHORADA")
    print("             Reconhecimento Ativo + Passivo")
    print(f"{'='*70}{Colors.RESET}\n")

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(
        description="ReconTool CTF - Reconhecimento Ativo e Passivo",
        usage="python3 %(prog)s -d DOMINIO [opções]"
    )

    parser.add_argument("-d", "--domain", required=True, help="Domínio alvo")
    parser.add_argument("--active", action="store_true", help="Ativar brute-force + fuzzing (modo agressivo)")
    parser.add_argument("--threads", type=int, default=50, help="Número de threads (padrão: 50)")
    parser.add_argument("--wordlist", default="/usr/share/wordlists/dirb/common.txt",
                        help="Caminho da wordlist para fuzzing")
    parser.add_argument("-o", "--output", default=None, help="Diretório de saída personalizado")

    args = parser.parse_args()

    # Configuração de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(args.output) if args.output else Path(f"ctf_recon_{args.domain}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler(output_dir / "recon.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    print_banner()
    logger.info(f"Alvo: {args.domain}")
    logger.info(f"Modo: {'Ativo' if args.active else 'Passivo'}")
    logger.info(f"Saída: {output_dir}\n")

    subs_file = output_dir / "subdomains.txt"
    alive_file = output_dir / "alive.txt"

    # 1. Enumeração de Subdomínios
    logger.info("[1] Enumeração de subdomínios (passivo)")
    subprocess.run(["subfinder", "-d", args.domain, "-silent", "-o", str(subs_file)])

    if args.active:
        logger.info("[2] Brute-force de subdomínios (dnsx)")
        subprocess.run(["dnsx", "-d", args.domain, "-w", args.wordlist, "-silent", "-o", str(subs_file)], 
                      stdout=subprocess.DEVNULL)

    # 2. Hosts vivos
    logger.info("[3] Verificando hosts vivos com httpx")
    subprocess.run([
        "httpx", "-l", str(subs_file), "-silent", "-threads", str(args.threads),
        "-title", "-status-code", "-web-server", "-o", str(alive_file)
    ])

    alive_count = len(open(alive_file).readlines()) if alive_file.exists() else 0
    logger.info(f"✓ {alive_count} hosts vivos encontrados")

    # 3. Fuzzing de diretórios (somente se --active)
    if args.active:
        logger.info("[4] Fuzzing de diretórios com ffuf")
        with open(alive_file) as f:
            for line in f:
                url = line.strip()
                if not url:
                    continue
                domain_clean = url.replace("https://", "").replace("http://", "").replace("/", "_")
                out_file = output_dir / f"ffuf_{domain_clean}.txt"

                logger.info(f"Fuzzing → {url}")
                subprocess.run([
                    "ffuf", "-u", f"{url}/FUZZ", "-w", args.wordlist,
                    "-mc", "200,204,301,302,307,401,403",
                    "-t", str(args.threads), "-silent", "-o", str(out_file)
                ])

    # 4. Teste rápido de endpoints interessantes
    logger.info("[5] Testando endpoints comuns")
    interesting = ["api", "graphql", "admin", "login", "dashboard", "internal", "v1", "v2", "auth", "test"]

    with open(alive_file) as f:
        for line in f:
            base = line.strip()
            for path in interesting:
                full = f"{base}/{path}"
                try:
                    result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", full], 
                                          timeout=10, capture_output=True, text=True)
                    code = result.stdout.strip()
                    if code in ["200", "301", "302", "403", "401"]:
                        logger.info(f"[{code}] {full}")
                except:
                    pass

    elapsed = (time.time() - start_time) / 60
    logger.info(f"\n{'='*70}")
    logger.info(f"RECONCLUÍDO EM {elapsed:.1f} minutos")
    logger.info(f"Resultados salvos em: {output_dir}")
    logger.info(f"{'='*70}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"[!] Erro: {e}")
