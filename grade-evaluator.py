import csv
import os


def load_csv_data():
    """
    Keeps asking the user for a filename until a valid, non-empty CSV
    with all required fields and clean data is provided.
    Returns a list of assignment dictionaries.
    """
    while True:
        filename = input("\nEnter the name of the CSV file to process (e.g., grades.csv): ").strip()

        # --- Check 1: File must exist ---
        if not os.path.exists(filename):
            print(f"  ✘ File '{filename}' is empty. Please provide a file with data.")
            continue

        # --- Check 2: File must not be completely empty ---
        if os.path.getsize(filename) == 0:
            print(f"  ✘ File '{filename}' is empty. Please provide a file with data.")
            continue

        assignments = []
        error_found = False

        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # --- Check 3: File must have the required columns ---
                required_columns = {'assignment', 'group', 'score', 'weight'}
                if not required_columns.issubset(set(reader.fieldnames or [])):
                    missing = required_columns - set(reader.fieldnames or [])
                    print(f"  ✘ The file is missing required column(s): {', '.join(missing)}.")
                    print("     Make sure your CSV has: assignment, group, score, weight.")
                    error_found = True

                if not error_found:
                    for line_number, row in enumerate(reader, start=2):

                        assignment_name = row.get('assignment', '').strip()
                        group           = row.get('group', '').strip()

                        # --- Check 4: Group must be Summative or Formative ---
                        if group.lower() not in ('summative', 'formative'):
                            print(f"  ✘ Row {line_number} ('{assignment_name}'): Group '{group}' is invalid. Must be 'Summative' or 'Formative'.")
                            error_found = True
                            continue

                        # --- Check 5: Missing score ---
                        raw_score = row.get('score', '').strip()
                        if raw_score == '':
                            print(f"  ✘ Row {line_number} ('{assignment_name}'): Score is missing.")
                            error_found = True
                            continue

                        # --- Check 6: Missing weight ---
                        raw_weight = row.get('weight', '').strip()
                        if raw_weight == '':
                            print(f"  ✘ Row {line_number} ('{assignment_name}'): Weight is missing.")
                            error_found = True
                            continue

                        # --- Check 7: Score must be a valid number ---
                        try:
                            score = float(raw_score)
                        except ValueError:
                            print(f"  ✘ Row {line_number} ('{assignment_name}'): Score '{raw_score}' is not a valid number.")
                            error_found = True
                            continue

                        # --- Check 8: Weight must be a valid number ---
                        try:
                            weight = float(raw_weight)
                        except ValueError:
                            print(f"  ✘ Row {line_number} ('{assignment_name}'): Weight '{raw_weight}' is not a valid number.")
                            error_found = True
                            continue

                        assignments.append({
                            'assignment': assignment_name,
                            'group':      group,
                            'score':      score,
                            'weight':     weight
                        })

        except Exception as e:
            print(f"  ✘ An unexpected error occurred while reading the file: {e}")
            continue

        if error_found:
            print("  → Please fix the issues in your CSV file and try again.")
            continue

        # --- Check 9: File has a header but no data rows ---
        if len(assignments) == 0:
            print(f"  ✘ File '{filename}' has no assignment data (only a header row).")
            print("     Please add at least one assignment row and try again.")
            continue

        print(f"  ✔ File '{filename}' loaded successfully with {len(assignments)} assignment(s).")
        return assignments


def evaluate_grades(data):
    """
    Evaluates student grades and prints results in transcript format.
    Returns True if valid, False if data errors found.
    """
    error_found = False

    # a) Validate all scores are within 0-100
    for record in data:
        if not (0 <= record['score'] <= 100):
            print(f"  ✘ Score for '{record['assignment']}' is {record['score']}%, which is out of range (must be 0–100).")
            error_found = True

    # b) Validate weights (strict 60/40 split)
    total_weight     = sum(r['weight'] for r in data)
    summative_weight = sum(r['weight'] for r in data if r['group'].strip().lower() == 'summative')
    formative_weight = sum(r['weight'] for r in data if r['group'].strip().lower() == 'formative')

    if round(total_weight, 2) != 100:
        print(f"  ✘ Total weight is {total_weight}% but must equal exactly 100%.")
        error_found = True
    if round(summative_weight, 2) != 40:
        print(f"  ✘ Summative weight is {summative_weight}% but must equal exactly 40%.")
        error_found = True
    if round(formative_weight, 2) != 60:
        print(f"  ✘ Formative weight is {formative_weight}% but must equal exactly 60%.")
        error_found = True

    if error_found:
        print("\n  → Please fix the issues in your CSV file and try again.")
        return False

    # c) Calculate final weight per assignment (score × weight / 100)
    for r in data:
        r['final_weight'] = round((r['score'] * r['weight']) / 100, 2)

    summative_records = [r for r in data if r['group'].strip().lower() == 'summative']
    formative_records = [r for r in data if r['group'].strip().lower() == 'formative']

    formative_total = round(sum(r['final_weight'] for r in formative_records), 2)
    summative_total = round(sum(r['final_weight'] for r in summative_records), 2)
    total_grade     = round(formative_total + summative_total, 2)
    gpa             = round((total_grade / 100) * 5.0, 3)

    # d) Pass/Fail: weighted average per category must be >= 50%
    summative_avg = round(sum(r['score'] * r['weight'] for r in summative_records) / summative_weight, 2)
    formative_avg = round(sum(r['score'] * r['weight'] for r in formative_records) / formative_weight, 2)

    passed_summative = summative_avg >= 50
    passed_formative = formative_avg >= 50
    passed_overall   = passed_summative and passed_formative

    # e) Resubmission: failed formative(s) with highest weight
    failed_formative        = [r for r in formative_records if r['score'] < 50]
    resubmission_candidates = []
    if failed_formative:
        max_weight              = max(r['weight'] for r in failed_formative)
        resubmission_candidates = [r for r in failed_formative if r['weight'] == max_weight]

    # f) Print transcript-style output
    col_a = 26  # assignment column width
    col_b = 10  # category
    col_c = 11  # grade (%)
    col_d = 8   # weight
    col_e = 14  # final weight

    sep = "-" * (col_a + col_b + col_c + col_d + col_e + 4)

    print()
    print(sep)
    print(
        f"{'Assignment':<{col_a}} {'Category':<{col_b}} {'Grade (%)':<{col_c}} {'Weight':<{col_d}} {'Final Weight':<{col_e}}"
    )
    print(sep)

    for r in data:
        category = "FA" if r['group'].strip().lower() == 'formative' else "SA"
        print(
            f"{r['assignment']:<{col_a}} {category:<{col_b}} {r['score']:<{col_c}} {r['weight']:<{col_d}} {r['final_weight']:<{col_e}}"
        )

    print(sep)
    print(f"{'Formatives (60)':<{col_a}} {'':<{col_b}} {'':<{col_c}} {'':<{col_d}} {formative_total:<{col_e}}")
    print(f"{'Summatives (40)':<{col_a}} {'':<{col_b}} {'':<{col_c}} {'':<{col_d}} {summative_total:<{col_e}}")
    print(sep)
    print(f"{'GPA':<{col_a}} {gpa:<{col_b}} {'':<{col_c}} {'':<{col_d}} {'':<{col_e}}")
    print(sep)

    status = "PASSED" if passed_overall else "FAILED"
    print(f"{'Status':<{col_a}} {'':<{col_b}} {'':<{col_c}} {'':<{col_d}} {status:<{col_e}}")

    if not passed_summative:
        print(f"  → Summative average is {summative_avg}% (below 50% threshold).")
    if not passed_formative:
        print(f"  → Formative average is {formative_avg}% (below 50% threshold).")

    if resubmission_candidates:
        names = ", ".join(r['assignment'] for r in resubmission_candidates)
        print(f"{'Available for resubmission':<{col_a}} {'':<{col_b}} {'':<{col_c}} {'':<{col_d}} {names:<{col_e}}")
    else:
        print(f"{'Available for resubmission':<{col_a}} {'':<{col_b}} {'':<{col_c}} {'':<{col_d}} {'None':<{col_e}}")

    print(sep)
    return True


def ask_to_exit():
    """
    Asks the user if they want to exit or try again.
    Returns True to exit, False to continue.
    """
    while True:
        choice = input("\nWould you like to exit the program? (Y = Yes / N = No): ").strip()
        if choice.lower() == 'y':
            print("Goodbye! Exiting the program.")
            return True
        elif choice.lower() == 'n':
            print("Okay, let's try again.")
            return False
        else:
            print(f"  ✘ '{choice}' is not a valid choice. Please enter Y or N.")


if __name__ == "__main__":
    print("=" * 69)
    print("                  GRADE EVALUATOR PROGRAM")
    print("=" * 69)

    while True:
        course_data = load_csv_data()
        evaluate_grades(course_data)
        if ask_to_exit():
            break
