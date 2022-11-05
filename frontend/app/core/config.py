auth_url = "http://localhost/api/v1/auth/login"
recom_url_content = "http://localhost/api/v1/recommendations/base"
recom_url_ml = "http://localhost/api/v1/recommendations/model"
ugc_like_url = "http://localhost/api/v1/ugc/movie-likes"
ugc_progress_url = "http://localhost/api/v1/ugc/progress"

fake_token = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzMxNjg4MCwianRpIjoiZDQ5YTU5NjMtOGQyMS00OTA1LWFkOGYtYjYyYjE4MDM5MzU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoiOTA4ZTMzZGEtNmY1Ny00MGE1LWE4Y2YtNTcyMmRiZWVkMWRjIiwiYWN0aW9uX2lkcyI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwLDExLDEyLDEzLDE0LDE1XX0sIm5iZiI6MTY2NzMxNjg4MCwiZXhwIjoxNjY3MzE3MTgwfQ.-IM9dHs9WYccXjXqLQ8_lGfNLq1QuKZ-Z1AuMq9S70E",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzMxNjg4MCwianRpIjoiNTA5NDg2NjAtYmRkYS00NDQyLTg2MmYtZTE4OTE0ZjA5ZDU3IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcl9pZCI6IjkwOGUzM2RhLTZmNTctNDBhNS1hOGNmLTU3MjJkYmVlZDFkYyJ9LCJuYmYiOjE2NjczMTY4ODAsImV4cCI6MTY2ODYxMjg4MH0.zktWSXrSXU710K1Os-KipfBvh3YvkwxAa3K0yHCAUcU"
}

fake_movies_response = [
  {
    "uuid": "2a090dde-f688-46fe-a9f4-b781a985275e",
    "imdb_rating": 9.6,
    "title": "Star Wars: Knights of the Old Republic"
  },
  {
    "uuid": "c241874f-53d3-411a-8894-37c19d8bf010",
    "imdb_rating": 9.5,
    "title": "Star Wars SC 38 Reimagined"
  },
  {
    "uuid": "05d7341e-e367-4e2e-acf5-4652a8435f93",
    "imdb_rating": 9.5,
    "title": "The Secret World of Jeffree Star"
  },
  {
    "uuid": "05d7341e-e367-4e2e-acf5-4652a8435f95",
    "imdb_rating": 9.3,
    "title": "The Secret World"
  }

]
