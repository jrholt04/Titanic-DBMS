#!/usr/bin/ruby
#File: massDelete.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
# 
#       Create a page that allows you to delete things based on the conditions
#       Similar to search but all the entries that meet the conditioin will be deleted
#
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

#strings to generate query
selectClause = ""
whereClause = ""
columnNames = []

#where fields 
firstName = cgi['firstName']
if firstName != ""
    whereClause += " Fname #{firstName} AND"
end
lastName = cgi['lastName']
if lastName != ""
    whereClause += " Lname #{lastName} AND"
end
unmarriedName = cgi['unmarriedName']
if unmarriedName != ""
    whereClause += " unmarriedName #{unmarriedName} AND"
end
honorific = cgi['honorific']
if honorific != ""
    whereClause += " honorific #{honorific} AND"
end
age = cgi ['age']
if age != ""
    whereClause += " age #{age} AND"
end
gender = cgi['gender']
if gender != ""
    whereClause += " Gender #{gender} AND"
end
siblingSpouse = cgi ['siblingSpouse']
if siblingSpouse != ""
    whereClause += " siblingSpouse #{siblingSpouse} AND"
end
parentsKids = cgi['parentsKids']
if parentsKids != ""
    whereClause += " parentsKids #{parentsKids} AND"
end
ticketNo = cgi['ticketNo']
if ticketNo != ""
    whereClause += " ticket_no #{ticketNo} AND"
end
cabinClass = cgi['class']
if cabinClass != ""
    whereClause += " class #{cabinClass} AND"
end
embark = cgi['embark']
if embark != ""
    whereClause += " embark #{embark} AND"
end
fare = cgi['fare']
if fare != ""
    whereClause += " fare #{fare} AND"
end
survived = cgi['survived']
if survived != ""
    whereClause += " survived #{survived} AND"
end
cabin = cgi['cabin']
if cabin != ""
    whereClause += " cabin_no #{cabin} AND"
end

#checks if form was submitted 
submitted = cgi['submitFlag']

if submitted != ""
    
end

puts "<html>"
    puts "<head>"
        puts "<title>Delete</title>"
        puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
    puts "</head>"
    puts "<body>"
        # go back to index if we are lookng at delete fields
        if submitted != "True"
            puts "<a href='index.html'>&larr; Back</a>"
        #go back to delete fields if we are looking at a confirmed delete
        else 
            puts "<a href='massDelete.cgi'>&larr; Back</a>"
        end 
        puts "<h1>What Are We Deleting?</h1>"
        #if the form hasn't been submited give them the delete fields
        if submitted != "True"
            puts "<form enctype='multipart/form-data' action='massDelete.cgi' method='post'>"
                puts "<p>Delete According Too: </p>"
                #rules for deleting
                puts "<p>Rules:</p>"
                puts "<p>words on the right sid of conditions should be in quotes(single): 'example'</p>"
                puts "<p>Survive can either be True or False</p>"
                puts "<p>Conditional Options: </p>"
                puts "<p> = Equal </p>"
                puts "<p> <> Not Equal </p>"
                puts "<p> > Greater than </p>"
                puts "<p> < less than </p>"
                puts "<p> >= Greater or Equal</p>"
                puts "<p> <= Less or Equal</p>"
                puts "<p> IS NULL or IS NOT NULL(no quotes needed)</p>"
                puts "<p>BETWEEN X AND Y Range</p>"
                puts "<p>Examples:</p>"
                puts "<p> >= 42</p>"
                puts "<p> = 'Cherbourg'</p>"
                puts "<p>BETWEEN 68 AND 88</p>"
                puts "<p> IS NULL</p>"
                puts "<p> = True</p>"
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
                puts "<input type='hidden' id='submitFlag' name='submitFlag' value='True'required><br>" 
                puts "<input type='submit' value='submit' >"
                puts "<p>#{submitted}</p>"
            puts "</form>"
        #present the data from the search
        else 
            begin 
                #get rid of the last and and the extra , 
                whereClause = whereClause.chop
                whereClause = whereClause.chop
                whereClause = whereClause.chop
                selectClause = selectClause.chop
                ids = db.query("
                    SELECT passenger_info.id
                    FROM passenger_info
                    JOIN journey_info ON passenger_info.id = journey_info.id
                    JOIN survival_info ON passenger_info.id = survival_info.id
                    LEFT JOIN cabin_info ON passenger_info.id = cabin_info.id
                    WHERE
                    #{whereClause};
                    ")
                #delete all entries where the id matches 
                ids.each do |id|
                    db.query("DELETE FROM journey_info WHERE id = #{id['id']};")
                    db.query("DELETE FROM survival_info WHERE id = #{id['id']};")
                    db.query("DELETE FROM cabin_info WHERE id = #{id['id']};")
                    db.query("DELETE FROM passenger_info WHERE id = #{id['id']};")
                end
                puts "<h1>Deleted</h1>"
            rescue 
                puts "<h1>invalid</h1>"
                puts "<p>Unfortunaltley some of the parameters you entered were not valid</p>"
            end
        end
    puts "</body>"
puts "</html>"