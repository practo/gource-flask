from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/stream")
def stream():
    gource = subprocess.Popen(('gource', '-o', '-'),
                              stdout=subprocess.PIPE)
    ffmpeg = subprocess.Popen(('ffmpeg', '-y', '-r', '60', '-f', 'image2pipe',
                               '-vcodec', 'ppm', '-i', '-', '-vcodec', 'libvpx',
                               '-b', '10000K', '-f', 'webm', '-'),
                              stdin=gource.stdout,
                              stdout=subprocess.PIPE)
    return Response(ffmpeg.stdout, content_type='video/webm')


if __name__ == "__main__":
    app.run(debug=True)
