# Synthetic Clinical Note Generator

A framework for generating high-quality synthetic clinical notes for machine learning research in medical coding.

## Project Goal

Build a reproducible pipeline that generates realistic synthetic clinical notes from structured diagnosis and patient information, with the goal of supporting ICD-10 code prediction from clinical text.

### V2 Architecture

                 Patient Profile
                       │
                       ▼
                Patient History
                       │
                       ▼
                Current Encounter
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Face-to-Face  Medication    Referral
          Note         List        Document
          │            │             │
          └────────────┼─────────────┘
                       ▼
              Synthetic Patient Record
                       │
                       ▼
               Coding Ground Truth
                 │            │
                 ▼            ▼
           Primary Code   Secondary Codes