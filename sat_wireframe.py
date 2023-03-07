import numpy as np
from SARToolbox.geometryRadar import RadarGeometry
from obliqueDrawing import obliqueProject


class SatObj():
    def __init__(self):
        self.faces = []
        # aperture
        xyz = np.array([[-5, -1, 0],
                        [-5, 1, 0],
                        [5, 1, 0],
                        [5, -1, 0],
                        [-5, -1, 0]]).T
        self.faces.append(xyz)
        # front square
        xyz = np.array([[-1, 1, 0],
                        [-1, 1, -2],
                        [1, 1, -2],
                        [1, 1, 0]]).T
        self.faces.append(xyz)
        # side line
        xyz = np.array([
                        [-1, 1, -2],
                        [-1, -1, -2],
                        [-1, -1, -1]
                        ]).T
        self.faces.append(xyz)
        # backup
        self.endfaces = self.faces

        # init
        self.radgeo = RadarGeometry()

        # angle
        self.angle = 45
        # cf
        self.cf = 2
        # zcf
        self.zcf = 2

    def set_projection(self, angle, cf, zcf):
        """
        oblique projection
        :param angle:
        :param cf:
        :param zcf:
        :return:
        """
        self.angle = angle
        self.cf = cf
        self.zcf = zcf

    pass

    def attach_radar(self, radgeo: RadarGeometry):
        self.radgeo = radgeo

    def scale_radar(self, faces, xscale=1, yscale=1, zscale=1):
        endfaces = []
        for face in faces:
            # edit rotation
            newface = face * np.array([[xscale], [yscale], [zscale]])
            # save
            endfaces.append(newface)
        self.endfaces = endfaces

    def position_radar(self, faces, radgeo: RadarGeometry):
        endfaces = []
        for face in faces:
            # edit rotation
            newface = radgeo.Bs2c @ face
            # edit position
            newface = newface + radgeo.S_0
            # save
            endfaces.append(newface)
        self.endfaces = endfaces

    def plot(self, ax, xscale=1, yscale=1, zscale=1, style='k', **args):
        self.scale_radar(self.faces, xscale, yscale, zscale)
        self.position_radar(self.endfaces, self.radgeo)
        for face in self.endfaces:
            x, y, z = face
            x1, y1 = obliqueProject(x, y, z, self.cf, self.angle, self.zcf)
            ax.plot(x1, y1, style)
