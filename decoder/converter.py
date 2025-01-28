from asammdf import MDF
import pandas as pd

# Load the MDF file
mdf = MDF('tesla/00000001.MF4')
for message in mdf:
    for i in range(min(500, len(message.samples))):
        print(f'Message Samples = {message.samples[i]} and Timestamp = {message.timestamps[i]}')

# Export to CSV format
# mdf.export(fmt='csv', filename='tesla/output_tesla_1.csv')

# reading the CSV file
# csvFile = pd.read_csv('hyundai/output_hyundai.ChannelGroup_0.csv')

# displaying the contents of the CSV file
# print(csvFile.to_string())

# print("MDF file converted to CSV successfully.")

df = pd.read_csv('tesla/output_tesla_1.ChannelGroup_0.csv')
print(df)


# Split DataFrame into chunks (adjust chunk size as needed)

# chunk_size = 1040000
# chunks = [df[i:i+chunk_size] for i in range(0, df.shape[0], chunk_size)]
#
# # Create an Excel writer
#
# output_excel_filename = 'tesla/output_tesla.xlsx'
# with pd.ExcelWriter(output_excel_filename) as writer:
#     for i, chunk in enumerate(chunks, start=1):
#         sheet_name = f'Sheet_{i}'
#         chunk.to_excel(writer, sheet_name=sheet_name, index=False)

