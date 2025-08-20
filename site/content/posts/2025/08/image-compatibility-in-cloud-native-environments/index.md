---
title: 'Image Compatibility In Cloud Native Environments'
date: "2025-08-19T18:35:06"
category: "Markets"
slug: image-compatibility-in-cloud-native-environments
source_urls:
  - "https://kubernetes.io/blog/2025/06/25/image-compatibility-in-cloud-native-environments/"
seo:
  keywords: ["news", "markets", "brief"]
---
The text discusses the implementation of image compatibility in Kubernetes, a feature that allows containerized applications to define and validate host OS requirements. The feature is built on top of the Node Feature Discovery (NFD) project, which provides a way for nodes to expose their features to the cluster.  Here are some key points from the text:  1. **Image Compatibility**: Image compatibility allows containerized applications to specify the required node features, such as kernel modules or CPU models. 2. **Node Feature Discovery (NFD)**: NFD is a project that provides a way for nodes to expose their features to the cluster. It uses a discovery mechanism to find available features on each node. 3. **Compatibility Artifact**: A compatibility artifact is an OCI artifact that contains metadata about the image's requirements based on node features. 4. **Client Implementation**: The client tool allows users to validate whether a node meets the image's requirements using the `nfd compat validate-node` command. 5. **Validation Report**: The client generates a JSON report indicating whether the node meets the image's requirements.  The text also provides an example of how to define image compatibility metadata, attach it to an image using ORAS, and validate image compatibility using the NFD client tool.  Overall, the implementation of image compatibility in Kubernetes aims to improve the reliability and performance of specialized containerized applications by allowing them to define and validate host OS requirements more efficiently. 
