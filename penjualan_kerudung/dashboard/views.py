from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from prediction.models import PenjualanKerudung
from django.contrib import messages
import pandas as pd
# Create your views here.


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')


@login_required
def kelola_data(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)
            # Print columns to debug
            # print(df.columns)

            # Convert 'tanggal' column to date only
            df['Tanggal'] = pd.to_datetime(df['Tanggal']).dt.date

            # Clear existing data
            PenjualanKerudung.objects.all().delete()
            # return
            for _, row in df.iterrows():
                PenjualanKerudung.objects.create(
                    tanggal=f"{row.get('Tanggal')}",
                    brand=f"{row.get('Brand')}",
                    jenis=f"{row.get('Jenis')}",
                    bahan=f"{row.get('Bahan')}",
                    harga=f"{row.get('Harga')}",
                    ukuran_kain=row.get('Ukuran Kain'),
                    terjual=row.get('Terjual')
                )

            # Optionally remove the file after processing
            messages.success(request, 'Data berhasil diimport.')
        except KeyError as e:
            messages.error(request, f'Kolom tidak ditemukan: {e}')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')

        fs.delete(filename)
        return redirect('kelola_data')

    return render(request, 'kelola_data/index.html', {'penjualans': PenjualanKerudung.objects.all()})


@login_required
def preprocessing(request):
    return render(request, 'preprocessing/index.html')


@login_required
def models(request):
    return render(request, 'model/index.html')


@login_required
def performance(request):
    return render(request, 'performance/index.html')
