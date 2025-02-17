from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import PenjualanKerudung, ProcessingDataLatih, ModelPerformance
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse


from .ml_models import train_model, predict_sales, plot_tree


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
    return render(request, 'preprocessing/index.html', {'processings': ProcessingDataLatih.objects.all()})


@login_required
def processing_data_v(request):
    data = PenjualanKerudung.objects.all()

    if not data.exists():
        return

    # Konversi queryset ke DataFrame untuk pemrosesan yang lebih mudah
    import pandas as pd
    df = pd.DataFrame(list(data.values()))

    # Hitung nilai tengah, tertinggi, dan terendah untuk harga
    harga_max = df['harga'].max()
    harga_min = df['harga'].min()
    harga_mid = (harga_max + harga_min) / 2

    # Hitung nilai tengah untuk terjual
    terjual_max = df['terjual'].max()
    terjual_min = df['terjual'].min()
    terjual_mid = (terjual_max + terjual_min) / 2

    # Fungsi untuk mengkategorikan harga
    def categorize_harga(harga):
        if harga >= harga_mid:
            return 'tinggi'
        elif harga <= harga_min:
            return 'rendah'
        else:
            return 'sedang'

    # Fungsi untuk mengkategorikan terjual
    def categorize_terjual(terjual):
        if terjual >= terjual_mid:
            return 'laku tinggi'
        else:
            return 'laku rendah'

    # Proses data dan masukkan ke dalam ProcessingDataLatih
    processing_data = []
    for _, row in df.iterrows():
        processing_data.append(ProcessingDataLatih(
            brand=row['brand'],
            jenis=row['jenis'],
            bahan=row['bahan'],
            harga=categorize_harga(row['harga']),
            terjual=categorize_terjual(row['terjual']),
        ))

    # Hapus semua data lama di ProcessingDataLatih
    ProcessingDataLatih.objects.all().delete()
    # Bulk create data baru
    ProcessingDataLatih.objects.bulk_create(processing_data)

    return redirect('preprocessing')


@login_required
def models(request):
    prediction = None
    data = ProcessingDataLatih.objects.all()
    if request.method == 'POST':
        model, feature_columns = train_model()
        plot_tree(model, feature_columns, model.classes_)
        brand = request.POST.get('brand')
        jenis = request.POST.get('jenis')
        bahan = request.POST.get('bahan')
        harga = request.POST.get('harga')
        input_data = {'brand': brand, 'jenis': jenis,
                      'bahan': bahan, 'harga': harga}
        prediction = predict_sales(model, feature_columns, input_data)
    return render(request, 'model/index.html', {'prediction': prediction, 'data': data})


@login_required
def performance(request):
    performance = ModelPerformance.objects.last()
    return render(request, 'performance/index.html',  {'performance': performance})
