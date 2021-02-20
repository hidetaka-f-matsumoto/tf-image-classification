#!/bin/ruby
require 'csv'

test_result = ARGV[0]
grad_cam_dir = ARGV[1]
dst = ARGV[2]
cwd = Dir.getwd

File.open(dst, 'w') do |f|
  f << '<html>'
  f << '<body>'
  f << '<table>'
  f << '<thead>'
  f << '<tr>'
  f << '<th>prediction</th>'
  f << '<th>src</th>'
  f << '<th>grad_cam</th>'
  f << '</tr>'
  f << '</thead>'
  f << '<tbody>'
  CSV.read(test_result).each do |row|
    src_path = "#{cwd}/#{row[0]}"
    prediction = row[1].to_f
    color = prediction >= 0.5 ? 'red' : 'blue'
    grad_cam_path = "#{cwd}/#{grad_cam_dir}/#{File.basename(row[0])}"
    f << '<tr>'
    f << "<td><font size=\"16\" color=\"#{color}\">#{prediction}</font></td>"
    f << "<td><img src=\"#{src_path}\"></td>"
    f << "<td><img src=\"#{grad_cam_path}\"></td>"
    f << '</tr>'
  end
  f << '</tbody'
  f << '</table>'
  f << '</body>'
  f << '</html>'
end
