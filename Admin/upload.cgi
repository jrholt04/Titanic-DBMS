#!/usr/bin/ruby
#File: upload.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#       recives information from the upload.html and populates the table with it
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

#connect to the html file and collect data
#if integers are not present you have to set them to null
cgi = CGI.new("html5")
firstName = cgi['firstName']
lastName = cgi['lastName']
unmarriedName = cgi['unmarriedName']
honorific = cgi['honorific']
age = cgi ['age']
if age == ""
    age = 'NULL'
end
gender = cgi['gender']
siblingSpouse = cgi ['siblingSpouse']
if siblingSpouse == ""
    siblingSpouse = 'NULL'
end
parentsKids = cgi['parentsKids']
if parentsKids == ""
    parentsKids = 'NULL'
end
ticketNo = cgi['ticketNo']
cabinClass = cgi['class']
embark = cgi['embark']
fare = cgi['fare']
if fare == ""
    fare = 'NULL'
end
survived = cgi['survived']
cabin = cgi['cabin']

#error cathcing 
begin 
#add data to their repective tables. using gsub to escape special name characters. 
db.query("INSERT INTO passenger_info (Fname, Lname, UnmarriedName, Honorific, Age, Gender, Sibling_Spouses, Parents_Kids)VALUES ('#{firstName.gsub("'", "''")}', '#{lastName.gsub("'", "''")}', '#{unmarriedName.gsub("'", "''")}','#{honorific}',#{age}, '#{gender}',#{siblingSpouse}, #{parentsKids});")
#get the foreign key for other tables
id = db.last_id
db.query("INSERT INTO survival_info (id, survived)VALUES (#{id}, #{survived})")
db.query("INSERT INTO journey_info (id, ticket_no, class, embark, fare)VALUES (#{id}, '#{ticketNo}', '#{cabinClass}', '#{embark}', #{fare})")
#check if cabin is null
if cabin != ""
    cabins = cabin.split(" ")
    cabins.each do |cabinNo|
        db.query("INSERT INTO cabin_info (id, cabin_no)VALUE (#{id}, '#{cabinNo}')")
    end 
end

#display that insert was sucessful 
puts "<html>"
        puts "<head>"
            puts "<meta http-equiv='refresh' content='10; url=upload.html'>"
            puts "<title>Single Insert</title>"
            puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
        puts "</head>"
        puts "<body>"
            puts "<a href='index.html'>&larr; Back</a>"
            puts "<h1>Insert Complete</h1>"
        puts "</body>"
puts "</html>"

#if the sql fails 
rescue 
    puts "<html>"
        puts "<head>"
            puts "<meta http-equiv='refresh' content='10; url=upload.html'>"
            puts "<title>Single Insert Error</title>"
            puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
        puts "</head>"
        puts "<body>"
            puts "<a href='index.html'>&larr; Back</a>"
            puts "<h1>Insert failed</h1>"
            puts "<p>Unfortunaltley some of the parameters you entered were not valid</p>"
        puts "</body>"
    puts "</html>"
end