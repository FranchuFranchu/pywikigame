import django.db.models as models
from urllib.request import urlopen
from json import load

def get_random_wikipedia_page():
    data = urlopen("https://en.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0&grnlimit=1")
    return list(load(data.fp)['query']['pages'].values())[0]["title"]


class Match(models.Model):
    name = models.TextField(unique=True)
    wikipedia_base = models.TextField()
    target = models.TextField(null=True)
    source = models.TextField(null=True)
    started = models.BooleanField(default=False)
    def check_start(self):
        start = True
        for i in self.players.all():
            print(i.ready)
            start &= i.ready
        print("Test start")

        if start:
            self.started = True
            self.source = get_random_wikipedia_page()
            self.target = get_random_wikipedia_page()
            self.save()

            for i in self.players.all():
                i.page_log = self.source
                i.save()



        return start


class Player(models.Model):
    page_log = models.TextField(default="")
    name = models.TextField(default="")
    ready = models.BooleanField(default=False)
    cookie = models.TextField(unique=True)
    match = models.ForeignKey(Match, related_name="players", on_delete=models.CASCADE, null=True)
