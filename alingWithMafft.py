import subprocess
import os
import time

def alignWithMafft(reference_file, fragments_file, output):
    
    os.makedirs(os.path.dirname(output), exist_ok=True)

    command = ["mafft", "--add", fragments_file, reference_file]

    with open(output, "a") as file:
        subprocess.run(command, stdout=file, check=True)

################################ Executar #########################
base_directory = os.getcwd()

start_time = time.time()  # Início da medição de tempo
for i in range(1, 5):
    reference_fasta = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    fragments_fasta = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    seqsAlinh = os.path.join(base_directory, f"sequenciasAlinhadas_com_mafft/Env{i}.sam")

    alignWithMafft(reference_fasta, fragments_fasta, seqsAlinh)

end_time = time.time()  # Fim da medição de tempo

elapsed_time = end_time - start_time  # Tempo total em segundos
print(f"Alinhamento concluído. Resultados salvos em {seqsAlinh}")
print(f"Tempo de execução: {elapsed_time:.2f} segundos")
