from config import REAL_USER_UUID
from psql import get_genres_map, get_genres
from user import generate_user
from mongo import insert_many


if __name__ == "__main__":
    genres = get_genres()
    data = get_genres_map(genres)
    users_list = []
    count = 0
    for num in range(50000):
        user = generate_user(genres, data)
        users_list.append(user)
        count += 1
        if len(users_list) == 250:
            insert_many(users_list)
            users_list.clear()
    user_real = generate_user(genres, data, REAL_USER_UUID)
    insert_many([user_real])
    print("DONE")
