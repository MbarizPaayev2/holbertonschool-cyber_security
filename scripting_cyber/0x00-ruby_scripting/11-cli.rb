#!/usr/bin/env ruby
require 'optparse'

TASKS_FILE = 'tasks.txt' unless defined?(TASKS_FILE)

def load_tasks
  File.exist?(TASKS_FILE) ? File.readlines(TASKS_FILE, chomp: true) : []
end

def save_tasks(tasks)
  File.write(TASKS_FILE, tasks.join("\n") + (tasks.empty? ? '' : "\n"))
end

def add_task(task)
  tasks = load_tasks
  tasks << task
  save_tasks(tasks)
  puts "Task '#{task}' added."
end

def list_tasks
  tasks = load_tasks
  if tasks.empty?
    puts 'No tasks found.'
  else
    puts 'Tasks:'
    tasks.each_with_index { |task, i| puts "#{i + 1}. #{task}" }
  end
end

def remove_task(index)
  tasks = load_tasks
  idx = index.to_i - 1
  if idx < 0 || idx >= tasks.length
    puts 'Invalid task index.'
  else
    removed = tasks.delete_at(idx)
    save_tasks(tasks)
    puts "Task '#{removed}' removed."
  end
end

options = {}
parser = OptionParser.new do |opts|
  opts.banner = 'Usage: cli.rb [options]'

  opts.on('-a', '--add TASK', 'Add a new task')          { |task| options[:add] = task }
  opts.on('-l', '--list', 'List all tasks')               { options[:list] = true }
  opts.on('-r', '--remove INDEX', 'Remove a task by index') { |i| options[:remove] = i }
  opts.on('-h', '--help', 'Show help')                   { puts opts; exit }
end

parser.parse!

if options[:add]
  add_task(options[:add])
elsif options[:list]
  list_tasks
elsif options[:remove]
  remove_task(options[:remove])
else
  puts parser
end
