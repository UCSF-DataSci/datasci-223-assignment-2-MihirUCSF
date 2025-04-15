## Patient Cohort Analysis

### Data Analysis

Analyzed patient health data by cohorting individuals based on their Body Mass Index (BMI), using standard WHO guidelines. The data pipeline uses **Polars' lazy API** and **Parquet file format** to optimize performance for large datasets.

### Cohort Definitions

- **Underweight**: 10 ≤ BMI < 18.5  
- **Normal**: 18.5 ≤ BMI < 25  
- **Overweight**: 25 ≤ BMI < 30  
- **Obese**: 30 ≤ BMI ≤ 60

Outliers with BMI < 10 or > 60 were excluded as potential data errors.

### Summary Statistics

| BMI Range    | Avg. Glucose | Patient Count | Avg. Age |
|--------------|--------------|----------------|----------|
| Underweight  | 96.92        | 6,510          | 21.00    |
| Normal       | 106.73       | 286,460        | 27.41    |
| Overweight   | 116.42       | 556,488        | 29.64    |
| Obese        | 127.21       | 1,699,217      | 31.89    |

### Insights

- **Glucose levels** and **average age** both increase consistently from underweight to obese cohorts.
- The largest cohort is the **Obese** group, highlighting potential public health concerns.
- **Polars**' lazy evaluation significantly reduced memory usage and runtime during cohort analysis.

### Efficiency Notes

- Used `pl.scan_parquet` for streaming and lazy transformations.
- Computed statistics using chained lazy operations and grouped aggregations.
- Automatically handled missing cohorts to ensure output consistency.