import csv
from faker import Faker
import codecs
import random
import datetime



def generate_fake_jira_report():

    """Generate fake JIRA CSV Report"""

    # Initialize Faker object
    fake = Faker()

    # Define the headers for the CSV file
    headers = ['ReportDate', 'Key', 'IssueType', 'Summary', 'Description', 'Requestor', 'Assignee', 'FixVersion', 'EpicLink', 'Sprint',
               'Status', 'CreatedDate', 'UpdatedDate', 'DueDate']

    # Define the number of rows to generate
    num_rows = 500

    # Define the possible issue types
    issue_types = ['Bug', 'Task', 'Story', 'Epic']

    # Define the possible statuses
    statuses = ['To Do', 'In Progress', 'In Review', 'Done']

    # Define the possible sprints
    sprints = ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4']

    fake_names = ["Adam Sandler", "Buddy Love", "John Smith", "Jane Doe", "William Shatner", "Michael Frown"]

    epics = []
    report_date = "2023-05-03"

    # Open a CSV file for writing
    with codecs.open(r'D:\workspace\test_data_{}.csv'.format(report_date), 'w', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)

        # Write the headers to the file
        writer.writerow(headers)

        # Generate rows of data
        for i in range(6, num_rows+5):
            # Generate random data for each row
            key = f"PROJ-{i + 1}"
            issue_type = random.choice(issue_types)
            summary = fake.sentence(nb_words=6)
            description = fake.text(max_nb_chars=200)
            requestor = random.choice(fake_names)
            assignee = random.choice(fake_names)
            fix_version = f"1.0.{random.randint(1, 5)}"
            epic_link = f"PROJ-{random.randint(1, 5)}"
            sprint = random.choice(sprints)
            status = random.choice(statuses)
            created_date = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            updated_date = (datetime.datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
            due_date = (datetime.datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                days=random.randint(10, 90))).strftime('%Y-%m-%d %H:%M:%S')

            # Write the data to the CSV file
            writer.writerow(
                [report_date, key, issue_type, summary, description, requestor, assignee, fix_version, epic_link, sprint, status,
                 created_date, updated_date, due_date])

    # Print a message indicating that the data has been generated
    print(f"{num_rows} rows of test data have been generated and saved to test_data.csv")



if __name__ == '__main__':
    generate_fake_jira_report()
    pass