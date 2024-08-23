
"""Takes in a dataset, sums the missing 
values counts for each column and displays it as a table """

from pyspark.sql.functions import col, sum

def get_missing_value_counts(dataset):

    # Initialise an empty list to hold the sum columns
    sum_columns = []

    # Iterate over each column, summing their counts of NULL values
    for c in dataset.columns:
        sum_expression = sum(col(c).isNull().cast("int")).alias(c + '_count')
        sum_columns.append(sum_expression)

    # Selection and display
    missing_values = dataset.select(sum_columns)
    missing_values.show()

    return

"""Takes in a dataset, counts and prints out its shape"""

def get_dataset_shape(dataset):

    # Number of rows
    # Number of rows
    num_rows = dataset.count()

    # Number of columns
    num_columns = len(dataset.columns)

    print(f"Dataset shape is: {num_rows} rows, {num_columns} columns")

    return

