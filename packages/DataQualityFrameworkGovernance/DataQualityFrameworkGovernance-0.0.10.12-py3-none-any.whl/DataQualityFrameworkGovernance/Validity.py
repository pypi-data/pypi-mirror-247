#Validity

def validate_age(location, age_column, min_age, max_age, calculate='No'):
    import pandas as pd

    df = pd.DataFrame(location)

    # Check the validity of the 'Age' column
    df['Age Validity'] = (df[age_column] >= min_age) & (df[age_column] <= max_age)

    return df

def validate_age_count(location, age_column, min_age, max_age, calculate='No'):
    import pandas as pd

    df = pd.DataFrame(location)

    # Check the validity of the 'Age' column
    validity_check = (df[age_column] >= min_age) & (df[age_column] <= max_age)

    # Count the number of valid and invalid rows
    valid_count = validity_check.sum()
    invalid_count = len(df) - valid_count

    data = pd.DataFrame({
        'Count of dataset': [len(df)],
        'Valid count': [valid_count],
        'Invalid count': [invalid_count],
        'Valid count (%)': [(valid_count / len(df))*100],
        'Invalid count (%)': [(invalid_count / len(df))*100]
        })

    return data

#email valid?
def valid_email_pattern(location,email_column_name, calculate='No'):
    import pandas as pd
    import re

    df = pd.DataFrame(location)

    # Define a regular expression pattern to match valid email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email addresses follow the valid format
    df['Valid Email'] = df[email_column_name].apply(lambda x: bool(re.match(email_pattern, x)))
    return df

def is_within_range(location, column_name_to_look, array_list, calculate='No'):
    import pandas as pd

    df = pd.DataFrame(location)
    df['Within Range'] = df[column_name_to_look].isin(array_list)

    return df

def is_number_in_column(location, column_name, calculate='No'):
    df = location
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    df['is_number'] = df[column_name].apply(lambda x: is_number(x))
    return df

def is_number_in_dataset(df, calculate='No'):
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    for column in df.columns:
        result_series = df[column].apply(lambda x: is_number(x))
        df[f'{column}_is_number'] = result_series

    return df

def is_text_in_column(location, column_name, calculate='No'):
    def is_text(value):
        return str(value).isalpha()

    location[f'{column_name}_is_text'] = location[column_name].apply(lambda x: is_text(x))
    return location

def is_text_in_dataset(df, calculate='No'):
    def is_text(value):
        return str(value).isalpha()

    for column in df.columns:
        result_series = df[column].apply(lambda x: is_text(x))
        df[f'{column}_is_text'] = result_series

    return df

def is_date_in_column(location, column_name, date_format, calculate='No'):
    import pandas as pd
    def is_date(value):
        try:
            pd.to_datetime(value, format=date_format)
            return True
        except (ValueError, TypeError):
            return False

    location[f'{column_name}_is_date'] = location[column_name].apply(lambda x: is_date(x))
    return location

def is_date_in_dataset(location, date_format, calculate='No'):
    import pandas as pd
    def is_date(value):
        try:
            pd.to_datetime(value, format=date_format)
            return True
        except (ValueError, TypeError):
            return False

    for column in location.columns:
        location[f'{column}_is_date'] = location[column].apply(lambda x: is_date(x))

    return location