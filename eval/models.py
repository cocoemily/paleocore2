from django.db import models
import datetime
from django.utils.safestring import mark_safe

PROGRAM_CHOICES = (('Archaeology', 'Archaeology'),
                   ('Biological Anthropology', 'Biological Anthropology'),
                   ('Linguistic Anthropology', 'Linguistic Anthropology'),
                   ('Sociocultural Anthropology', 'Sociocultural Anthropology'), )

RESIDENCY_CHOICES = (('US', 'US'), ('International', 'International'), ('PRA', 'PRA'))

REGISTRATION_CHOICES = (('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('ISR', 'ISR'),
                        ('Graduated', 'Graduated'), ('Exited', 'Exited'), ('On Leave', 'On Leave'))

PROGRESS_CHOICES = (('Admitted', 'Admitted'), ('Qualifying Exams', 'Qualifying Exams'), ('MA Thesis', 'MA Thesis'),
                    ('Candidacy', 'Candidacy'),
                    ('Defense', 'Defense'),
                    ('Revisions', 'Revisions'),
                    ('Graduated', 'Graduated'),
                    ('Departed', 'Departed'))

sufficient = "Good"  # Meeting or exceeding expectations
concern = "Concern"
probation = "Serious Concern"

EVALUATION_CHOICES = ((sufficient, 'Good'), (concern, 'Concern'), (probation, 'Serious Concern'))

# Status choices and variable declarations
exited = 'Exited'
exited_ma = 'Exited MA'
exited_phd = 'Exited PhD'
progressing = 'Progressing'
STATUS_CHOICES = ((progressing, 'Progressing'),
                  (exited, 'Exited'),
                  (exited_ma, 'Exited MA'),
                  (exited_phd, 'Exited PhD'),
                  )

lecturer = 'lecturer'
assistant_professor = 'assistant_professor'
associate_professor = 'associate_professor'
professor = 'professor'
emeritus = 'emeritus'
FACULTY_APPOINTMENT_CHOICES = ((emeritus, 'emeritus'),
                       (professor, 'professor'),
                       (associate_professor, 'associate_professor'),
                       (assistant_professor, 'assistant_professor'),
                       (lecturer, 'lecturer')
                       )

mastudent = 'MA student'
ma = 'MA'
phdstudent = 'PhD student'
phdcandidate = 'PhD candidate'
phd = 'PhD'
STUDENT_APPOINTMENT_CHOICES = (
    (mastudent, 'MA student'),
    (phdstudent, 'PhD student'),
    (phdcandidate, 'PhD candidate')
)


student_self_evaluation = 'Student'
faculty_student_evaluation = 'Faculty'
EVALUATION_TYPE_CHOICES = (
    (student_self_evaluation, 'Student self evaluation'),
    (faculty_student_evaluation, 'Faculty student evaluation')
)

he = 'he/him/his'
her = 'she/her/hers'
they = 'they/them/theirs'
PRONOUN_CHOICES = (
    (he, he),
    (her, her),
    (they, they)
)


class Person(models.Model):
    eid = models.CharField(max_length=10, null=True, blank=True, help_text='UT EID', unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    #full_name = models.CharField(max_length=255, null=True, blank=True)
    former_last_name = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    office = models.CharField(max_length=255, null=True, blank=True)
    # program = academic subfield
    gender_pronouns = models.CharField(max_length=255, null=True, blank=True, choices=PRONOUN_CHOICES)
    program = models.CharField(max_length=255, null=True, blank=True, choices=PROGRAM_CHOICES)

    def __str__(self):
        """
        Define the string representation for a Person object. Returns name with eid in parentheses if name is available
        Otherwise returns just eid
        :return:
        """
        if self.name:
            return self.name+' ({})'.format(self.eid)
        elif self.last_name and self.first_name:
            return self.last_name+', '+self.first_name+' ({})'.format(self.eid)
        else:
            return str(self.eid)


class Faculty(Person):
    appointment = models.CharField(max_length=100, null=True, blank=True,
                                   choices=FACULTY_APPOINTMENT_CHOICES)

    class Meta:
        verbose_name_plural = 'Faculty'
        ordering = ['name']


DEGREE_CHOICES = (
    ('BA', 'BA'),
    ('MA', 'MA')
)


class Student(Person):

    supervisor = models.ForeignKey(to=Faculty, related_name='student_supervisor', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    cosupervisor = models.ForeignKey(to=Faculty, related_name='student_cosupervisor', name='co-supervisor',
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL)
    #appointment = models.CharField(null=True, blank=True, choices=STUDENT_APPOINTMENT_CHOICES)
    committee_text = models.TextField(null=True, blank=True)
    committee = models.ManyToManyField(Faculty, blank=True)
    cohort = models.IntegerField(null=True, blank=True)
    exit_semester = models.IntegerField(null=True, blank=True)
    first_semester = models.IntegerField(null=True, blank=True)
    last_semester = models.IntegerField(null=True, blank=True)
    residence = models.CharField(max_length=255, null=True, blank=True, choices=RESIDENCY_CHOICES)
    texas_resident = models.NullBooleanField()
    home_town = models.TextField(max_length=255, null=True, blank=True)
    prior_institution = models.TextField(max_length=255, null=True, blank=True)
    prior_degree = models.TextField(max_length=255, null=True, blank=True)
    incoming_degree = models.CharField(max_length=100, null=True, blank=True, choices=DEGREE_CHOICES)

    # Deprecated Fields from import
    cola_status = models.TextField(max_length=255, null=True, blank=True)
    ut_assumed_status = models.CharField(max_length=255, null=True, blank=True)
    ut_derived_status = models.CharField(max_length=255, null=True, blank=True)
    ut_school_major = models.CharField(max_length=20, null=True, blank=True)
    ut_program_code = models.CharField(max_length=20, null=True, blank=True)
    ut_withdrawn = models.CharField(max_length=20, null=True, blank=True)

    active = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS_CHOICES)

    abd = models.BooleanField(default=False)
    registration = models.CharField(max_length=255, null=True, blank=True, choices=REGISTRATION_CHOICES,
                                    help_text='Registration Status')
    enrollment = models.CharField(max_length=255, null=True, blank=True)
    concern = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)

    # Progress Fields
    track = models.IntegerField(default=6)  # values should be 5 for PhD and 6 for MA + PHD

    ma_thesis = models.BooleanField(default=False, help_text='Has completed MA thesis/report')
    ma_thesis_date = models.DateField(null=True, blank=True)
    ma_thesis_title = models.TextField(null=True, blank=True)

    quals = models.BooleanField(default=False)
    quals_date = models.DateField(null=True, blank=True)

    phd_admitted = models.BooleanField(default=False, blank=True, help_text='Has been admitted to the PhD program')
    phd_admitted_date = models.DateField(null=True, blank=True)
    prospectus = models.BooleanField(default=False, help_text='Has defended a PhD prospectus/proposal')
    prospectus_date = models.DateField(null=True, blank=True)
    defense = models.BooleanField(default=False, help_text='Has defended a PhD dissertation')
    defense_date = models.DateField(null=True, blank=True)
    revisions = models.BooleanField(default=False)
    revisions_date = models.DateField(null=True, blank=True)
    graduated = models.BooleanField(default=False, help_text='Has graduated and exited the program')
    graduated_date = models.DateField(null=True, blank=True)
    exited = models.BooleanField(default=False)
    exited_date = models.DateField(null=True, blank=True)
    summer_funding = models.TextField(null=True, blank=True)

    phd_thesis_title = models.TextField(null=True, blank=True)
    phd_thesis_abstract = models.TextField(null=True, blank=True)

    student_eval_2018 = models.BooleanField(default=False)
    fac_eval_2018 = models.BooleanField(default=False)

    # Deprecated
    courses = models.BooleanField(default=False)
    courses_date = models.DateField(null=True, blank=True)
    language = models.BooleanField(default=False)
    language_date = models.DateField(null=True, blank=True)

    def year_in_program(self):
        """
        Calculates the number of years a student has been in the program. Students in fall cohorts switch over
        in September.
        :return:
        """
        yip = 0
        today = datetime.date.today()
        current_year, current_month = today.year, today.month
        if len(str(self.cohort)) == 5:  # e.g. '20139'
            cohort_year = int(str(self.cohort)[:4])  # e.g. 2013
            cohort_month = int(str(self.cohort)[4])  # e.g. 9
            if cohort_month == 9:
                if current_month in list(range(1, 10)):  # [1, 2 ... , 9]
                    yip = current_year - cohort_year
                elif current_month in list(range(10, 13)):
                    yip = current_year - cohort_year + 1
            if cohort_month == 2:
                yip = current_year - cohort_year + 1
        return yip

    def semesters_in_program(self):
        """
        Calculates the number of the current semester that a student has been enrolled
        :return:
        """
        pass

    class Meta:
        ordering = ['cohort', 'name']

    def standing(self):
        overall_standing = None
        evals = Evaluation.objects.filter(student=self)  # get all evaluations for a student
        if evals:
            latest_eval = evals.get(date=max(eval.date for eval in evals))  # get the latest evaluation
            standings = [latest_eval.academic_decision, latest_eval.research_decision, latest_eval.teaching_decision,
                     latest_eval.professional_decision]
            if probation in standings:
                overall_standing = probation
            elif concern in standings:
                overall_standing = concern
            elif sufficient in standings:
                overall_standing = sufficient

        return overall_standing

    def easi_link(self):
        easi_url_string = u"<a href=https://utdirect.utexas.edu/easi/index.WBX?s_pref_eid={}/" \
               "&easi_process=STUDENT_REC_INFO&easi_process_title=View+Student+" \
               "Record&easi_fwp=STUDENT_REC_INFO++++-02&" \
               "easi_fm=STUDENT_REC_INFO++++-02-02&eqs_submit=go target='_blank'>EASI RECORD</a>".format(self.eid)
        return mark_safe(easi_url_string)

    def student_appointment(self):
        appointment = ''
        if self.ma_thesis:
            if self.quals:
                if self.prospectus:
                    if self.defense and self.graduated:
                        appointment=phd
                    else:
                        appointment=phdcandidate
                else:
                    appointment=phdstudent
            else:
                appointment=mastudent
        if self.ma_thesis and self.graduated:
            appointment = ma
        return appointment

    def progress(self):
        """
        Calculates the progress score relative to milestones and timeline
        :return:
        """
        pscore = 0
        if self.ma_thesis:
            pscore += 4
        if self.quals:
            pscore += 1
        if self.prospectus:
            pscore += 1

        if self.year_in_program():
            pscore = pscore-self.year_in_program()

        return pscore


class ActiveStudent(Student):
    class Meta:
        proxy = True


class Evaluation(models.Model):
    # year is deprecated and replaced by date, remove field #
    year = models.IntegerField(null=True, blank=True)  # DEPRECATED
    type = models.CharField(max_length=255, null=True, blank=True, choices=EVALUATION_TYPE_CHOICES)
    date = models.DateField(null=True, blank=True)
    student = models.ForeignKey(to=Student, null=True, blank=True, on_delete=models.CASCADE)
    adviser_questionnaire = models.BooleanField(default=False)
    student_questionnaire = models.BooleanField(default=False)
    evaluation_decision = models.CharField(max_length=255, null=True, blank=True, choices=EVALUATION_CHOICES)
    academic_decision = models.CharField(max_length=50, null=True, blank=True, choices=EVALUATION_CHOICES)
    research_decision = models.CharField(max_length=50, null=True, blank=True, choices=EVALUATION_CHOICES)
    professional_decision = models.CharField(max_length=50, null=True, blank=True, choices=EVALUATION_CHOICES)
    teaching_decision = models.CharField(max_length=50, null=True, blank=True, choices=EVALUATION_CHOICES)
    commendations = models.TextField(null=True, blank=True)
    evaluation_text = models.TextField(null=True, blank=True)
    evaluation_remarks = models.TextField(null=True, blank=True)
    registration = models.CharField(max_length=255, null=True, blank=True, choices=REGISTRATION_CHOICES,
                                    help_text='Registration Status')

    def __str__(self):
        return self.student.last_name+' '+str(self.year)

    class Meta:
        ordering = ['year', 'student__name']


class Award(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    student = models.ForeignKey(Student, null=True, blank=True,
                                on_delete=models.CASCADE) # Note if student is deleted then so is funding!
    award_id = models.CharField(max_length=30, null=True, blank=True)
    doc_id = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.BigIntegerField(null=True, blank=True)
    account_title = models.CharField(max_length=255, null=True, blank=True)
    award_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    award_status = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    award_summary = models.CharField(max_length=255, null=True, blank=True)
    recipient_major = models.CharField(max_length=255, null=True, blank=True)
    recipient_classification = models.CharField(max_length=30, null=True, blank=True)
    gpa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    residency = models.CharField(max_length=100, null=True, blank=True)
    distribution_method = models.CharField(max_length=100, null=True, blank=True)
    travel = models.NullBooleanField()
    destination = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
