
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work. 
#
#    Student no:   1822441005
#    Student name:  Stan   (吕家伟)
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  POPULARITY CLOUDS
#
#  Movie fans have strong opinions about their favourite actors.  In
#  this task you will develop a program that helps visualise some
#  of the opinions of movie fans derived from a survey of
#  Microsoft employees.  To do so you will make use of three
#  different computer languages, Python, SQLite and HTML.  You
#  will develop a Python function, show popularity, which accesses
#  data in an SQL database and uses this to generate HTML documents
#  which visually display an actor's popularity according to the
#  survey results.  See the instructions accompanying this file for
#  full details.
#
#--------------------------------------------------------------------#



#-----Acceptance Tests-----------------------------------------------#
#
#  This section contains unit tests that run your program.  You
#  may not change anything in this section.  NB: 'Passing' these
#  tests does NOT mean you have completed the assignment because
#  they do not check the HTML files produced by your program.
#
"""
------------------- Normal Cases with valid input --------------------

>>> show_popularity(['Female', 'Male', '30-40'], 20, 'Test01') # Test 1

>>> show_popularity(['20-30', '30-40', '40-50'], 50, 'Test02') # Test 2

>>> show_popularity(['20-40', '40-80', 'All'], 30, 'Test03') # Test 3

>>> show_popularity(['Female', 'Male', '30-40', '40-60', '60-100', 'All'], 30, 'Test04') # Test 4

>>> show_popularity(['All'], 20, 'Test05') # Test 5

>>> show_popularity(['30-40'], 50, 'Test06') # Test 6

>>> show_popularity(['30-50'], 0, 'Test07') # Test 7

------------------- Cases with invalid input ------------------------

>>> show_popularity(['20-30', '30-40', '3a-34' ], 30, 'Test08') # Test 8
Invalid customer group: 3a-34

>>> show_popularity(['teens', '20-20','30-40','40-50', '50-50', '60-d0'], 30, 'Test09') # Test 9
Invalid customer group: teens
Invalid customer group: 60-d0

>>> show_popularity(['old people', '30', '40-60', '-70', '70-100'], 30, 'Test10') # Test 10
Invalid customer group: old people
Invalid customer group: 30
Invalid customer group: -70

>>> show_popularity(['-', '30-50', '40-60', '50-20', '40 60'], 50, 'Test11') # Test 11
Invalid customer group: -
Invalid customer group: 40 60

>> show_popularity(['9-20'], 50, 'TestX')

""" 
#
#--------------------------------------------------------------------#



#-----Students' Solution---------------------------------------------#
#
#  Complete the task by filling in the template below.

# Get the sql functions
from sqlite3 import *
import re           ## Import re library to use regular expression
import random       ## Import random library to use randint function

########################## PUT YOUR show_popularity FUNCTION HERE


## Define an empty list to store the names of HTML pages
text_name=[]
flag=0


##  Function for creating and storing file names
def create_file(element,no):
##      Allow functions to manipulate external variables
     global text_name
     file_name = no+"_"+element+".html"
     file = open(file_name,'w')
     file.close()
##     Add filename to list
     text_name.append(str(file_name))


##  Function to generate random color encoding and return encoding
def random_font_color():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color


##  Function to execute SQL statements and generate HTML files
def show_popularity(limits,num,no):
##     Allow functions to manipulate external variables
     global flag

     # Create a connection to the database.
     connection = connect(database='movie_survey.db')
     # Get a pointer into the database.
     movie_db = connection.cursor()

     for element in limits:
          illegal=0  ##  Whether the string is a canonical identifier
          count=0    ##  Number of qualified customers

          ##  Filter the qualified actors and use aggregate function
          ##  to generate the popularity of each actor,
          ##  and then arrange them in descending order of popularity
          if element=='Male':
               movie_db.execute("""SELECT favorite_actors.actor,count(1) AS num 
                                   FROM customers,favorite_actors
                                   WHERE customers.gender='Male'
                                   AND customers.customerID=favorite_actors.customerID 
				   GROUP BY actor HAVING count(1)>1
                                   ORDER BY num desc;""")
          elif element=='Female':
               movie_db.execute("""SELECT favorite_actors.actor,count(1) AS num 
                                   FROM customers,favorite_actors
                                   WHERE customers.gender='Female'
                                   AND customers.customerID=favorite_actors.customerID 
				   GROUP BY actor HAVING count(1)>1
                                   ORDER BY num desc;""")
          elif element=='All':
               movie_db.execute("""SELECT favorite_actors.actor,count(1) AS num 
                                   FROM favorite_actors
                                   GROUP BY actor HAVING count(1)>1
                                   ORDER BY num desc;""")
          elif ((re.findall("[0-9]0-[0-9]0",element))!=[]):
               movie_db.execute("""SELECT favorite_actors.actor,count(1)
                                AS num FROM favorite_actors,customers
                                WHERE customers.age>="""+element[0:2]+"""
                                AND customers.age<="""+element[3:]+"""
                                AND customers.customerID=favorite_actors.customerID
                                GROUP BY actor HAVING count(1) ORDER BY num desc;""")
          else:
               print('Invalid customer group: '+element)
               illegal=1      ##  Record that this element is irregular                                 


##  If the element meets the requirements, the function to
##   create the file is called and the HTML file is generated
          if illegal==0:                                       
               create_file(element,no)                        
          ##   Store the results of SQL statement execution in list row1
               row1 = list(movie_db.fetchall())
          ##   Take the first num lines of list row1 and put it in list row2
               row2 = row1[0:num]
          ##   Sort by actor name
               row2.sort()
               
               file_name = no+"_"+element+".html"
               file_write = open(file_name,'w')

          ##   Execute SQL statement to count the number of qualified customers
               if element=='Male':
                    movie_db.execute("""SELECT  COUNT(*) FROM customers
                                                 WHERE gender='Male'""")

               elif element=='Female':
                    movie_db.execute("""SELECT  COUNT(*) FROM customers
                                                 WHERE gender='Female'""")

               elif element=='All':
                     movie_db.execute("""SELECT  COUNT(*) FROM customers""")


               elif ((re.findall("[0-9]0-[0-9]0",element))!=[]):
                    movie_db.execute("""SELECT  COUNT(*) FROM customers
                                             WHERE age>="""+element[0:2]+""" 
                                             AND age<="""+element[3:]+""";""")

               ## Receive the number returned by SQL language
               count=list(movie_db.fetchone()) 


               ## Write HTML statement to file
               file_write.write("""
     <!DOCtype HTML>
     <html>
          <h1 align="center">Top """+str(num)+""" Most Popular Actors
          </h1>
          <p></p>
          <p align="center"> <b>Customer Group:"""+str(element)+"""</b></p>
          <p align="center"> <b>Number of Customers:"""+str(count[0])+"""</b></p>
          <hr>
          <p align="center">
     """)

              ##  Display name and number in web page
               for actor in row2:
                    ## Receive a randomly generated color code
                    font_color=random_font_color()
                    ## The size of the font depends on the popularity of the actors
                    font_size=5+actor[1]/6

                    file_write.write("""
     <span style="font-size:"""+str(font_size)+"""px;text-align:center;
     color:"""+str(font_color)+"""""> <nobr>"""+str(actor[0])+"""</span>
     <span style="font-size:"""+str(font_size/10)+"""px;text-align:center;
     color:"""+str(font_color)+""""">("""+str(actor[1])+""")
</nobr></span>""")

               ## judge whether it is the first web page
               if flag!=0:
                    file_write.write("""</p><hr>
     <a href='"""+text_name[flag-1]+"""'>Previous Page</a>
     """)
               else:
                    file_write.write("""<hr>""")

               if(flag>=1):
                    file_write = open(text_name[flag-1],'a')
                    file_write.write("""<a href='"""+text_name[flag]+"""'
     style="display:block;text-align:right;"'>Next Page</a>
     </html>""")

               flag=flag+1   ## Record the serial number of the web page
               file_write.close()


# Close the cursor and release the server connection
     movie_db.close()
     connection.close()


#
#--------------------------------------------------------------------#



#-----Automatic Testing----------------------------------------------#
#
#  The following code will automatically run the unit tests
#  when this program is "run".  Do not change anything in this
#  section.  If you want to prevent the tests from running, comment
#  out the code below, but ensure that the code is uncommented when
#  you submit your program.
#
if __name__ == "__main__":
     from doctest import testmod
     testmod(verbose=True)   
#
#--------------------------------------------------------------------#
