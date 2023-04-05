from VectorFieldPlotter import VectorFieldPlotter
import gif

if __name__ == '__main__':
    vfp = VectorFieldPlotter(["U", "V"])

    frames = vfp.getGifFrames()
    gif.save(frames, 'VectorAnimation.gif', duration=1000, between="frames", loop = False)

