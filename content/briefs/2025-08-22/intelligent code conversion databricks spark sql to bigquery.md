---
title: "Intelligent code conversion: Databricks Spark SQL to BigQuery SQL via Gemini'
date: '2025-08-22T04:49:31"
category: "Markets"
summary: ""
slug: "intelligent code conversion databricks spark sql to bigquery"
source_urls:
  - "https://cloud.google.com/blog/products/data-analytics/automate-sql-translation-databricks-to-bigquery-with-gemini/"
seo:
  title: "Intelligent code conversion: Databricks Spark SQL to BigQuery SQL via Gemini | Hash n Hedge'
  description: '"
  keywords: ["news", "markets", "brief"]
---
The provided text is a comprehensive guide on how to translate Databricks Spark SQL to BigQuery SQL using the Gemini model. The article covers various aspects of this process, including:  1. **Function mapping guide**: A curated guide that maps Databricks-specific SQL functions (e.g., First_value, UCase) to their BigQuery equivalents (FIRST_VALUE, UPPER, TIMESTAMP). 2. **Few-shot examples**: Hand-translated queries are used as high-quality training prompts to improve Gemini's consistency. 3. **Retrieval-Augmented Generation (RAG) layer**: The RAG engine is used to retrieve relevant function mappings and example translations before querying Gemini for translation. 4. **Gemini API integration**: The RAG-enriched prompt is sent to Gemini for translation, and the returned SQL is optionally post-processed to fix edge cases. 5. **Validation layer**: Translated SQL queries are validated by executing them in a BigQuery dry run mode to detect syntax issues.  The article also provides lessons learned from this process:  1. RAG + Gemini = Smart SQL translation: Grounding Gemini with real-world examples and mapping logic made it significantly more accurate. 2. A comprehensive function mapping guide is essential: Invest time in building a robust function mapping resource. 3. Thorough validation is the key: Use BigQueryΓÇÖs dry run and information schema to ensure translated queries are safe and optimized.  The article concludes by encouraging readers to streamline their SQL migrations using the Gemini model, which can make the process faster, more reliable, and less painful. 
