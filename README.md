# ONLYOFFICE Desktop Editors - Optimized v1 (ruletzz Edition)
[![License](https://img.shields.io/badge/License-GNU%20AGPL%20V3green.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)

[ONLYOFFICE Desktop Editors](https://www.onlyoffice.com/desktop.aspx) is a free office suite that combines text, spreadsheet, presentation, and PDF editors & Diagram Viewer. It is fully compatible with Office Open XML formats: .docx, .xlsx, .pptx.

## ⚡ What is this?
This is a **major performance enhancement** of ONLYOFFICE Desktop Editors. This version, dubbed **v1**, has been surgically optimized to be significantly faster and more responsive than the stock distribution. It is amazing.

### 🚀 The "ruletzz" Optimization Strategy
To achieve these speeds, I have:
1. **UI Layout Optimization:** Removed the toolbar to reduce DOM depth.
2. **Modular Decoupling:** Physically decoupled and removed the Editing menu, Plugin, Protection and Templates from the application core.
3. **Local-Only Execution:** Stripped Collaboration and Cloud.
4. **High-Density Sidebar:** Removed all text labels and template sections from the sidebar, implementing an icon-only navigation rail to maximize the workspace area.
5. **Core Engine Integration:** Custom **Rust-based processing engine** to increase document operation throughput and efficiency.
6. **Localization Pruning:** Restricted localization assets exclusively to **PT-PT** and **ENG**, drastically reducing the application's resource footprint.
7. **Initialization Bypass:** Removed the loading panel to enable quicker transition to the editing interface upon execution.

### 📊 Benchmarks
- **Cold Start:** [Before: 17.5s | After: 6.1s]
- **Memory Usage:** [Before: ~600mb | After: ~300mb]
- **Time Reduction:** 65% faster initialization.
- **Processing Throughput:** Significant reduction in main-thread blocking due to modular decoupling.

### 🎞️   Performance Comparison
[Before and After]
<p align="center">
  <img src="https://puu.sh/KMfwK/f142f9d052.gif" width="45%" />
  <img src="https://puu.sh/KKFCT/17292cf3dc.gif" width="45%" />
</p>

---

## ⚖️ Legal & Licensing
This is a **modified version** of ONLYOFFICE.
- **Original Authors:** (c) Copyright Ascensio System Limited 2010-2022.
- **License:** GNU Affero General Public License (AGPL) version 3.
- **Modifications:** All optimizations, surgical stripping, and performance enhancements were performed by **ruletzz**.
- **Important:** Pursuant to Section 7 of the AGPL, this version is provided "AS-IS" with no warranties. The original ONLYOFFICE logo and branding are respected where required by the license.

---
*Stay tuned for the next version - it's going to be even faster.*
