#!/bin/ruby
require 'open-uri'

def crop(src, dst, size)
  cmd = "convert #{src} -resize #{size}x#{size}^ -gravity Center -extent #{size}x#{size} #{dst}"
  system(cmd)
end

src_dir = ARGV[0].to_s
dst_dir = ARGV[1].to_s
size = ARGV[2].to_i
if src_dir.empty? || dst_dir.empty? || size == 0
  puts 'Usage: ruby scripts/crop_photos.rb <input dir> <output dir> <size>'
  exit 1
end

Dir.glob("#{src_dir}/*.jpeg").each.with_index do |path, i|
  puts i
  name = File.basename(path)
  crop(path, "#{dst_dir}/#{name}", size)
end
