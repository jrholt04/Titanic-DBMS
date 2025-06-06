#!/usr/bin/ruby
#File: fullState.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#   shows the current state of all tables
#   This is the version for the admin page
#
#   to float: https://how.dev/answers/what-is-integertof-in-ruby accessed 4/7
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

#get the rows in the db 
pData = db.query("Select * from passenger_info;")
jData = db.query("Select * from journey_info;")
cData = db.query("Select * from cabin_info;")
sData = db.query("Select * from survival_info;")

#display full state of db
puts "<html>"
puts "<head>"
    puts "<title>Full state</title>"
    puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
    puts "</head>"
puts "<body>"
    puts "<a href='index.html'>&larr; Back</a>"
    # Begin scroll container
    puts "<div class='scroll-row'>"
        
        # Passenger Info
        puts "<div class='table-wrapper'>"
            puts "<h1>Passenger Info</h1>"
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
                puts "</tr>"
            puts "</thead>"
            pData.each do |d|  
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
                puts "</tr>"
            end 
            puts "</table>"
        puts "</div>"

        # Journey Info
        puts "<div class='table-wrapper'>"
            puts "<h1>Journey Info</h1>"
            puts "<table>"
            puts "<thead>"
                puts "<tr>"
                puts "<th>ID</th>"
                puts "<th>Ticket #</th>"
                puts "<th>Class</th>"
                puts "<th>Embarked From</th>"
                puts "<th>Fare</th>"
                puts "</tr>"
            puts "</thead>"
                jData.each do |d| 
                    puts "<tr>"
                    puts "<td>#{d['id']}</td>"
                    puts "<td>#{d['ticket_no']}</td>"
                    puts "<td>#{d['class']}</td>"
                    puts "<td>#{d['embark']}</td>"
                    puts "<td>$#{d['fare'].to_f}</td>"
                    puts "</tr>"   
                end 
            puts "</table>"
        puts "</div>"

        # Cabin Info
        puts "<div class='table-wrapper'>"
            puts "<h1>Cabin Info</h1>"
            puts "<table>"
            puts "<thead>"
                puts "<tr>"
                    puts "<th>ID</th>"
                    puts "<th>Cabin #</th>"
                puts "</tr>"
            puts "</thead>"
            cData.each do |d| 
                puts "<tr>"
                    puts "<td>#{d['id']}</td>"
                    puts "<td>#{d['cabin_no']}</td>"
                puts "</tr>"   
            end 
            puts "</table>"
        puts "</div>"

    # Survival Info
        puts "<div class='table-wrapper'>"
            puts "<h1>Survival Info</h1>"
            puts "<table>"
                puts "<thead>"
                    puts "<tr>"
                        puts "<th>ID</th>"
                        puts "<th>Survived</th>"
                    puts "</tr>"
                puts "</thead>"
                sData.each do |d| 
                        puts "<tr>"
                            puts "<td>#{d['id']}</td>"
                            if d['survived'] == 0
                                puts "<td>False</td>"
                            end
                            if d['survived'] == 1
                                puts "<td>True</td>"
                            end
                        puts "</tr>"   
                end 
            puts "</table>"
        puts "</div>"
    # End scroll container
    puts "</div>" 
puts "</body>"
puts "</html>"
