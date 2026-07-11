import os
import uuid

""" ================ File Upload Helper =============== """

def upload_to(instance, filename):
    ext = filename.split(".")[-1]

    filename = f"{uuid.uuid4().hex}.{ext}"

    model = instance.__class__.__name__.lower()

    return os.path.join(model, filename)