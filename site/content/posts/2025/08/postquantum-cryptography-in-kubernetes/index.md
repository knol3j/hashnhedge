---
title: 'Postquantum cryptography in kubernetes'
date: "2025-08-19T18:34:40"
category: "Markets"
slug: postquantum-cryptography-in-kubernetes
source_urls:
  - "https://kubernetes.io/blog/2025/07/18/pqc-in-k8s/"
seo:
  keywords: ["news", "markets", "brief"]
---
**Headline:** Kubernetes Adopting Post-Quantum Cryptography by Default  **Summary Meta Description:** Kubernetes has quietly begun adopting post-quantum cryptography (PQC) for secure connections, leveraging Go's default support for hybrid PQC key exchange mechanisms. This development comes as the industry prepares for a future where quantum computers can break current cryptographic standards.  **Key Points:**  * Kubernetes v1.33 uses Go 1.24 by default, which enables support for post-quantum cryptography (PQC) in TLS connections. * The `X25519MLKEM768` hybrid scheme is the most widely supported PQC key exchange mechanism, combining classical and quantum-resistant algorithms. * PQC digital signatures are still in earlier stages of development and adoption due to larger keys and signature sizes, as well as performance concerns.  **Takeaways:**  1.  **Quantum-Safe Kubernetes:** Kubernetes has made significant strides in adopting post-quantum cryptography (PQC) for secure connections by default. This move is a proactive step towards securing the platform against potential quantum computer attacks. 2.  **Awareness and Considerations:** As PQC adoption increases, awareness of potential pitfalls such as Go version mismatches leading to downgrades and issues with Client Hello packet sizes becomes crucial. Kubernetes maintainers and contributors should stay informed about these developments to ensure long-term security.  **Sources:**  * Kubernetes Blog: "Post-Quantum Cryptography in Kubernetes" (https://kubernetes.io/blog/2025/07/18/pqc-in-k8s/) 
