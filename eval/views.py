from django.views import generic
from .models import Student


class ActiveStudentListView(generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    model = Student
    template_name = 'eval/student_index.html'

    def get_queryset(self):
        return Student.objects.filter(active=True).order_by('name')


class ActiveStudentDetailView(generic.DetailView):
    template_name = 'eval/student_detail.html'

    def get_queryset(self):
        return Student.objects.filter(active=True)

