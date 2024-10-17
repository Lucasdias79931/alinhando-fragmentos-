import os
import random

class Generator:
    def __init__(self) -> None:
        pass
    
    # Colhe todas as sequências
    def get_sequences(self, genome_name):
        all_sequences = []
        try:
            with open(genome_name, "r") as file:
                sequence_name = ""
                sequence = ""

                # Processa uma sequência de cada vez
                for line in file:
                    if line.startswith('>'):  # Identifica a sequência
                        if sequence_name and sequence:  # Se já houver uma sequência anterior, armazena-a
                            all_sequences.append({sequence_name: sequence})
                        sequence_name = line.strip().replace('>', '')  # Remove o '>'
                        sequence = ""  # Reseta a sequência
                    else:
                        sequence += line.strip()  # Acumula a sequência

                # Adiciona a última sequência após o loop
                if sequence_name and sequence:
                    all_sequences.append({sequence_name: sequence})

            return all_sequences

        except FileNotFoundError:
            print(f"Erro: O arquivo {genome_name} não foi encontrado.")
        except Exception as error:
            print("Erro:", str(error))

    # Gera fragmentos das sequências
    def fragmentos(self, sequenceList: list):

        all_fragmentos = []
        number_of_fragments = random.randint(300, 1000)
        for inter in range(number_of_fragments):
            # Pega um índice aleatório para selecionar uma sequência
            seq_index = random.randint(0, len(sequenceList) - 1)
            sequence_info = sequenceList[seq_index]

            for key, value in sequence_info.items():
                annotation = key
                
                while True:
                    lenSubSequence = random.randint(100, 1000)
                    start = random.randint(0, len(value) - lenSubSequence)
                    sub_sequence = value[start:start + lenSubSequence]
                    # Adiciona o fragmento à lista
                    all_fragmentos.append({annotation: sub_sequence})
                    break  # Sai do loop para pegar outra sequência

        return all_fragmentos

    # Escreve os fragmentos com as anotações no arquivo de destino
    def write_frag(self, fragments: list, directory_destine: str) -> None:
        try:
            with open(directory_destine, "w") as file:
                for fragmento in fragments:
                    sequence_name, sequence = fragmento.popitem()
                    file.write(f">{sequence_name}\n")
                    file.write(f"{sequence}\n")
        except os.error as error:
            print("Erro:" + str(error))

###################### Início ##########################

base_directory = os.getcwd()
fragmentsG = Generator()

sequencesToFragments = []

# Loop para processar cada arquivo FASTA
for i in range(1, 5):
    file_to_fragments = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    
    seq = fragmentsG.get_sequences(file_to_fragments)
    
    if seq:  # Verifica se a sequência foi lida com sucesso
        sequencesToFragments.append(seq)

# Gera e escreve fragmentos
for i, sequencia in enumerate(sequencesToFragments, start=1):
    
    fragments = fragmentsG.fragmentos(sequencia)

    directory_fragments = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    print(f"Escrevendo em: {directory_fragments}")
    fragmentsG.write_frag(fragments, directory_fragments)
