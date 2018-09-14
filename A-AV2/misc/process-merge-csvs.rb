require 'csv'
require 'find'

if ARGV.size != 3
  puts "Requires PARENT_DIR, IMAGE_DIR, and OUTPUT_FILE."
  exit
end

csv_file_paths = []

# Parent directory where CSVs are stored
PARENT_DIR=ARGV[0]

# Directory where images are stored
IMG_DIR=ARGV[1]

# Full path to the output CSV file
OUTPUT_FILE=ARGV[2]

Find.find(PARENT_DIR) do |path|
  csv_file_paths << path if path =~ /.*\.csv$/
end

CSV.open(OUTPUT_FILE, "w") do |csv|

  csv << ["NAME", "STEER"]

  csv_file_paths.each do |path|
    CSV.foreach(path) do |row|
      # Requirements:
      # 1. Get first column which contains a path, and only keep filename with extension.
      # 2. Get second column as it is.
      # 3. Ignore the rest of the data.
      filenamepath = IMG_DIR + File.basename(row[0])
      steering = row[1]

      csv << [filenamepath, steering]
    end
  end
end
