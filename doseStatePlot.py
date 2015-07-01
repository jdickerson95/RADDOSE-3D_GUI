# Authors: Prabhu Ramachandran <prabhu [at] aero.iitb.ac.in>
# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

# Standard imports.
from numpy import zeros, array

# Enthought imports.
from traits.api import HasTraits, Instance, Property, Enum
from traitsui.api import View, Item, HSplit, VSplit, InstanceEditor
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.core.ui.engine_view import EngineView
from mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.modules.orientation_axes import OrientationAxes


######################################################################
class doseStatePlot(HasTraits):

    # The scene model.
    scene = Instance(MlabSceneModel, ())

    # The mayavi engine view.
    engine_view = Instance(EngineView)

    # The current selection in the engine tree view.
    current_selection = Property


    ######################
    view = View(HSplit(VSplit(Item(name='engine_view',
                                   style='custom',
                                   resizable=True,
                                   show_label=False
                                   ),
                              Item(name='current_selection',
                                   editor=InstanceEditor(),
                                   enabled_when='current_selection is not None',
                                   style='custom',
                                   springy=True,
                                   show_label=False),
                                   ),
                               Item(name='scene',
                                    editor=SceneEditor(),
                                    show_label=False,
                                    resizable=True,
                                    height=500,
                                    width=500),
                        ),
                resizable=True,
                scrollable=True
                )

    def __init__(self, mainGUI, **traits):
        HasTraits.__init__(self, **traits)
        self.engine_view = EngineView(engine=self.scene.engine)

        # Hook up the current_selection to change when the one in the engine
        # changes.  This is probably unnecessary in Traits3 since you can show
        # the UI of a sub-object in T3.
        self.scene.engine.on_trait_change(self._selection_change,
                                          'current_selection')

        self.generate_data_mayavi(mainGUI)

    def generate_data_mayavi(self, mainGUI):
        """Shows how you can generate data using mayavi instead of mlab."""
        expName = str(mainGUI.expChoice.get())
        doseState = self.getDoseStateFromR("{}/output-DoseState.R".format(expName))
        self.scene.mlab.contour3d(doseState, colormap='hot', contours=[doseState.min(), (doseState.max() + doseState.min())/2.0, doseState.max()], transparent=True, opacity=0.5, vmin=0, vmax=doseState.max())
        self.scene.mlab.outline()
        self.scene.mlab.orientation_axes()
        self.scene.mlab.title("Final dose state of crystal from experiment: {}".format(expName))

    def _selection_change(self, old, new):
        self.trait_property_changed('current_selection', old, new)

    def _get_current_selection(self):
        return self.scene.engine.current_selection

    def parseCrystalSizeLine(self, line):
        colonIndex = line.find(':')
        splitLine = line[colonIndex+1:-1].split()
        crystDims = (int(splitLine[0]), int(splitLine[2]), int(splitLine[4]))
        return crystDims

    def getDoseStateFromR(self, filename):
        with open(filename, "r") as rCode:
            for line in rCode:
                if "Crystal size" in line:
                    crystalDims = self.parseCrystalSizeLine(line)
                    crystalDose = zeros(crystalDims)
                elif "dose[,," in line:
                    for zDim in xrange(1, crystalDims[2] + 1):
                        string = "dose[,,{}]".format(zDim)
                        if string in line:
                            openBracketIndex = line.find("(")
                            closeBracketIndex = line.find(")")
                            zDimTuple = eval(line[openBracketIndex:closeBracketIndex+1])
                            zDimArray = array(zDimTuple)
                            crystalDose[:,:,zDim-1] = zDimArray.reshape(crystalDims[1],crystalDims[0]).transpose()
        return crystalDose


#if __name__ == '__main__':
    #m = Mayavi()
    #m.configure_traits()
