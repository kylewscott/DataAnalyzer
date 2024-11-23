import warnings

warnings.filterwarnings("ignore")

import json
import os

import cellxgene_census
import datasets
import numpy as np
import scanpy as sc
from geneformer import (
    DataCollatorForCellClassification,
    EmbExtractor,
    TranscriptomeTokenizer,
)
from transformers import BertForSequenceClassification, Trainer

adata = sc.read_10x_mtx("data/filtered_gene_bc_matrices/hg19/", var_names="gene_ids")
adata.var["ensembl_id"] = adata.var.index
adata.obs["n_counts"] = adata.X.sum(axis=1)
adata.obs["joinid"] = list(range(adata.n_obs))

h5ad_dir = "./data/h5ad/"

if not os.path.exists(h5ad_dir):
    os.makedirs(h5ad_dir)

adata.write(h5ad_dir + "pbmcs.h5ad")

token_dir = "data/tokenized_data/"

if not os.path.exists(token_dir):
    os.makedirs(token_dir)

tokenizer = TranscriptomeTokenizer(custom_attr_name_dict={"joinid": "joinid"})
tokenizer.tokenize_data(
    data_directory=h5ad_dir,
    output_directory=token_dir,
    output_prefix="pbmc",
    file_format="h5ad",
)

model_dir = "../../Geneformer/fine_tuned_models/gf-6L-30M-i2048_CellClassifier_cardiomyopathies_220224"
label_mapping_dict_file = os.path.join(model_dir, "config.json")

with open(label_mapping_dict_file) as fp:
    label_mapping_dict = json.load(fp)
print(label_mapping_dict)

dataset = datasets.load_from_disk(token_dir + "pbmc.dataset")
print(dataset)
dataset = dataset.add_column("label", [0] * len(dataset))

# reload pretrained model
model = BertForSequenceClassification.from_pretrained(model_dir)
# create the trainer
trainer = Trainer(model=model, data_collator=DataCollatorForCellClassification(token_dictionary=tokenizer.get_vocab()))
# use trainer
predictions = trainer.predict(dataset)

predicted_label_ids = np.argmax(predictions.predictions, axis=1)
predicted_logits = [predictions.predictions[i][predicted_label_ids[i]] for i in range(len(predicted_label_ids))]
predicted_labels = [label_mapping_dict[str(i)] for i in predicted_label_ids]

adata.obs["predicted_cell_subclass"] = predicted_labels
adata.obs["predicted_cell_subclass_probability"] = np.exp(predicted_logits) / (1 + np.exp(predicted_logits))

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
adata = adata[:, adata.var.highly_variable]
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(adata)

sc.tl.leiden(adata)
original_cell_types = [
    "CD4-positive, alpha-beta T cell (1)",
    "CD4-positive, alpha-beta T cell (2)",
    "CD14-positive, monocyte",
    "B cell (1)",
    "CD8-positive, alpha-beta T cell",
    "FCGR3A-positive, monocyte",
    "natural killer cell",
    "dendritic cell",
    "megakaryocyte",
    "B cell (2)",
]
adata.rename_categories("leiden", original_cell_types)

sc.pl.umap(adata, color="leiden", title="Original Annotations")













# from geneformer import EmbExtractor

# embex = EmbExtractor(model_type="CellClassifier",
#                      num_classes=3,
#                      filter_data={"cell_type":["Cardiomyocyte1","Cardiomyocyte2","Cardiomyocyte3"]},
#                      max_ncells=1000,
#                      emb_layer=0,
#                      emb_label=["disease","cell_type"],
#                      labels_to_plot=["disease"],
#                      forward_batch_size=200,
#                      nproc=16)

# embs = embex.extract_embs("../../Geneformer/fine_tuned_models/gf-6L-30M-i2048_CellClassifier_cardiomyopathies_220224",
#                           "./human_dcm_hcm_nf.dataset",
#                           "C:\Projects\LLM\Datasets\outputs",
#                           "output_prefix")

# embex.plot_embs(embs=embs, 
#                 plot_style="umap",
#                 output_directory="C:\Projects\LLM\Datasets\outputs",  
#                 output_prefix="emb_plot")

# embex.plot_embs(embs=embs, 
#                 plot_style="heatmap",
#                 output_directory="C:\Projects\LLM\Datasets\outputs",
#                 output_prefix="emb_plot")