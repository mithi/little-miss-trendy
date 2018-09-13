require 'csv'
require 'find'

csv_file_paths = []

# Parent directory where CSVs are stored
PARENT_DIR="./racing-logs/"

# Full path to the output CSV file
OUTPUT_FILE="./samples/logs-v2.csv"

Find.find(PARENT_DIR) do |path|
  csv_file_paths << path if path =~ /.*\.csv$/
end

CSV.open(OUTPUT_FILE, "w") do |csv|
  csv_file_paths.each do |path|
    CSV.foreach(path) do |row|
      # Requirements:
      # 1. Get first column which contains a path, and only keep filename with extension.
      # 2. Get second column as it is.
      # 3. Ignore the rest of the data.
      filename = File.basename(row[0])
      steering = row[1]

      csv << [filename, steering]
    end
  end
end
