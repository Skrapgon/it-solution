import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quote
from django.contrib import messages

@login_required
def add_quote(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        source = request.POST.get('source')
        source_type = request.POST.get('source_type')
        priority = request.POST.get('priority', 1)

        if not Quote.can_add_quote(request.user, text, source, source_type):
            messages.error(request, 'Цитата уже существует или у указанного произведения 3 цитаты')
        else:
            Quote.objects.create(
                user=request.user,
                text=text,
                source=source,
                source_type=source_type,
                priority=priority
            )
            return redirect('my_quotes')

    return render(request, 'quotes/add_quote.html')


@login_required
def my_quotes(request):
    quotes = Quote.objects.filter(user=request.user)
    return render(request, 'quotes/my_quotes.html', {'quotes': quotes})


@login_required
def random_quote(request):
    quotes = list(Quote.objects.all())
    if quotes:
        weights = [q.priority for q in quotes]
        quote = random.choices(list(quotes), weights=weights, k=1)[0]
        quote.views += 1
        quote.save()
        return render(request, 'quotes/random_quote.html', {'quote': quote})
    else:
        messages.info(request, 'Цитат пока нет')
        return redirect('my_quotes')


@login_required
def like_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.likes.add(request.user)
    quote.dislikes.remove(request.user)
    return redirect('random_quote')


@login_required
def dislike_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.dislikes.add(request.user)
    quote.likes.remove(request.user)
    return redirect('random_quote')

@login_required
def top_10_quotes(request):
    top_quotes = list(Quote.get_top_n_by_likes(10))
    if not top_quotes:
        messages.info(request, 'Цитат пока нет')
        return redirect('my_quotes')
    return render(request, 'quotes/top_10_quotes.html', {'quotes': top_quotes})