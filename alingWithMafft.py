import subprocess
import os
import time


def alignWithMafft(reference_file, fragments_file, output):
    # Cria o diretório de saída, se não existir
    os.makedirs(os.path.dirname(output), exist_ok=True)

    # Monta o comando para MAFFT
    command = ["mafft", "--add", fragments_file, reference_file]

    try:
        # Executa o comando e redireciona a saída para o arquivo de saída
        with open(output, "w") as file:  # Usar "w" para sobrescrever o arquivo se existir
            subprocess.run(command, stdout=file, check=True)
        print(f"Alinhamento concluído e salvo em: {output}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o MAFFT: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

################################ Executar #########################
base_directory = os.getcwd()

start_time = time.time()  # Início da medição de tempo
for i in range(1, 5):
    reference_fasta = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    fragments_fasta = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    seqsAlinh = os.path.join(base_directory, f"sequenciasAlinhadas_com_mafft/Env{i}.fasta")

    alignWithMafft(reference_fasta, fragments_fasta, seqsAlinh)

end_time = time.time()  # Fim da medição de tempo

elapsed_time = end_time - start_time  # Tempo total em segundos

print(f"Tempo de execução: {elapsed_time:.2f} segundos")
