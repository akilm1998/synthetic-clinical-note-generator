# Synthetic Clinical Note Generator

A framework for generating high-quality synthetic clinical notes for machine learning research in medical coding.

## Project Goal

Build a reproducible pipeline that generates realistic synthetic clinical notes from structured diagnosis and patient information, with the goal of supporting ICD-10 code prediction from clinical text.

## Current Status

- [x] Repository initialized
- [x] Initial architecture designed
- [x] Diagnosis profile schema implemented
- [x] First diagnosis profile created
- [x] Synthetic patient generation implemented
- [x] Prompt-based clinical note generation implemented
- [x] Initial prompt refinement completed
- [x] Support additional diagnoses
- [x] Generate larger synthetic dataset
- [x] Implement automated dataset export
- [x] Export synthetic clinical notes to Apache Parquet format
- [x] Validate dataset structure
- [x] Prepare clinical notes and ICD-10 codes for machine learning
- [x] Train an initial baseline machine learning model
- [x] Evaluate initial model performance

## V1 Findings

The initial baseline model achieved very high accuracy. Further inspection showed that the generated clinical notes explicitly contained the diagnosis or condition name associated with the target ICD-10 code.

This created a form of data leakage: the model could learn to associate explicitly stated condition names with their corresponding ICD-10 codes rather than learning to infer diagnoses from clinical findings, symptoms, laboratory values, and other contextual information.

The V1 dataset and model are therefore retained as an initial end-to-end proof of concept, but the dataset generation process will be revised to reduce explicit diagnosis leakage.

## Next Steps

- [ ] Revise clinical note generation prompts to avoid explicitly naming the target diagnosis
- [ ] Generate V2 synthetic clinical notes
- [ ] Validate V2 notes for diagnosis-name leakage
- [ ] Perform exploratory data analysis
- [ ] Retrain the baseline model on V2
- [ ] Evaluate model performance using unseen clinical notes
- [ ] Compare V1 and V2 model performance