# show svg in tkinter
import cairosvg


"""class svg2png
takes 2 args : input file and scale to resize the output
input must be svg
-> USING CAIROSVG
"""

class svg2png:
    def __init__(self, input, scale):
        self.input = input
        self.output = "WeatherIcon.png"
        self.scale = float(scale)

    def convert(self):
        output = cairosvg.svg2png(url=self.input, write_to=self.output, scale=4.0)
        output_path = self.output
        return output_path
        


if __name__ == "__main__":
    c = svg2png("DATA/weather_icons/d/sunny.svg", 4.0)
    print(c.convert())