require 'open-uri'
require 'uri'
require 'fileutils'

if ARGV.length != 2
  puts 'Usage: 9-download_file.rb URL LOCAL_FILE_PATH'
  exit
end

url        = ARGV[0]
local_path = ARGV[1]

puts "Downloading file from #{url}..."

FileUtils.mkdir_p(File.dirname(local_path))

URI.open(url, 'rb') do |remote_file|
  File.open(local_path, 'wb') { |local_file| local_file.write(remote_file.read) }
end

puts "File downloaded and saved to #{local_path}."
