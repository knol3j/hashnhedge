---
title: "Navigating Failures in Pods With Devices'
date: '2025-08-22T05:04:02"
category: "Markets"
summary: ""
slug: "navigating failures in pods with devices"
source_urls:
  - "https://kubernetes.io/blog/2025/07/03/navigating-failures-in-pods-with-devices/"
seo:
  title: "Navigating Failures in Pods With Devices | Hash n Hedge'
  description: '"
  keywords: ["news", "markets", "brief"]
---
The provided text is a detailed blog post about the challenges of handling device failures in Kubernetes, particularly for Artificial Intelligence (AI) and Machine Learning (ML) workloads. The author discusses various failure modes, including:  1.  **Device Failure**: When a device fails or becomes unresponsive. 2.  **Container Code Failed**: When the container code crashes or fails to execute correctly. 3.  **Device Degradation**: When devices become slow or underperform due to misconfiguration or driver failures.  The author also mentions various DIY solutions that have been implemented by users to handle these failure modes, but notes that these solutions are often fragile and may not work for all scenarios.  To address these challenges, the Kubernetes community is working on several initiatives, including:  1.  **KEP 4680**: Adding Resource Health Status to the Pod Status for Device Plugin and DRA. 2.  **Node-local retry policies**: Enabling pod failure policies for Pods with restartPolicy=OnFailure and possibly beyond that. 3.  **Ability to deschedule a pod**: Including with the restartPolicy: Always, so it can get a new device allocated.  The author also highlights several extension points in Kubernetes that are being targeted to make error handling and recovery cheaper, such as:  1.  Reusing pre-allocated resources as much as possible. 2.  Restarting containers in-place instead of rescheduling whenever possible. 3.  Snapshotting support. 4.  Prioritizing node local restart of containers.  Finally, the author encourages feedback and participation from the community to shape the future of device failure handling in Kubernetes.  Key points:  *   Device failures are a major challenge for AI/ML workloads in Kubernetes. *   DIY solutions have been implemented but are often fragile. *   The Kubernetes community is working on several initiatives to address these challenges. *   Extension points in Kubernetes are being targeted to make error handling and recovery cheaper. 
