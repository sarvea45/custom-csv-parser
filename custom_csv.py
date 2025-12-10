class CustomCsvReader:
    """
    A custom CSV reader implemented as a streaming iterator.
    Handles quoted fields, escaped quotes (""), and embedded newlines.
    """
    def __init__(self, file_handle, delimiter=',', quotechar='"'):
        self.file = file_handle
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.in_quotes = False
    
    def __iter__(self):
        return self

    def _read_char(self):
        """Reads one character and handles EOF."""
        char = self.file.read(1)
        if not char:
            raise StopIteration
        return char

    def __next__(self):
        """Parses and returns the next row (list of fields)."""
        row = []
        current_field = ""
        self.in_quotes = False 

        while True:
            try:
                char = self._read_char()
            except StopIteration:
                # If EOF is hit, return the last non-empty field/row
                if row or current_field:
                    row.append(current_field)
                    return row
                raise

            # === State Machine Logic ===
            if self.in_quotes:
                if char == self.quotechar:
                    # Look ahead for escaped quote ("")
                    next_char = self.file.read(1)
                    if next_char == self.quotechar:
                        # Escaped quote: "" -> append single "
                        current_field += self.quotechar
                    else:
                        # End of quoted field. Put the lookahead char back and change state
                        self.in_quotes = False
                        if next_char:
                            self.file.seek(self.file.tell() - 1)
                else:
                    # Anything else (including \n) is part of the field
                    current_field += char
            
            else: # State: Not in Quotes
                if char == self.delimiter:
                    # Delimiter: End field
                    row.append(current_field)
                    current_field = ""
                elif char == self.quotechar:
                    # Start of a quoted field (only if field is currently empty)
                    if not current_field.strip():
                        self.in_quotes = True
                    else:
                        # Treat quote as literal if not at field start (malformed CSV)
                        current_field += char
                elif char == '\n' or char == '\r':
                    # Newline: End row
                    if char == '\r': # Handle Windows \r\n
                        next_char = self.file.read(1)
                        if next_char != '\n':
                            self.file.seek(self.file.tell() - 1)
                    
                    row.append(current_field)
                    # Return if a non-empty row was parsed
                    if row and any(field for field in row):
                        return row
                    else:
                        # Skip blank lines (reset)
                        current_field = ""
                        row = []
                else:
                    # Standard character
                    current_field += char


class CustomCsvWriter:
    """
    A custom CSV writer that handles necessary quoting and escaping.
    """
    def __init__(self, file_handle, delimiter=',', quotechar='"'):
        self.file = file_handle
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.newline = '\n'

    def _process_field(self, field):
        """Escapes internal quotes and adds external quotes if necessary."""
        field_str = str(field)
        
        # 1. Check if quoting is REQUIRED (contains delimiter, quotechar, or newline)
        needs_quoting = any(char in field_str for char in (self.delimiter, self.quotechar, self.newline))

        if needs_quoting:
            # 2. Escape: Replace internal " with ""
            escaped_field = field_str.replace(self.quotechar, self.quotechar * 2)
            
            # 3. Quote: Wrap the escaped string in quotes
            return f"{self.quotechar}{escaped_field}{self.quotechar}"
        else:
            return field_str

    def writerow(self, row):
        """Writes a single row (list of strings) to the file."""
        processed_fields = [self._process_field(field) for field in row]
        line = self.delimiter.join(processed_fields)
        self.file.write(line + self.newline)

    def writerows(self, rows):
        """Writes multiple rows."""
        for row in rows:
            self.writerow(row)