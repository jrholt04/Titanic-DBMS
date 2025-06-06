#!/usr/bin/ruby
#File: update.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#   This is the main page for collecting the data for the updating of a row 
#
#   Left Join: https://stackoverflow.com/questions/6279620/join-if-exists-in-a-mysql-query accessed 4/7
#       This is useful for the cabin because it will only join if their exists a match. This was an issue 
#       I was running into with the cabin selection. 
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

#get the rows in the db 
data = db.query("Select * from passenger_info;")

#get info from html forms
cgi = CGI.new("html5")
pId = cgi['pId']

#after we selected a user
if pId != ""
    #query to join on the id's 
    passengerData = db.query("SELECT 
    p.id,
    Fname,
    Lname,
    Honorific,
    UnmarriedName,
    Gender,
    age,
    Sibling_Spouses,
    Parents_Kids,
    survived,
    ticket_no,
    class,
    embark,
    fare,
    cabin_no
    FROM (
        passenger_info AS p 
        JOIN journey_info AS j ON p.id = j.id
        JOIN survival_info AS s ON p.id = s.id
        LEFT JOIN cabin_info AS c ON p.id = c.id
    )
    WHERE p.id = #{pId};")

    #display the options for an updating
    puts "<html>"
    puts "<head>"
        puts "<title>Update an Entry</title>"
        puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
    puts "</head>"
    puts "<body>"
        puts "<a href='update.cgi'>&larr; Back</a>"
        puts "<h1>Here is what to update</h1>"
        # table for all the passengers and what you can delete
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
                    puts "<th>Survived</th>"
                    puts "<th>Ticket #</th>"
                    puts "<th>Class</th>"
                    puts "<th>Embarked From</th>"
                    puts "<th>Fare</th>"
                    puts "<th>Cabin #</th>"
                puts "</tr>"
            puts "</thead>"
            passengerData.each do |data|
                puts"<tr>"
                    puts "<td>#{data['id']}</td>"
                    puts "<td>#{data['Fname']}</td>"
                    puts "<td>#{data['Lname']}</td>"
                    puts "<td>#{data['UnmarriedName']}</td>"
                    puts "<td>#{data['Honorific']}</td>"
                    puts "<td>#{data['Gender']}</td>"
                    puts "<td>#{data['age']}</td>"
                    puts "<td>#{data['Sibling_Spouses']}</td>"
                    puts "<td>#{data['Parents_Kids']}</td>"
                    if data['survived'] == 0 
                        puts "<td>False</td>"
                    end 
                    if data['survived'] == 1 
                        puts "<td>True</td>"
                    end 
                    puts "<td>#{data['ticket_no']}</td>"
                    puts "<td>#{data['class']}</td>"
                    puts "<td>#{data['embark']}</td>"
                    puts "<td>#{data['fare'].to_f}</td>"
                    puts "<td>#{data['cabin_no']}</td>"
                puts "</tr>"
            end
        puts "</table>"

        #all of the options for updating or adding information
        puts "<form enctype='multipart/form-data' action='updateLogic.cgi' method='post'>"
            puts "<p>Update</p>"
            puts "<input type='text' name='firstName' placeholder='First Name'><br>"
            puts "<input type='text' name='lastName' placeholder='Last Name'><br>"
            puts "<input type='text' name='unmarriedName' placeholder='Unmarried Name'><br>"
            puts "<input type='text' name='honorific' placeholder='Honorific'><br>"
            puts "<input type='text' name='age' placeholder='Age'><br>"
            puts "<input type='text' name='gender' placeholder='Gender'><br>"
            puts "<input type='text' name='siblingSpouse' placeholder='Siblings/Spouses'><br>"
            puts "<input type='text' name='parentsKids' placeholder='Parents/Kids'><br>"
            puts "<input type='text' name='ticketNo' placeholder='Ticket #'><br>"
            puts "<input type='text' name='class' placeholder='Class'><br>"
            puts "<input type='text' name='embark' placeholder='Embark From'><br>"
            puts "<input type='text' name='fare' placeholder='Fare'><br>"
            puts "<input type='text' name='survived' placeholder='Survived'><br>"
            puts "<input type='text' name='cabin' placeholder='Cabin'><br>"
            puts "<input type='hidden' id='pId' name='pId' value='#{pId}'>"
            puts "<input type='submit' value='submit' >"
        puts "</form>"
    puts "</body>"
    puts "</html>"

#before selection 
else 
    puts "<html>"
            puts "<head>"
                puts "<title>Update an Entry</title>"
                puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
            puts "</head>"
            puts "<body>"
                puts "<a href='index.html'>&larr; Back</a>"
                puts "<h1>Select a Row to Update</h1>"
                #display all the possible options to delete soemones information
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
                            puts "<th></th>"
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
                                puts "<form class='button' action='update.cgi' method='post'></input>"
                                    puts "<input type='hidden' id='pId' name='pId' value='#{d['id']}'>"
                                    puts "<input type='submit' value='update'>"
                                puts "</form>"
                            puts "</td>"
                        puts "</tr>"
                    
                    end 
                puts "</table>"
            puts "</body>"
    puts "</html>"
end 