import csv


rooms = []
capacity = []
input1_courses = []
course_time = []
course_data = []
max = 0


with open('error.txt', "w") as file:
    file.truncate()

with open('report.txt', "w") as file:
    file.truncate()

with open('time_table.csv', "w") as file:
    file.truncate()


class Course:
    def __init__(self, course_no, course_enrollment, course_preference):
        self.c_no = course_no
        self.c_enrollment = course_enrollment
        self.c_preference = course_preference


def check_room_number():
    for i in rooms:
        if not (int(i) >= 100 and int(i) <= 999):
            with open('error.txt', "a") as file:
                file.write(i + ": Classroom number has wrong format\n")
            rooms.remove(i)


def check_capacity():
    for i in capacity:
        if not (int(i) >= 10 and int(i) <= 300):
            with open('error.txt', "a") as file:
                file.write(i + ": Classroom capacity out of range\n")
            capacity.remove(i)


def check_courses():
    for i in input1_courses:
        if not (int(i[2:]) >= 100 and int(i[2:]) <= 999 and i[0:2].__eq__("cs")):
            with open('error.txt', "a") as file:
                file.write(i + ": The course number has wrong format\n")
            input1_courses.remove(i)


def check_time():
    for i in course_time:
        if not (i == "MWF9" or i == "MWF10" or i == "MWF11" or i == "MWF2" or i == "TT9" or i == "TT10:30" or i == "TT2" or i == "TT3:30"):
            with open('error.txt', "a") as file:
                file.write(i + ": Lecture time has wrong format\n")
            course_time.remove(i)


def is_course_valid(course):
    if course not in input1_courses:
        with open('error.txt', "a") as file:
            file.write(course + ": No course of this number\n")
        return False
    return True


def is_enrollment_valid(course, enrollment):
    if int(enrollment) > max or int(enrollment) < 3 or int(enrollment) > 250:
        with open('error.txt', "a") as file:
            file.write(course + ": " + enrollment +
                       ": No classroom of this capacity\n")
        return False
    return True


def is_preference_valid(course, preference):
    for i in preference:
        if i not in course_time:
            with open('error.txt', "a") as file:
                file.write(course + ": " + i + ": No such lecture time\n")
            preference.remove(i)

    if len(preference) > 5:
        with open('error.txt', "a") as file:
            file.write(course +
                       ": There are more than permissible preferences. Later ones are ignored.\n")
        for i in range(5, len(preference)):
            preference.pop(i)

    return preference


def schedule_post_graduate_courses():
    post_grad_schedule_time = [False]*len(course_time)
    for i in course_data:
        if int(i.c_no[2:]) > 600:
            course_scheduled = False
            for j in i.c_preference:
                col = course_time.index(j)
                for k in rooms:
                    row = rooms.index(k)
                    if time_table[row][col] == '0' and int(capacity[row]) >= int(i.c_enrollment) and not post_grad_schedule_time[col]:
                        time_table[row][col] = i.c_no
                        course_scheduled = True
                        post_grad_schedule_time[col] = True
                        break
                if course_scheduled:
                    break

            if not course_scheduled:
                for j in range(0, len(rooms)):
                    for k in range(0, len(course_time)):
                        if k not in i.c_preference and int(capacity[j]) >= int(i.c_enrollment) and time_table[j][k] == '0' and not post_grad_schedule_time[k]:
                            time_table[row][col] = i.c_no
                            course_scheduled = True
                            post_grad_schedule_time[k] = True
                            break
                    if course_scheduled:
                        break

            if not course_scheduled:
                with open('report.txt', "a") as file:
                    file.write(
                        i.c_no + ": No available classroom with proper capacity\n")


def schedule_under_graduate_courses():
    for i in course_data:
        if int(i.c_no[2:]) <= 600:
            course_scheduled = False
            for j in i.c_preference:
                col = course_time.index(j)
                for k in rooms:
                    row = rooms.index(k)
                    if time_table[row][col] == '0' and int(capacity[row]) >= int(i.c_enrollment):
                        time_table[row][col] = i.c_no
                        course_scheduled = True
                        break
                if course_scheduled:
                    break

            if not course_scheduled:
                for j in range(0, len(rooms)):
                    for k in range(0, len(course_time)):
                        if k not in i.c_preference and int(capacity[j]) >= int(i.c_enrollment) and time_table[j][k] == '0':
                            time_table[row][col] = i.c_no
                            course_scheduled = True
                            break
                    if course_scheduled:
                        break

            if not course_scheduled:
                with open('report.txt', "a") as file:
                    file.write(
                        i.c_no + ": No available classroom with proper capacity\n")


try:
    with open('input1.txt', 'r') as file1:
        input1_data = file1.readlines()
        course_index = input1_data.index('courses\n')
        time_index = input1_data.index('times\n')

        for i in range(1, course_index):
            data = input1_data[i].split(':')
            if i == course_index - 1:
                rooms.append(data[0])
                capacity.append(data[1][0:len(data[1]) - 2])
            else:
                rooms.append(data[0])
                capacity.append(data[1][0:len(data[1]) - 1])
        print("Rooms:", rooms)
        print("Capacity:", capacity)

        check_room_number()
        check_capacity()

        for i in capacity:
            if int(i) > max:
                max = int(i)

        input1_courses = input1_data[course_index +
                                     1][0:len(input1_data[course_index + 1]) - 2].split(',')
        print("Courses:", input1_courses)

        check_courses()

        course_time = input1_data[time_index +
                                  1][0:len(input1_data[time_index + 1]) - 1].split(',')
        print("Course Time:", course_time)

        check_time()

except FileNotFoundError:
    print("Input File1 does not exist")

try:
    with open('input2.txt', 'r') as file2:
        input2_data = file2.readlines()
        for i in range(1, len(input2_data)):
            data = input2_data[i].split(' ')
            if len(course_data) < 20:
                if i == len(input2_data) - 1:
                    course_valid = is_course_valid(data[0])
                    enrollment_valid = is_enrollment_valid(data[0], data[1])
                    preference = is_preference_valid(
                        data[0], data[2].split(','))
                    if course_valid and enrollment_valid:
                        c = Course(data[0], data[1], preference)
                        course_data.append(c)
                else:
                    course_valid = is_course_valid(data[0])
                    enrollment_valid = is_enrollment_valid(data[0], data[1])
                    preference = is_preference_valid(
                        data[0], data[2][0:len(data[2]) - 1].split(','))
                    if course_valid and enrollment_valid:
                        c = Course(data[0], data[1], preference)
                        course_data.append(c)

        for i in course_data:
            print(i.c_no)
            print(i.c_enrollment)
            print(i.c_preference)
except FileNotFoundError:
    print("Input File2 does not exist")

time_table = []

for i in range(0, len(rooms)):
    list = []
    for j in range(0, len(course_time)):
        list.append('0')
    time_table.append(list)

schedule_post_graduate_courses()
schedule_under_graduate_courses()

with open("time_table.csv", 'w') as file:
    writer = csv.writer(file)
    course_time.insert(0, '')
    writer.writerow(course_time)
    for i in range(0, len(time_table)):
        row = time_table[i]
        row.insert(0, rooms[i])
        writer.writerow(row)
print(time_table)
