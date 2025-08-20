---
category: Markets
date: '2025-08-19T18:32:36'
image: /images/posts/how-karrot-built-a-feature-platform-on-aws-part-2-feature-in.png
seo:
  keywords:
  - news
  - markets
  - brief
slug: how-karrot-built-a-feature-platform-on-aws-part-2-feature-in
source_urls:
- https://aws.amazon.com/blogs/architecture/how-karrot-built-a-feature-platform-on-aws-part-2-feature-ingestion/
title: How karrot built a feature platform on aws part 2 feature in
---

**Headline:** Karrot's Real-Time Feature Ingestion on AWS: A Technical Breakdown  **Summary Meta Description:** Learn how Karrot built a feature platform on Amazon Web Services (AWS) in this two-part series. Part 2 focuses on the real-time and batch ingestion of features into an online store, highlighting technical approaches for stable operation.  **Key Points:**  * Karrot's feature platform consists of three main components: feature serving, stream ingestion pipeline, and batch ingestion pipeline. * The stream ingestion pipeline collects features in real-time using AWS Kinesis Data Firehose. * Features are also ingested in batches using an Apache Airflow workflow. * Technical approaches for stable operation include data validation, caching, and exponential backoff.  **Short Takeaways with Analysis:**  1. Karrot's use of a stream ingestion pipeline demonstrates the importance of real-time data processing in modern software development. This approach allows for faster feature delivery and more agile development practices. 2. The incorporation of batch ingestion highlights the need for balanced approach to data processing, ensuring that both real-time and historical data are accounted for.  **Sources:**  * [https://aws.amazon.com/blogs/architecture/how-karrot-built-a-feature-platform-on-aws-part-2-feature-ingestion/](https://aws.amazon.com/blogs/architecture/how-karrot-built-a-feature-platform-on-aws-part-2-feature-ingestion/)