import os
import sys

# -----------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------
OUTPUT_FILE = "transactions2024_12.sql"
ROW_CAP = 500      # Maximum VALUES rows per batch
# -----------------------------------------------------------


def extract_header_and_values(line):
    """
    Splits an INSERT line into header and values.
    Example:
        INSERT INTO `Transactions` (...) VALUES (0,'...',1);
    Returns:
        header: INSERT INTO `Transactions` (...) VALUES
        values: (0,'...',1)
    """
    line = line.strip().rstrip(";")
    header_part, values_part = line.split("VALUES", 1)

    header = header_part.strip() + " VALUES"
    values = values_part.strip()

    return header, values


def write_batch(out, header, values_list):
    """Writes a completed batch to the output file."""
    if not values_list:
        return

    out.write(header + "\n")

    for i, val in enumerate(values_list):
        if i < len(values_list) - 1:
            out.write(val + ",\n")
        else:
            out.write(val + ";\n\n")  # end batch

    
def process_table(lines, table_keyword, out):
    """
    Processes a table's INSERT statements by:
      - preserving original order
      - creating a new batch when header changes
      - creating a new batch when row count reaches ROW_CAP
    """
    table_lines = [l for l in lines if l.startswith(table_keyword)]
    print(f"Processing {table_keyword}: {len(table_lines)} rows found")

    if not table_lines:
        return

    current_header = None
    current_values = []

    for line in table_lines:
        header, values = extract_header_and_values(line)

        header_changed = (current_header is not None and header != current_header)
        cap_reached = (len(current_values) >= ROW_CAP)

        # If header changes OR row cap reached → end current batch
        if header_changed or cap_reached:
            write_batch(out, current_header, current_values)
            current_values = []

        current_header = header
        current_values.append(values)

    # Write remaining values
    write_batch(out, current_header, current_values)


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_sql.py <input_file.sql>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    print("Reading:", input_file)

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        # Most important: preserve original line order
        lines = [line.strip() for line in f if line.strip()]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Important: Transactions FIRST, in exact order
        process_table(lines, "INSERT INTO `Transactions`", out)

        # Then TransactionItems, also preserving order
        process_table(lines, "INSERT INTO `TransactionItems`", out)

    print(f"\nDONE — Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
