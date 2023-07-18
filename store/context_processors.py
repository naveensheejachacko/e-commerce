from categories.models import  Main_Category,Sub_Category

def menu_links(request):
    links=Main_Category.objects.all()
    sub=Sub_Category.objects.all()
    return dict(links=links,sub=sub)
