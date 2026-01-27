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


#Gale Shapley Algorithms (hospitals propose)
def gale_shapley(pref):
    # initalize all var needed for the algo
    free_hospitals = [False] * n #keeps track of free hospitals
    applicant_match = [-1] * n # keeps track of applicant matches (this is what will be returned)
    free_hospital_count = n # count for the while loop
    next_proposal = [0] * n
# the next proposal array is formatted as such: each index corresponds to a hospital and the value stored there is what applicant in the list they are on

    while free_hospital_count > 0:
        #get the next hospital that is maked a false (free) in the free hospitals array
        hospital = next(i for i in range(n) if not free_hospitals[i])

        #get next applicant to propose to
        i = next_proposal[hospital]

        #set applicant and move proposal index to make that a specific applicant has been proposed to
        applicant = pref[hospital][i] - 1         
        next_proposal[hospital] += 1

        # if they are not matched create the pair
        if applicant_match[applicant] == -1:
            applicant_match[applicant] = hospital
            free_hospitals[hospital] = True
            free_hospital_count -= 1


        #if a hospital wants to match to an already paired applicant we check the applicant preference
        else:
            #the hospital the applicant is already paired to
            hospital_2 = applicant_match[applicant]
            # check for unstable match
            for j in range(n):
                #if the applicant prefers its current hospital no change is made
                if pref[n + applicant][j] == hospital_2 + 1:
                    break
                #if the desired applicant preferes the proposing hospital to its current we switch
                if pref[n + applicant][j] == hospital + 1:
                    applicant_match[applicant] = hospital
                    free_hospitals[hospital] = True
                    free_hospitals[hospital_2] = False
    #return applicant choices
    return applicant_match



applicant_match = gale_shapley(pref)

#output method
with open("example.out", 'w') as f:
    for hospital in range(n):
        applicant = next(s for s in range(n) if applicant_match[s] == hospital)
        #must add 1 due to the normalization because we used indices and not the true numbers
        f.write(f"{hospital + 1} {applicant + 1}\n")

