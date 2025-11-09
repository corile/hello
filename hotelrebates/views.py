from django.shortcuts import render

from hotelrebates.forms import CalcForm

# Create your views here.
def calc (request):
    form = CalcForm()
    if request.method == 'POST':
        form = CalcForm(request.POST)
        if form.is_valid():
            # Process the valid form data
            cash_price = form.cleaned_data['cash_price']
            return render(
                request,
                'hotel_card.html',
                {
                    'form': form,
                    'hotel_name': 'Residence Inn by Marriott',
                    'price_options': [
                        {
                            'cash_price': cash_price,
                            'rebates': 10,
                            'final_price': cash_price - 10
                        },
                        {
                            'cash_price': cash_price,
                            'rebates': 20,
                            'final_price': cash_price - 20
                        },
                        {
                            'cash_price': cash_price,
                            'rebates': 30,
                            'final_price': cash_price - 30
                        }
                    ]
                })
    return render(request, 'hotel_card.html', {'form': form})