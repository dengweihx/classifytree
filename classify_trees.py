import os
import shutil
from Bio import Phylo
from ete3 import Tree
import pandas as pd
import argparse
import csv

# define genus
species_genus_mapping = {
    "AFL": "Arthrobotrys", "Aoli": "Arthrobotrys", "Acon": "Arthrobotrys", "Airi": "Arthrobotrys",
    "Amus": "Arthrobotrys", "Apse": "Arthrobotrys", "Asin": "Arthrobotrys", "Asph": "Arthrobotrys",
    "Aver": "Arthrobotrys", "DEN": "Dactylellina", "Dcio": "Dactylellina", "Dcio1": "Dactylellina",
    "Dcio2": "Dactylellina", "Ddre": "Dactylellina", "Dhap": "Dactylellina", "Dlep": "Dactylellina",
    "Dpar": "Dactylellina", "Dque": "Dactylellina", "Dtib": "Dactylellina", "Dste": "Drechslerella",
    "Ddac": "Drechslerella", "Dcoe": "Drechslerella", "Dbro": "Drechslerella"
}

def classify_trees(input_folder, output_base):
    """
    Classify trees into 'tree' and 'unclassified'.
    """
    tree_folder = os.path.join(output_base, 'tree')
    unclassified_folder = os.path.join(output_base, 'unclassified')
    os.makedirs(tree_folder, exist_ok=True)
    os.makedirs(unclassified_folder, exist_ok=True)

    tree_classification = {}

    for filename in os.listdir(input_folder):
        try:
            filepath = os.path.join(input_folder, filename)
            tree = Phylo.read(filepath, "newick")
            genera_present = set(species_genus_mapping.values())
            classified = False
            for genus in genera_present:
                species_of_genus = {species for species, g in species_genus_mapping.items() if g == genus}
                common_ancestor = tree.common_ancestor(species_of_genus)
                descendant_species = {c.name for c in common_ancestor.get_terminals()}
                if descendant_species != species_of_genus:
                    shutil.copy(filepath, os.path.join(unclassified_folder, filename))
                    tree_classification[filename] = "unclassified"
                    classified = True
                    break
            if not classified:
                shutil.copy(filepath, os.path.join(tree_folder, filename))
                tree_classification[filename] = "tree"
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return tree_folder, tree_classification

def further_classify_trees(tree_folder, output_base):
    """
    Further classify 'tree' into 'tree1', 'tree2', 'tree3', and 'other'.
    """
    classifications = {"tree1": [], "tree2": [], "tree3": [], "other": []}

    # Define species groups
    arthrobotrys_species = ["AFL", "Aoli", "Acon", "Airi", "Amus", "Apse", "Asin", "Asph", "Aver"]
    dactylellina_species = ["DEN", "Dcio", "Dcio1", "Dcio2", "Ddre", "Dhap", "Dlep", "Dpar", "Dque", "Dtib"]
    drechslerella_species = ["Dste", "Ddac", "Dcoe", "Dbro"]

    for filename in os.listdir(tree_folder):
        try:
            filepath = os.path.join(tree_folder, filename)
            tree = Tree(filepath)
            classification = "other"
            for node in tree.traverse("postorder"):
                if node.is_leaf():
                    continue
                species_list = sorted(node.get_leaf_names())
                if set(species_list) in [
                    set(arthrobotrys_species + dactylellina_species),
                    set(arthrobotrys_species + drechslerella_species),
                    set(dactylellina_species + drechslerella_species)
                ]:
                    index = 1 + [
                        set(arthrobotrys_species + dactylellina_species),
                        set(arthrobotrys_species + drechslerella_species),
                        set(dactylellina_species + drechslerella_species)
                    ].index(set(species_list))
                    classification = f"tree{index}"
                    break
            classifications[classification].append(filename)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    for classification, files in classifications.items():
        output_folder = os.path.join(output_base, classification)
        os.makedirs(output_folder, exist_ok=True)
        for file in files:
            shutil.copy(os.path.join(tree_folder, file), os.path.join(output_folder, file))

    return classifications

def write_classification_results(all_classifications, output_csv_path):
    """
    Write the classification results to a CSV file.
    """
    with open(output_csv_path, mode='w', newline='') as csvfile:
        fieldnames = ['Tree File', 'Classification']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tree_file, classification in all_classifications.items():
            writer.writerow({'Tree File': tree_file, 'Classification': classification})


def main(input_folder, output_base):
    tree_folder, initial_classification = classify_trees(input_folder, output_base)
    further_classifications = further_classify_trees(tree_folder, output_base)
    all_classifications = initial_classification
    for cls, files in further_classifications.items():
        for file in files:
            all_classifications[file] = cls
    output_csv_path = os.path.join(output_base, "tree_classification_summary.csv")
    write_classification_results(all_classifications, output_csv_path)
    print("Classification completed. Summary CSV generated at:", output_csv_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify phylogenetic trees into predefined categories.")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to the input folder containing Newick tree files.")
    parser.add_argument("--output_base", type=str, required=True, help="Base path for output folders and classification summary CSV.")
    args = parser.parse_args()
    
    main(args.input_folder, args.output_base)
