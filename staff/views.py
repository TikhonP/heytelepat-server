from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from medsenger_agent.models import Speaker
from staff.models import Issue


@staff_member_required
@require_http_methods(['GET', 'POST'])
def create_issue(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        speaker_pk = request.POST.get('speaker')
        speaker = Speaker.objects.get(pk=int(speaker_pk))
        issue = Issue.objects.create(
            description=description,
            author=request.user,
            speaker=speaker
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'speaker_issue_%s' % speaker.pk,
            {
                'type': 'receive_issue',
                'data': {'id': issue.pk}
            }
        )

    return render(request, 'add_issue.html', {
        'get': request.method == 'GET', 'speakers': Speaker.objects.filter(user=request.user)
    })


@csrf_exempt
@require_http_methods(['POST'])
def receive_file(request, issue_id: int, speaker_token: str):
    speaker = get_object_or_404(Speaker, token=speaker_token)
    issue = get_object_or_404(Issue, pk=issue_id)

    if issue.speaker != speaker:
        return HttpResponseBadRequest("Issue not related to this speaker")

    print(request.FILES)
    for file in request.FILES:
        issue.log_file = request.FILES[file]
        issue.save()
        break

    return HttpResponse()
