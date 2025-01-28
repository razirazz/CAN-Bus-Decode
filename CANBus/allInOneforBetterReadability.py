from asammdf import MDF
import cantools
import pandas as pd

def raw_to_physical(start, length, matrix, factor, offset, unit):

  start_row, start_col = int(start) // 8, int(start) % 8
  end_row, end_col = start_row + ((start_col + length) // 8), ((start_col + length) % 8) - 1
  col = start_col
  limit = 0
  appended_bin = 0
  decimal_value = 0
  for row in range(start_row, end_row):
    # print(f'row = {row}')
    while col < 8:
      appended_bin = int(appended_bin) + (int(matrix[row][col]) * pow(10, limit))
      decimal_value = int(decimal_value) + (int(matrix[row][col]) * pow(2, limit))
      limit = limit + 1
      col = col + 1
    col = 0

  physical_value = factor * decimal_value + offset
  if unit is None:
    unit =''
  physical_value_unit = f'{physical_value} {unit}'

  return physical_value_unit


def fetch_messages_signals_from_DBC_file(messages, signals_set, data_binary, bit_data_value_matrix):

  signals_set.append({
      'message_name' : messages.name,
    })

  for signal in messages.signals:
    signals_set.append({
        'signal_name' : signal.name,
      })

    value = raw_to_physical(start=signal.start, length=signal.length, matrix=bit_data_value_matrix, factor=signal.conversion.scale, offset=signal.conversion.offset, unit=signal.unit)
    signals_set.append({'value': value})

  return signals_set

# Function -> iteration_through_files
# LOG_file -> (ID, DLC, Data, Time)
# DBC_file -> messages and signals
# match the ID's from both files

def iteration_through_files(LOG_file, DBC_file):

  data_processed_list = [] # A null set to store the data from LOG file and the corresponding Messages and signals for further operations

  for dataframe in LOG_file:
    # for samples_index in range((min(25, len(dataframe.samples)))): # Iteration through LOG file -> dataframe
    for samples_index in range(0, len(dataframe.samples)): # Cruising inside dataframe, So that, we can find "What it's actually trynna convey :)""
      for messages in DBC_file.messages:  #Iterate through DBC file

        DBC_ID = messages.frame_id
        dataframe_ID = dataframe.samples[samples_index][1]

        if dataframe_ID == DBC_ID:
          signals_set = []

          generated_data = dataframe.samples[samples_index][5]

          time = float(dataframe.timestamps[samples_index]) - float(dataframe.timestamps[0])

          data_binary = [format(int(items), 'b').zfill(8) for items in generated_data]
          # print(f'data_bin = {data_bin}')
          bit_data_value_matrix = [[0 for row in range(8)] for col in range(8)]
          # print(bit_data_value_matrix)
          for row in range(8):
            for col in range(8):
              bit_data_value_matrix[row][col] = data_binary[row][7 - int(col)]

          messages_from_DBC_file = fetch_messages_signals_from_DBC_file(messages, signals_set, data_binary, bit_data_value_matrix)

          data_processed_list.append({
              'timestamp' : time,
              'ID' : dataframe_ID,
              'data' : generated_data,
              'DBC_file_data' : messages_from_DBC_file
            })

  return data_processed_list



def main():

  # Load DBC_file_Path and LOG_file_Path
  DBC_path = 'D:/project/ADAS/dataset/Tesla Model 3/dbc_files/Model3CAN.dbc'
  LOG_path = 'D:/project/ADAS/dataset/Tesla Model 3/LOG/3F78A21D/00000001/00000001.MF4'

  # Read DBC file using cantools.database.load_file() and LOG file using asammdf.MDF(), These are in-built functions to read this type of data
  DBC_file = cantools.database.load_file(DBC_path)
  LOG_file = MDF(LOG_path)

  # Function -> iteration through files
  physical_value_file = iteration_through_files(LOG_file, DBC_file)

  # print(physical_value_file)

  d = pd.DataFrame(physical_value_file)
  # print(d.to_string())

  d.to_csv('D:/project/ADAS/output/Tesla/allInOneforBetterReadbility-01.csv')

# Here begins the main function
if __name__ == '__main__':
  main()