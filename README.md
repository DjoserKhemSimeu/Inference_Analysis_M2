# Estimating the Environmental Impact of AI Inference Deployment: Large Scale vs Edge Devices

## 🔍 Project Objective

This project aims to **quantify the environmental impact of AI model inference** across a spectrum of hardware platforms—from large-scale datacenter GPUs (like NVIDIA H100) to low-power Edge devices (like the Jetson AGX Orin).

The work was conducted as part of a Master's thesis at LIG (Laboratoire d’Informatique de Grenoble), and is fully documented in the [Final Report (PDF)](Final_Report.pdf). It includes experimental results using the **MLPerf Inference** benchmark and a **Life Cycle Assessment (LCA)** methodology to estimate CO₂ emissions.

---

## 🗂️ Project Structure

```
.
├── Data/                   # Power and latency measurement results per GPU
│   ├── data_*             # Raw and mean metrics from MLPerf Inference runs
│
├── Doc/                    # Documentation, reports, and research references
│   └── Environnemental_impact_of_inference_for_LLM.pdf
│
├── GreenDays/              # Presentation material and related publications
├── images/                 # All generated figures (PDF, PNG) for reports
├── Logs/                   # Logs of MLPerf benchmark executions
├── Plots/                  # Python plotting scripts for figures and analysis
│
├── README.md               # This file
```

---

## ⚙️ Methodology

### 1. **MLPerf Inference Benchmarking**

- Benchmarked with **MLPerf Inference v1.1 and v4.1** using the BERT model (SQuAD v1.1).
- Inference scenario: `SingleStream` (edge-like usage).
- Number of queries: {16, 32, 64, 128, 256}.

### 2. **Energy Measurement**

- Jetson (Xavier, Orin): via `tegrastats`.
- Grid’5000 GPUs (H100, A100, etc.): via `nvidia-smi` (NVML).
- 10 runs per experiment to assess variability.
- Numerical integration (trapezoidal rule) to compute energy in kWh.

### 3. **CO₂ Estimation**

Based on [Berthelot et al., 2022] LCA formula:

```
GWP = E_use × EGMg × PUE + (t / lifetime) × F_GPU
```

Where:
- `E_use`: energy used during inference (in kWh)
- `EGMg`: grid emission factor (France = 79.1 gCO₂/kWh)
- `PUE`: Power Usage Effectiveness (assumed 1.5)
- `F_GPU`: manufacturing footprint of the GPU (based on Morand et al.)

---

## 📊 Key Results

- H100 emits up to **10× more CO₂** than Jetson Orin for the same inference workload.
- Edge devices are more energy efficient but **significantly slower**.
- A clear trade-off exists between **performance** and **environmental impact**.

---

## 👤 Author

Research project by **Djoser Simeu**, supervised by **Danilo Carastan Dos Santos**, **Laurent Lefèvre**, and **Denis Trystram** at LIG Grenoble.

---
