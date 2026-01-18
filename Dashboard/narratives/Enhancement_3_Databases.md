# Enhancement 3: Databases

## Artifact Description

This enhancement focuses on the **MongoDB backend** supporting the Grazioso Salvare Animal Data Dashboard. In its original implementation, the project relied primarily on basic CRUD operations to retrieve and display animal shelter data.

## Justification for Inclusion

This artifact was selected because it provided an opportunity to demonstrate advanced database concepts within a realistic, production-oriented environment. Enhancing the database layer allowed for the application of indexing strategies, aggregation pipelines, and secure cloud deployment techniques commonly used in professional data engineering workflows.

## Enhancement Summary

For this enhancement, **MongoDB aggregation pipelines** were implemented to compute analytical insights such as outcome trends and shelter statistics by breed. **Compound indexes** were added to frequently queried fields to significantly improve query performance. Additionally, the database was deployed using **MongoDB Atlas**, enabling secure cloud-based access, authentication, and improved scalability.

These enhancements transformed the database from a simple data store into an analytical engine capable of supporting decision-making and performance-sensitive queries.

## Reflection on the Enhancement Process

This enhancement strengthened my understanding of how database design directly affects application performance and scalability. I gained experience structuring aggregation pipelines to minimize data transfer and leverage the database engine for computation. Deploying the system in a secure cloud environment reinforced the importance of addressing security and scalability considerations early in the design process. This work aligns strongly with course outcomes related to database systems, data management, and secure computing practices.
