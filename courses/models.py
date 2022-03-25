from django.db import models
from django.conf import settings

class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query)
        )

# Create your models here.
class Course(models.Model):
    #CharField input text
    name = models.CharField('Nome', max_length=100)
    #SlugField input url unico por tabela 
    #slug = models.SlugField('Atalho', primary_key=True)
    slug = models.SlugField('Atalho')
    #TextField textarea, blank = True (aceita valor vazio), 
    description = models.TextField('Descrição', blank=True)
    #TextField textarea, blank = True (aceita valor vazio), 
    content = models.TextField('Conteúdo Programado ', blank=True)
    #DateField opcional ou branco
    start_date = models.DateField('Data de Início', null=True, blank=True)
    #ImageField salva arquivos de imagem em um diretorio relativo (ver settings media_root)
    image = models.ImageField(upload_to='courses/images', null=True, blank=True, verbose_name="Imagem de Capa")
    #DateTimeField salva data hora sempre que criado o curso é adicionada o valor (auto_now_add)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    #DeteTimeField sava data hora sempre que atualizado o curso
    updated_at =models.DateTimeField('Atualizado em', auto_now=True) 

    objects = CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courses:detail_slug', args=[str(self.slug)])
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural= 'Cursos'
        ordering = ['name']

class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Usuário", on_delete=models.PROTECT,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course, verbose_name='Curso', on_delete=models.PROTECT,
        related_name='enrollments'
    )

    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, 
        default=1,blank=True
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    def active(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name= 'Inscrição'
        verbose_name_plural='Inscrições'
        unique_together=(('user','course'))

