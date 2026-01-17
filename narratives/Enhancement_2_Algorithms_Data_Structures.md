# Enhancement 2: Algorithms and Data Structures

## Artifact Description

This enhancement builds on the **Grazioso Salvare Animal Data Dashboard**, focusing specifically on the data processing and transformation logic within the ETL pipeline. The application processes over **150,000 records** sourced from multiple MongoDB collections, requiring efficient algorithms to maintain performance and support responsive user interaction.

## Justification for Inclusion

This artifact was selected for the algorithms and data structures enhancement because it presents real-world data engineering challenges, including record deduplication, dataset merging, and aggregation for visualization. These challenges provided an opportunity to apply algorithmic reasoning and performance optimization techniques beyond basic coursework examples.

## Enhancement Summary

To improve performance, the data transformation logic was redesigned using optimized algorithms and appropriate data structures. **Hash-based joins** were implemented to efficiently merge intake and outcome records by `animal_id`, reducing time complexity compared to iterative or nested-loop approaches. Additionally, **Pandas vectorized operations** replaced row-by-row processing, significantly improving execution speed when handling large datasets.

These algorithmic improvements allow the dashboard to scale effectively while maintaining responsiveness. The enhanced ETL pipeline now supports complex filtering and aggregation operations without unnecessary recomputation.

## Reflection on the Enhancement Process

This enhancement reinforced the critical impact that algorithm selection and data structure choice have on system performance. I gained experience evaluating trade-offs between readability and efficiency and learned how vectorized operations can dramatically improve processing speed in data-intensive applications. This work demonstrates my ability to design and evaluate computing solutions using sound algorithmic principles, directly supporting a core course outcome.
