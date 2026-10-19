import csv
import json
import random
from datetime import date
from faker import Faker

fake = Faker("en_GB")

Faker.seed(42)
random.seed(42)

# SCHEMA: one mortgage applicant
#
# field              | type   | how it's made
# -------------------|--------|-----------------------------------------------
# annual_income      | int    | random 20,000 to 150,000
# loan_amount        | int    | annual_income x random multiplier (3 to 5)
# ltv                | float  | random 0.60 to 0.95 
# property_value     | int    | loan_amount / ltv produces in output
# applicant_id       | string | "SYN-" + padded number, e.g. SYN-0001
# full_name          | string | Faker first name + random surname from my fictional list
# application_date   | date   | random date in the last 1 to 2 years
#
# ORDER OF GENERATION:
# 1. income
# 2. loan (needs income)
# 3. LTV
# 4. property value (needs loan and LTV)
# 5. applicant_id
# 6. full_name
# 7. application_date



FICTIONAL_SURNAMES = ["Testwell", "Mockford", "Samplesmith", "Fakeness", "Dummerton","Fakeley", "Placeholder", "Examplar", "Notrealson", "Syntheton", "Pretendley", "Fictworth", "Demoman", "Mockingley", "Sandboxe", "Stubbington"]





def make_applicant(i):
# money fields: income, loan, ltv, property_value
    # 1. income
    annual_income = random.randint(20000, 150000)

    # 2. loan (needs income)
    multiplier = random.uniform(3,5)
    loan_amount = round(annual_income * multiplier)

    # 3. LTV
    ltv = random.uniform(0.60, 0.95)

    # 4. property value (needs loan and ltv)
    property_value = round(loan_amount/ltv)

    # applicant_id, full_name, application_date
    applicant_id = f"SYN-{i:04d}"

    full_name = fake.first_name()+" "+random.choice(FICTIONAL_SURNAMES)

    application_date = fake.date_between(start_date="-2y", end_date=date(2026, 10, 1))

    return {
        "applicant_id": applicant_id,
        "full_name": full_name,
        "annual_income": annual_income,
        "loan_amount": loan_amount,
        "ltv": round(ltv, 2),
        "property_value": property_value,
        "application_date": application_date.isoformat(),
    }

applicants = []
for n in range(1, 501):
    applicants.append(make_applicant(n))

with open("data/applicants.json", "w") as f:
    json.dump(applicants, f, indent=2)

with open("data/applicants.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=applicants[0].keys())
    writer.writeheader()
    writer.writerows(applicants)

print(len(applicants))