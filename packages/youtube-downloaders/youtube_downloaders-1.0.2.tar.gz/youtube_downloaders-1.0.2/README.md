![alt text](./youtube.jpg)

## Dependency

- [pytube](https://pypi.org/project/pytube/)
- [flask](https://pypi.org/project/Flask/)

## CLI

USAGE
```
usage: Download [-h] [-v] [-gui] [-web] {video,playlist} ...

Download Youtube CLI

positional arguments:
  {video,playlist}
    video              video to download
    playlist           playlist to download

options:
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
  -gui, --gui_console  download videos using Graphical Interface
  -web, --web_console  download videos using Web Console
```

##### To download single video:
```
youtube_download video -url "https://www.youtube.com/watch?v=7uCpVOSXk8I" -save "C:\Users\im530\Downloads\dtdt"
```

##### To download entire playlist:
```
youtube_download playlist -url "https://www.youtube.com/playlist?list=PLW489siXAtnoA_fOdIzMHU8gAZHHfp-T5" -save "C:\Users\im530\Downloads\dtdt" -num 2
```
 - num : How many videos to be downloaded parallelly.

## To load the web page:
```
youtube_download -web
```

#### url to visit
```
http://127.0.0.1:5789/
```

#### Input
![alt text](./web1.JPG)

#### Response
![alt text](./web2.JPG)


## To load the GUI:
```
youtube_download -gui
```
#### Input
![alt text](./gui1.JPG)

#### Response
![alt text](./gui2.JPG)
