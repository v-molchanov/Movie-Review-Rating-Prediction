from django.shortcuts import render
from .models import Review
from .forms import ReviewForm

from django.utils import timezone

import os
import re
from bs4 import BeautifulSoup
import joblib

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def preprocessor(text):
    # remove html tags
    text = BeautifulSoup(text, "html.parser").get_text()

    # remove noize
    text = re.sub('[^A-Za-z0-9\']', ' ', text)  
    text = re.sub('\s{2,}', ' ', text)

    text = text.lower()

    # convert apostrophes into standard lexicons
    apostrophes = load_apostrophes_from_json(os.path.join(CURRENT_DIR, 'ml/apostrophes.json'))
    reformed = [apostrophes[word] if word in apostrophes else word for word in text.split()]
    text = " ".join(reformed)

    # also convert 'cannot' into 'can not'
    text = re.sub('cannot', ' can not', text)

    # finally delete possessive cases and apostrophes
    text = re.sub('\'s', '', text)
    text = re.sub('\'', '', text)

    return text

vectorizer = joblib.load(os.path.join(CURRENT_DIR, 'ml/vectorizer.joblib'))
classifier = joblib.load(os.path.join(CURRENT_DIR, 'ml/classifier.joblib'))

def index(request):

    if (request.method == 'POST'):
        review_text = request.POST['text']

        if len(review_text) != 0:
            review = Review()

            review.text = review_text
            review.publish_date = timezone.now()

            review.rating = classifier.predict(vectorizer.transform([review_text]))[0]

            review.save()

    review_form = ReviewForm()

    sorted_reviews = Review.objects.order_by('-publish_date')

    reviews = []

    for review in sorted_reviews:
        review_info = {'text': review.text, 'rating': review.rating, 'publish_date': review.publish_date}

        reviews.append(review_info)

    context = {'review_form': review_form, 'reviews': reviews}

    return render(request, 'index.html', context)
