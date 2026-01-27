# Gale–Shapley Algorithm (Hospitals Propose)
def gale_shapley(pref):
    n = len(pref) // 2

    # keeps track of whether each hospital is matched (True = matched)
    free_hospitals = [False] * n

    # applicant_match[student] = hospital (0-based), -1 if unmatched
    applicant_match = [-1] * n

    free_hospital_count = n

    # next_proposal[hospital] = index of next student to propose to
    next_proposal = [0] * n

    while free_hospital_count > 0:
        # find a free hospital
        hospital = next(i for i in range(n) if not free_hospitals[i])

        # get next student this hospital proposes to
        i = next_proposal[hospital]
        applicant = pref[hospital][i] - 1  # convert to 0-based
        next_proposal[hospital] += 1

        # if student is free, match them
        if applicant_match[applicant] == -1:
            applicant_match[applicant] = hospital
            free_hospitals[hospital] = True
            free_hospital_count -= 1

        else:
            # student is currently matched
            current_hospital = applicant_match[applicant]

            # check student's preference list
            for j in range(n):
                # student prefers current hospital → reject new one
                if pref[n + applicant][j] == current_hospital + 1:
                    break

                # student prefers new hospital → switch
                if pref[n + applicant][j] == hospital + 1:
                    applicant_match[applicant] = hospital
                    free_hospitals[hospital] = True
                    free_hospitals[current_hospital] = False
                    break

    return applicant_match


# ===============================
# File I/O (only runs when executed directly)
# ===============================
if __name__ == "__main__":

    # Read Example File (example.in)
    with open("example.in", 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    # Get n
    n = int(lines[0])

    # Initialize preference list
    pref = []

    # Load hospital + student preferences
    for i in range(1, 2 * n + 1):
        pref.append(list(map(int, lines[i].split())))

    # Run Gale–Shapley
    applicant_match = gale_shapley(pref)

    # Output matching
    with open("example.out", 'w') as f:
        for hospital in range(n):
            applicant = next(
                s for s in range(n) if applicant_match[s] == hospital
            )
            f.write(f"{hospital + 1} {applicant + 1}\n")
