from django.db import models


class Season(models.Model):
    name = models.CharField(max_length=50)  # e.g., "2024-2025", "Season 2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    GENDER_CHOICES = [
        ("G", "Garcons"),
        ("F", "Filles"),
    ]
    
    CATEGORY_CHOICES = [
        ("BENJAMIN", "Benjamin (G)"),
        ("BENJAMINE", "Benjamine (F)"),
        ("ECOLES", "Ecoles"),
        ("MINIMES", "Minimes"),
        ("CADET", "Cadet (G)"),
        ("CADETTE", "Cadette (F)"),
        ("JUNIORS", "Juniors"),
        ("SENIORS", "Seniors"),
    ]

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.get_name_display()} - {self.get_gender_display()}"


class Player(models.Model):
    POSITION_CHOICES = [
        ("S", "Passeur"),
        ("OH", "Attaquant"),
        ("MB", "Central"),
        ("OPP", "Opposé"),
        ("L", "Libéro"),
        ("U", "Inconnu"),
    ]

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="players")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="players")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    height_cm = models.PositiveIntegerField()
    weight_kg = models.PositiveIntegerField()
    spike_height_cm = models.PositiveIntegerField(null=True, blank=True)
    block_height_cm = models.PositiveIntegerField(null=True, blank=True)

    position = models.CharField(max_length=3, choices=POSITION_CHOICES)

    jersey_number = models.PositiveIntegerField(null=True, blank=True)

    def age(self):
        from datetime import date
        return date.today().year - self.birth_date.year - (
            (date.today().month, date.today().day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class Match(models.Model):
    MATCH_TYPE_CHOICES = [
        ("TRAINING", "Entrainement"),
        ("FRIENDLY", "Amical"),
        ("LEAGUE", "Ligue"),
        ("CUP", "Coupe"),
        ("TOURNAMENT", "Tournoi"),
    ]

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="matches")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="matches")
    date = models.DateTimeField()
    opponent = models.CharField(max_length=200)
    match_type = models.CharField(max_length=20, choices=MATCH_TYPE_CHOICES, default="LEAGUE")

    location = models.CharField(max_length=200, blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)  # e.g., "3-1", "2-3"

    players = models.ManyToManyField(Player, through="MatchParticipation", related_name="matches")

    def __str__(self):
        return f"{self.category} vs {self.opponent} ({self.date.strftime('%Y-%m-%d')})"
    



class MatchParticipation(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="match_stats")
    match = models.ForeignKey("Match", on_delete=models.CASCADE, related_name="participations")

    # --- Attack ---
    attack_kills = models.PositiveIntegerField(default=0)
    attack_errors = models.PositiveIntegerField(default=0)
    attack_attempts = models.PositiveIntegerField(default=0)
    #attack_efficiency = models.FloatField(default=0.0)
    #attack_kill_percentage = models.FloatField(default=0.0)
    #attack_error_percentage = models.FloatField(default=0.0)

    # --- Serve ---
    serve_aces = models.PositiveIntegerField(default=0)
    serve_errors = models.PositiveIntegerField(default=0)
    serve_attempts = models.PositiveIntegerField(default=0)
    serve_rate = models.FloatField(default=0.0)  # %
    #serve_efficiency = models.FloatField(default=0.0)
    serve_1s = models.PositiveIntegerField(default=0)
    serve_2s = models.PositiveIntegerField(default=0)
    serve_3s = models.PositiveIntegerField(default=0)

    # --- Receive ---
    receive_3s = models.PositiveIntegerField(default=0)
    receive_2s = models.PositiveIntegerField(default=0)
    receive_1s = models.PositiveIntegerField(default=0)
    receive_0s = models.PositiveIntegerField(default=0)
    receive_attempts = models.PositiveIntegerField(default=0)
    #receive_pass_rating = models.FloatField(default=0.0)  # avg rating
    #perfect_pass_percentage = models.FloatField(default=0.0)
    #good_pass_percentage = models.FloatField(default=0.0)

    # --- Set ---
    set_assists = models.PositiveIntegerField(default=0)
    set_attempts = models.PositiveIntegerField(default=0)
    set_errors = models.PositiveIntegerField(default=0)
    #set_assist_percentage = models.FloatField(default=0.0)

    # --- Dig ---
    dig_successes = models.PositiveIntegerField(default=0)
    dig_errors = models.PositiveIntegerField(default=0)

    # --- Block ---
    block_solos = models.PositiveIntegerField(default=0)
    block_assists = models.PositiveIntegerField(default=0)
    block_errors = models.PositiveIntegerField(default=0)

    # --- General ---
    sets_played = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("player", "match")

    def __str__(self):
        return f"{self.player} - {self.match}"


