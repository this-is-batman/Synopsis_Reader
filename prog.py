from imdb import IMDb

class Movie:
        def __init__(self, name):
                self.name = name
        
        def get_synopsis(self):
                ia = IMDb()
                movie= ia.search_movie(self.name)
                print("Synopsis of the movie showing")
                try:
                        synopsis = ia.get_movie_synopsis(ia.get_imdbID(movie[0]))['data']['synopsis'][0]
                except Exception:
                        synopsis = "Movie not found in the IMDB database or Synopsis not present."
                return synopsis 
                #print(ia.get_movie_synopsis(ia.get_imdbID(movie[0]))['data']['synopsis'][0])
        
        def get_actors(self):
                ia = IMDb()
                movie = ia.search_movie(self.name)
                print("Cast: ")
                i= 0
                while i<5:
                        print(ia.get_movie_full_credits(ia.get_imdbID(movie[0]))['data']['cast'][i])
                        i+=1
                
        
def main():
        mov = Movie("The Dark Knight")
        mov.get_synopsis()
        mov.get_actors()

if __name__=="__main__":
        main()
