#!/bin/ruby
require 'csv'

src_dir = ARGV[0].to_s
dst_path = ARGV[1].to_s
project_name = ARGV[2].to_s
gcs_bucket = ARGV[3].to_s
if src_dir.empty? || dst_path.empty? || project_name.empty? || gcs_url.empty?
  puts 'Usage: ruby scripts/make_automl_vision_csv.rb <input dir> <output path> <project name> <gcs bucket>'
  exit 1
end

CSV.open(dst_path, 'w', force_quotes: true) do |csv|
  Dir.glob("#{src_dir}/**/*.jpeg").map do |path|
    file_name = File.basename(path)
    label = File.dirname(path).split('/').last
    gcs_path = "#{gcs_bucket}/#{project_name}/dataset/#{label}/#{file_name}"
    csv << [gcs_path, label]
  end
end
