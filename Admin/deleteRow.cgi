#!/usr/bin/ruby
#File: deleteRow.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#   allows you to delete one new single row on the db
#   You can find a row and select delete and poof that data is gone
#
$stdout.sync = true 
$stderr.reopen $stdout 

print "Content-type: text/html\n\n"

require 'mysql2'
require 'cgi'
require 'stringio'

db = Mysql2::Client.new(
    :host=>'10.20.3.4',
    :username=>'dbms_jho',
    :password=>'jho_26_england',
    :database=>'dbms_jho_dbA'
    )
#get info from html forms
cgi = CGI.new("html5")
pId = cgi['pId']

#if the id is not empty delete it.
if pId != ""
    db.query("DELETE FROM journey_info WHERE id = #{pId.to_i};")
    db.query("DELETE FROM survival_info WHERE id = #{pId.to_i};")
    db.query("DELETE FROM cabin_info WHERE id = #{pId.to_i};")
    db.query("DELETE FROM passenger_info WHERE id = #{pId.to_i};")
end

#get the rows in the db 
data = db.query("Select * from passenger_info;")

puts "<html>"
        puts "<head>"
            puts "<title>Single Delete</title>"
            puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
        puts "</head>"
        puts "<body>"
            puts "<a href='index.html'>&larr; Back</a>"
            puts "<h1>Select a Row to delete</h1>"
            puts "<table>"
                puts "<thead>"
                    puts "<tr>"
                        puts "<th>ID</th>"
                        puts "<th>First Name</th>"
                        puts "<th>Last Name</th>"
                        puts "<th>Unmarried Name</th>"
                        puts "<th>Honorific</th>"
                        puts "<th>Gender</th>"
                        puts "<th>Age</th>"
                        puts "<th>Siblings/Spouses</th>"
                        puts "<th>Parents/Kids</th>"
                        puts "<th>Delete</th>"
                    puts "</tr>"
                puts "</thead>"
                data.each do |d| 
                    
                    puts "<tr>"
                        puts "<td>#{d['id']}</td>"
                        puts "<td>#{d['Fname']}</td>"
                        puts "<td>#{d['Lname']}</td>"
                        puts "<td>#{d['UnmarriedName']}</td>"
                        puts "<td>#{d['Honorific']}</td>"
                        puts "<td>#{d['Gender']}</td>"
                        puts "<td>#{d['age']}</td>"
                        puts "<td>#{d['Sibling_Spouses']}</td>"
                        puts "<td>#{d['Parents_Kids']}</td>"
                        puts "<td>"
                            puts "<form class='button' action='deleteRow.cgi' method='post'>"
                                puts "<input type='hidden' id='pId' name='pId' value='#{d['id']}'>"
                                puts "<input type='submit' value='remove'>"
                            puts "</form>"
                        puts "</td>"
                    puts "</tr>"
                   
                end 
            puts "</table>"
        puts "</body>"
puts "</html>"