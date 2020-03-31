# Use the rows variable from cleaned_rows.py
rows = [['URL', 'Short title', 'Type', 'Status', 'Parties', 'Date of signature', 'Date of entry into force', 'Termination date', 'Text URL'],['/international-investment-agreements/treaties/bit/1/afghanistan---germany-bit-2005-', 'Afghanistan - Germany BIT (2005)', 'BITs', 'In force', 'Afghanistan, Germany', '20/04/2005', '12/10/2007', '', 'Full text: en']]
base = 'https://investmentpolicy.unctad.org'

def format_rows(rows):
    table = ''
    for i, row in enumerate(rows, start=1):
        table += f"""<tr>
        <td class="id">{ i }</td>
        <td class="url"><a href="{ base + row[0] }">url</a></td>
        <td class="short-title">{ row[1] }</td>
        <td class="type">{ row[2] }</td>
        <td class="status">{ row[3] }</td>
        <td class="parties">{ row[4] }</td>
        <td class="signature">{ row[5] }</td>
        <td class="entry">{ row[6] }</td>
        <td class="termination">{ row[7] }</td>
        </tr>\n"""
    return table

with open('rows.html', 'w') as f:
    f.write(format_rows(rows))
print('Done.')