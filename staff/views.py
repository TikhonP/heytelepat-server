from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from medsenger_agent.models import Speaker
from staff.models import Issue


def publish_issue_to_slack(issue: Issue):
    client = WebClient(token=settings.SLACK_TOKEN)

    text = f"""Добавлена новая проблема с колонкой от *{issue.author.first_name}*:
{issue.description} <http://{settings.DOMAIN}{issue.log_file.url}|Скачать лог>
"""

    try:
        result = client.chat_postMessage(
            channel=settings.SLACK_CHANNEL_ID,
            text=text,
            mrkdwn=True
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")


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

        publish_issue_to_slack(issue)
        break

    return HttpResponse()


@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u: u.is_superuser)
def staff_main(request):
    if request.method == 'POST':
        issue = get_object_or_404(Issue, pk=request.POST.get('issue_id'))
        issue.is_closed = True
        issue.save()

    return render(request, 'staff_main.html', {
        'issues': Issue.objects.filter(is_closed=False)
    })
