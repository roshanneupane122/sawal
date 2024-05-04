from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import QuizSession

@login_required(login_url='login')
def user_page(request):
    # Step 1: Extract the currentScore from the URL parameters
    current_score = int(request.GET.get('currentScore', 0))

    # Step 2: Save the currentScore to the user session
    request.session['currentScore'] = current_score

    # Step 3: Save the user session data to the database
    user = request.user
    quiz_session = QuizSession.objects.create(user=user, final_score=current_score)
    quiz_session.save()

    return render(request, 'user.html', {'current_score': current_score})

# Create your views here.
from django.shortcuts import render, redirect
from .forms import QuestionForm

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_random_question')  # Redirect to a success page
    else:
        form = QuestionForm()

    return render(request, 'add_question.html', {'form': form})






# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question
import random

def display_random_question(request):
    # Retrieve all questions from the database
    questions = list(Question.objects.all())

    # Get the shuffled question order from the session or create a new one
    question_order = request.session.get('question_order')
    if not question_order:
        question_order = list(range(len(questions)))
        random.shuffle(question_order)
        request.session['question_order'] = question_order

    # Get the current question index from the session or set it to 0
    current_question_index = request.session.get('current_question_index', 0)

    # Get the current question using the shuffled order
    current_question_id = question_order[current_question_index]
    current_question = questions[current_question_id]

    context = {
        'current_question': current_question,
        'current_question_index': current_question_index,
        'num_questions': min(len(questions), 25),  # Limit the total number of questions to 25
    }
   
    return render(request, 'display_questions.html', context)

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Question, QuizSession

@login_required(login_url='login')
def next_random_question(request):
    # Get the current question index from the session or set it to 0
    current_question_index = request.session.get('current_question_index', 0)

    # Retrieve all questions from the database
    questions = list(Question.objects.all())

    # Get the shuffled question order from the session
    question_order = request.session.get('question_order')

    # Increment the index or start over if all questions have been asked
    current_question_index += 1

    # Check if all questions have been displayed, and reset for a new game
    if current_question_index >= min(len(questions), 11):
        # Get the username of the current user
        username = request.user.username

        # Retrieve the currentScore from the URL parameter
        current_score = int(request.GET.get('currentScore', 0))

        # Clear only the currentScore session data
        request.session['currentScore'] = current_score

        # Print statements for debugging
        print(f"Debug: Entered next_random_question view for {username}")
        print(f"Debug: Received current_question_index: {current_question_index}")
        print(f"Debug: Received currentScore from URL: {current_score}")

        # Save the QuizSession to the database
        # quiz_session = QuizSession.objects.create(user=request.user, final_score=current_score)
        # quiz_session.save()

        # Print statements for debugging
       

        # Render the scorecard template with the final score and username
        context = {'final_score': current_score, 'username': username}
        print("Debug: Rendering scorecard.html with context:", context)

        return render(request, 'scorecard.html', context)

    # Update the session to move to the next question
    request.session['current_question_index'] = current_question_index

    return redirect('display_random_question')









from django.http import JsonResponse

def handle_submission(request):
    if request.method == 'POST':
        selected_value = request.POST.get('option')  # Update to match the form input name
        current_question_index = int(request.session.get('current_question_index', 0))
        questions = list(Question.objects.all())
        correct_option = questions[current_question_index].correct_option

        if selected_value == correct_option:
            request.session['currentScore'] = request.session.get('currentScore', 0) + 1

        return JsonResponse({'correct': selected_value == correct_option, 'currentScore': request.session['currentScore']})
    else:
        return HttpResponse(status=400)
    


from django.shortcuts import render
from .models import QuizSession

def analyticals(request):
    quiz_sessions = QuizSession.objects.all()
    context = {'quiz_sessions': quiz_sessions}
    return render(request, 'analytics.html', context)