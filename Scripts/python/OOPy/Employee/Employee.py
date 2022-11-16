import pprint


class Employee:
    def __init__(self, firstname:str, lastname: str, date_of_birth: str, sin: str):
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.sin = sin

    def generate_email(self):
        self.email = "{}.{}@{}.com".format(self.firstname.replace(' ','').replace('-', '_'),
                                           self.lastname.replace(' ','').replace(' ','').replace('-','_'),
                                           'gmail')
        return self.email


if __name__ == '__main__':
    list_Employees = list()
    e1 = Employee('John', 'Smith', '1972-02-07', '589456789')
    e1.generate_email()
    list_Employees.append(e1.__dict__)
    e2 = Employee('Jane', 'Doe', '2002-08-12', '589456789')
    e2.generate_email()
    list_Employees.append(e2.__dict__)
    pprint.pprint(list_Employees, indent=4)