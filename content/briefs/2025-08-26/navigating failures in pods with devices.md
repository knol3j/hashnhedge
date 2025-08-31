---
title: "Navigating Failures in Pods With Devices'
date: '2025-08-26T20:54:38"
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
This text is a comprehensive overview of device failure handling in Kubernetes, covering various failure modes such as:  1.  **K8s Infrastructure**: This includes issues related to kubelet integration with systemd watchdog, detecting stale DRA plugin sockets, supporting takeover for devicemanager/device-plugin, kubelet plugin registration reliability, recreating the Device Manager gRPC server if failed, and retrying pod admission on device plugin gRPC failures. 2.  **Device Failed**: This includes work in progress such as making information about failed devices available easier through KEP 4680 (Add Resource Health Status to the Pod Status for Device Plugin and DRA). Other ideas include integrating device failures into Pod Failure Policy, node-local retry policies, descheduling pods, and adding device health to the ResourceSlice used by DRA. 3.  **Container Code Failed**: This includes improvements targeting cheaper error handling and recovery. The main goals are reusing pre-allocated resources as much as possible, restarting containers in-place instead of rescheduling whenever possible, snapshotting support, and rescheduling prioritizing the same node to save on image pulls. 4.  **Device Degradation**: There is limited work done in this area, but it's expected that hardware vendors and cloud providers will contribute to DIY solutions for detecting device performance or degradation.  **Key points:**  *   The Kubernetes community encourages feedback and participation in shaping the future of device failure handling. *   Addressing these issues will solidify Kubernetes' position as the leading platform for AI/ML workloads, ensuring resilience and reliability for applications that depend on specialized hardware. 
