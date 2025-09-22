# Handwritten Signature Feature Extraction

## Overview
This project implements a **feature extraction pipeline for handwritten signatures**.  
The goal is to analyze structural and geometric properties of a signature that can later be used for tasks such as **signature verification** or **biometric identification**.  

---

## Steps in the Algorithm

1. **Bounding Box Extraction**  
   - A bounding box is drawn around the signature segment to localize the region of interest.

2. **Recursive Centroid Segmentation**  
   - The bounding box is recursively divided into **64 segments** by locating centroids, ensuring localized feature capture.

3. **Black-to-White Transitions**  
   - For every group of 4 segments, transitions between black (ink) and white (background) pixels are counted.  
   - These transitions serve as key structural features of the signature.

4. **Inclination Angle Calculation**  
   - The overall **angle of inclination** of the signature is determined, providing information on writing slant.

---

## Applications

 - Signature verification systems
 - Biometric authentication
 - Handwriting analysis
