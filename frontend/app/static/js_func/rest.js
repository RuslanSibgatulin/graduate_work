function movieViewed(uid) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/viewed", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        movie_id: uid,
        time: 1200,
        total_time: 1200    
    }));
  }


function movieLike(uid) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/like", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        movie_id: uid,
        score: 8
    }));
  }