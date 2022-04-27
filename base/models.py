import hashlib

from django.db import models
from django.utils.text import slugify
from cms.models import Recurso

from base.managers import NoticiaQueryset, test_url, build_wordcloud


class Termo(models.Model):
    termo = models.CharField(max_length=120, unique=True)
    texto_explicativo = models.TextField(null=True)
    id_externo = models.BigIntegerField(null=True, blank=True)
    num_reads = models.BigIntegerField('Núm.Acessos', default=0)

    class Meta:
        verbose_name = 'Termo'
        verbose_name_plural = 'Termos'

    def __str__(self):
        return self.termo

    def tot_noticias(self):
        return self.assunto_set.count() or 0
    tot_noticias.short_description = "Total de Notícias"

URL_MAX_LENGTH = 500


class Noticia(models.Model):
    dt = models.DateField(db_index=True)
    url = models.URLField(max_length=URL_MAX_LENGTH)
    url_hash = models.CharField(max_length=64, unique=True)
    url_valida = models.BooleanField('URL Válida', default=False)
    atualizado = models.BooleanField('Texto atualizado', default=False)
    revisado = models.BooleanField('Texto revisado', default=False)
    titulo = models.TextField('Título')
    texto = models.TextField('Texto Base', null=True, blank=True)
    media = models.URLField('Imagem', max_length=400, null=True, blank=True)
    imagem = models.CharField('Imagem Local', max_length=100, null=True, blank=True)
    fonte = models.CharField('Fonte da Notícia', max_length=80, null=True, blank=True)
    texto_completo = models.TextField('Texto Completo', null=True, blank=True)
    nuvem = models.TextField(null=True, blank=True)
    texto_busca = models.TextField(null=True, blank=True)
    id_externo = models.IntegerField(null=True, blank=True, db_index=True)

    objects = NoticiaQueryset.as_manager()

    def gerar_nuvem(self):
        if not self.texto_completo:
            return None, None
        texto = self.texto_completo + ' ' + self.texto + ' ' + self.titulo
        for assunto in self.assunto_set.all():
            texto += ' ' + assunto.termo.termo

        stopwords = Recurso.objects.get_or_create(recurso='TAGS-EXC')[0].valor or ''
        stopwords = stopwords.lower()
        stopwords = [exc.strip() for exc in stopwords.split(',')] if stopwords else []
        return build_wordcloud(texto, [], stopwords)

    class Meta:
        verbose_name = 'Notícia'
        ordering = ('dt',)

    def __str__(self):
        return u'%s' % self.titulo

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = hashlib.sha256(self.url.encode('utf-8')).hexdigest()

        if not self.url_valida:
            self.url_valida = test_url(self.url)

        nuvem, nuvem_sem_bigramas = self.gerar_nuvem()
        if nuvem:
            # Retorna apenas as palavras que tenham frequência > 2
            # ou então toda a lista caso todos tenham frequência menor que 2
            limit = 0
            for word, cnt in nuvem.most_common():
                if cnt > 2:
                    limit += 1
                else:
                    break
            if limit == 0: limit = None
            self.nuvem = nuvem.most_common(limit)
            busca = ''
            for item,count in nuvem_sem_bigramas.most_common():
                busca += item+' '
            self.texto_busca = busca
        super(Noticia, self).save(*args, **kwargs)


class AssuntoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('termo')


class Assunto(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    termo = models.ForeignKey(Termo, on_delete=models.CASCADE)
    id_externo = models.IntegerField(null=True, blank=True)

    objects = AssuntoManager()

    class Meta:
        indexes = [
            models.Index(fields=['termo', 'id_externo'], name='termo_idx'),
        ]

    def __str__(self):
        return '%s' % self.noticia


class Busca(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=20, db_index=True)
    count = models.IntegerField()
    busca = models.TextField()

    def __str__(self):
        return '%s' % self.busca

    def save(self, *args, **kwargs):
        self.hash = slugify(self.busca)
        self.count = 0
        super(Busca, self).save(*args, **kwargs)
