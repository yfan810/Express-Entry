# Express Entry Draw Dashboard

This dashboard presents the previous IRCC Express Entry draw datasets, providing insights into immigration patterns and trends.

## Motivation

The Express Entry (EE) program is one of the fastest pathways for skilled workers to immigrate to Canada. Candidates are ranked based on their Comprehensive Ranking System (CRS) scores, and only the highest-scoring individuals receive an Invitation to Apply (ITA) for permanent residency.

Understanding historical trends in CRS scores and ITA issuance is crucial for applicants to:

-   Plan Strategically: Anticipate future CRS cutoffs and improve their scores accordingly.

-   Make Informed Decisions: Determine the best time to enter the Express Entry pool.

-   Track Progress: Monitor changes in immigration policies and their impact on CRS scores.

This dashboard is designed to empower applicants with the data they need to navigate the Express Entry system effectively.

## App Description

#### Video Demo

https://github.ubc.ca/mds-2024-25/DSCI_532_individual-assignment_yfan47/blob/master/img/demo.mp4

#### Data

The app uses publicly available datasets from IRCC Express Entry draws, including:

-   Draw Date: The date of each draw.

-   Draw Type: The category of the draw (e.g., CEC, FSW, PNP).

-   CRS Score: The minimum CRS score required for an ITA.

-   ITA Issued: The number of invitations issued in each draw.

## Installation Instruction

#### Step 1: Install Required Packages

```{r}
install.packages("shiny") 
install.packages("dplyr") 
install.packages("ggplot2") 
install.packages("bslib")
```

#### Step 2: Clone the repository

The repository can be found [here](https://github.ubc.ca/mds-2024-25/DSCI_532_individual-assignment_yfan47).

#### Step 3: Step 3: Run the App

-   Open the app.R file in RStudio.

-   Click the `Run App` button in RStudio.
