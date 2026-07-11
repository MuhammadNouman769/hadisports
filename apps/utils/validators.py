from django.core.exceptions import ValidationError


""" ================= Validators =============== """

def validate_image_size(image):
    max_size = 5 * 1024 * 1024

    if image.size > max_size:
        raise ValidationError(
            "Image size cannot exceed 5 MB."
        )


def validate_file_size(file):
    max_size = 10 * 1024 * 1024

    if file.size > max_size:
        raise ValidationError(
            "File size cannot exceed 10 MB."
        )