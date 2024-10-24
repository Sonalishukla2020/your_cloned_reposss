from typing import Dict, List

import pandas as pd


def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    # Your code goes here.
    result = []
    length = len(lst)
    for i in range(0, length, n):
        x = lst[i:i+n]
        x_length = len(x)
        for j in range(x_length // 2):
            x[j], x[x_length - 1 - j] = x[x_length - 1 - j], x[j]
        result.extend(x)
    return result


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    """
    Groups the strings by their length and returns a dictionary.
    """
    # Your code here
    length_dict = {}
    for i in strings:
        length = len(i)  
        if length not in length_dict:
            length_dict[length] = []
        length_dict[length].append(i)
        x=dict(sorted(length_dict.items()))
    return x

def flatten_dict(nested_dict: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """
    Flattens a nested dictionary into a single-level dictionary with dot notation for keys.
    
    :param nested_dict: The dictionary object to flatten
    :param sep: The separator to use between parent and child keys (defaults to '.')
    :return: A flattened dictionary
    """
    # Your code here
    flattened = {}

    def flatten(current_dict: Dict[str, Any], parent_key: str = ''):
        for key, value in current_dict.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                flatten(value, new_key)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    item_key = f"{new_key}[{index}]"
                    if isinstance(item, dict):
                        flatten(item, item_key)
                    else:
                        flattened[item_key] = item
            else:
                flattened[new_key] = value

    flatten(nested_dict)
    return flattened
    

def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    
    :param nums: List of integers (may contain duplicates)
    :return: List of unique permutations
    """
    # Your code here
    def backtrack(start: int):
        if start == len(nums):
            result.append(nums[:])
            return
        seen = set() 
        for i in range(start, len(nums)):
            if nums[i] in seen:  
                continue
            seen.add(nums[i]) 
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    result = []
    nums.sort()  
    backtrack(0)
    return result
    pass


def find_all_dates(text: str) -> List[str]:
    """
    This function takes a string as input and returns a list of valid dates
    in 'dd-mm-yyyy', 'mm/dd/yyyy', or 'yyyy.mm.dd' format found in the string.
    
    Parameters:
    text (str): A string containing the dates in various formats.

    Returns:
    List[str]: A list of valid dates in the formats specified.
    """
    patterns = [
        r'\b([0-2][0-9]|(3)[0-1])-(0[1-9]|1[0-2])-(\d{4})\b',  # dd-mm-yyyy
        r'\b(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|(3)[0-1])-(\d{4})\b',  # mm/dd/yyyy
        r'\b(\d{4})\.(0[1-9]|1[0-2])\.([0-2][0-9]|(3)[0-1])\b'  # yyyy.mm.dd
    ]
    valid_dates = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                if pattern == patterns[0]: 
                    valid_dates.append(f"{match[0]}-{match[1]}-{match[2]}")
                elif pattern == patterns[1]: 
                    valid_dates.append(f"{match[0]}/{match[1]}-{match[2]}")
                elif pattern == patterns[2]: 
                    valid_dates.append(f"{match[0]}.{match[1]}.{match[2]}")
            else:
                valid_dates.append(match)
    return valid_dates
    pass

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    """
    Converts a polyline string into a DataFrame with latitude, longitude, and distance between consecutive points.
    
    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        pd.DataFrame: A DataFrame containing latitude, longitude, and distance in meters.
    """
    return pd.Dataframe()


def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then multiply each element 
    by the sum of its original row and column index before rotation.
    
    Args:
    - matrix (List[List[int]]): 2D list representing the matrix to be transformed.
    
    Returns:
    - List[List[int]]: A new 2D list representing the transformed matrix.
    """
    # Your code here
    n = len(matrix)
    rotated_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n - 1 - i] = matrix[i][j]
    final_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i])  
            col_sum = sum(rotated_matrix[k][j] for k in range(n))  
            final_matrix[i][j] = row_sum + col_sum - rotated_matrix[i][j]  
            
    return final_matrix
    return []


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    results = {}
    grouped = df.groupby(['id', 'id_2'])
    
    for (id_val, id_2_val), group in grouped:
        all_days = set(group['start'].dt.day_name()) 
        full_24_hours = (group['start'].min().date() == group['end'].max().date()) 
        complete_time = group['start'].dt.floor('H').nunique() == 24  # Must have all 24 hours
        results[(id_val, id_2_val)] = (len(all_days) == 7 and full_24_hours and complete_time)
    return pd.Series(results)
    
