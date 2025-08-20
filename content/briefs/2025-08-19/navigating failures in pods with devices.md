---
title: "Navigating Failures in Pods With Devices"
date: "2025-08-19T18:34:55"
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
The article discusses the challenges of handling failures in Kubernetes environments, particularly for AI/ML workloads. The authors identify three main failure modes:  1. **Device Failure**: This occurs when a device, such as a GPU or network interface, fails to function correctly. 2. **Container Code Failure**: This happens when a container's code executes incorrectly, causing the pod to fail. 3. **Device Degradation**: In this scenario, a device may still be functional but is experiencing performance degradation, which can impact the workload.  The authors propose several solutions and recommendations for handling these failure modes:  **Device Failure**  * Improve plugin reliability through best practices in development and deployment * Integrate device failures into Pod Failure Policy * Node-local retry policies to enable pod failure policies for Pods with restartPolicy=OnFailure  **Container Code Failure**  * Implement cheaper error handling and recovery, such as: 	+ Reusing pre-allocated resources (e.g., reusing Pods by restarting containers in-place) 	+ Node local restart of containers instead of rescheduling 	+ Snapshotting support 	+ Rescheduling prioritizing the same node to save on image pulls  **Device Degradation**  * There is limited work done in this area, and more research is needed * Hardware vendors and cloud providers are expected to develop solutions for device degradation  The authors also highlight several ongoing projects and discussions within the Kubernetes community that aim to address these failure modes.  **Takeaways:**  1. Device failures can have a significant impact on AI/ML workloads. 2. Kubernetes needs to provide better support for handling device failures. 3. Container code failures are already well-handled by Kubernetes, but there's room for improvement in terms of cost and efficiency. 4. Device degradation is an emerging area that requires more research and development.  **Recommendations:**  1. Join the Kubernetes community (SIG Node) to contribute to ongoing discussions and shape the future of device failure handling. 2. Provide feedback on patterns used in device degradation scenarios, as this space is expected to evolve rapidly. 3. Participate in ongoing projects and discussions that aim to address device failure modes. 
