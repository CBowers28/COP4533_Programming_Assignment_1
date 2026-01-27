import time
import random

from main import gale_shapley
from verifier import check_stability


def generate_random_preferences(n):
    ids = list(range(1, n + 1))
    pref = []

    for _ in range(n):      # hospitals
        order = ids[:]
        random.shuffle(order)
        pref.append(order)

    for _ in range(n):      # students
        order = ids[:]
        random.shuffle(order)
        pref.append(order)

    return pref


def split_preferences(pref):
    n = len(pref) // 2
    return n, pref[:n], pref[n:]


def build_matching_maps(applicant_match):
    n = len(applicant_match)
    hospital_to_student = {}
    student_to_hospital = {}

    for s_idx, h_idx in enumerate(applicant_match):
        h = h_idx + 1
        s = s_idx + 1
        hospital_to_student[h] = s
        student_to_hospital[s] = h

    return hospital_to_student, student_to_hospital


def benchmark_matching(ns, repeats=3):
    times = {}

    for n in ns:
        total = 0.0
        for _ in range(repeats):
            pref = generate_random_preferences(n)
            start = time.perf_counter()
            gale_shapley(pref)
            end = time.perf_counter()
            total += end - start
        times[n] = total / repeats

    return times


def benchmark_verifier(ns, repeats=3):
    times = {}

    for n in ns:
        total = 0.0
        for _ in range(repeats):
            pref = generate_random_preferences(n)
            n_check, hospital_prefs, student_prefs = split_preferences(pref)
            applicant_match = gale_shapley(pref)
            hospital_to_student, student_to_hospital = build_matching_maps(applicant_match)

            start = time.perf_counter()
            check_stability(
                n_check,
                hospital_prefs,
                student_prefs,
                hospital_to_student,
                student_to_hospital
            )
            end = time.perf_counter()
            total += end - start

        times[n] = total / repeats

    return times


def main():
    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    matching_times = benchmark_matching(ns)
    verifier_times = benchmark_verifier(ns)

    print("n,matching_time_seconds,verifier_time_seconds")
    for n in ns:
        print(f"{n},{matching_times[n]:.6e},{verifier_times[n]:.6e}")


if __name__ == "__main__":
    main()
