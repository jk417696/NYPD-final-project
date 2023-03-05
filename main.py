from Bio import SeqIO
import math


# get a list of sequences from fasta file
def get_sequences(fasta_file):
    with open(fasta_file) as fasta:
        sequences_fasta = SeqIO.parse(fasta, "fasta")
        sequences = [str(record.seq) for record in sequences_fasta]
    return sequences


# find a set of kmers for a sequence seq
def kmers(seq, k):
    return set([seq[i:i+k] for i in range(0, len(seq)-k+1)])


# check if it is possible to find the set of probes of length k
def check_k(sequences, k):
    # create a list with sets of kmers for each sequence, sorted by length
    kmers_sets = sorted([kmers(seq, k) for seq in sequences], key = len)
    # check if for every sequence there exists a kmer that is not presents in any other set of kmers
    for i in range(len(kmers_sets)):
        others = set().union(*(kmers_sets[:i] + kmers_sets[i+1:]))
        # if all kmers in a set are in some other set of kmers then it is impossible to identify this sequence based
        # on a probe of length k
        if kmers_sets[i].issubset(others):
            return 0
    return 1


# find minimal k for which a set of probes of length k identifying sequences in a set exists
def minimal_k(sequences):
    low_k = 1
    top_k = min([len(seq) for seq in sequences])
    k = top_k
    # trivial cases
    if check_k(sequences, 1):
        return 1
    if not check_k(sequences, top_k):
        return 0
    # assume that 1 < k < minimal length of a sequence in the set
    while top_k - low_k > 1:
        k = math.floor((top_k + low_k) / 2)
        if check_k(sequences, k):
            top_k = k
        else:
            low_k = k
            k = k+1
    return k


def main():
    sequences = get_sequences('yeast.fa')
    print('Minimal k for \'yeast.fa\' file:', minimal_k(sequences))

if __name__=='__main__':
    main()