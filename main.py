from flask import Flask, redirect, render_template, request, url_for
from pytube import YouTube

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
  if request.method == "POST":
    video_url = request.form["url-input"]
    if "https://www.youtube.com/watch?v=" in video_url and len(
        video_url) >= 43:
      return redirect(url_for("options", video_url=video_url))

    elif video_url == "":
      return render_template("home.html")
  else:
    return render_template("home.html")  # renders homescreen otherwise


@app.route("/options", methods=["POST", "GET"])
def options():

  url = request.args.get(
    'video_url')  # gets the damn URL without changing the LINK!!!
  yt = YouTube(url)  # feeds url to pytube

  ## puts all video resolutions & itags into lists
  res_list = [
    stream.resolution
    for stream in yt.streams.filter(file_extension='mp4', progressive=True)
  ]

  itag_list = [
    stream.itag
    for stream in yt.streams.filter(file_extension='mp4', progressive=True)
  ]

  # convert resolution list into string to insert to HTML
  available_res = ' '.join(res_list)

  if request.method == 'POST':
    video_choose = request.form['download-options']
    download_index = res_list.index(str(video_choose))
    download_link = yt.streams.get_by_itag(int(itag_list[download_index])).url
    return redirect(url_for("download", download_link=download_link)) # THIS IS HOW YOU CONNECT A VARIABLE TO ANOTHER FUNCTION!!!

  else:
    # request the form response
    return render_template(
      "download.html",
      yt_title=yt.title,
      yt_image=yt.thumbnail_url,
      available_res=available_res
    )  # renders download if submitted. defines some variables


@app.route("/download", methods=["POST", "GET"])
def download():
  link=request.args.get('download_link') 
  return redirect(str(link))

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
