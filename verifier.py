import sys


def read_preferences(filename):
    # returns (n, hospital_prefs, student_prefs) or (None, None, None) on error
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("INVALID: preference file not found")
        return None, None, None

    if not lines:
        print("INVALID: empty preference file")
        return None, None, None

    try:
        n = int(lines[0])
    except ValueError:
        print("INVALID: first line must be integer n")
        return None, None, None

    if n <= 0:
        print("INVALID: n must be positive")
        return None, None, None

    if len(lines) != 1 + 2 * n:
        print(f"INVALID: expected {2 * n} preference lines, got {len(lines) - 1}")
        return None, None, None

    prefs = []
    for idx in range(1, 1 + 2 * n):
        parts = lines[idx].split()
        if len(parts) != n:
            print(f"INVALID: line {idx + 1} does not have {n} entries")
            return None, None, None

        try:
            row = list(map(int, parts))
        except ValueError:
            print(f"INVALID: non-integer value on line {idx + 1}")
            return None, None, None

        if sorted(row) != list(range(1, n + 1)):
            print(f"INVALID: line {idx + 1} is not a permutation of 1..n")
            return None, None, None

        prefs.append(row)

    return n, prefs[:n], prefs[n:]


def read_matching(filename, n):
    # returns (ok, hospital_to_student, student_to_hospital)
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("INVALID: matching file not found")
        return False, None, None

    if len(lines) != n:
        print(f"INVALID: expected {n} matching lines, got {len(lines)}")
        return False, None, None

    hospital_to_student = {}
    student_to_hospital = {}

    for line_no, line in enumerate(lines, start=1):
        parts = line.split()
        if len(parts) != 2:
            print(f"INVALID: line {line_no} in matching must have 2 integers")
            return False, None, None

        try:
            h, s = map(int, parts)
        except ValueError:
            print(f"INVALID: non-integer on line {line_no} in matching")
            return False, None, None

        if not (1 <= h <= n and 1 <= s <= n):
            print(f"INVALID: ids out of range on line {line_no} in matching")
            return False, None, None

        if h in hospital_to_student:
            print(f"INVALID: hospital {h} appears more than once in matching")
            return False, None, None

        if s in student_to_hospital:
            print(f"INVALID: student {s} appears more than once in matching")
            return False, None, None

        hospital_to_student[h] = s
        student_to_hospital[s] = h

    if len(hospital_to_student) != n or len(student_to_hospital) != n:
        print("INVALID: not all hospitals/students are matched")
        return False, None, None

    return True, hospital_to_student, student_to_hospital


def build_rank_maps(n, hospital_prefs, student_prefs):
    hospital_rank = {h: {} for h in range(1, n + 1)}
    student_rank = {s: {} for s in range(1, n + 1)}

    for h in range(1, n + 1):
        for pos, st in enumerate(hospital_prefs[h - 1]):
            hospital_rank[h][st] = pos

    for s in range(1, n + 1):
        for pos, h in enumerate(student_prefs[s - 1]):
            student_rank[s][h] = pos

    return hospital_rank, student_rank


def check_stability(n, hospital_prefs, student_prefs,
                    hospital_to_student, student_to_hospital):
    hospital_rank, student_rank = build_rank_maps(n, hospital_prefs, student_prefs)

    for h in range(1, n + 1):
        for s in range(1, n + 1):
            cur_s = hospital_to_student[h]
            cur_h = student_to_hospital[s]

            if hospital_rank[h][s] < hospital_rank[h][cur_s]:
                if student_rank[s][h] < student_rank[s][cur_h]:
                    return False, h, s

    return True, None, None


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 verifier.py <preferences_file> <matching_file>")
        sys.exit(1)

    pref_file = sys.argv[1]
    match_file = sys.argv[2]

    n, hospital_prefs, student_prefs = read_preferences(pref_file)
    if n is None:
        sys.exit(1)

    ok, hospital_to_student, student_to_hospital = read_matching(match_file, n)
    if not ok:
        sys.exit(1)

    stable, h, s = check_stability(
        n, hospital_prefs, student_prefs,
        hospital_to_student, student_to_hospital
    )

    if not stable:
        print(f"UNSTABLE: blocking pair ({h}, {s})")
    else:
        print("VALID STABLE")


if __name__ == "__main__":
    main()
