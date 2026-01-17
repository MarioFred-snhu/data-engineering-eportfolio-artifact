# Enhancement 1: Software Design and Engineering

## Artifact Description

The selected artifact for enhancement is the **Grazioso Salvare Animal Data Dashboard**, initially developed in CS-340. This project is a comprehensive full-stack Python application built with **Dash** and **MongoDB**, designed to visualize data from animal shelters and identify dogs ready for rescue through interactive filtering and data visualization.

## Justification for Inclusion

This artifact was chosen for its representation of a realistic software system comprising multiple components, making it an exemplary subject for showcasing professional software design and engineering practices. In its initial form, the application utilized tightly coupled logic and procedural workflows. Enhancing this artifact provided an opportunity to implement object-oriented design principles, thereby improving scalability, maintainability, and security—essential expectations within the software development industry.

## Enhancement Summary

The enhancement involved refactoring the application into a modular and object-oriented architecture. Core responsibilities were delineated among dedicated classes:

- **ETLManager** to oversee data flow  
- **DataLoader** to manage data extraction and validation  
- **Dashboard Controller** to maintain application state  

Sensitive configuration data was removed from source files and secured using **environment variables**. Additionally, **structured logging** was introduced to enhance traceability and debugging capabilities.

These modifications significantly improved code readability, minimized duplication, and facilitated easier testing and future extension. The revised design aligns more closely with professional software engineering standards and reflects contemporary development practices.

## Reflection on the Enhancement Process

Throughout the enhancement process, I recognized the significance of designing software with long-term maintainability as a primary consideration. The refactoring effort required meticulous planning to preserve existing functionality while improving the overall system structure. A notable challenge was determining appropriate class boundaries and responsibilities, which reinforced the importance of clear abstraction and adherence to the principle of separation of concerns.

This enhancement directly supports course outcomes related to software design, effective communication through code structure, and the application of industry-standard development practices.
