import  jinja2, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#assinging command line's argument 
option = sys.argv[1]
argument= sys.argv[2]

global final_template

# Reading the CSV file
file = open('data.csv')
file.readline()
datalist = [line.strip().split(',') for line in file]


#function for handling wrong invalid inputs
error_template ="""
<!DOCTYPE html>
<html>
<head>
    <title>Something Went Wrong</title>
</head>
<body>
<h1>Wrong Inputs</h1>
<h5>Something Went Wrong</h5>             
</body>
</html>    
                """


# if user choose student option in command line
if option == '-s':
    student_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Data</title>
</head>
<body>
<h1> Students Details </h1>
    <table border="2px">
    <tr>
        <th>Student id</th>
        <th>Course id</th>
        <th>Marks</th>
    </tr>
    {% for row in rows %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
        </tr>
    {% endfor %}
    <tr>
        <td colspan="2"> <center>Total Marks </center></td>
        <td>{{total_marks}}</td>
    </tr> 
    </table>
</body>
</html>
                        """
    sum, result = 0,[]
    
    for row in datalist:
        if str(row[0]) == argument:
            result.append(row)
            sum += int(row[2])
    
    if not result:
        final_template = error_template
  
    else:
        final_template = jinja2.Template(student_template).render(rows=result,total_marks=sum)      
     


# if user choose course option in command line
elif option == '-c':
    marks =[]
    course_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Course Data</title>
</head>
<body>
<h1> Course Details </h1>
    <table border="2px">
    <tr>
        <th>Average Marks</th>
        <th>Maximum Marks</th>
    </tr>
    <tr>
        <td>{{avg_marks}}</td>
        <td>{{max_marks}}</td>
    </tr> 
    
    </table>
    <img src='plot.png'>
</body>
</html>
                        """    
    
    for row in datalist:
        if str(row[1]) == " "+argument:
            marks.append(int(row[2]))
    
    if not marks:
        final_template = error_template
  
    else:
        avg_marks = sum(marks)/len(marks)
        max_marks = max(marks)
        
        final_template = jinja2.Template(course_template).render(avg_marks=avg_marks,max_marks=max_marks)
       

    # Prepare the Data
    # Create the Plot
    plt.hist(marks)
    
    # Customize the Plot
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram Example')

    # Display the Plot
    plt.savefig('plot.png')
    

else:
    print('else')
    final_template = error_template


with open('output.html', 'w') as file:
    file.write(final_template)
    pass
print("Output file created: output.html")