from datetime import datetime
import pandas as pd

# Funkcja formatuje znacznik czasu z podanego ciągu znaków na określony format.
# Parametry:
# - timestamp_str: Znacznik czasu w formie stringa.
# - option: Opcja formatu (1 dla formatu "%Y-%m-%d %H:%M:%S.%f", 2 dla formatu "%Y/%m/%d %H:%M:%S.%f").
# Zwraca:
# - Sformatowany znacznik czasu w formie stringa w formacie "%Y-%m-%d %H:%M".
def format_timestamp(timestamp_str, option = 1):
    date_format_one, date_format_two = "%Y-%m-%d %H:%M:%S.%f", "%Y/%m/%d %H:%M:%S.%f"
    curr_date_format = date_format_one if option == 1 else date_format_two
    
    return datetime.strptime(timestamp_str, curr_date_format).strftime("%Y-%m-%d %H:%M")

# Funkcja przetwarza plik CSV do pliku tekstowego z określonym formatowaniem znaczników czasu.
# Parametry:
# - input_csv_path: Ścieżka do wejściowego pliku CSV.
# - output_txt_path: Ścieżka do wyjściowego pliku tekstowego.
# - timestamp_option: Opcja formatu znaczników czasu (1 dla formatu "%Y-%m-%d %H:%M:%S.%f", 2 dla formatu "%Y/%m/%d %H:%M:%S.%f").
# Zwraca:
# - Nic (zapisuje przetworzony plik tekstowy).
def process_csv_to_txt(input_csv_path, output_txt_path, timestamp_option = 1):
    df = pd.read_csv(input_csv_path)
    
    df['Start Timestamp'] = df['Start Timestamp'].apply(lambda x: format_timestamp(x, option=timestamp_option))
    df['Complete Timestamp'] = df['Complete Timestamp'].apply(lambda x: format_timestamp(x, option=timestamp_option))
    
    processed_df = df[['Case ID', 'Start Timestamp', 'Complete Timestamp', 'Activity']]
    processed_df.to_csv(output_txt_path, header=False, index=False, sep=',')


if __name__ == '__main__':
    file_name_without_extenstion = 'teleclaims'

    input_csv_path = f'./data/real/initial/{file_name_without_extenstion}.csv'
    output_txt_path = f'./data/real/preprocessed/{file_name_without_extenstion}.txt'

    process_csv_to_txt(input_csv_path, output_txt_path)