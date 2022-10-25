from flask import Flask, request
from flask import render_template

import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

file = open('data.csv')
file.readline()
data = []
for line in file:
    data.append(line.strip().split(','))
s_id = [i[0] for i in data]
c_id = [int(i[1]) for i in data]

@app.route("/", methods=["GET","POST"])
def main():
    global s_id
    global c_id
    if request.method == 'GET':
        return render_template('Index.html')
    elif request.method == 'POST':
        try:
            req_detail = request.form['ID']
            ID_value = request.form['id_value']
        except:
            return render_template('wrong.html')
        #print("req_detail",req_detail,"ID_value",ID_value)
        if req_detail == 'student_id' and ID_value in s_id:
            student_id = ID_value
            course_id=[]
            marks=[]
            total = 0
            count=0
            for i in data:
                if i[0]==student_id:
                    total += int(i[2])
                    marks.append(int(i[2]))
                    course_id.append(int(i[1]))
                    count+=1
            return render_template('student_output.html', heading='Student Details', title='Student Data',req=req_detail,student_id=student_id ,course_id=course_id,marks=marks,size=count,total=total)
        elif req_detail == 'course_id' and int(ID_value) in c_id:
            course_id = int(ID_value)
            marks_list=[]
            for i in data:
                if int(i[1])==course_id:
                    marks_list.append(int(i[2]))
            maximum=max(marks_list)
            average=sum(marks_list)/len(marks_list)
            plt.clf()
            plt.hist(marks_list)
            plt.xlabel("Marks")
            plt.ylabel('Frequency')
            plt.savefig('./static/hist.png')
            return render_template('course_output.html',title='Course Data',req=req_detail,average=average,maximum=maximum,heading='Course Details')
        else:
            return render_template('wrong.html')



if __name__ == '__main__':
    app.debug = True
    app.run()