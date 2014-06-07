import pygray
import pygrayutils


def findValidFramerate(rawf):
    framerates = [(3.75, pygray.FRAMERATE_3_75),
                  (7.5, pygray.FRAMERATE_7_5),
                  (15.0, pygray.FRAMERATE_15),
                  (30.0, pygray.FRAMERATE_30),
                  (60.0, pygray.FRAMERATE_60),
                  (120.0, pygray.FRAMERATE_120),
                  (240.0, pygray.FRAMERATE_240)]
    for (frate, cval) in framerates:
        if frate >= rawf:
            return (cval, frate)
    return (30.0, pygray.FRAMERATE_30)  # default to 30


class CameraProcess:

    def __init__(self):
        self.cams = {}
        self.camlist = []
        self.datas = {}
        self.processes = []
        self.frameidx = 0

    def add_process(self, proc, inputs, ouputs):
        self.processes.append((proc, inputs, outputs))

    def do_iteration(self):
        self.frameidx += 1
        self.datas["frameidx"] = self.frameidx
        self.grab_frames()
        self.run_processes()

    def grab_frames(self):
        for cam, dataname in self.camlist:
            camdata = cam.getframe()
            imdata = pygrayutils.framestr_to_array(camdata)
            self.datas[dataname] = imdata

    def run_processes(self):
        for (proc, inputs, outputs) in self.processes:
            # is a blanket exception good python form? No.
            # is a blanket exception what we need to avoid crashing
            # the whole vision system? Yes.
            try:
                idata = [self.data[dname] for dname in inputs]
                outdata = proc.run(idata)
                for (data, outname) in zip(outdata, outputs):
                    self.data[outname] = data
            except Exception as e:
                print("Had exception running process %s: %s" %
                      (proc.name, str(e)))

    def get_data(self, dataname):
        return self.datas[dataname]

    def start_cams(self, nretries=10):
        for cam, oname in self.camlist:
            for i in range(nretries):
                try:
                    cam.start()
                    break
                except pygray.CameraError as e:
                    print("Had camera error while opening camera: " + str(e))
                    print("Retrying.")

    def stop_cams(self):
        for cam, oname in self.camlist:
            cam.stop()

    def add_raw_camera(self, cam, camname):
        self.cams[camname] = cam
        self.camlist.append((cam, camname))

    def add_color_camera(self, guid, camname, framerate=10.0):
        frate, frateconst = findValidFramerate(framerate)
        resolutionconst = pygray.VIDEOMODE_1280x960RGB
        cam = pygray.Camera(guid)
        cam.setcolormode(True)
        cam.setvideomode(resolutionconst, frateconst)
        self.add_raw_camera(cam, camname)
        print("Requested framrate %f, using %f" % (framerate, frate))

    def add_bw_camera(self, guid, camname, framerate=10.0):
        frate, frateconst = findValidFramerate(framerate)
        resolutionconst = pygray.VIDEOMODE_640x480Y8
        cam = pygray.Camera(guid)
        cam.setcolormode(True)
        cam.setvideomode(resolutionconst, frateconst)
        self.add_raw_camera(cam, camname)
        print("Requested framrate %f, using %f" % (framerate, frate))
