import instaloader
from pathlib import Path
import re

class MyInstaLoader:
    USER = None   # innstagramdagi user_name -ni kiriting
    PASSWORD = None  # innstagramdagi password -ni kiriting

    def __init__(self,user:str,password:str):
        self.L = instaloader.Instaloader()
        self.PATH = Path(__file__).resolve()
        
        self.USER = user
        self.PASSWORD = password

    async def _check_target_folder(self):
        self.target_path = Path(self.FullPath)
        self.target_path.mkdir(parents=True, exist_ok=True)


    async def get_shortcode(self,url):
        # Define regular expression pattern to match shortcode
        pattern1 = re.compile(r'\/p\/([a-zA-Z0-9_-]+)\/')
        pattern2 = re.compile(r'/reel/([a-zA-Z0-9_-]+)')


        # Find the shortcode in the URL
        self.shortcode = (pattern1.search(url) or pattern2.search(url)).group(1)

        # Print the shortcode
        return self


    async def download_shortcode(self,file_path:Path,folder_name:str):
        """
        'file_path' yuklangan media ma'lum joyga saqlash uchun kerak
        'folder_name' papka nomi, 'file_path'/'folder_name'


        'FullPath' orqli media yuklangan PATH -ni olish mumkin
        """
        
        self.file_path = file_path
        self.folder_name = folder_name
        self.FullPath = fr"{file_path}/{folder_name}"
        if not self.shortcode:
            raise Exception("Shortcode mavjud emas. Avval 'get_shortcode' ni ishlatib ko'ring")
        if not self.folder_name:
            raise Exception("Papkaga nom berilmadi")
        try:
            self.L.load_session_from_file(self.USER,filename=fr"{self.PATH.parent}\{self.USER}") # session joylashgan path  #  `instaloader -l USERNAME`)
                
        except FileNotFoundError:                                                                      ## ❗❗❗ bu jarayonda sizda passwordni so'raydi. ❗ u vaqtda yozgan kodiz ko'rinmaydi
            self.L.login(self.USER, self.PASSWORD)        # (login)
            #self.L.interactive_login(self.USER)      # (ask password on terminal)
            self.L.save_session_to_file(filename=fr"{self.PATH.parent}\{self.USER}")
            self.L.load_session_from_file(self.USER,filename=fr"{self.PATH.parent}\{self.USER}") # session joylashgan path
        # except instaloader.exceptions.InvalidOrExpiredSession:
        #     self.L.

        self.L.sanitize_paths = False
        self.L.download_pictures = True
        self.L.download_videos = True
        self.L.download_video_thumbnails = False
        self.L.download_geotags = False
        self.L.download_comments = False
        self.L.save_metadata = False
        self.L.compress_json = False


        self.post = instaloader.Post.from_shortcode(self.L.context,self.shortcode)                 # post -ni olish
        # print(self.post.video_view_count,"\n")
        # print(self.post.caption,"\n")
        # print(self.post.title,"\n")

        
        await self._check_target_folder()
        self.successfully = self.L.download_post(post=self.post,target=self.target_path) # target -> yuklangan video qayerga tushsin


        return self 


if __name__ == "__main__":
    url = 'https://www.instagram.com/link'
    user,password = "username","password"
    folder_name = "11223344"   # botda, from.user.id

    user1 = MyInstaLoader(user=user,password=password)
    user1.get_shortcode(url=url)
    user1.download_shortcode(file_path=user1.PATH.parent,folder_name=f"DataMedia\{folder_name}")
