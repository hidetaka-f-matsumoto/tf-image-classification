#!/bin/ruby
require 'csv'
require 'open-uri'

def download(url, output_path)
  open(output_path, 'w') do |f|
    open(url) do |data|
      f.write(data.read)
    end
  end
rescue => e
  puts e
end

src_file = ARGV[0].to_s
dst_dir = ARGV[1].to_s
number = ARGV[2].to_i
if src_file.empty? || dst_dir.empty?
  puts 'Usage: ruby scripts/download_photos.rb <input csv> <output dir> <number>'
  exit 1
end

CSV.table(src_file).to_a.drop(1).shuffle.slice(0, number).each.with_index do |row, i|
  puts "#{i}/#{number}"
  id = row[0]
  url = row[3]
  dst_path = "#{dst_dir}/#{id}.jpeg"
  download(url, dst_path)
end
