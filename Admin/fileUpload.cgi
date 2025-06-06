#!/usr/bin/ruby
#File: fileUpload.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#   This is a cgi that allows you to upload a csv and it will populate automagically
#   This is similar to the Upload and populate works but we do not have to have the keys since those 
#   are already choosen.
#
#   Finding last id method: https://stackoverflow.com/questions/7201359/get-last-inserted-id-using-mysql2-gem accessed 4/9
#   gsub to escape special charachters https://stackoverflow.com/questions/63654536/what-exactly-is-gsub-in-ruby accessed 4/9
#       since sql escapes single quotes with double quotes I globabal sub them anytime I see them 
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

#connect to the html file
cgi = CGI.new("html5")
fromFile = cgi.params['fileName'].first
originalName = cgi.params['fileName'].first.instance_variable_get("@original_filename")

#Get the file info and store it in a local dir on the file server 
uploadLocation = "/NFSHome/jholt/public_html/Finally/uploads/"
toFile = uploadLocation + originalName 
File.open(toFile.untaint, 'w') { |file| file << fromFile.read}
fileData = IO.readlines(toFile)
#drop attribute names
fileData = fileData.drop(1)

#error catch the sql
begin
    #add data to the table 
    fileData.each do |data|
        tupple = data.split("|")
        #check if age is empty 
        if tupple[7] == ""
            tupple[7] = "NULL"
        end
        db.query("INSERT INTO passenger_info (Fname, Lname, UnmarriedName, Honorific, Age, Gender, Sibling_Spouses, Parents_Kids)VALUES ('#{tupple[3].gsub("'", "''")}', '#{tupple[4].gsub("'", "''")}', '#{tupple[5].gsub("'", "''")}','#{tupple[2]}',#{tupple[7]}, '#{tupple[6]}',#{tupple[8]}, #{tupple[9]});")
        #get the foreign key for other tables
        id = db.last_id
        db.query("INSERT INTO survival_info (id, survived)VALUES (#{id}, #{tupple[0]})")
        db.query("INSERT INTO journey_info (id, ticket_no, class, embark, fare)VALUES (#{id}, '#{tupple[10]}', '#{tupple[1]}', '#{tupple[13]}', #{tupple[11]})")
        #check if cabin is null
        if tupple[12] != ""
            cabins = tupple[12].split(" ")
            cabins.each do |cabinNo|
                db.query("INSERT INTO cabin_info (id, cabin_no)VALUE (#{id}, '#{cabinNo}')")
            end 
        end
    end
    #display success
    puts "<html>"
            puts "<head>"
                puts "<meta http-equiv='refresh' content='10; url=fileUpload.html'>"
                puts "<title>Mass Insert</title>"
                puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
            puts "</head>"
            puts "<body>"
                puts "<a href='index.html'>&larr; Back</a>"
                puts "<h1>Insert Complete</h1>"
            puts "</body>"
    puts "</html>"
#display failure
rescue 
    puts "<html>"
        puts "<head>"
            puts "<meta http-equiv='refresh' content='10; url=fileUpload.html'>"
            puts "<title>Mass Insert Error</title>"
            puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
        puts "</head>"
        puts "<body>"
            puts "<a href='index.html'>&larr; Back</a>"
            puts "<h1>Insert Failed</h1>"
            puts "<p>Unfortunaltley some of the parameters you entered were not valid</p>"
        puts "</body>"
    puts "</html>"
end