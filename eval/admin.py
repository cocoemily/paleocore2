from django.contrib import admin
from .models import *
from django.http import HttpResponse
import html.parser
from django.template import loader


def replace_tags(html_string):
    """
    Function to replace common HTML formatting strings with RTF encoding strings.
    :param html_string:
    :return:
    """
    result = None
    if html_string:
        rtf_string = html_string.replace("<em>", "\i ")  # Replace emphasis tag with italics
        rtf_string = rtf_string.replace("</em>", " \i0")  # Replace closing emphasis tag
        rtf_string = rtf_string.replace("<i>", "\i ")
        rtf_string = rtf_string.replace("</i>", " \i0")
        rtf_string = rtf_string.replace("<b>", r"\b ")  # Need the r to signify a raw string rather than an escape
        rtf_string = rtf_string.replace("</b>", r" \b0")
        rtf_string = rtf_string.replace("<strong>", r"\b ")
        rtf_string = rtf_string.replace("</strong>", r" \b0")
        rtf_string = rtf_string.replace("<s>", "\strike ")
        rtf_string = rtf_string.replace("</s>", " \strike0")
        rtf_string = rtf_string.replace("<p>", "")
        rtf_string = rtf_string.replace("</p>", "")
        result = rtf_string

    return result


def rtf_encode(unicode_string):
    """
    Converts HTML encoding and Unicode encoding to RTF.
    Be sure that autoescaping is off in the template. Autoescaping converts <, >, ", ', &
    The unescape function used here is helpful for catching additional escape sequences used for special
    characters, greek letters, symbols, and accents.
    :param unicode_string:
    :return:
    """
    result = None
    if unicode_string:
        html_parser = html.parser.HTMLParser()  # Create an HTML parser
        unicode_string = html.unescape(unicode_string)  # Convert html encodings to unicode e.g. &eacute -> \ex9
        rtf_bytestring = unicode_string.encode('rtfunicode')  # Convert unicode to rtf e.g. \ex9 -> \u233?
        rtf_string = rtf_bytestring.decode('utf-8')
        rtf_string = replace_tags(rtf_string)  # replaces common tags with rtf encodings
        result = rtf_string
    return result


default_list_display = ['name', 'eid', 'program', 'appointment', 'email', 'phone', 'office']
default_filters = ['program']
default_search_fields = ['name', 'last_name', 'first_name', 'former_last_name', 'nickname', 'eid']
default_read_only_fields = ['year_in_program', 'standing', 'easi_link', 'student_appointment', 'progress']
progress_fieldsets = ('Progress', {
    'fields': [
        ('incoming_degree',),
        ('ma_thesis', 'ma_thesis_date'),
        ('ma_thesis_title',),
        ('quals', 'quals_date'),
        ('prospectus', 'prospectus_date'),
        ('abd',),
        ('defense', 'defense_date'),
        ('phd_thesis_title',),
        ('phd_thesis_abstract',),
    ],
})
name_fieldsets = ('Name', {
            'fields': [('eid', 'active', 'status'),
                       ('name',),
                       ('first_name', 'last_name'),
                       ('former_last_name', 'nickname', 'gender_pronouns'),
                       ('easi_link',)
                       ]
        })
contact_fieldsets = ('Contact Information', {
            'fields': [('email', 'phone', 'office'),
                       ]
        })
concern_fieldsets = ('Concerns and Notes', {
            'fields': [
                ('concern',),
                ('remarks',)
            ]
        })


class EvaluationInline(admin.TabularInline):
    model = Evaluation
    extra = 0
    fieldsets = (
        ('Evaluations', {
            'fields': (('date', ),
                       ('adviser_questionnaire', 'student_questionnaire'),
                       ('academic_decision', 'research_decision', 'professional_decision', 'teaching_decision'),
                       ('evaluation_text',),
                       ('evaluation_remarks',)
                       )
        }),
    )


class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id']+default_list_display
    list_editable = ['program', 'appointment']
    list_display_links = ['id']
    list_filter = ['program', 'appointment']
    fieldsets = [
        ('Name', {
            'fields': [('eid',),
                       ('name',),
                       ('first_name', 'last_name'),
                       ('former_last_name', 'nickname'),
                       ]
        }),
        ('Contact Information', {
            'fields': [('email', 'phone', 'office'),
                       ]
        }),
    ]


class StudentAdmin(admin.ModelAdmin):
    list_display = ['eid', 'name', 'program', 'cohort', 'exit_semester', 'supervisor', 'status', 'active']
    readonly_fields = default_read_only_fields
    list_filter = default_filters+['supervisor', 'status', 'cola_status', 'ut_assumed_status']
    search_fields = default_search_fields
    inlines = [EvaluationInline]
    fieldsets = [
        name_fieldsets,
        contact_fieldsets,
        ('Supervisor', {
            'fields': [('program', 'cohort', 'exit_semester'),
                       ('supervisor', 'co-supervisor'),
                       ('committee',),
                       ('committee_text',),
                       ]
        }),
        progress_fieldsets,
        concern_fieldsets,
    ]

    # The Media class is used to define custom css and js for a model or form
    # https://docs.djangoproject.com/en/1.11/topics/forms/media/
    class Media:
        css = {
            'all': ('admin/css/eval.css',)  # css class to style admin list view
        }
        js = ['admin/js/eval.js']  # toggle filter lists


class ActiveStudentAdmin(admin.ModelAdmin):
    list_display = ['eid', 'name', 'program', 'cohort', 'year_in_program', 'progress', 'supervisor',
                    'standing', 'status', 'active']
    readonly_fields = default_read_only_fields
    list_filter = default_filters+['supervisor', 'cohort', 'status']
    search_fields = default_search_fields
    inlines = [EvaluationInline]
    fieldsets = [
        name_fieldsets,
        contact_fieldsets,
        ('Supervisor', {
            'fields': [('program', 'cohort'),
                       ('supervisor', 'co-supervisor'),
                       ('committee',),
                       ('committee_text',),
                       ]
        }),
        progress_fieldsets,
        concern_fieldsets,


    ]

    def get_queryset(self, request):
        return Student.objects.filter(status=progressing)

    # The Media class is used to define custom css and js for a model or form
    # https://docs.djangoproject.com/en/1.11/topics/forms/media/
    class Media:
        css = {
            'all': ('admin/css/eval.css',)  # css class to style admin list view
        }
        js = ['admin/js/eval.js']  # toggle filter lists


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['date', 'student']
    list_filter = ['date', 'student__program']
    search_fields = ['student']
    actions = ['create_eval_html']

    def create_eval_html(modeladmin, request, queryset):
        evaluations = queryset
        #for eval in evaluations:
        #    student_evals = student.eval_set.all().order_by("author_rank")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.html"'.format(evaluations[0].student)
        t = loader.get_template("eval/eval_template.html")
        c = {'data': evaluations}
        response.write(t.render(c))
        return response

    create_eval_html.short_description = "Download Evaluation Letters"


class AwardAdmin(admin.ModelAdmin):
    list_display = ['student', 'award_summary','award_amount', 'year', 'travel']
    list_filter = ['year', 'student']


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ActiveStudent, ActiveStudentAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Award, AwardAdmin)
