from django.db import models

class PenjualanKerudung(models.Model):
    tanggal = models.DateField()
    brand = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    bahan = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    ukuran_kain = models.DecimalField(max_digits=5, decimal_places=2)
    terjual = models.IntegerField()

    def __str__(self):
        return f"{self.brand} - {self.jenis} ({self.tanggal})"


class ProcessingDataLatih(models.Model):
    brand = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    bahan = models.CharField(max_length=100)
    harga = models.CharField(max_length=100)
    ukuran_kain = models.CharField(max_length=100)
    terjual = models.CharField(max_length=100)

    # def __str__(self):
    #     return f"{self.brand} - {self.jenis}"
