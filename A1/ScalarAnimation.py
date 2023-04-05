from ScalarFieldPlotter import ScalarFieldPlotter
import gif

if __name__ == '__main__':
    sfp = ScalarFieldPlotter(["SST", "SSS", "SSHA"])

    # frames = sfp.getGifFrames("SST", [18,35,1])
    # frames = sfp.getGifFrames("SSHA", [-0.5,0.4,0.01])
    frames = sfp.getGifFrames("SSS", [24,40,0.5])
    gif.save(frames, 'ScalarAnimationSSS.gif', duration=1000, between="frames", loop = False)

