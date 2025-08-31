---
title: "Tuning Linux Swap for Kubernetes: A Deep Dive'
date: '2025-08-28T03:37:02"
category: "Markets"
summary: ""
slug: "tuning linux swap for kubernetes a deep dive"
source_urls:
  - "https://kubernetes.io/blog/2025/08/19/tuning-linux-swap-for-kubernetes-a-deep-dive/"
seo:
  title: "Tuning Linux Swap for Kubernetes: A Deep Dive | Hash n Hedge'
  description: '"
  keywords: ["news", "markets", "brief"]
---
**Headline** Linux Swap Tuning Crucial for Stable Kubernetes Clusters: A Deep Dive  **Summary Meta Description** Optimize Linux swap behavior in Kubernetes clusters with expert guidance on key kernel parameters, including swappiness, min_free_kbytes, and watermark_scale_factor. Understand the trade-offs between performance and stability under memory pressure.  **Bullet Key Points**  * The NodeSwap feature in Kubernetes allows for swap usage to improve resource utilization and reduce OOM kills * Enabling swap is not a "turn-key" solution; Linux kernel parameters must be tuned for optimal performance and stability * Key kernel parameters for swap tuning include swappiness, min_free_kbytes, and watermark_scale_factor  **Short Takeaways**  1. **Swappiness**: The swappiness parameter controls the kernel's preference between reclaiming anonymous memory (swapping) and dropping page cache. A high value (90) prioritizes swapping out inactive anonymous memory to keep file cache active, while a low value (0) favors dropping file-cache pages. 2. **Tuning Watermarks**: Increasing min_free_kbytes and watermark_scale_factor can provide a larger safety buffer for reclamation and prevent OOM kills during sudden memory allocation spikes.  **Risks and Recommendations**  * Swapping can lead to performance degradation if not properly tuned * Swap can mask memory leaks in applications, making diagnosis more challenging * Improper tuning can disable evictions, leading to premature OOM kills  **Kubernetes Context** The kernel watermarks and kubelet eviction threshold create a series of memory pressure zones on a node. Adjusting the eviction-threshold parameters is essential to configure Kubernetes-managed evictions before OOM kills occur.  **Recommended Starting Point**  * vm.swappiness=60 (Linux default for general-purpose workloads) * vm.min_free_kbytes=500000 (500MB) to provide a reasonable safety buffer * vm.watermark_scale_factor=2000 to create a larger window for kswapd to work with 
