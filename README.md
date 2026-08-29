# Synthetic Clinical Note Generator

A framework for generating high-quality synthetic clinical notes for
machine learning research in medical coding.

## Project Goal

Build a reproducible pipeline that generates realistic synthetic clinical
notes from structured diagnosis and patient information, with the goal of
supporting ICD-10 code prediction from clinical text.

### V1 Architecture
```text
              Structured Input
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
  Diagnosis Profile     Patient Profile
          │                   │
          └─────────┬─────────┘
                    ▼
            Synthetic Patient
                    │
                    ▼
           LLM Clinical Note
                Generation
                    │
                    ▼
           Synthetic Clinical
                  Notes
                    │
                    ▼
              Dataset Creation
                    │
                    ▼
           ICD-10 + Clinical Note
                    │
                    ▼
            Baseline ML Model
                    │
                    ▼
                Evaluation
```

## V1 Status

V1 established the initial end-to-end synthetic clinical note generation
and machine learning pipeline.

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
- [x] Create and commit reference clinical notes

## V1 Findings

The initial baseline model achieved very high accuracy. Further inspection
showed that the generated clinical notes explicitly contained the diagnosis
or condition name associated with the target ICD-10 code.

As a result, the model could learn to associate explicitly stated condition
names with their corresponding ICD-10 codes rather than needing to infer
the diagnosis from clinical findings, symptoms, laboratory values, and
other contextual information.

The V1 approach also does not adequately distinguish the clinical context,
etiology, or subcondition that may determine a more specific ICD-10 code.

The supervised ML approach is also dependent on the conditions and ICD-10
codes represented in its training data. Introducing previously unseen
conditions would require additional training data and model retraining,
which limits scalability.

The V1 dataset and model are therefore retained as an initial end-to-end
proof of concept.

The reference clinical notes created during V1 are also retained as
baseline examples for subsequent iterations.

## V1 Conclusion

V1 successfully demonstrated the complete pipeline from structured patient
and diagnosis information to synthetic clinical notes, dataset creation,
and an initial ICD-10 prediction model.

The primary limitations identified in V1 are that:

1. The model can recognize an explicitly stated condition but does not adequately distinguish the clinical context, etiology, or subcondition that determines the more specific ICD-10 code.

2. The supervised ML approach depends on training data for the conditions and ICD-10 codes it is expected to predict. Introducing previously unseen conditions requires additional training data and model retraining, limiting scalability.