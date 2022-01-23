import re
from binascii import a2b_base64
from urllib.parse import unquote
from random import shuffle

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Word, Game
from .forms import StartForm, HostForm, CategoryForm, WordForm


N_WORD_CHOICES = 4


def host(request):
    form = HostForm()
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            n_rounds = form.cleaned_data['n_rounds']
            game = Game(n_rounds=n_rounds)
            game.save()
            return redirect(f'/start?&alert=Game created with id {game.pk}')
    return render(request, 'drawing/host.html', {'form': form})


def index(request):
    return HttpResponseRedirect('/start')


def start(request):
    error = ''
    form = StartForm()
    if request.method == 'POST':
        form = StartForm(request.POST)
        if form.is_valid():
            first = (form.cleaned_data['player'] == 'First')
            game_id = form.cleaned_data['id']
            game = Game.objects.filter(id=game_id)
            if not game:
                error = 'Game not found!'
            else:
                game = game[0]
                game.start()
                if first:
                    player = 'first'
                else:
                    player = 'second'
                if game.turn != first:
                    return HttpResponseRedirect(f'/play/{game_id}/{player}/choose_cat')
                else:
                    return HttpResponseRedirect(f'/play/{game_id}/{player}/guess_wait')
    params = {'form': form, 'error': error, 'alert_type': request.GET.get('alert_type', ''),
              'alert': request.GET.get('alert', '')}
    return render(request, 'drawing/start.html', params)


def choose_cat(request, game_id, player, alert=''):
    game = get_object_or_404(Game, pk=game_id)
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category']
            category = Category.objects.get(name=category_name)
            game.current_category = category
            game.save()
            if player == 'first':
                return HttpResponseRedirect(f'/play/{game_id}/first/choose_word/cat={category.id}')
            else:
                return HttpResponseRedirect(f'/play/{game_id}/second/choose_word/cat={category.id}')
    params = {'form': form, 'game': game, 'player': player, 'alert': alert}
    return render(request, 'drawing/choose_category.html', params)


def choose_word(request, game_id, player, category_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        words = request.session['choice_words']
        form = WordForm(words=words, data=request.POST)
        print(form.fields['word'].choices)
        for field in form:
            print("Field Error:", field.name,  field.errors)
        if form.is_valid():
            print(form.cleaned_data['word'])
            word = get_object_or_404(Word, word=form.cleaned_data['word'])
            game.secret_word = word
            game.save()
            if player == 'first':
                return HttpResponseRedirect(f'/play/{game_id}/first/draw')
            else:
                return HttpResponseRedirect(f'/play/{game_id}/second/draw')
    else:
        words = game.generate_words(N_WORD_CHOICES, category_id=category_id)
        request.session['choice_words'] = words
        form = WordForm(words=words)
        context = {'form': form, 'game': game, 'player': player, 'category_id': category_id}
        return render(request, 'drawing/choose_word.html', context)


def draw(request, game_id, player):
    game = get_object_or_404(Game, pk=game_id)
    context = {'game': game, 'player': player}
    if request.is_ajax():
        # DON'T YOU DARE TOUCH THIS
        datauri = unquote(request.body)
        imgstr = re.search(r'base64,(.*)', datauri).group(1)
        binary_data = a2b_base64(imgstr)
        path = f'drawing/static/jpg/game{game_id}_pic.jpg'
        out = open(path, 'wb')
        out.write(binary_data)
        out.close()
        time_elapsed = int(request.POST.get('time_elapsed', None))
        word = get_object_or_404(Word, word=game.secret_word)
        category = word.category_id
        base_points = category.points
        converted_points = game.points_converter(base_points, time_elapsed)
        game.add_points(player, converted_points)
        if not game.end_turn():
            return HttpResponseRedirect(request, f'/{game.id}/{player}/end')
        return HttpResponse('')
    return render(request, 'drawing/draw.html', context)


def guess(request, game_id, player):
    game = get_object_or_404(Game, pk=game_id)
    category = get_object_or_404(Category, pk=game.current_category.id)
    if request.method == 'POST':
        words = request.session['choice_words']
        form = WordForm(words=words, data=request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            if word == game.secret_word.word:
                game.add_points(player, category.points)
                alert = f'You guessed! You get {category.points} points'
            else:
                alert = "You didn't guess. You don't get any points"
            if not game.end_turn():
                return HttpResponseRedirect(request, f'/{game.id}/{player}/end')
            return HttpResponseRedirect(f'/play/{game_id}/{player}/choose_cat?alert={alert}')
    else:
        words = [game.secret_word.word] + game.generate_words(N_WORD_CHOICES - 1, category.id)
        shuffle(words)
        request.session['choice_words'] = words
        form = WordForm(words=words)
        picture_path = f'jpg/game{game_id}_pic.jpg'
        context = {'form': form, 'game': game, 'player': player, 'category_id': category.id,
                   'picture_path': picture_path}
        return render(request, 'drawing/guess.html', context)


def draw_wait(request, game_id, player):
    game = get_object_or_404(Game, pk=game_id)
    context = {'game': game, 'player': player}
    return render(request, 'drawing/draw_wait.html', context)


def guess_wait(request, game_id, player):
    game = get_object_or_404(Game, pk=game_id)
    context = {'game': game, 'player': player}
    return render(request, 'drawing/guess_wait.html', context)


# DON'T YOU DARE TOUCH THAT
# THIS HAS ALREADY CAUSED 2 MENTAL BREAKDOWNS
def check_status(request, game_id, player):
    if request.is_ajax():
        game = get_object_or_404(Game, pk=game_id)
        if game.is_finished():
            return JsonResponse({'message': 'End'})
        elif game.turn ^ (player == 'first') ^ game.drawing_finished:
            return JsonResponse({'message': 'Ready!'})
        return JsonResponse({'message': 'Not ready'})
    return HttpResponse('Forbidden')


def end(request, game_id, player):
    game = get_object_or_404(Game, pk=game_id)
    if game.first_points == game.second_points:
        result = 'Tie!'
    elif (player == 'first') == (game.first_points > game.second_points):
        result = 'You win!'
    else:
        result = 'You lose...'
    if player == 'first':
        your_points = game.first_points
        opponent_points = game.second_points
    else:
        your_points = game.second_points
        opponent_points = game.first_points
    context = {'game': game, 'player': player, 'result': result, 'your_points': your_points,
               'opponent_points': opponent_points}
    return render(request, 'drawing/end.html', context)


def rules(request):
    return render(request, 'drawing/rules.html')
