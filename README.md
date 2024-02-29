## classifytree

## Phylogenetic Tree Classifier
This Python script classifies phylogenetic trees into predefined categories based on their species composition. It processes trees in Newick format, classifies them into `tree`, `unclassified`, `tree1`, `tree2`, `tree3`, and `other`, then copies the trees into corresponding folders and generates a summary CSV report.

## Installation

Before you begin, ensure you have Python installed on your system. This script has been tested with Python 3.8 and above. You will also need to install the required Python libraries:

```sh
pip install biopython ete3 pandas
```

## Usage

To use the script, you need to have a folder containing your Newick tree files. Then, you can run the script as follows:

```sh
python classify_trees.py --input_folder path/to/input_trees --output_base path/to/output_folder
```

- `--input_folder`: The path to the folder containing the Newick format tree files you want to classify.
- `--output_base`: The base path where the script will create folders for each classification category and the summary CSV.

After execution, the script will create folders for each category (`tree`, `unclassified`, `tree1`, `tree2`, `tree3`, and `other`) in the specified output base path, copy the classified tree files into these folders, and generate a `tree_classification_summary.csv` file summarizing the classification of each tree.

## Output Structure

- `tree/`: Contains trees that were classified as general trees.
- `unclassified/`: Contains trees that could not be classified into the predefined genera.
- `tree1/`, `tree2/`, `tree3/`: Contains trees classified into more specific categories based on their species composition.
- `other/`: Contains trees that did not fit into the other categories.
- `tree_classification_summary.csv`: A summary CSV file listing each tree file and its classification.

## Contributing

Contributions to this project are welcome. You can contribute by improving the script, adding features, or reporting bugs. Please feel free to fork the repository and submit a pull request.

## License

This project is open source and available under the [MIT License](LICENSE).
