from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CEBinaryClassificationEvaluator
from sentence_transformers import InputExample

num_epochs = 5
model_save_path = "./model_dump"
model_name = 'cross-encoder/nli-deberta-v3-base' # base model, use 'vectara/hallucination_evaluation_model' if you want to further fine-tune ours

model = CrossEncoder(model_name, num_labels=1, automodel_args={'ignore_mismatched_sizes':True})

# Load some training examples as such, using a pandas dataframe with source and summary columns:
train_examples, test_examples = [], []
for i, row in df_train.iterrows():
    train_examples.append(InputExample(texts=[row['source'], row['summary']], label=int(row['label'])))

for i, row in df_test.iterrows():
    test_examples.append(InputExample(texts=[row['source'], row['summary']], label=int(row['label'])))
test_evaluator = CEBinaryClassificationEvaluator.from_input_examples(test_examples, name='test_eval')

# Then train the model as such as per the Cross Encoder API:
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=train_batch_size)
warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1) #10% of train data for warm-up
model.fit(train_dataloader=train_dataloader,
          evaluator=test_evaluator,
          epochs=num_epochs,
          evaluation_steps=10_000,
          warmup_steps=warmup_steps,
          output_path=model_save_path,
          show_progress_bar=True)
