Got it 👍 — you have a **single-entity NER dataset** with the following structure:

| text                                | start | end |
| ----------------------------------- | ----- | --- |
| "John works at Google."             | 0     | 4   |
| "Alice joined Microsoft last year." | 0     | 5   |

Let’s go step-by-step on how to **train a Named Entity Recognition (NER)** model (e.g., using **spaCy** or **Hugging Face Transformers**) from this data.

---

## 🧩 1. Prepare Your Data

Convert your dataset into a format suitable for NER training.

Here’s an example with `pandas`:

```python
import pandas as pd

# Example data
data = [
    {"text": "John works at Google.", "start": 0, "end": 4},
    {"text": "Alice joined Microsoft last year.", "start": 0, "end": 5},
]

df = pd.DataFrame(data)
```

You’ll need to transform it into **spaCy’s training format**, i.e.:

```python
TRAIN_DATA = [
    ("John works at Google.", {"entities": [(0, 4, "ENTITY")]}),
    ("Alice joined Microsoft last year.", {"entities": [(0, 5, "ENTITY")]}),
]
```

---

## 🧠 2. Training with spaCy

### Install spaCy

```bash
pip install spacy
```

### Initialize a blank model

```python
import spacy
from spacy.training import Example

# Create blank model (English)
nlp = spacy.blank("en")

# Add NER pipeline
ner = nlp.add_pipe("ner")

# Define label
ner.add_label("ENTITY")
```

---

### Prepare Training Data

```python
train_data = [
    ("John works at Google.", {"entities": [(0, 4, "ENTITY")]}),
    ("Alice joined Microsoft last year.", {"entities": [(0, 5, "ENTITY")]}),
]
```

---

### Train the Model

```python
from tqdm import trange

optimizer = nlp.begin_training()

for epoch in trange(30):
    losses = {}
    for text, annotations in train_data:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], sgd=optimizer, losses=losses)
    print(losses)
```

---

### Save the Model

```python
nlp.to_disk("ner_model")
```

---

### Test the Model

```python
nlp2 = spacy.load("ner_model")
doc = nlp2("John works at Google.")
print([(ent.text, ent.label_) for ent in doc.ents])
```

Expected output:

```
[('John', 'ENTITY')]
```

---

## ⚡ Option 2: Training with Hugging Face Transformers

If you want a **more powerful model** (e.g., BERT-based), we can format your dataset for the `transformers` library (using `datasets` + `Trainer`).

You’ll need:

```bash
pip install transformers datasets seqeval
```

Then you can:

1. Convert your dataset to token-level labels.
2. Fine-tune a pretrained model (like `bert-base-cased`) for token classification.

This approach is a bit more complex but gives much better results for real-world tasks.

---

Would you like me to show you the **Hugging Face version** (with code for token alignment and fine-tuning)?
It’s more powerful but requires a bit more setup.
