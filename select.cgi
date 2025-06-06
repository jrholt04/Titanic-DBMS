#!/usr/bin/ruby
#File: select.cgi
#Jackson Holt, Transy U
#Dr. Moorman CS3114
#
# 
#       Create a page that allows you to search and view items in the db  
#       the user can type in the search field and select what result fields they would like 
#
#       chop: https://how.dev/answers/removing-the-last-character-of-a-string-in-ruby accessed 4/8
#       adding things to an array:  https://ruby-doc.org/core-2.5.8/Array.html#:~:text=Adding%20Items%20to%20Arrays%C2%B6%20%E2%86%91&text=unshift%20will%20add%20a%20new%20item%20to%20the%20beginning%20of%20an%20array.&text=With%20insert%20you%20can%20add,an%20array%20at%20any%20position accessed 4/8
#       Adding error catching for sql: https://stackoverflow.com/questions/2191632/begin-rescue-and-ensure-in-ruby
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

#where fields. generates where part of the query
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

#result fields and creating the column names array
firstNameR = cgi['firstNameR']
if firstNameR == "Fname"
    selectClause += "#{firstNameR},"
    columnNames.push(firstNameR)
end
lastNameR = cgi['lastNameR']
if lastNameR == "Lname"
    selectClause += "#{lastNameR},"
    columnNames.push(lastNameR)
end
unmarriedNameR = cgi['unmarriedNameR']
if unmarriedNameR == "UnmarriedName"
    selectClause += "#{unmarriedNameR},"
    columnNames.push(unmarriedNameR)
end
honorificR = cgi['honorificR']
if honorificR == "Honorific"
    selectClause += "#{honorificR},"
    columnNames.push(honorificR)
end
ageR = cgi ['ageR']
if ageR == "age"
    selectClause += "#{ageR},"
    columnNames.push(ageR)
end
genderR = cgi['genderR']
if genderR == "Gender"
    selectClause += "#{genderR},"
    columnNames.push(genderR)
end
siblingSpouseR = cgi ['siblingSpouseR']
if siblingSpouseR == "Sibling_Spouses"
    selectClause += "#{siblingSpouseR},"
    columnNames.push(siblingSpouseR)
end
parentsKidsR = cgi['parentsKidsR']
if parentsKidsR == "Parents_Kids"
    selectClause += "#{parentsKidsR},"
    columnNames.push(parentsKidsR)
end
ticketNoR = cgi['ticketNoR']
if ticketNoR == "ticket_no"
    selectClause += "#{ticketNoR},"
    columnNames.push(ticketNoR)
end
cabinClassR = cgi['classR']
if cabinClassR == "class"
    selectClause += "#{cabinClassR},"
    columnNames.push(cabinClassR)
end
embarkR = cgi['embarkR']
if embarkR == "embark"
    selectClause += "#{embarkR},"
    columnNames.push(embarkR)
end
fareR = cgi['fareR']
if fareR == "fare"
    selectClause += "#{fareR},"
    columnNames.push(fareR)
end
survivedR = cgi['survivedR']
if survivedR == "survived"
    selectClause += "#{survivedR},"
    columnNames.push(survivedR)
end
cabinR = cgi['cabinR']
if cabinR == "cabin_no"
    selectClause += "#{cabinR},"
    columnNames.push(cabinR)
end

#checks if form was submitted 
submitted = cgi['submitFlag']

#show the selection options 
puts "<html>"
    puts "<head>"
        puts "<title>Search</title>"
        puts "<link rel='stylesheet' href='DatabaseManagerStyles.css'>"
    puts "</head>"
    puts "<body>"
        if submitted != "True"
            puts "<a href='index.html'>&larr; Back</a>"
            puts "<h1>What are you searching for?</h1>"
            puts "<form enctype='multipart/form-data' action='select.cgi' method='post'>"
                #rules for searching
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
                #what are the fields you want returned from your search
                puts "<p>Looking For: </p>"
                puts "<input type='checkbox' name='firstNameR' value='Fname'>First Name<br>"
                puts "<input type='checkbox' name='lastNameR' value='Lname'>Last Name<br>"
                puts "<input type='checkbox' name='unmarriedNameR' value='UnmarriedName'>Unmarried Name<br>"
                puts "<input type='checkbox' name='honorificR' value='Honorific'>Honorific<br>"
                puts "<input type='checkbox' name='ageR' value='age'>Age<br>"
                puts "<input type='checkbox' name='genderR' value='Gender'>gender<br>"
                puts "<input type='checkbox' name='siblingSpouseR' value='Sibling_Spouses'>Siblings/Spouse<br>"
                puts "<input type='checkbox' name='parentsKidsR' value='Parents_Kids'>Parents/Kids<br>"
                puts "<input type='checkbox' name='ticketNoR' value='ticket_no'>Ticket Number<br>"
                puts "<input type='checkbox' name='classR' value='class'>Class<br>"
                puts "<input type='checkbox' name='embarkR' value='embark'>Embark<br>"
                puts "<input type='checkbox' name='fareR' value='fare'>Fare<br>"
                puts "<input type='checkbox' name='survivedR' value='survived'>Survived<br>"
                puts "<input type='checkbox' name='cabinR' value='cabin_no'>Cabin(s)<br>"
                puts "<p>Searching by:</p>"
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
        #if the form was submited present the data from the search
        else 
            #get rid of the last and and the extra , 
            whereClause = whereClause.chop
            whereClause = whereClause.chop
            whereClause = whereClause.chop
            selectClause = selectClause.chop
            
            #error catch bad sql
            begin
                results = db.query("
                    SELECT #{selectClause}
                    FROM passenger_info
                    JOIN journey_info ON passenger_info.id = journey_info.id
                    JOIN survival_info ON passenger_info.id = survival_info.id
                    LEFT JOIN cabin_info ON passenger_info.id = cabin_info.id
                    WHERE
                    #{whereClause};
                    ")
                
                #if the query is valid display results
                puts "<a href='select.cgi'>&larr; Back</a>"
                puts "<h1>Passenger Info</h1>"
                puts "<table>"
                    puts "<thead>"
                        puts "<tr>"
                        columnNames.each do |c|
                            puts "<th>#{c}</th>"
                        end
                        puts "</tr>"
                    puts "</thead>"
                    results.each do |d|  
                        puts "<tr>"
                        columnNames.each do |c|
                            puts "<td>" + d["#{c}"].to_s + "</td>"
                        end
                        puts "</tr>"
                    end 
                puts "</table>"
            rescue
                puts "<a href='select.cgi'>&larr; Back</a>"
                puts "<h1>invalid</h1>"
                puts "<p>Unfortunaltley some of the parameters you entered were not valid</p>"
            end  
        end 
    puts "</body>"
puts "</html>"