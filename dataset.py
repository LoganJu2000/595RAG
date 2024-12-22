from datasets import load_dataset
import pandas as pd

nq_ds = load_dataset("sentence-transformers/natural-questions")
nq_train_df = pd.DataFrame(nq_ds["train"])
