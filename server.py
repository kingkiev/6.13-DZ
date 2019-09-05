
import os
from bottle import run, request, route, HTTPError
import artist_find


@route("/albums/<artist>")
def albums(artist):
	albums_list = artist_find.find(artist)
	count_albums = len(albums_list)
	if not albums_list:
		message = "Альбомов {} не найдено".format(artist)
		result = HTTPError(404, message)
	else:
		album_names = [album.album for album in albums_list]
		result = "Количество альбомов {}: {}. Список альбомов: \n".format(artist, count_albums)
		result += "\n".join(album_names)
	return result

@route("/albums", method="POST")
def new_album():
	album_data = {
		"year": request.POST.get("year"),
		"artist": request.POST.get("artist"),
		"genre": request.POST.get("genre"),
		"album": request.POST.get("album")
	}
	valid = artist_find.validation(album_data)
	if valid:
		result_work = artist_find.find_album(album_data)
		if result_work > 0:
			artist = album_data["artist"]
			album = album_data["album"]
			message = "В базе есть уже альбом {} исполнителя {}".format(album, artist)
			return HTTPError(409, message)
		elif result_work == 0:
			return artist_find.add_album(album_data)
	else:
		return "Проверьте введенные данные. Все поля должны быть заполненны. Год в интервале 1900-2019"

if __name__ == '__main__':
	run(host="localhost", port=8080, debug=True)