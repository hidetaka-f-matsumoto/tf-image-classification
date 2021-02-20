#!/bin/ruby
require 'fileutils'

src_dir = ARGV[0].to_s
dst_parent_dir = ARGV[1].to_s
label = ARGV[2].to_s
sizes = ARGV[3].to_s.split(',').map(&:to_i)
if src_dir.empty? || dst_parent_dir.empty? || label.empty? || sizes.empty?
  puts 'Usage: ruby scripts/distribute_dataset.rb <input dir> <output dir> <label> <sizes>'
  exit 1
end

src_files = Dir.glob("#{src_dir}/*.jpeg").shuffle
['train', 'validation', 'test'].zip(sizes).each do |dst_subdir, size|
  dst_dir = "#{dst_parent_dir}/#{dst_subdir}/#{label}"
  FileUtils.mkdir_p(dst_dir)
  src_files.shift(size).each do |path|
    name = File.basename(path)
    dst_path = "#{dst_dir}/#{name}"
    FileUtils.cp(path, dst_path)
  end
end
