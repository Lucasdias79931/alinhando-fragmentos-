import re
import os
import time
import subprocess
from Bio import SeqIO

# Função para corrigir o cabeçalho das sequências no arquivo FASTA
def corrigir_cabecalho(input_fasta, output_fasta, tipo_virus, intervalo, descricao="envelope protein"):
    with open(input_fasta, "r", encoding="utf-8") as infile, open(output_fasta, "w", encoding="utf-8") as outfile:
        for record in SeqIO.parse(infile, "fasta"):
            original_id = record.id.split(".")[0]
            parts = re.split(r'[.,]', record.description)
            if len(parts) >= 2:
                pais = parts[1].strip()
                if len(parts) > 2 and parts[2].strip().isdigit():
                    data = parts[2].strip()
                    header_corrigido = f"{original_id}:{intervalo} Dengue virus {tipo_virus}, {descricao}, {pais},{data}"
                else:
                    header_corrigido = f"{original_id}:{intervalo} Dengue virus {tipo_virus}, {descricao}, {pais}, N/A"
            else:
                header_corrigido = record.description

            print(f"Novo cabeçalho: {header_corrigido}")
            record.id = header_corrigido
            record.description = ""
            SeqIO.write(record, outfile, "fasta")

# Função para realizar o alinhamento com Minimap2 (sem gerar arquivos .paf)
def alinhar_sequencias(reference_file, fragment_file, output_file, tipo_virus, intervalo):
    # Corrigir o cabeçalho do fragmento
    corrigir_cabecalho(fragment_file, output_file, tipo_virus, intervalo)

    # Iniciar a contagem de tempo do alinhamento
    start_time = time.time()

    # Comando Minimap2 para realizar o alinhamento
    minimap2_command = ["minimap2", "-x", "asm5", reference_file, output_file]

    try:
        subprocess.run(minimap2_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        elapsed_time = time.time() - start_time
        print(f"Alinhamento concluído para {fragment_file} em {elapsed_time:.2f} segundos.")
    except subprocess.CalledProcessError as e:
        print(f"Erro no alinhamento de {fragment_file}: {e.stderr.decode('utf-8')}")

# Função principal para executar o alinhamento
def executar_alinhamento(base_directory):
    start_time = time.time()  # Início da medição de tempo
    for i in range(1, 5):
        reference_fasta = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
        fragments_fasta = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
        seqsAlinh = os.path.join(base_directory, f"sequenciasAlinhadas_com_minimap2/Env{i}.sam")

        alinhar_sequencias(reference_fasta, fragments_fasta, seqsAlinh, tipo_virus=3, intervalo="9521-10267")

    end_time = time.time()  # Fim da medição de tempo
    elapsed_time = end_time - start_time  # Tempo total em segundos
    print(f"Tempo de execução: {elapsed_time:.2f} segundos")

# Executar
if __name__ == "__main__":
    base_directory = os.getcwd()  # Define o diretório base como o atual
    executar_alinhamento(base_directory)
