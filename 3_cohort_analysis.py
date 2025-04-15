import polars as pl

def preprocess_data(input_file: str, output_file: str) -> None:
    """
    Preprocess the dataset by filtering out rows with invalid BMI values
    and rows with 0 in key columns.
    
    Args:
        input_file: Path to the input CSV file.
        output_file: Path to save the cleaned CSV file.
    """
    df = pl.read_csv(input_file)

    cleaned_df = df.filter(
        (pl.col("BMI") >= 10) & (pl.col("BMI") <= 60) &
        (pl.col("Glucose") > 0) &
        (pl.col("BloodPressure") > 0) &
        (pl.col("SkinThickness") > 0) &
        (pl.col("Insulin") > 0)
    )

    cleaned_df.write_csv(output_file)
    print(f"Preprocessed data saved to {output_file}")


def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    # Convert CSV to Parquet
    pl.read_csv(input_file).write_parquet("patients_cleaned.parquet")

    # Debug BMI stats
    print("Debugging BMI statistics:")
    print(
        pl.scan_parquet("patients_cleaned.parquet")
        .select([
            pl.col("BMI").min().alias("min_BMI"),
            pl.col("BMI").max().alias("max_BMI"),
            pl.col("BMI").mean().alias("mean_BMI"),
            pl.col("BMI").std().alias("std_BMI"),
        ])
        .collect()
    )

    # Full lazy pipeline
    lazy_df = pl.scan_parquet("patients_cleaned.parquet").with_columns([
    pl.when(pl.col("BMI") < 18.5).then(pl.lit("Underweight"))
      .when(pl.col("BMI") < 25).then(pl.lit("Normal"))
      .when(pl.col("BMI") < 30).then(pl.lit("Overweight"))
      .otherwise(pl.lit("Obese"))
      .alias("bmi_range")
    ])
    cohort_results = (
        lazy_df.group_by("bmi_range")
        .agg([
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.len().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
        .sort("bmi_range")
        .collect()
    )

    # Ensure all BMI ranges are present
    expected_ranges = ["Underweight", "Normal", "Overweight", "Obese"]
    existing_ranges = set(cohort_results["bmi_range"])
    missing = [r for r in expected_ranges if r not in existing_ranges]

    if missing:
        print(f"Note: Missing cohort(s) detected: {missing}")
        missing_df = pl.DataFrame({
            "bmi_range": missing,
            "avg_glucose": [None] * len(missing),
            "patient_count": [0] * len(missing),
            "avg_age": [None] * len(missing),
        })
        cohort_results = pl.concat([cohort_results, missing_df]).sort("bmi_range")

    return cohort_results


def main():
    input_file = "patients_large.csv"
    cleaned_file = "patients_cleaned.csv"

    preprocess_data(input_file, cleaned_file)
    results = analyze_patient_cohorts(cleaned_file)

    print("\nCohort Analysis Summary:")
    print(results)


if __name__ == "__main__":
    main()
