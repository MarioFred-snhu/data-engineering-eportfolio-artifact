# Data Engineering ePortfolio Artifact

## Author: Mario Frederick  
## Degree Program: B.S. in Computer Science – Southern New Hampshire University  
## Course: CS-499: Capstone  

---

## About This Repository 

This repository serves as the central hub for my **CS-499 Computer Science Capstone ePortfolio**. It showcases enhanced versions of key projects developed throughout my degree program, demonstrating growth in three major areas of computer science:

1. Software Design and Engineering  
2. Algorithms and Data Structures  
3. Databases  

Each enhancement reflects both my technical development and my readiness for a professional **data engineering** role.

---

## Featured Artifact
### Project: Grazioso Salvare Animal Data Dashboard (CS-340)

- **Original Purpose:** Developed a full-stack dashboard application using Python, MongoDB, and Dash to help *Grazioso Salvare* identify rescue-ready dogs through interactive data visualization and filtering.  
- **Enhancement Goal:** Refactor the application into an object-oriented ETL pipeline with secure credential handling, improved algorithms for data transformation, and advanced MongoDB aggregation for analytical insights.

---

## Original and Enhanced Artifacts

- **Original Artifact (CS-340 – Pre-Enhancement):**  
  https://github.com/MarioFred-snhu/CS-340-Final-Project  
  This repository contains the original implementation of the Grazioso Salvare Animal Data Dashboard prior to all CS-499 enhancements.

- **Enhanced Artifact (CS-499 – Capstone):**  
  https://github.com/MarioFred-snhu/data-engineering-eportfolio-artifact  
  This repository contains the enhanced version developed for the CS-499 Capstone, incorporating improvements in software design, algorithm efficiency, and database analytics.

---

## Enhancement Overview

| Category | Focus | Enhancement Summary |
|--------|------|---------------------|
| **Software Design & Engineering** | Object-Oriented Refactoring | Refactored CRUD and ETL logic into modular classes (ETLManager, DataLoader, DashboardController), improving scalability, maintainability, and security through environment variables and structured logging. |
| **Algorithms & Data Structures** | ETL & Data Processing Efficiency | Implemented optimized merge and transformation logic using hash-based joins and Pandas vectorization to efficiently process 150k+ records. |
| **Databases** | MongoDB Optimization & Analytics | Designed aggregation pipelines to analyze shelter outcomes and trends, implemented compound indexes for performance, and deployed securely using MongoDB Atlas. |

---

## Geolocation Design Decision & Data Limitations

The Grazioso Salvare dataset does not include geographic coordinate data (latitude and longitude). Location information is provided only as unstructured text fields (e.g., “Found Location”), which limits the ability to perform true geospatial plotting without introducing external services.

Rather than relying on third-party geocoding APIs—which introduce rate limits, accuracy concerns due to inconsistent address formatting, and external dependencies—the dashboard map was intentionally designed to center on the Austin, TX service region and provide contextual location awareness without fabricating or over-processing data.

This design decision reflects real-world data engineering constraints and emphasizes responsible handling of incomplete datasets while maintaining transparency and system reliability.

---

## Technical Skills Demonstrated

- Python (Object-Oriented Programming, Data Analysis, Dash Framework)
- MongoDB (CRUD Operations, Aggregation Pipelines, Atlas Cloud Hosting)
- ETL Design (Extract, Transform, Load workflows with Pandas and PyMongo)
- Secure Software Practices (Environment Variables, Logging, Authentication)
- Algorithm Optimization & Data Structure Utilization
- UML & Data Flow Diagram Documentation

---

## Career Alignment

This ePortfolio highlights skills essential for **entry-level data engineering roles**, including building scalable ETL pipelines, optimizing data transformations, and designing secure, cloud-based data systems. The artifact reflects my readiness to contribute to real-world data engineering teams and supports my long-term goal of advancing into data systems engineering and leadership roles in technology.

---

## Capstone Narratives & Documentation

- [Professional Self-Assessment](narratives/Professional_Self_Assessment.md)
- [Enhancement 1 – Software Design & Engineering](narratives/Enhancement_1_Software_Design.md)
- [Enhancement 2 – Algorithms & Data Structures](narratives/Enhancement_2_Algorithms_Data_Structures.md)
- [Enhancement 3 – Databases](narratives/Enhancement_3_Databases.md)

Additional materials:
- Code Review Video (linked externally)
- Original and Enhanced Source Code
- Architecture & Data Flow Documentation

---

## Explore the Work

- **Enhanced Repository:** https://github.com/MarioFred-snhu/data-engineering-eportfolio-artifact  
- **Original CS-340 Repository:** https://github.com/MarioFred-snhu/CS-340-Final-Project  
- **GitHub Pages:** https://mariofred-snhu.github.io/data-engineering-eportfolio-artifact/
