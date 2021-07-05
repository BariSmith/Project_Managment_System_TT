from django.http import JsonResponse
from django.shortcuts import render

from .forms import ProjectForm, ProgrammerForm
from .models import Project, Programmer


def projects(request):
    project_form = ProjectForm()
    projects = Project.objects.all().order_by('-id')
    response_data = {}

    # This creates a new object
    if request.is_ajax() and request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)

        if project_form.is_valid():
            project_form.save(commit=True)

            response_data['name'] = project_form.cleaned_data['project_name']
            response_data['detail'] = project_form.cleaned_data['project_detail']
            response_data['image'] = Project.objects.get(project_name=response_data['name']).project_image.url
            response_data['id'] = Project.objects.get(project_name=response_data['name']).id

            return JsonResponse(response_data, status=200)


    if request.is_ajax() and request.method == 'GET':

        # This remove an object
        if request.GET.get('form_name') == 'delete-card':
            name = request.GET.get('project_name')
            project = Project.objects.get(project_name=name)
            project.delete()

        # This gets all the students related to a project
        if request.GET.get('form_name') == 'show-list':
            programmer_API = []
            id = request.GET.get('the_project')
            project = Project.objects.get(pk=id)
            programmer_list = Programmer.objects.filter(student_project=project)
            for programmer in programmer_list:
                response_data['image'] = programmer.programmer_image.url
                response_data['name'] = programmer.programmer_name
                response_data['deadline'] = programmer.programmer_deadline
                programmer_API.append(response_data.copy())
            return JsonResponse(programmer_API, safe=False)

    return render(request, 'app/project.html', {'project_form': project_form, 'project_list': projects})


def programmer(request):
    programmer_form = ProgrammerForm()
    programmer = Programmer.objects.all()
    projects = Project.objects.all()
    response_data = {}

    if request.is_ajax() and request.method == 'POST':
        student_form = ProgrammerForm(request.POST, request.FILES)

        # This takes new registration
        if programmer_form.is_valid() and request.POST.get('purpose') == 'create':
            programmer_form.save(commit=True)

            response_data['name'] = programmer_form.cleaned_data['student_name']
            response_data['project'] = programmer_form.cleaned_data['student_project'].project_name
            response_data['deadline'] = programmer_form.cleaned_data['student_deadline']
            response_data['image'] = Programmer.objects.get(student_name=response_data['name']).student_image.url
            response_data['id'] = Programmer.objects.get(student_name=response_data['name']).id
            print(response_data)

            return JsonResponse(response_data, status=200)

        # This modifies existing objects
        if programmer_form.is_valid() and request.POST.get('purpose') == 'edit':
            print(programmer_form.cleaned_data['programmer_name'])
            print(request.POST['programmer_name'])

            id = request.POST['student_id']
            # print(Project.objects.get(pk = request.POST['programmer_project']).project_name)
            get_project = Project.objects.get(pk = request.POST['programmer_project'])
            edit_programmer = Programmer.objects.get(pk = id)
            edit_programmer.programmer_name = request.POST['programmer_name']
            edit_programmer.programmer_project = get_project
            edit_programmer.programmer_deadline = request.POST['programmer_deadline']
            try:
                edit_programmer.programmer_image = request.FILES['programmer_image']
            # This handle any errors related to image upload
            # Django is going to ignore it in case it is empty
            except:
                pass
            edit_programmer.save()

            response_data['id'] = edit_programmer.id
            response_data['name'] = edit_programmer.programmer_name
            response_data['project'] = get_project.project_name
            response_data['deadline'] = edit_programmer.programmer_deadline
            response_data['image'] = edit_programmer.programmer_image.url
            print(response_data)

            return JsonResponse(response_data, status=200)

    # This delete an object
    if request.is_ajax() and request.method == 'GET':

        # This removes one specific item
        if request.GET.get('button_name') == 'remove-item':
            id = request.GET.get('programmer_id')
            programmer = Programmer.objects.get(pk=id)
            programmer.delete()

        # This removes multiple items
        elif request.GET.get('button_name') == 'multi-delete':
            programmers = (request.GET.getlist('programmers'))[0].split(',')
            for programmer in programmers:
                Programmer.objects.get(pk=int(programmer)).delete()

    return render(request, 'app/students.html', {'programmer_form': programmer_form,
                                                          'programmer_list': programmers,
                                                          'project_exists': projects})


def testing(request):
    list_project = Project.objects.all()
    data_test = {
        'testings': list_project,
    }
    return render(request, 'app/test.html', context=data_test)