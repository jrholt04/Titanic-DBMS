#!/usr/bin/ruby
#File: updateLogic.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
#   after we have collected the update information we pass it to
#   this file and let it update the row in the tables 
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
pId = cgi['pId']
firstName = cgi['firstName']
lastName = cgi['lastName']
unmarriedName = cgi['unmarriedName']
honorific = cgi['honorific']
age = cgi ['age']
gender = cgi['gender']
siblingSpouse = cgi ['siblingSpouse']
parentsKids = cgi['parentsKids']
ticketNo = cgi['ticketNo']
cabinClass = cgi['class']
embark = cgi['embark']
fare = cgi['fare']
survived = cgi['survived']
cabin = cgi['cabin']

begin 
    #update passanger 
    survivalUpdates = ""
    if firstName != ""
        db.query("UPDATE passenger_info SET Fname = '#{firstName}' WHERE id = #{pId};")
    end
    if lastName != ""
        db.query("UPDATE passenger_info SET Lname = '#{lastName}' WHERE id = #{pId};")
    end
    if unmarriedName != ""
        db.query("UPDATE passenger_info SET UnmarriedName = '#{unmarriedName}' WHERE id = #{pId};")
    end
    if honorific != ""
        db.query("UPDATE passenger_info SET Honorific = '#{honorific}' WHERE id = #{pId};")
    end
    if age != ""
        db.query("UPDATE passenger_info SET age = #{age} WHERE id = #{pId};")
    end
    if gender != ""
        db.query("UPDATE passenger_info SET Gender = '#{gender}' WHERE id = #{pId};")
    end
    if siblingSpouse != ""
        db.query("UPDATE passenger_info SET  Sibling_Spouses = #{siblingSpouse} WHERE id = #{pId};")
    end
    if parentsKids != ""
        db.query("UPDATE passenger_info SET Parents_Kids = #{parentsKids} WHERE id = #{pId};")
    end

    #update journey
    if ticketNo != ""
        db.query("UPDATE journey_info SET ticket_no = '#{ticketNo}' WHERE id = #{pId};")
    end
    if cabinClass != ""
        db.query("UPDATE journey_info SET class = '#{cabinClass}' WHERE id = #{pId};")
    end
    if embark != ""
        db.query("UPDATE journey_info SET embark = '#{embark}' WHERE id = #{pId};")
    end
    if fare != ""
        db.query("UPDATE journey_info SET fare = #{fare} WHERE id = #{pId};")
    end

    #update cabin 
    if cabin != ""
        db.query("UPDATE cabin_info SET cabin_no = '#{cabin}' WHERE id = #{pId};")
    end

    #update survival
    if survived != ""
        if survived == 1
            db.query("UPDATE survival_info SET survived = True WHERE id = #{pId};")
        end
        if survived == 0
            db.query("UPDATE survival_info SET survived = False WHERE id = #{pId};")
        end
    end

    #displays a success message
    puts "<html>"
            puts "<head>"
                puts "<meta http-equiv='refresh' content='1; url=update.cgi'>"
                puts "<title>Update Complete</title>"
                puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
            puts "</head>"
            puts "<body>"
            puts "<a href='update.cgi'>&larr; Back</a>"
                puts "<h1>Update Complete</h1>" 
            puts "</body>"
    puts "</html>"
rescue 
    puts "<html>"
            puts "<head>"
                puts "<title>Update Failed</title>"
                puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
            puts "</head>"
            puts "<body>"
                puts "<a href='update.cgi'>&larr; Back</a>"
                puts "<h1>invalid</h1>"
                puts "<p>Unfortunaltley some of the parameters you entered were not valid</p>"
            puts "</body>"
    puts "</html>"
end 