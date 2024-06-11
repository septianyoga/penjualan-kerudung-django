from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from prediction.models import PenjualanKerudung
from .ml_models import train_model, predict_sales, plot_tree
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


model, feature_columns = train_model()
plot_tree(model, feature_columns, model.classes_)
@login_required
def models(request):
    prediction = None
    if request.method == 'POST':
        brand = request.POST.get('brand')
        jenis = request.POST.get('jenis')
        bahan = request.POST.get('bahan')
        harga = request.POST.get('harga') == 'TRUE'
        ukuran_kain = request.POST.get('ukuran_kain')
        input_data = {'brand': brand, 'jenis': jenis,
                    'bahan': bahan, 'harga': harga, 'ukuran_kain': ukuran_kain}
        prediction = predict_sales(model, feature_columns, input_data)
    return render(request, 'model/index.html', {'prediction': prediction})


@login_required
def performance(request):
    return render(request, 'performance/index.html')
