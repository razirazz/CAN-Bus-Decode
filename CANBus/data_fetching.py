import raw_to_physical

def fetch_messages_signals_from_DBC_file(messages, signals_set, data_binary, bit_data_value_matrix):

  signals_set.append({
      'message_name' : messages.name,
      'message_length' : messages.length,
    })

  for signal in messages.signals:
    signals_set.append({
        'signal_name' : signal.name, # Signal Name
        # 'start_bit' : signal.start, # Starting Bit
        # 'signal_length' : signal.length, # Bit Length
        # 'byte_order' : signal.byte_order, # Little Endian or Big Endian
        # 'is_signed' : signal.is_signed, # Signed - or Unsigned +
        # 'factor' : signal.conversion.scale, # Factor (Factor, Offset)
        # 'offset' : signal.conversion.offset, # Offset (Factor, Offset)
        'min' : signal.minimum, # Minimum Value
        'max' : signal.maximum, # Maximum Value
        # 'unit' : signal.unit, # Extension
        # 'multiplexer' : signal.is_multiplexer, # Multiple Values -> Bool (True/ False)
        # 'multiplexer_ids' : signal.multiplexer_ids, # Multiple Values ID -> List
        # 'multiplexer_signal' : signal.multiplexer_signal # Multiple Values Signals -> List
      })

    value = raw_to_physical.raw_to_physical(start=signal.start, length=signal.length, matrix=bit_data_value_matrix, factor=signal.conversion.scale, offset=signal.conversion.offset, unit=signal.unit)
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

          # messages_from_DBC_file = fetch_messages_signals_from_DBC_file(messages, signals_set)

          time = float(dataframe.timestamps[samples_index]) - float(dataframe.timestamps[0])

          # data_processed_list.append({
          #     'timestamp' : time,
          #     'ID' : dataframe_ID,
          #     'DLC' : dataframe.samples[samples_index][3],
          #     'data' : generated_data,
          #   })

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
              # 'DLC' : dataframe.samples[samples_index][3],
              'data' : generated_data,
              'DBC_file_data' : messages_from_DBC_file
            })

  return data_processed_list
