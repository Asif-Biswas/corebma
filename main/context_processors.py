from .models import Text

def text(request):
    return {'text': Text.objects.all().order_by('id').last()}