from django.db import models
from account.models import User
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import os
# Create your models here.


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.content[:20] if self.content else "Image Post"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False) 
    reported = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_bullying():
            self.flagged = True 
            self.text = "This comment has been deleted by admin"
        super().save(*args, **kwargs)

    def is_bullying(self):
        """
        Detect if the comment contains bullying content using the ML model.
        """
        try:

            vocab_path = os.path.join(BASE_DIR, "posts", "vector_vocabulary.pkl")
            with open(vocab_path, "rb") as f:
                vocabulary = pickle.load(f)

            count_vector = CountVectorizer(stop_words='english', lowercase=True, vocabulary=vocabulary)

            data = count_vector.transform([self.text])

        
            model_path = os.path.join(BASE_DIR, "posts", "LinearSVC.pkl")
            with open(model_path, "rb") as f:
                trained_model = pickle.load(f)

            prediction = trained_model.predict(data)

            return prediction[0] == 1
        except Exception as e:
            print("Error in ML prediction:", e)
            return False  

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"