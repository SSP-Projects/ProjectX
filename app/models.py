from django.db import models
import uuid
class Centers(models.Model):
    # Campos
    center_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, help_text="Ingrese el nombre del género")
    address = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    CIF = models.CharField(max_length=9)
    email = models.EmailField(max_length=50)
    image = models.ImageField(blank =True)

'''    # Metadata
    class Meta:
        ordering = ["center_id","CIF","name","address","phone_number","email"]
    
    # Métodos
    def get_absolute_url(self):
         """
         Devuelve la url para acceder a una instancia particular de MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto MyModelName (en el sitio de Admin, etc.)
        """
        return self.field_name'''