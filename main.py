#Read Example File (example.in)
with open("example.in", 'r') as file:
    lines = [line.strip() for line in file if line.strip()]

# Get n from first line of example.in
n = int(lines[0])

#initalize preference list
hospital_pref = []
student_pref = []

#load hospital preferences
for i in range(1, 1+n):
    hospital_pref.append(list(map(int, lines[i].split())))

#load student preferences
for i in range(n, 2*n):
    student_pref.append(list(map(int, lines[i].split())))

#convert to a base of 0 for prefrences (can add a 1 to everthing at the end)
hospital_pref = [[s - 1 for s in row] for row in hospital_pref]
student_pref  = [[h - 1 for h in row] for row in student_pref]

#Gale Shapely


