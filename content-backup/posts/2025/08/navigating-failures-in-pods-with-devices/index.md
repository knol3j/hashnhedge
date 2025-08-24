---
title: "Navigating Failures in Pods With Devices\'
date: \'2025-08-23T15:18:19\'
category: \'Markets"
summary: ""
slug: "navigating failures in pods with devices"
source_urls:
  - "https://kubernetes.io/blog/2025/07/03/navigating-failures-in-pods-with-devices/"
seo:
  title: "Navigating Failures in Pods With Devices | Hash n Hedge\'
  description: \'\'
  keywords: [\'news", "markets", "brief"]
---
This text is a comprehensive overview of the challenges and future directions for device failure management in Kubernetes, specifically in the context of Artificial Intelligence (AI) and Machine Learning (ML) workloads. Here's a summary:  **Challenges:**  1. **Device failures:** Kubernetes has no way to express or handle device failures, which can lead to significant downtime and losses. 2. **Container code failures:** AI/ML workloads require more complex error handling and recovery mechanisms than traditional workloads. 3. **Device degradation:** Devices can degrade over time, affecting the performance of AI/ML workloads.  **Future directions:**  1. **KEP 4680:** Adding resource health status to the pod status for device plugin and DRA (Device Runtime Agent). 2. **Integrate device failures into Pod Failure Policy.** 3. **Node-local retry policies** for pods with restartPolicy=OnFailure and beyond. 4. **Ability to deschedule** pods, including those with restartPolicy=Always. 5. **Add device health** to the ResourceSlice used by DRA.  **Roadmap:**  The Kubernetes community is investing in extension points to make error handling and recovery cheaper for AI/ML workloads. The main improvements will target:  1. **In-place pod restarts** to reuse pre-allocated resources. 2. **Node local restart of containers** instead of rescheduling whenever possible. 3. **Snapshotting support**, and re-scheduling prioritizing the same node to save on image pulls.  The community encourages feedback and participation in shaping the future of device failure handling in Kubernetes. 
