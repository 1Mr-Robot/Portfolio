from django.templatetags.static import static

def get_og_image_url(request, image):
    if image:
        return request.build_absolute_uri(image.url)
    return request.build_absolute_uri(static('og.jpg'))

def get_og_image_alt(alt):
    if alt:
        return alt
    return 'Portfolio profesional de Uziel Flores'