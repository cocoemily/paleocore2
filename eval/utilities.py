import re
from .models import Faculty, Student, Award, Evaluation
from decimal import Decimal

funding_data_path = '/Users/reedd/active/_all_projects/graduate_advisor/grad_student_awards/funding_combined.txt'

def import_evals(file_path='/Users/reedd/Documents/projects/graduate_advisor/evaluations2017.csv'):
    """
    Function to read data from a delimited text file
    :return: list of header values, list of row data lists
    """
    dbfile = open(file_path)
    data = dbfile.readlines()
    dbfile.close()
    data_list = []
    header_list = data[0][:-1].split(',')  # list of column headers
    # populate data list
    for row in data[1:]:  # skip header row
        data_list.append(row[:-1].split(','))  # remove newlines and split by delimiter
    print('Importing data from {}'.format(file_path))
    return header_list, data_list


def read_file(fp, delimiter=','):
    """
    Function to read data from a delimited file.
    :param fp:
    :param delimiter:
    :return: returns a list of header values and data values
    """
    data_file = open(fp, encoding = "ISO-8859-1")  # explicit encoding for MS Excel
    data = data_file.readlines()
    data_file.close()
    data_list = []
    line_terminator = data[0][-1]
    if line_terminator != '\n':
        raise ImportError("Unknown line terminator {}".format(line_terminator))
    else:
        header_list = data[0][:-1].split(delimiter)  # list of column headers
        header_length = len(header_list)
        for row in data[1:]:  # skip header row
            data_list.append(row[:-1].split(delimiter))  # remove newlines and split by delimiter
        print('Importing data from {}'.format(fp))
        return header_list, data_list


def write_data(hl, dl):
    faculty_list = []

    for row in dl:
        print(row)
        row_list = row
        name_list = row[0].replace(' ', '').split(',')  # remove whitespaces and split on commas
        prog = row_list[6].strip()
        program = None
        prog_dict = {'Archaeology':'Archaeology', 'Biological': 'Biological Anthropology',
                     'Linguistics': 'Linguistic Anthropology', 'Sociocultural': 'Sociocultural Anthropology'}
        if prog in  prog_dict.keys():
            program = prog_dict[prog]
        if row_list[7] not in faculty_list:
            supervisor = Faculty.objects.create(last_name=row_list[7], program=program)
            faculty_list.append(row_list[7])
        else:
            supervisor = Faculty.objects.get(last_name__exact=row_list[7])
        res = row_list[12].replace('Intnl', 'International')
        if row_list[13].replace(' ','') == 'ABD':
            abd=True
        else:
            abd=False
        if row_list[14].replace(' ','') == 'non-Texas':
            texas_resident = False
        elif row_list[14].replace(' ','') == "Texas":
            texas_resident = True
        else:
            texas_resident = None
        reg = None
        reg_str = row_list[16].replace(' ', '')
        if reg_str == 'p/t':
            reg = 'Part-time'
        elif reg_str == 'ft':
            reg = 'Full-time'
        elif reg_str == 'ISR':
            reg = 'ISR'
        Student.objects.create(
            last_name=row[0].replace('"', ''),
            first_name=row[1].replace('"', ''),
            former_last_name=row_list[2],
            nickname=row_list[3],
            eid=row_list[4],
            cohort=row_list[5],
            program=program,
            supervisor=supervisor,
            residence=res,
            abd=abd,
            texas_resident=texas_resident,
            registration=reg,
            remarks=row_list[17]
        )


def import_profile_data(hl, dl):
    for row in dl:
        print(row)
        #  0 'EID',
        #  1 'Name',
        #  2 'Department',
        #  3 'Current or Last Known Major',
        #  4 'Degree Sought',
        #  5 'Current or Last Known Exit Status'
        update_dict = dict([('name', row[1]), ('cola_status', row[5])])
        student, created = Student.objects.update_or_create(eid=row[0], defaults=update_dict)


def import_grad_status(dl):
    for row in dl:
        print(row)
        #  0 'Name',
        #  1 'EID',
        #  2 'WDNote',
        #  3 'FirstSemestter',
        #  4 'LastSemestter',
        #  5 'AcademicStatus'
        #  6 'DerivedStatus'
        #  7 'SchoolMajor'
        #  8 'ProgramCode'
        if row[3] and row[4]:
            update_dict = dict([
                ('ut_withdrawn', row[2]),
                ('first_semester', row[3]),
                ('last_semester', row[4]),
                ('ut_assumed_status', row[5]),
                ('ut_derived_status', row[6]),
                ('ut_school_major', row[7]),
                ('ut_program_code', row[8]),
                                ])
        else:
            update_dict = dict([
                ('ut_withdrawn', row[2]),
                ('first_semester', None),
                ('last_semester', None),
                ('ut_assumed_status', row[5]),
                ('ut_derived_status', row[6]),
                ('ut_school_major', row[7]),
                ('ut_program_code', row[8]),
                                ])

        student, created = Student.objects.update_or_create(eid=row[1], defaults=update_dict)
        if not student.name:
            student.name = row[0]
        if row[3] and not student.cohort:
            student.cohort = row[3]
        student.save()


def import_awards(hl, dl):
    for i in dl:
        eid = i[1]
        if Student.objects.filter(eid=eid).count()==1:  # if eid matches a student in the DB
            idict = dict(zip(hl, i))  # create a dictionary from two lists
            student = Student.objects.get(eid=eid) #
            idict['student'] = student
            idict.pop('eid')
            if idict['travel']=='Y':  # convert "Y,N" to "True, False"
                idict['travel']=True
            else:
                idict['travel']=False
            amount=re.sub('[^\d\.]', '', idict['award_amount']), # remove extra characters
            idict['award_amount']=amount[0]
            Award.objects.get_or_create(award_id=idict['award_id'], defaults=idict)


def update_decisions():
    evals = Evaluation .objects.all()
    for e in evals:
        if e.academic_decision == 'Sufficient':
            e.academic_decision = 'Good'
        if e.research_decision == 'Sufficient':
            e.research_decision = 'Good'
        if e.professional_decision == 'Sufficient':
            e.professional_decision = 'Good'
        if e.teaching_decision == 'Sufficient':
            e.teaching_decision = 'Good'
        if e.evaluation_decision == 'Sufficient':
            e.evaluation_decision == 'Good'
        e.save()



