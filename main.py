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

#use the array indices to match.
student_match = []
hospital_match = []


