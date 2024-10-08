import subprocess
import os
import time


def alignWithMinimap2(reference_file, fragments_file, output_file):
    

    command = [
        "minimap2", 
        "-a",  # Formato de saída SAM
        reference_file, 
        fragments_file
    ]
    
    with open(output_file, "w") as out:
        subprocess.run(command, stdout=out, check=True)

     

################################ Executar #########################
base_directory = os.getcwd()

start_time = time.time()  # Início da medição de tempo
for i in range(1,5):
    

    reference_fasta = os.path.join(base_directory,f"referencias/refseq_envelope_denv{i}.fasta")
    fragments_fasta = os.path.join(base_directory,f"fragmentos/fragEnv{i}.fasta")
    seqsAlinh = os.path.join(base_directory,f"sequenciasAlinhadas/Env{i}.sam")
    alignWithMinimap2(reference_fasta, fragments_fasta, seqsAlinh)

end_time = time.time()  # Fim da medição de tempo

elapsed_time = end_time - start_time  # Tempo total em segundos
print(f"Alinhamento concluído. Resultados salvos em {seqsAlinh}")
print(f"Tempo de execução: {elapsed_time:.2f} segundos")


