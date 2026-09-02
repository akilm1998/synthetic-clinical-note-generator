# Project Goal
Build a reproducible pipeline that generates realistic synthetic clinical notes from structured diagnosis and patient information, with the goal of supporting ICD-10 code prediction from clinical text.

# V3 Architecture

V3 extends the ICD-10 scraping work from V2 into an end-to-end clinical coding pipeline.
The key idea is to separate:
Clinical understanding — handled by an LLM
ICD-10 information retrieval — handled through ICD10Data search and scraping
Final coding decision — handled by a second LLM using the retrieved ICD-10 information and coding rules
High-Level Architecture

```text
                    Clinical Documents
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Patient History          Clinical Encounter
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    ┌─────────────┐
                    │   LLM #1    │
                    │             │
                    │ Correlate   │
                    │ documents   │
                    │ and identify│
                    │ conditions  │
                    └──────┬──────┘
                           │
                           ▼
                 Clinical Conditions
                 + Clinical Relationships
                           │
                           ▼
                  ICD-10 Search / Mapping
                           │
                           ▼
                  Candidate ICD-10 Codes
                           │
                           ▼
                    ICD-10 Scraper
                           │
                           ▼
             Code Information + Coding Rules
                           │
                           ▼
                    ┌─────────────┐
                    │   LLM #2    │
                    │             │
                    │ Coding      │
                    │ Decision    │
                    └──────┬──────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Combination      Primary       Secondary
          Codes           Code           Codes
```
