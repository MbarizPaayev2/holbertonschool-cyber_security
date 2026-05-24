require 'json'

def count_user_ids(file_path)
  data = JSON.parse(File.read(file_path))

  counts = Hash.new(0)
  data.each { |entry| counts[entry['userId']] += 1 }

  counts.sort.each { |user_id, count| puts "#{user_id}: #{count}" }
end
