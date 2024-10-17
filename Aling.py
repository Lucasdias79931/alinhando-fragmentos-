import subprocess
import os
import time

# Classe Mafft
class Mafft:
    def __init__(self, reference_file, sequence_file, output_file) -> None:
        self.reference_file = reference_file
        self.sequence_file = sequence_file
        self.output_file = output_file

    def align(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        command = ["mafft", "--add", self.sequence_file, self.reference_file]

        try:
            with open(self.output_file, "w") as file:
                subprocess.run(command, stdout=file, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o MAFFT: {e.stderr.decode('utf-8')}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Classe Minimap2
class Minimap2:
    def __init__(self, reference_file, sequence_file, output_file) -> None:
        self.reference_file = reference_file
        self.sequence_file = sequence_file
        self.output_file = output_file

    def align(self):
        command = [
            "minimap2",
            "-a",
            self.reference_file,
            self.sequence_file
        ]

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        try:
            with open(self.output_file, "w") as out:
                subprocess.run(command, stdout=out, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o Minimap2: {e.stderr.decode('utf-8')}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Classe base Align usando polimorfismo
class Align:
    def __init__(self, aligner):
        self.aligner = aligner

    def perform_alignment(self):
        self.aligner.align()

################################ Executar #########################
base_directory = os.getcwd()

# Alinhar com Minimap2
start_timeWithMinimap2 = time.time()
for i in range(1, 5):
    reference_fasta = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    fragments_fasta = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    seqs_alinhadas = os.path.join(base_directory, f"sequenciasAlinhadas_com_minimap2/Env{i}.sam")

    aligner = Minimap2(reference_fasta, fragments_fasta, seqs_alinhadas)
    align = Align(aligner)
    align.perform_alignment()

elapsed_timeWithMinimap2  = time.time() - start_timeWithMinimap2 

# Alinhar com MAFFT
start_timeWithMafft = time.time()
for i in range(1, 5):
    reference_fasta = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    fragments_fasta = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    seqs_alinhadas = os.path.join(base_directory, f"sequenciasAlinhadas_com_mafft/Env{i}.fasta")

    aligner = Mafft(reference_fasta, fragments_fasta, seqs_alinhadas)
    align = Align(aligner)
    align.perform_alignment()

elapsed_timeWithMafft = time.time() - start_timeWithMafft





print(f"Alinhamento Minimap2 concluído. Tempo de execução: {elapsed_timeWithMinimap2 :.2f} segundos")
print(f"Alinhamento MAFFT concluído. Tempo de execução: {elapsed_timeWithMafft:.2f} segundos")


