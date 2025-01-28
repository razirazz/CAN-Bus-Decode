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
      # print(f'decimal_value = {decimal_value}')
      limit = limit + 1
      col = col + 1
    col = 0

  physical_value = factor * decimal_value + offset
  if unit is None:
    unit =''
  physical_value_unit = f'{physical_value} {unit}'

  return physical_value_unit
