---
title: "Tuning Linux Swap for Kubernetes: A Deep Dive"
date: "2025-08-19T18:34:08"
category: "Markets"
summary: ""
slug: "tuning linux swap for kubernetes a deep dive"
source_urls:
  - "https://kubernetes.io/blog/2025/08/19/tuning-linux-swap-for-kubernetes-a-deep-dive/"
seo:
  title: "Tuning Linux Swap for Kubernetes: A Deep Dive | Hash n Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---
**Headline** Linux Swap Tuning: A Deep Dive into Optimizing Node Performance for Kubernetes  **Summary Meta Description** Tune your Linux swap settings for optimal performance in Kubernetes. This article delves into the intricacies of Linux kernel parameters, presenting test results and recommendations to balance stability and resource utilization.  **Key Points**  * Enabling swap on Linux nodes allows for efficient use of secondary storage as virtual memory * Key Linux kernel parameters for swap tuning: `vm.swappiness`, `vm.min_free_kbytes`, and `vm.watermark_scale_factor` * Misconfiguration can lead to performance degradation and interfere with Kubelet's eviction logic * Test results demonstrate the impact of different configurations on node stability and performance  **Short Takeaways**  1.  **Swappiness Trade-Off**: A higher swappiness value (e.g., `swappiness=90`) leads to proactive swapping out of inactive anonymous memory, while a lower value (e.g., `swappiness=0`) favors dropping file-cache pages. 2.  **Watermark Tuning for Stability**: Increasing `min_free_kbytes` and `watermark_scale_factor` helps prevent OOM kills and eviction by giving the kernel more time to swap pages to disk during memory spikes.  **Recommendations**  * Use a starting point of `vm.swappiness=60`, `vm.min_free_kbytes=500000` (500MB), and `vm.watermark_scale_factor=2000` * Benchmark with your own workloads in test environments when setting up swap for the first time * Monitor performance and adjust settings as needed to balance stability and resource utilization 
