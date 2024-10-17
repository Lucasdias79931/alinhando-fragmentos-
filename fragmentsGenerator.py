import os
import random







# Colhe todas as sequências
def get_sequences(genome_name: str):
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

    
    


# Escreve os fragmentos no fragmentos.fasta
def fragmentos(nFragments: int, sequenceList: list):
    all_fragmentos = list()

    # Interage (nFragments) vezes
    for inter in range(nFragments):
        # Pega o index de forma aleatória para pegar uma sequência aleatória
        seq_index = random.randint(0, len(sequenceList) - 1)
        sequence_info = sequenceList[seq_index]
        
        for key, value in sequence_info.items():
            annotation = key
            
            while True:
                lenSubSequence = random.randint(100, 1000)

                # Verifica se o comprimento é múltiplo de 3 e não é maior que a sequência
                if (lenSubSequence % 3) != 0 or lenSubSequence > len(value):
                    continue

                # Determina o início da sub-sequência de forma aleatória
                init_sub_sequence = random.randint(0, len(value) - 1)

                # Se a sub-sequência ultrapassar o tamanho da sequência, deve calcular novamente
                if lenSubSequence + init_sub_sequence > len(value):
                    continue

                # Extrai a sub-sequência
                sub_sequence = value[init_sub_sequence:init_sub_sequence + lenSubSequence]

                all_fragmentos.append({annotation: sub_sequence})
                break  # Sai do loop enquanto para pegar outra sequência

    return all_fragmentos


#  Escreve os fragmentos com as anotações no fragmentos.fasta
def writeFrag(fragments: list, directory_destine)->None:

    
    try:
        with open(directory_destine, "a") as file:
            for fragmento in fragments:
                sequence_name, sequence = fragmento.popitem()

                file.write(f">{sequence_name}\n")
                file.write(f"{sequence}\n")
    except os.error as error:
        print("Erro:" + str(error))


    



######################start##########################       

#pega todas as sequencias

sequencesToFragments =  []
# Verificar depois por quê está retornando lista vazia nos index pares. colhendo apenas i primeiro arquivo por enquanto
base_directory = os.getcwd()

# Loop para processar cada arquivo FASTA
for i in range(1, 5):
    # Constrói o caminho para cada arquivo FASTA
    file_to_fragments = os.path.join(base_directory, f"referencias/refseq_envelope_denv{i}.fasta")
    
    #print(f"Lendo o arquivo: {file_to_fragments}")  # Mensagem de depuração

    seq = get_sequences(file_to_fragments)
    
    if seq is not None:  # Verifica se a sequência foi lida com sucesso
        sequencesToFragments.append(seq)
    

   



#pega os fragmentos
fragments = list()
for sequencia in sequencesToFragments:
    #Número de fragmentos
    number_of_fragments = random.randint(300, 1000)
    frag = fragmentos(number_of_fragments,sequencia)
    fragments.append(frag)


#escreve os fragmentos no fragmentos.fasta
for i in range(1,5):
    directory_fragments = os.path.join(base_directory, f"fragmentos/fragEnv{i}.fasta")
    print("escrevendo em:" + directory_fragments)
    writeFrag(fragments[i-1],directory_fragments)
    












