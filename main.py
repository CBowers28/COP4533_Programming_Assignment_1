#Read Example File (example.in)
with open("example.in", 'r') as file:
    lines = [line.strip() for line in file if line.strip()]

# Get n from first line of example.in
n = int(lines[0])

#initalize preference list
pref = []

#load hospital preferences
for i in range(1, 2*n + 1):
    pref.append(list(map(int, lines[i].split())))


print(pref)
#pref checker
def pref_checker(pref, hospital, applicant, applicant_2, n):
    for i in range(n):
        if pref[hospital][i] == applicant_2:
            return False
        if pref[hospital][i] == applicant:
            return True
    return True


#Gale Shapely
def gale_shapley (pref):
    free_applicants = [False] * n
    hospital_match = [-1] * n
    free_applicant_count = n

    while free_applicant_count > 0:
        print(hospital_match)
        applicant = next(i for i in range(n) if not free_applicants[i])
        #check if applicant is free and if they are a match is made
        print(applicant)
        for i in range(n):
            if free_applicants[i]:
                break
            hospital = pref[applicant][i]
        #check if hospital has been matched
        if hospital_match[hospital - n] == -1:
            hospital_match[hospital - n] = applicant
            free_applicants[applicant] = True
            free_applicant_count -= 1

        else:
            applicant_2 = hospital_match[hospital - n]
            #check if unstable
            for j in range(n):
                if pref_checker(pref, hospital, applicant, applicant_2, n):
                    #swap applicants
                    hospital_match[hospital - n] = applicant
                    free_applicants[applicant] = True
                    free_applicants[applicant_2] = False

    return  hospital_match

hospital_match = gale_shapley(pref)
print(hospital_match)
