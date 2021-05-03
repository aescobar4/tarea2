from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base64 import b64encode

import json

from ti.models import Album, Artist, Track

def index(request):
    response = json.dumps({})
    return HttpResponse(response, content_type='application/json')

# POST y GET de /artists
@csrf_exempt
def artists(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        try:
            name = payload['name']
            age = payload['age']
            if str(name) != name:
                return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        except:
            return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        id = b64encode(name.encode()).decode('utf-8')[:22]
        try:
            artist = Artist.objects.get(id=id)
            self_ = 'https://cloudy-city-01.herokuapp.com/artists/' + artist.id
            response = json.dumps({
                'id': artist.id,
                'name': artist.name,
                'age': artist.age,
                'albums': self_ + '/albums',
                'tracks': self_ + '/tracks',
                'self': self_,
            })
            return HttpResponse(response, content_type='application/json', status=409, reason='artista ya existe')
        except:
            artist = Artist(id=id, name=name, age=age)
            artist.save()
            self_ = 'https://cloudy-city-01.herokuapp.com/artists/' + id
            response = json.dumps({ 
                'id': id, 
                'name': name, 
                'age': age,
                'albums': self_ + '/albums',
                'tracks': self_ + '/tracks',
                'self': self_,
                })
        return HttpResponse(response, content_type='application/json', status=201, reason='artista creado')
    elif request.method == 'GET':
        artists = Artist.objects.all()
        return_list = []
        for artist in artists:
            self_ = 'https://cloudy-city-01.herokuapp.com/artists/' + artist.id
            artist_to_add = {
                'id': artist.id,
                'name': artist.name,
                'age': artist.age,
                'albums': self_ + '/albums',
                'tracks': self_ + '/tracks',
                'self': self_,
            }
            return_list.append(artist_to_add)
        response = json.dumps(return_list)
        return HttpResponse(response, content_type='application/json', status=200, reason='resultados obtenidos')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET y DELETE de /artists/{artist_id}
@csrf_exempt
def artistsId(request, artist_id):
    if request.method == 'GET':
        try:
            artist = Artist.objects.get(id=artist_id)
            self_ = 'https://cloudy-city-01.herokuapp.com/artists/' + artist.id
            response = json.dumps({ 
                'id': artist.id,
                'name': artist.name,
                'age': artist.age,
                'albums': self_ + '/albums',
                'tracks': self_ + '/tracks',
                'self': self_,
            })
            return HttpResponse(response, content_type='application/json', status=200, reason='operación exitosa')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='artista no encontrado')
    elif request.method == 'DELETE':
        try:
            artist = Artist.objects.get(id=artist_id)
            albums = Album.objects.filter(artist_id=artist_id).all()
            for album in albums:
                tracks = Track.objects.filter(album_id=album.id).all()
                for track in tracks:
                    track.delete()
                album.delete()
            artist.delete()
            return HttpResponse(content_type='application/json', status=204, reason='artista eliminado')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='artista inexistente')
    else:
        return HttpResponse(content_type='application/json', status=405)

# POST y GET de /artists/{artist_id}/albums
@csrf_exempt
def albumsPerArtist(request, artist_id):    
    if request.method == 'POST':
        payload = json.loads(request.body)
        try:
            name = payload['name']
            genre = payload['genre']
            if str(name) != name:
                return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        except:
            return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        try:
            Artist.objects.get(id=artist_id)
        except:
            return HttpResponse(content_type='application/json', status=422, reason='artista no existe')
        string_to_encode = name + ":" + artist_id
        id = b64encode(string_to_encode.encode()).decode('utf-8')[:22]
        try:
            album = Album.objects.get(id=id)
            exists = True
        except:
            album = Album(id=id, artist_id=artist_id, name=name, genre=genre)
            album.save()
            exists = False
        base = 'https://cloudy-city-01.herokuapp.com/'
        response = json.dumps({ 
            'id': id, 
            'artist_id': artist_id, 
            'name': name, 
            'genre': genre,
            'artist': base + 'artists/' + artist_id,
            'tracks': base + 'albums/' + id + '/tracks',
            'self': base + 'albums/' + id,
        })
        if exists:
            return HttpResponse(response, content_type='application/json', status=409, reason='album ya existe')
        else:
              return HttpResponse(response, content_type='application/json', status=201, reason='álbum creado')          
    elif request.method == 'GET':
        try:
            artist = Artist.objects.get(id=artist_id)
            albums = Album.objects.filter(artist_id=artist_id).all()
            return_list = []
            base = 'https://cloudy-city-01.herokuapp.com/'
            for album in albums:
                return_list.append({
                    'id': album.id, 
                    'artist_id': artist_id, 
                    'name': album.name, 
                    'genre': album.genre,
                    'artist': base + 'artists/' + artist_id,
                    'tracks': base + 'albums/' + album.id + '/tracks',
                    'self': base + 'albums/' + album.id,
                })
            response = json.dumps(return_list)
            return HttpResponse(response, content_type='application/json', status=200, reason='resultados obtenidos')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='artista no encontrado')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET y DELETE de /albums/{album_id}
@csrf_exempt
def albumsId(request, album_id):
    if request.method == 'GET':
        try:
            album = Album.objects.get(id=album_id)
            base = 'https://cloudy-city-01.herokuapp.com/'
            response = json.dumps({ 
                'id': album_id, 
                'artist_id': album.artist_id, 
                'name': album.name, 
                'genre': album.genre,
                'artist': base + 'artists/' + album.artist_id,
                'tracks': base + 'albums/' + album_id + '/tracks',
                'self': base + 'albums/' + album_id,
            })
            return HttpResponse(response, content_type='application/json', status=200, reason='operación exitosa')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='álbum no encontrado')
    elif request.method == 'DELETE':
        try:
            album = Album.objects.get(id=album_id)
            tracks = Track.objects.filter(album_id=album_id).all()
            for track in tracks:
                track.delete()
            album.delete()
            return HttpResponse(content_type='application/json', status=204, reason='álbum eliminado')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='álbum no encontrado')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET de /albums
@csrf_exempt
def albums(request):
    if request.method == 'GET':
        albums = Album.objects.all()
        return_list = []
        for album in albums:
            self_ = 'https://cloudy-city-01.herokuapp.com/albums/' + album.id
            album_to_add = {
                'id': album.id,
                'artist_id': album.artist_id,
                'name': album.name,
                'genre': album.genre,
                'artist': 'https://cloudy-city-01.herokuapp.com/albums/' + album.artist_id,
                'tracks': self_ + '/tracks',
                'self': self_,
            }
            return_list.append(album_to_add)
        response = json.dumps(return_list)
        return HttpResponse(response, content_type='application/json', status=200, reason='resultados obtenidos')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET y POST de /albums/{album_id}/tracks
@csrf_exempt
def tracksPerAlbum(request, album_id):
    if request.method == 'POST':
        payload = json.loads(request.body)
        try:
            name = payload['name']
            duration = payload['duration']
            if str(name) != name:
                return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        except:
            return HttpResponse(content_type='application/json', status=400, reason='input inválido')
        try:
            album = Album.objects.get(id=album_id)
        except:
            return HttpResponse(content_type='application/json', status=422, reason='álbum no encontrado')
        string_to_encode = name + ":" + album_id
        id = b64encode(string_to_encode.encode()).decode('utf-8')[:22]
        try:
            track = Track.objects.get(id=id)
            existe = True
        except:
            track = Track(id=id, name=name, album_id=album_id, duration=duration)
            existe = False
            track.save()   
        artist = Album.objects.get(id=album_id).artist_id
        base = 'https://cloudy-city-01.herokuapp.com/'
        response = json.dumps({
            'id': id,
            'album_id': album_id,
            'duration': duration,
            'name': name,
            'times_played': 0,
            'artist': base + 'artists/' + artist,
            'album': base + 'albums/' + album_id,
            'self': base + 'tracks/' + id,
        })
        if existe:
            return HttpResponse(response, content_type='application/json', status=409, reason='canción ya existe')
        else:
            return HttpResponse(response, content_type='application/json', status=201, reason='canción creada')
    elif request.method =='GET':
        try:
            tracks = Track.objects.filter(album_id=album_id).all()
            artist = Album.objects.get(id=album_id).artist_id
            return_list = []
            base = 'https://cloudy-city-01.herokuapp.com/'
            for track in tracks:
                return_list.append({
                    'id': track.id,
                    'album_id': track.album_id,
                    'duration': track.duration,
                    'name': track.name,
                    'times_played': track.times_played,
                    'artist': base + 'artists/' + artist,
                    'album': base + 'albums/' + track.album_id,
                    'self': base + 'tracks/' + track.id,
                })
            response = json.dumps(return_list)
            return HttpResponse(response, content_type='application/json', status=200, reason='resultados obtenidos')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='álbum no encontrado')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET y DELETE de /tracks/{track_id}
@csrf_exempt
def tracksId(request, track_id):
    if request.method == 'GET':
        try:
            track = Track.objects.get(id=track_id)
            artist = Album.objects.get(id=track.album_id).artist_id
            base = 'https://cloudy-city-01.herokuapp.com/'
            response = json.dumps({
                'id': track.id,
                'album_id': track.album_id,
                'duration': track.duration,
                'name': track.name,
                'times_played': track.times_played,
                'artist': base + 'artists/' + artist,
                'album': base + 'albums/' + track.album_id,
                'self': base + 'tracks/' + track.id,
            })
            return HttpResponse(response, content_type='application/json', status=200, reason='operación exitosa')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='canción no encontrada')
    elif request.method == 'DELETE':
        try:
            Track.objects.get(id=track_id).delete()
            return HttpResponse(content_type='application/json', status=204, reason='canción eliminada')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='canción inexistente')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET de /tracks
@csrf_exempt
def tracks(request):
    if request.method == 'GET':
        tracks = Track.objects.all()
        return_list = []
        base = 'https://cloudy-city-01.herokuapp.com/'
        for track in tracks:
            try:
                artist = Album.objects.get(id=track.album_id).artist_id
                return_list.append({
                    'id': track.id,
                    'album_id': track.album_id,
                    'duration': track.duration,
                    'name': track.name,
                    'times_played': track.times_played,
                    'artist': base + 'artists/' + artist,
                    'album': base + 'albums/' + track.album_id,
                    'self': base + 'tracks/' + track.id,
                })
            except:
                a = 'a'
        response = json.dumps(return_list)
        return HttpResponse(response, content_type='application/json', status=200, reason='operación exitosa')
    else:
        return HttpResponse(content_type='application/json', status=405)

# GET de /artists/{artist_id}/tracks
@csrf_exempt
def artistTracks(request, artist_id):
    if request.method == 'GET':
        try:
            Album.objects.get(artist_id=artist_id)
            albums = Album.objects.filter(artist_id=artist_id).all()
            return_list = []
            for album in albums:
                tracks = Track.objects.filter(album_id=album.id).all()
                base = 'https://cloudy-city-01.herokuapp.com/'
                for track in tracks:
                    return_list.append({
                        'id': track.id,
                        'album_id': track.album_id,
                        'duration': track.duration,
                        'name': track.name,
                        'times_played': track.times_played,
                        'artist': base + 'artists/' + artist_id,
                        'album': base + 'albums/' + track.album_id,
                        'self': base + 'tracks/' + track.id,
                    })
            response = json.dumps(return_list)
            return HttpResponse(response, content_type='application/json', status=200, reason='resultados obtenidos')
        except:
            return HttpResponse(content_type='application/json', status=404, reason='artista no encontrado')
    else:
        return HttpResponse(content_type='application/json', status=405)

# PUT de /artists/{artist_id}/albums/play
@csrf_exempt
def playArtist(request, artist_id):
    if request.method == 'PUT':
        try:
            Artist.objects.get(id=artist_id)
        except:
            return HttpResponse(content_type='application/json', status=404, reason='artista no encontrado')
        albums = Album.objects.filter(artist_id=artist_id).all()
        for album in albums:
            tracks = Track.objects.filter(album_id=album.id).all()
            for track in tracks:
                print(track.times_played, track.name)
                track.times_played += 1
                print(track.times_played, track.name)
                track.save(force_update=True)
        return HttpResponse(
            content_type='application/json', 
            status=200, 
            reason='todas las canciones del artista fueron reproducidas'
        )
    else:
        return HttpResponse(content_type='application/json', status=405)
    
# PUT de /albums/{album_id}/tracks/play
@csrf_exempt
def playAlbum(request, album_id):
    if request.method == 'PUT':
        try:
            Album.objects.get(id=album_id)
        except:
            return HttpResponse(content_type='application/json', status=404, reason='álbum no encontrado')
        tracks = Track.objects.filter(album_id=album_id).all()
        for track in tracks:
            track.times_played += 1
            track.save(force_update=True)
        return HttpResponse(content_type='application/json', status=200, reason='canciones del álbum reproducidas')
    else:
        return HttpResponse(content_type='application/json', status=405)

# PUT de /tracks/{track_id}/play
@csrf_exempt
def playTrack(request, track_id):
    if request.method == 'PUT':
        try:
            track = Track.objects.get(id=track_id)
        except:
            return HttpResponse(content_type='application/json', status=404, reason='canción no encontrada')
        track.times_played += 1
        track.save(force_update=True)
        print(track.times_played)
        return HttpResponse(content_type='application/json', status=200, reason='canción reproducida')
    else:
        return HttpResponse(content_type='application/json', status=405)
