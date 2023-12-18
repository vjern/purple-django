from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)


class Exclusion(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')


class Draw(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)


class DrawPair(models.Model):
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giver')
    taker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taker')
