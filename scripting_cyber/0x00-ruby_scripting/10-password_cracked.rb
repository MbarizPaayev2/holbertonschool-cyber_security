
require 'digest'

if ARGV.length != 2
  puts 'Usage: 10-password_cracked.rb HASHED_PASSWORD DICTIONARY_FILE'
  exit
end

hashed_password = ARGV[0]
dictionary_file = ARGV[1]

cracked = nil

File.foreach(dictionary_file) do |word|
  word = word.chomp
  if Digest::SHA256.hexdigest(word) == hashed_password
    cracked = word
    break
  end
end

if cracked
  puts "Password found: #{cracked}"
else
  puts 'Password not found in dictionary.'
end
