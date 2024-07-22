Here's the updated README for Laboratory #3:

# Laboratory #3 - Compilers: DSL Reservations Language Interpreter 🛠️

> **Due Date:** August 9, 2024

> **Due Time:** 11:35pm

> **Class:** Construcción de Compiladores

> **Class Time:** Section 10

> **Instructor:** Professor Bidkar Pojoy

> **Authors:** **Samuel Chamalé and Dáriel Villatoro**

<p align="center">
  <br>
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXJ3dnMwOGdsd2F2eHMzMWc1cDc4NHoyYXJxaHI3d3ZqM2NmazRhYSZlcD12MV9pbnRlcm5naWZfYnlfaWQmY3Q9Zw/xT5LMINTLCSOGdIyEo/giphy.webp" alt="wb" width="400">
  <br>
</p>
<p align="center" >
  <a href="#overview">Overview</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#instructions">Instructions</a> •
  <a href="#files">Files</a>
</p>

## Overview

This repository contains the code and resources for Laboratory #3 of the Compilers course. The objective of this laboratory is to design and run a custom Domain Specific Language (DSL) for conference room reservations using ANTLR.

## Prerequisites

Before you begin, ensure you have the following software installed on your machine:

- Docker

## Instructions

### Building and Running the Docker Image

1. **Build and Run the Docker Image:**
   Open a terminal in the root directory of this repository and execute the following command to build the Docker image and start the Docker container with the appropriate volume mapping:

   ```sh
   docker build --rm . -t lab3-image && docker run --rm -ti -v "$(pwd)/program":/program lab3-image
   ```

   _Note: When using Windows, use ${pwd}/program:/program._

### Compiling and Running the Program

2. **Generate ANTLR Files:**
   Inside the Docker container, run the following command to generate the ANTLR files:

   ```sh
   antlr -Dlanguage=Python3 ConfRoomScheduler.g4
   ```

3. **Run the Program:**
   After generating the ANTLR files, run the program using:

   ```sh
   python3 DriverConfroom.py test/<test file>
   ```

4. **Run Automated Tests:**
   For automated tests, run the following command:

   ```sh
   python3 automatedTests.py
   ```

## Files

- [**Dockerfile**](./Dockerfile): Contains the instructions to build the Docker image.
- [**DriverConfroom.py**](./program/DriverConfroom.py): The main driver script for running the conference room scheduler interpreter.
- [**ConfRoomScheduler.g4**](./program/ConfRoomScheduler.g4): The ANTLR grammar definition file.
- [**automatedTests.py**](./program/automatedTests.py): Script to run automated tests.
- [**tests**](./program/tests/): Directory containing test files.

> For any issues or further assistance, please contact us at [cha21881@uvg.edu.gt](mailto:cha21881@uvg.edu.gt) or [vil20776@uvg.edu.gt](mailto:vil20776@uvg.edu.gt)
