## V2 – ICD-10 Data Scraper

V2 focuses on building the ICD-10-CM data scraping component of the project.

The scraper retrieves ICD-10-CM information from ICD10Data.com for a user-provided diagnosis code.

### V2 Architecture

```text
                 ICD-10-CM Code
                       │
                       ▼
                Search ICD10Data
                       │
                       ▼
              Resolve Code URL
                       │
                       ▼
                Fetch Web Page
                       │
                       ▼
                 Parse HTML
                       │
                       ▼
          Extract ICD-10 Information
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        Code       Description   Code Details
                                      │
                                      ▼
                              Dynamic Sections
                                      │
                       ┌──────────────┼──────────────┐
                       ▼              ▼              ▼
                  Code First     Excludes       Includes
                       │
                       ▼
                 Other Sections
                       │
                       ▼
               Structured Output
```