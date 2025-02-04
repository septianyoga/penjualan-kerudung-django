from django.db import models


class PenjualanKerudung(models.Model):
    tanggal = models.DateField()
    brand = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    bahan = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    terjual = models.IntegerField()

    def __str__(self):
        return f"{self.brand} - {self.jenis} ({self.tanggal})"


class ProcessingDataLatih(models.Model):
    brand = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    bahan = models.CharField(max_length=100)
    harga = models.CharField(max_length=100)
    terjual = models.CharField(max_length=100)

    # def __str__(self):
    #     return f"{self.brand} - {self.jenis}"


class ModelPerformance(models.Model):
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
