from django.db import models
import uuid

# help us wala sabai section ko lagi. Yo model lai entire project ma use garni.
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        abstract=True