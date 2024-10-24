import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    unique_ids = pd.concat([df['id_start'], df['id_end']]).unique()
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)
    for _, row in df.iterrows():
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.at[row['id_end'], row['id_start']] = row['distance'] 
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, k] + distance_matrix.at[k, j] < distance_matrix.at[i, j]:
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_data = []
    ids = df.index.tolist()
    for i in ids:
        for j in ids:
            if i != j:  
                unrolled_data.append({'id_start': i, 'id_end': j, 'distance': df.at[i, j]})
    unrolled_df = pd.DataFrame(unrolled_data)
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    ref_distances = df[df['id_start'] == reference_id]['distance']
    if ref_distances.empty:
        return pd.DataFrame() 
    average_distance_ref = ref_distances.mean()
    lower_bound = average_distance_ref * 0.9
    upper_bound = average_distance_ref * 1.1
    average_distances = df.groupby('id_start')['distance'].mean().reset_index()
    filtered_ids = average_distances[
        (average_distances['distance'] >= lower_bound) &
        (average_distances['distance'] <= upper_bound)
    ]
    sorted_ids = filtered_ids.sort_values(by='id_start')
    return sorted_ids


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    ates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle, rate in rates.items():
        df[vehicle] = df['distance'] * rate

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_discount = {
        "morning": 0.8,  
        "day": 1.2,      
        "evening": 0.8   
    }
    weekend_discount = 0.7  

    start_days = []
    end_days = []
    start_times = []
    end_times = []
    for index, row in df.iterrows():
        for day in days:
            start_days.append(day)
            end_days.append(day)
            start_times.append(time(0, 0)) 
            end_times.append(time(23, 59, 59))  
            if day in ["Saturday", "Sunday"]:
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    df.at[index, vehicle] *= weekend_discount
            else:
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    df.at[index, vehicle] *= weekday_discount["morning"] if (start_times[-1] <= time(10, 0)) else weekday_discount["day"]
    df['start_day'] = start_days
    df['end_day'] = end_days
    df['start_time'] = start_times
    df['end_time'] = end_times
    return df
