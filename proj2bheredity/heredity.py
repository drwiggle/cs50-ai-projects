import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    import numpy as np
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    prob = 1

    # For each person, we need to compute
    # P(expresses_gene | num_copies) and P(num_copies | parents copies)
    # then we multiply all these numbers together
    
    for person in people.keys():
        copies = gene_copies(person, two_genes, one_gene)
        expresses_gene = person in have_trait

        # computes conditional probability of having trait given copies
        prob *= PROBS["trait"][copies][expresses_gene]
        
        if people[person]["mother"] is None:
            # parents are not in database, use unconditional probabilities
            prob *= PROBS["gene"][copies]
        else: # parents are in dictionary...
            # compute P(person has copies | data about parent copies)
            mom, dad = people[person]["mother"], people[person]["father"]
            mom_copies = gene_copies(mom, two_genes, one_gene)
            dad_copies = gene_copies(dad, two_genes, one_gene)

            if copies == 0:
               prob *= prob_of_passing(0, mom_copies) * prob_of_passing(0, dad_copies)
            elif copies == 2:
                prob *= prob_of_passing(1, mom_copies) * prob_of_passing(1, dad_copies)
            else: # copies == 1
                prob *= prob_of_passing(1, mom_copies) * prob_of_passing(0, dad_copies) + prob_of_passing(0, mom_copies) * prob_of_passing(1, dad_copies)
            
    return prob


def gene_copies(person, two_genes, one_gene):
    """
    returns the number of copies of the gene (0, 1, or 2) that
    person is expected to have"""
    
    return 2 if person in two_genes else 1 if person in one_gene else 0


def prob_of_passing(copies, parent_copies):
    """
    copies is the number of genes to be passed from parent to child
    parent_copies is the number of copies of the gene carried by the parent
    This function will return the probability that parent passes on exactly
    copies genes to the child.  copies must be 0 or 1.
    """

    # make a 2-element list representing the parent's genes
    parent_genes = [True if parent_copies > 0 else False,
                     True if parent_copies > 1 else False]

    # the probability the parent will pass 0 or 1 genes
    pass_0 = sum([gene == False for gene in parent_genes])/2
    pass_1 = sum([gene == True for gene in parent_genes])/2
    
    if copies == 0:
        return PROBS["mutation"] * pass_1 + (1-PROBS["mutation"]) * pass_0
    else: #copies == 1
        return PROBS["mutation"] * pass_0 + (1-PROBS["mutation"]) * pass_1


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person, distribution in probabilities.items():
        num_copies = gene_copies(person, two_genes, one_gene)
        distribution["trait"][person in have_trait] += p
        distribution["gene"][num_copies] += p
    return None


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, item in probabilities.items():
        for types in ["gene", "trait"]:
            distr = item[types]
            tot = sum(distr.values())
            for i in distr.keys():
                distr[i] = distr[i]/tot
        
    return None


if __name__ == "__main__":
    main()
