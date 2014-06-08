import pygray
import utils.pygrayutils as pygrayutils
import time

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
        allgood = self.grab_frames()
        if allgood:
                self.run_processes()
        return allgood

    def grab_frames(self):
        allgood = True
        for cam, dataname in self.camlist:
            try:
                camdata = cam.getframe()
                imdata = pygrayutils.framestr_to_array(camdata)
                self.datas[dataname] = imdata
            except pygray.FrameError as e:
                allgood = False
                print("Frame error: " + str(e))
        return allgood
                
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
                    time.sleep(0.3)
                    break
                except pygray.CameraError as e:
                    print("Had camera error while opening camera: " + str(e))
                    print("Retrying.")
                    time.sleep(1)

    def stop_cams(self):
        for cam, oname in self.camlist:
            cam.stop()

    def add_raw_camera(self, cam, camname):
        self.cams[camname] = cam
        self.camlist.append((cam, camname))

    def add_camera(self, guid, camname, usecolor=True, framerate=10.0):
        cam = pygray.Camera(guid)
        cam.setframerate(framerate)
        cam.setcolormode(usecolor)
        self.add_raw_camera(cam, camname)
