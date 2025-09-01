---
title: "Navigating Failures in Pods With Devices"
date: "2025-08-28T04:32:30"
category: "Markets"
summary: ""
slug: "navigating failures in pods with devices"
source_urls:
  - "https://kubernetes.io/blog/2025/07/03/navigating-failures-in-pods-with-devices/"
seo:
  title: "Navigating Failures in Pods With Devices | Hash n Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---
This text is a lengthy blog post about the challenges of handling failures in Kubernetes, particularly for AI/ML workloads. Here's a summary:  **Challenges:**  1. **Device failures**: Hardware failures can occur due to various reasons like driver errors, misconfiguration, or component degradation. 2. **Container code failures**: Container code can fail due to out-of-memory conditions, non-zero exit codes, or liveness probe failures. 3. **Device degradation**: Devices may degrade in performance over time due to wear and tear or other factors.  **Current State:**  1. Kubernetes has some built-in mechanisms for handling device failures, such as restarting containers or descheduling pods. 2. However, these mechanisms are limited in their expressiveness and may not be sufficient for AI/ML workloads, which require more complex failure handling strategies.  **Future Directions:**  1. **Extension points**: SIG Node plans to add extension points to enable more robust and workload-specific failure handling scenarios. 2. **Resource Health Status**: A new resource health status will be added to the pod status to provide easier access to information about device failures. 3. **Retry policies**: Node-local retry policies will be introduced to enable pod failure policies for pods with restartPolicy=OnFailure. 4. **Descheduling**: The ability to deschedule pods, including those with restartPolicy=Always, will be added.  **Roadmap:**  1. Short-term goals include integrating device failures into Pod Failure Policy and adding resource health status to the pod status. 2. Long-term goals involve implementing automatic remediations for device failures, such as descheduling or restarting containers in-place.  **Conclusion:**  The Kubernetes community encourages feedback and participation in shaping the future of device failure handling. By addressing these challenges, Kubernetes can solidify its position as the leading platform for AI/ML workloads, ensuring resilience and reliability for applications that depend on specialized hardware.  Overall, this text provides a comprehensive overview of the challenges and future directions for device failure management in Kubernetes. It highlights the importance of extending Kubernetes' capabilities to support more complex failure handling scenarios and emphasizes the need for community involvement in shaping the platform's future. 
