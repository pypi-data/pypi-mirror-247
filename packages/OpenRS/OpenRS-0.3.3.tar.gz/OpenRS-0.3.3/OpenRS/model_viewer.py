#!/usr/bin/env python
'''
Qt, VTK and matplotlib application to allow for viewing and querying residual stress fields. 
-------------------------------------------------------------------------------
0.1 - Inital release
0.2 - added clipping, etc
0.3 - allows for translation of model and resulting STL file
'''
__author__ = "M.J. Roy"
__version__ = "0.3"
__email__ = "matthew.roy@manchester.ac.uk"
__status__ = "Experimental"
__copyright__ = "(c) M. J. Roy, 2021-"

import os, sys
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy as v2n
from vtk.util.numpy_support import numpy_to_vtk as n2v
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5 import QtGui, QtWidgets, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import rc
from pkg_resources import Requirement, resource_filename
from OpenRS.open_rs_common import get_file, get_save_file, line_query_vtk, line_query_NDinterp, generate_axis_actor, generate_info_actor, xyview, yzview, xzview, flip_visible, make_logo, modeling_widget, generate_sphere, do_transform
from OpenRS.open_rs_hdf5_io import *
from OpenRS.transform_widget import make_translate_button_layout

def launch(*args, **kwargs):
    '''
    Start Qt/VTK interaction if started independently
    '''
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    app.processEvents()
    
    window = interactor(None) #otherwise specify parent widget
    window.show()
    
    if len(args) == 1:
        window.file = args[0]
        interactor.load_h5(window)
    
    ret = app.exec_()
    
    if sys.stdin.isatty() and not hasattr(sys, 'ps1'):
        sys.exit(ret)
    else:
        return window

class main_window(object):
    """
    Generic object containing all UI
    """
    
    def setup(self, MainWindow):
        '''
        Creates Qt interactor
        '''
        
        #if called as a script, then treat as a mainwindow, otherwise treat as a generic widget
        if hasattr(MainWindow,'setCentralWidget'):
            MainWindow.setCentralWidget(self.centralWidget)
        else:
            self.centralWidget=MainWindow
        MainWindow.setWindowTitle("OpenRS - model viewer v%s" %__version__)
        
        #create new layout to hold both VTK and Qt interactors
        mainlayout=QtWidgets.QHBoxLayout(self.centralWidget)

        #create VTK widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        
        #create Qt layout to contain interactions
        load_model_box = QtWidgets.QGridLayout()
        
        #create VTK widget
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        self.vtkWidget.setSizePolicy(sizePolicy)
        
        self.vtkWidget.setMinimumSize(QtCore.QSize(800, 600))
        
        #set fonts
        head_font=QtGui.QFont("Helvetica [Cronyx]",weight=QtGui.QFont.Bold)
        io_font = QtGui.QFont("Helvetica")
        
        #make display layout
        display_box = QtWidgets.QGroupBox('Display')
        #buttons
        self.load_button = QtWidgets.QPushButton('Load')
        self.load_label = QtWidgets.QLabel("Nothing loaded.")
        self.load_label.setWordWrap(True)
        self.load_label.setFont(io_font)
        self.load_label.setToolTip('Load results file')
        #make combo box for components
        self.component_cb = QtWidgets.QComboBox()
        self.component_cb.setToolTip('Change stress component displayed')
        # self.component_cb.addItems(['\u03C311', '\u03C322', '\u03C333'])
        self.component_cb.setEnabled(False)
        self.mesh_display=QtWidgets.QPushButton("Edges off")
        self.mesh_display.setToolTip('Turn mesh/edges on and off')
        self.mesh_display.setCheckable(True)
        self.mesh_display.setChecked(False)
        self.mesh_display.setEnabled(False)
        # self.translate_drop_button = make_trans_button(self)
        
        
        self.extract_boundaries_button = QtWidgets.QPushButton('Extract boundary')
        self.extract_boundaries_button.setEnabled(False)
        self.extract_boundaries_button.setToolTip('Extract boundary of model')
        self.export_STL_button = QtWidgets.QRadioButton("Write STL")
        self.export_STL_button.setChecked(False)
        self.export_STL_button.setEnabled(False)
        
        
        #make contour layout
        contour_layout = QtWidgets.QGridLayout()
        contour_box = QtWidgets.QGroupBox('Contours')
        min_contour_label = QtWidgets.QLabel("Min:")
        self.min_contour = QtWidgets.QDoubleSpinBox()
        self.min_contour.setMinimum(-100000)
        self.min_contour.setMaximum(100000)
        max_contour_label = QtWidgets.QLabel("Max:")
        self.max_contour = QtWidgets.QDoubleSpinBox()
        self.max_contour.setMinimum(-100000)
        self.max_contour.setMaximum(100000)
        num_contour_label = QtWidgets.QLabel("Interval:")
        self.num_contour = QtWidgets.QSpinBox()
        self.num_contour.setToolTip('Number of entries shown on colorbar')
        self.num_contour.setMinimum(3)
        self.num_contour.setMaximum(20)
        self.num_contour.setValue(5)
        self.update_contours_button = QtWidgets.QPushButton('Update')
        self.update_contours_button.setToolTip('Update the contour limits and interval')
        self.update_contours_button.setEnabled(False)
        contour_layout.addWidget(min_contour_label,1,0,1,1)
        contour_layout.addWidget(self.min_contour,1,1,1,1)
        contour_layout.addWidget(max_contour_label,1,2,1,1)
        contour_layout.addWidget(self.max_contour,1,3,1,1)
        contour_layout.addWidget(num_contour_label,1,4,1,1)
        contour_layout.addWidget(self.num_contour,1,5,1,1)
        contour_layout.addWidget(self.update_contours_button,1,6,1,1)
        
        
        # line extraction from surface
        extract_layout = QtWidgets.QGridLayout()
        extract_box = QtWidgets.QGroupBox('Extract')
        # labels for axes
        x_label = QtWidgets.QLabel("x")
        y_label = QtWidgets.QLabel("y")
        z_label = QtWidgets.QLabel("z")
        # x, y, z of first point
        start_label = QtWidgets.QLabel("Start")
        start_label.setToolTip('Start coordinate of line trace')
        self.point1_x_coord = QtWidgets.QDoubleSpinBox()
        self.point1_x_coord.setMinimum(-100000)
        self.point1_x_coord.setMaximum(100000)
        self.point1_y_coord = QtWidgets.QDoubleSpinBox()
        self.point1_y_coord.setMinimum(-100000)
        self.point1_y_coord.setMaximum(100000)
        self.point1_z_coord = QtWidgets.QDoubleSpinBox()
        self.point1_z_coord.setMinimum(-100000)
        self.point1_z_coord.setMaximum(100000)

        # x, y, z of second point
        end_label = QtWidgets.QLabel("End")
        end_label.setToolTip('End coordinate of line trace')
        self.point2_x_coord = QtWidgets.QDoubleSpinBox()
        self.point2_x_coord.setMinimum(-100000)
        self.point2_x_coord.setMaximum(100000)
        self.point2_y_coord = QtWidgets.QDoubleSpinBox()
        self.point2_y_coord.setMinimum(-100000)
        self.point2_y_coord.setMaximum(100000)
        self.point2_z_coord = QtWidgets.QDoubleSpinBox()
        self.point2_z_coord.setMinimum(-100000)
        self.point2_z_coord.setMaximum(100000)
        
        # x, y, z of clip point
        clip_label = QtWidgets.QLabel("Clip")
        clip_label.setToolTip('Tertiary coordinate to specify clipping plane')
        self.clip_x_coord = QtWidgets.QDoubleSpinBox()
        self.clip_x_coord.setMinimum(-100000)
        self.clip_x_coord.setMaximum(100000)
        self.clip_y_coord = QtWidgets.QDoubleSpinBox()
        self.clip_y_coord.setMinimum(-100000)
        self.clip_y_coord.setMaximum(100000)
        self.clip_z_coord = QtWidgets.QDoubleSpinBox()
        self.clip_z_coord.setMinimum(-100000)
        self.clip_z_coord.setMaximum(100000)
        
        #clip settings
        self.clip_active_button=QtWidgets.QPushButton("Update clip")
        self.clip_active_button.setToolTip('Show/update clipped model')
        self.clip_active_button.setEnabled(False)
        
        interval_label=QtWidgets.QLabel("Line interval:")
        self.extract_interval=QtWidgets.QSpinBox()
        self.extract_interval.setToolTip('Number of points to extract along line trace')
        self.extract_interval.setValue(50)
        self.extract_interval.setMinimum(3)
        self.extract_interval.setMaximum(1000)
        
        self.extract_button = QtWidgets.QPushButton('Update line')
        self.extract_button.setToolTip('Show/update line trace')
        self.extract_button.setEnabled(False)
        self.export_line_button = QtWidgets.QPushButton('Export line')
        self.export_line_button.setEnabled(False)
        self.export_line_button.setToolTip('Export line trace to file')

        
        
        #create figure canvas etc

        #initialize plot
        self.figure = plt.figure(figsize=(4,4))
        plt.text(0.5, 0.5, "'Update line' for plot", ha='center', style='italic', fontweight = 'bold', color='lightgray', size= 18)
        plt.axis('off')
        #changes the background of the plot, otherwise white
        # self.figure.patch.set_facecolor((242/255,242/255,242/255))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(QtCore.QSize(400, 500))

        #add everything to the extract layout
        extract_layout.addWidget(x_label,1,1,1,1)
        extract_layout.addWidget(y_label,1,2,1,1)
        extract_layout.addWidget(z_label,1,3,1,1)
        extract_layout.addWidget(start_label,2,0,1,1)
        extract_layout.addWidget(self.point1_x_coord,2,1,1,1)
        extract_layout.addWidget(self.point1_y_coord,2,2,1,1)
        extract_layout.addWidget(self.point1_z_coord,2,3,1,1)
        extract_layout.addWidget(end_label,3,0,1,1)
        extract_layout.addWidget(self.point2_x_coord,3,1,1,1)
        extract_layout.addWidget(self.point2_y_coord,3,2,1,1)
        extract_layout.addWidget(self.point2_z_coord,3,3,1,1)
        extract_layout.addWidget(clip_label,4,0,1,1)
        extract_layout.addWidget(self.clip_x_coord,4,1,1,1)
        extract_layout.addWidget(self.clip_y_coord,4,2,1,1)
        extract_layout.addWidget(self.clip_z_coord,4,3,1,1)
        extract_layout.addWidget(self.extract_button,5,2,1,1)
        extract_layout.addWidget(self.clip_active_button,5,3,1,1)
        extract_layout.addWidget(self.canvas,6,0,1,4)
        

        load_model_box.addWidget(self.load_button,0,0,1,1)
        load_model_box.addWidget(self.component_cb,0,1,1,1)
        load_model_box.addWidget(self.mesh_display,0,2,1,1)
        load_model_box.addWidget(self.load_label,1,0,1,3)
        # load_model_box.addWidget(self.translate_drop_button, 2,0,1,1)
        load_model_box.addLayout(make_translate_button_layout(self), 2,0,1,1)
        load_model_box.addWidget(self.extract_boundaries_button,2,1,1,1)
        load_model_box.addWidget(self.export_STL_button,2,2,1,1)
        
        #add layouts to boxes
        display_box.setLayout(load_model_box)
        contour_box.setLayout(contour_layout)
        evlayout=QtWidgets.QVBoxLayout()
        evbutton_layout = QtWidgets.QHBoxLayout()
        evbutton_layout.addWidget(interval_label)
        evbutton_layout.addWidget(self.extract_interval)
        verticalSpacer = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        evbutton_layout.addItem(verticalSpacer)
        evbutton_layout.addWidget(self.export_line_button)
        
        evlayout.addLayout(extract_layout)
        evlayout.addLayout(evbutton_layout)
        
        extract_box.setLayout(evlayout)
        
        lvlayout=QtWidgets.QVBoxLayout()
        lvlayout.addWidget(display_box)
        lvlayout.addWidget(contour_box)
        lvlayout.addWidget(extract_box)

        lvlayout.addStretch(1)
        
        mainlayout.addWidget(self.vtkWidget)
        mainlayout.addStretch(1)
        mainlayout.addLayout(lvlayout)

        def initialize(self):
            self.vtkWidget.start()

class interactor(QtWidgets.QWidget):
    '''
    Inherits most properties from Qwidget, but primes the VTK window, and ties functions and methods to interactors defined in main_window
    '''
    def __init__(self,parent):
        super(interactor, self).__init__(parent)
        self.ui = main_window()
        self.ui.setup(self)
        self.ren = vtk.vtkRenderer()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("aliceblue"))

        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        style=vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        self.iren.AddObserver("KeyPressEvent", self.keypress)
        self.iren.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.ren.GetActiveCamera().ParallelProjectionOn()
        self.ui.vtkWidget.Initialize()
        
        self.file = None #overwritten at launch
        self.picking = False
        self.trans = np.eye(4) #default
        self.c_trans = np.eye(4) #initialise cumulative transformation
        make_logo(self.ren)
        
        self.ui.load_button.clicked.connect(self.load_model)
        self.ui.mesh_display.clicked.connect(self.toggle_edges)
        self.ui.clip_active_button.clicked.connect(self.clip)
        self.ui.extract_button.clicked.connect(self.extract)
        self.ui.export_line_button.clicked.connect(self.export_line)
        self.ui.update_contours_button.clicked.connect(self.update_scale_bar)
        self.ui.extract_boundaries_button.clicked.connect(self.get_boundaries)
        self.ui.trans_widget.trans_origin_button.clicked.connect(self.apply_trans)
        self.ui.trans_reset_button.clicked.connect(self.reset_trans)
        self.ui.trans_widget.choose_vertex_button.clicked.connect(self.actuate_node_pick)
        self.ui.component_cb.currentIndexChanged.connect(self.draw_model)
    
    def reset_trans(self):
        '''
        Applies the inverse of the current transformation matrix to revert all transformations, resets inputs for movement
        '''
        self.trans = np.linalg.inv(self.c_trans)
        self.apply_transformation()
        
        self.ui.trans_widget.translate_x.setValue(0)
        self.ui.trans_widget.translate_y.setValue(0)
        self.ui.trans_widget.translate_z.setValue(0)
        self.display_info('Reset translation.')
    
    def apply_trans(self):
        '''
        Applies the appropriate transformation to the existing model object(s)
        '''
        self.ui.translate_drop_button.setChecked(False)

        self.trans[0,-1] = self.ui.trans_widget.translate_x.value()
        self.trans[1,-1] = self.ui.trans_widget.translate_y.value()
        self.trans[2,-1] = self.ui.trans_widget.translate_z.value()
        self.apply_transformation()
        self.display_info('Translated model.')
        if self.picking:
            self.actuate_node_pick()

    def apply_transformation(self):
    
        T = self.trans.copy()

        np_pts = v2n(self.model_obj.GetPoints().GetData())
        np_pts = do_transform(np_pts,T)
        self.c_trans = T @ self.c_trans
        self.trans = np.eye(4)
        
        self.model_obj.GetPoints().SetData(n2v(np_pts))
        self.model_obj.Modified()
        self.draw_model()
        self.ui.vtkWidget.update()

    def get_boundaries(self):
        '''
        Extracts the boundaries of the model to a polydata object, if export_STL is selected then ask for where to save it.
        '''
        #can't be activated unless load_model has run
        extract_surface = vtk.vtkDataSetSurfaceFilter()
        extract_surface.SetInputDataObject(self.model_obj)
        extract_surface.Update()
        self.model_boundary = vtk.vtkPolyData()
        self.model_boundary = extract_surface.GetOutput()
        msg = 'Extracted boundaries.'
        
        if self.ui.export_STL_button.isChecked():
            #get file name
            fileo, _ = get_save_file('*.stl')
            if fileo is None:
                return
            writer = vtk.vtkSTLWriter()
            writer.SetFileName(fileo)
            writer.SetInputData(self.model_boundary)
            msg = 'Extracted boundaries and wrote STL file.' #overwrite msg if stl was written
            writer.Write()
        
        self.display_info(msg)
        self.ui.vtkWidget.update()

    
    def toggle_edges(self):
        '''
        changes the visibility of edges on the active mesh_actor
        '''
        if hasattr(self,'mesh_actor'):
            if self.ui.mesh_display.isChecked():
                self.model_actor.GetProperty().EdgeVisibilityOff()
            else:
                self.model_actor.GetProperty().EdgeVisibilityOn()
        
        if hasattr(self,'clipped_actor'):
            if self.ui.mesh_display.isChecked():
                self.clipped_actor.GetProperty().EdgeVisibilityOff()
            else:
                self.clipped_actor.GetProperty().EdgeVisibilityOn()
        
        self.ui.vtkWidget.update()
        

    def write_h5(self):
        '''
        method which writes to an hdf5 file if there is anything to write
        '''
        if self.file is None:
            self.file = initialize_HDF5()
        
        #itinerary from this interactor is just the model. If there is an existing unstructured grid, then nothing needs to be written
        if hasattr(self,'active_obj') and isinstance(self.active_obj, str):
            if "vtkPolyData" in str(type(self.model_obj)):
                w = HDF5vtkpd_writer()
            else:
                w = HDF5vtkug_writer()
            #set up pipeline for pushing through the current mesh
            pt = vtk.vtkPassThrough()
            pt.SetInputData(self.model_obj)
            w.SetInputConnection(pt.GetOutputPort())
            
            w.SetFileName(self.file)
            w.Update()
            self.display_info('Saved to data file.')
            with h5py.File(self.file, 'r+') as f:
                f.attrs['date_modified'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                #if there's an stl file
                if hasattr(self,'model_boundary'):
                    # get points and verts from the boundary polydata, clearing anything that might already be there
                    del f['model_boundary/points']
                    del f['model_boundary/vertices']
                    np_pts = v2n(self.model_boundary.GetPoints().GetData())
                    np_verts = v2n(self.model_boundary.GetPolys().GetData())
                    f.create_dataset('model_boundary/points', data=np_pts)
                    f.create_dataset('model_boundary/vertices', data=np_verts)
                self.display_info('Saved to data file.')
        else:
            return

    def draw_model(self):
        '''
        Main method which updates the display of the model.
        '''
        
        #clear renderer
        self.ren.RemoveAllViewProps()
        
        #Logic which bypasses the initial call from the combobox on loading
        if self.ui.component_cb.currentText() != '':
            self.component = self.ui.component_cb.currentText()
        
        edges = False
        from_load = False #until turned false
        
        
        if hasattr(self,'active_obj') and not hasattr(self,'model_obj'):
            from_load = True
            #read the model data
            self.model_obj, components = read_model_data(self.active_obj)
            #update the combobox with the components
            self.ui.component_cb.clear()
            self.ui.component_cb.addItems(components)
            self.component = self.ui.component_cb.currentText()
            
            #edge display conditioning
            
            if "vtkUnstructuredGrid" in str(type(self.model_obj)):
                self.ui.mesh_display.setEnabled(True)
            elif "vtkPolyData" in str(type(self.model_obj)):
                self.ui.mesh_display.setEnabled(False)

            if "vtkPolyData" in str(type(self.model_obj)):
                self.model_actor, self.model_mapper, self.lut, range_ = gen_pd_actor(self.model_obj, self.component)
                self.ui.extract_boundaries_button.setEnabled(False)
                self.ui.export_STL_button.setEnabled(False)
            else:
            
                if not self.ui.mesh_display.isChecked():
                    edges = True
                self.model_actor, self.model_mapper, self.lut, range_ = gen_ug_actor(self.model_obj, self.component, edges)

                self.ui.extract_boundaries_button.setEnabled(True)
                self.ui.export_STL_button.setEnabled(True)

            self.ui.update_contours_button.setEnabled(True)
            self.ui.extract_button.setEnabled(True)
            self.ui.export_line_button.setEnabled(True)
            
            self.ui.trans_widget.trans_origin_button.setEnabled(True)
            self.ui.trans_reset_button.setEnabled(True)
            self.ui.trans_widget.choose_vertex_button.setEnabled(True)
            
        else: #hasattr(self,'model_obj'): #then operate on the existing model
            try:
                if "vtkPolyData" in str(type(self.model_obj)):
                    self.model_actor, self.model_mapper, self.lut, range_ = gen_pd_actor(self.model_obj, self.component)
                else:
                    if not self.ui.mesh_display.isChecked():
                        edges = True
                    self.model_actor, self.model_mapper, self.lut, range_ = gen_ug_actor(self.model_obj, self.component, edges)
            except:
                return
        
        #update contour limits
        self.ui.min_contour.setValue(range_[0])
        self.ui.max_contour.setValue(range_[1])
        
        
        #create scale bar
        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalarBarRep = scalar_bar_widget.GetRepresentation()
        scalarBarRep.GetPositionCoordinate().SetValue(0.01,0.01)
        scalarBarRep.GetPosition2Coordinate().SetValue(0.09,0.9)
        self.sb_actor=scalar_bar_widget.GetScalarBarActor()

        self.sb_actor.SetNumberOfLabels(self.ui.num_contour.value())

        self.sb_actor.SetLookupTable(self.lut)
        self.sb_actor.SetTitle('MPa')


        #attempt to change scalebar properties
        propT = vtk.vtkTextProperty()
        propL = vtk.vtkTextProperty()
        propT.SetColor(0,0,0)
        propL.SetColor(0,0,0)
        propT.SetFontFamilyToArial()
        # propT.ItalicOff()
        propT.BoldOn()
        propL.BoldOff()
        propL.SetFontSize(1)
        propT.SetFontSize(1)
        self.sb_actor.GetLabelTextProperty().SetColor(0,0,0)
        self.sb_actor.GetTitleTextProperty().SetColor(0,0,0)
        self.sb_actor.GetLabelTextProperty().SetFontSize(1)
        self.sb_actor.GetTitleTextProperty().SetFontSize(1)
        self.sb_actor.SetLabelFormat("%.1f")

        self.ren.AddActor(self.model_actor)
        self.ren.AddActor(self.sb_actor)
        self.axis_actor = generate_axis_actor(self.model_obj,self.ren)
        self.ren.AddActor(self.axis_actor)
        
        scalar_bar_widget.SetInteractor(self.iren)
        scalar_bar_widget.On()
        self.ren.ResetCamera()
        
        self.ui.vtkWidget.update()
    
    def update_scale_bar(self):
        '''
        updates the active scale bar with limits and number of intervals from ui
        '''
        r = (self.ui.min_contour.value(),self.ui.max_contour.value())
        self.model_mapper.SetScalarRange(r[0], r[1])
        if hasattr(self,'clip_mapper'):
            self.clip_mapper.SetScalarRange(r[0], r[1])
        self.sb_actor.SetNumberOfLabels(self.ui.num_contour.value())
        self.ui.vtkWidget.update()

    def extract(self):
        '''
        Get points from ui, call line_query and plot data on matplotlib canvas
        '''
        if not hasattr(self,'model_obj'):
            return
        
        p1 = [self.ui.point1_x_coord.value(), self.ui.point1_y_coord.value(), self.ui.point1_z_coord.value()]
        p2 = [self.ui.point2_x_coord.value(), self.ui.point2_y_coord.value(), self.ui.point2_z_coord.value()]
        if "vtkPolyData" in str(type(self.model_obj)):
            self.q = line_query_NDinterp(self.model_obj,p1,p2,self.ui.extract_interval.value(),self.component)
        else:
            self.q = line_query_vtk(self.model_obj,p1,p2,self.ui.extract_interval.value(),self.component)
        self.x = range(self.q.shape[0])
        self.ui.figure.clear()
        
        ax = self.ui.figure.add_subplot(111)
        ax.scatter(self.x,self.q[:,-1])
        ax.set_ylabel("%s (MPa)"%self.component)
        ax.set_xlabel("Point number")
        ax.grid(visible=True, which='major', color='#666666', linestyle='-')
        ax.minorticks_on()
        ax.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        self.ui.figure.tight_layout()
        self.ui.canvas.draw()
        
        #remove any line actor currently present
        if hasattr(self,'line_actor'):
            self.ren.RemoveActor(self.line_actor)
        self.ui.vtkWidget.update()
        
        #draw a line on the interactor
        line = vtk.vtkLineSource()
        line.SetResolution(self.ui.extract_interval.value())
        line.SetPoint1(p1)
        line.SetPoint2(p2)
        line.Update()
        
        sphere1 = vtk.vtkSphereSource()
        sphere1.SetCenter(p1)
        sphere1.Update()
        
        sphere2 = vtk.vtkSphereSource()
        sphere2.SetCenter(p2)
        sphere2.Update()
        
        appendFilter = vtk.vtkAppendPolyData()
        appendFilter.AddInputData(sphere1.GetOutput())
        appendFilter.AddInputData(line.GetOutput())
        appendFilter.AddInputData(sphere2.GetOutput())
        appendFilter.Update()
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(appendFilter.GetOutput())
        self.line_actor = vtk.vtkActor()
        self.line_actor.SetMapper(mapper)
        colors = vtk.vtkNamedColors()
        self.line_actor.GetProperty().SetColor(colors.GetColor3d("Violet"))
        self.ren.AddActor(self.line_actor)
        self.ui.export_line_button.setEnabled(True)
        
        self.ui.vtkWidget.update()

    def clip(self):
        '''
        Activates clipping by hiding mesh_actor and replacing it with a clipped actor based on the points set in the text box. Clipping plane is specified by the plane defined by 'Start','End' and 'Clip'.
        Clipping is removed by specifying zeros for the third point, and by virtue avoids a divide by zero error when calculating the clipping plane normal.
        '''
        
        if hasattr(self,'clipped_actor'):
            self.ren.RemoveActor(self.clipped_actor)
            
        #read points for plane
        p1 = np.array([self.ui.point1_x_coord.value(), self.ui.point1_y_coord.value(), self.ui.point1_z_coord.value()])
        p2 = np.array([self.ui.point2_x_coord.value(), self.ui.point2_y_coord.value(), self.ui.point2_z_coord.value()])
        p3 = np.array([self.ui.clip_x_coord.value(), self.ui.clip_y_coord.value(), self.ui.clip_z_coord.value()])
        
        c = p3 == np.zeros(3)
        if c.all() and self.model_actor.GetVisibility() == 0: #no clipping plane (p3 = 0,0,0) is specified & mesh is hidden
            flip_visible(self.model_actor)

        elif not c.all():
            clipPlane = vtk.vtkPlane()
            clipPlane.SetOrigin(((p1+p2)/2).tolist())
            #solve cross product between p1,p2 and p2,p3
            xnorm = np.cross((p2-p1),(p3-p2))
            xnorm = xnorm / np.sqrt(np.sum(xnorm**2))
            clipPlane.SetNormal(xnorm.tolist())
            
            clipper = vtk.vtkTableBasedClipDataSet() #needs to be table based, otherwise the grid is interpolated
            clipper.SetClipFunction(clipPlane)
            clipper.SetInputData(self.model_obj) #needs to remain vtk object
            clipper.GenerateClippedOutputOn()
            clipper.Update()

            self.clip_mapper = vtk.vtkDataSetMapper()
            self.clip_mapper.SetInputData(clipper.GetClippedOutput())
            self.clip_mapper.SetLookupTable(self.lut)
            self.clip_mapper.SetScalarRange(self.model_obj.GetScalarRange())

            self.clipped_actor = vtk.vtkActor()
            self.clipped_actor.SetMapper(self.clip_mapper)
            if self.ui.mesh_display.isChecked():
                self.clipped_actor.GetProperty().EdgeVisibilityOff()
            else:
                self.clipped_actor.GetProperty().EdgeVisibilityOn()
            if self.model_actor.GetVisibility() == 1:
                flip_visible(self.model_actor)
            self.ren.AddActor(self.clipped_actor)
        
        self.ui.vtkWidget.update()
        # QtWidgets.QApplication.processEvents()
        
    def export_line(self):
        """
        Collects data from ui, writes to a valid file
        """
        
        fileo, _ = get_save_file('*.csv')
        if fileo is None:
            return
        
        np.savetxt(fileo,
        np.column_stack((self.x,self.q)), 
        delimiter=',',
        header = "%s\nPoint number, x, y, z, %s (MPa)"%(self.active_obj,self.component),
        fmt='%i, %.3f, %.3f, %.3f, %.3f')
        self.display_info('Line exported.')

    def load_model(self):
        """
        Method to return a valid model file
        """
        
        filep, startdir = get_file('*.vtu','*.vtp')
        if filep is None:
            return
        if not(os.path.isfile(filep)):
            self.display_info('Invalid model file.')
            return
        
        if hasattr(self,'model_obj'):
            delattr(self, 'active_obj')
            delattr(self, 'model_obj')
            delattr(self, 'component')
            #clear all actors
            self.ren.RemoveAllViewProps()
            
        self.active_obj = filep
        self.ui.load_label.setText(filep)
        #call draw_model
        self.ui.component_cb.setEnabled(True)
        
        self.ui.clip_active_button.setEnabled(True)
        self.draw_model()
        
        
        
            
    def load_h5(self):
        if self.file is None:
            self.file, _ = get_file("*.OpenRS")
        
        self.polydata_mode = False
        if self.file is not None:
            #check the file has a populated model object
            with h5py.File(self.file, 'r') as f:
                if "model_data/piece0" not in f:
                    self.display_info('Model data could not be loaded.')
                if "model_data/piece0/cell_types" not in f:
                    self.polydata_mode = True
            
            if not self.polydata_mode:
                r = HDF5vtkug_reader()
                r.SetFileName(self.file)
                r.Update()
            else:
                r = HDF5vtkpd_reader()
                r.SetFileName(self.file)
                r.Update()
            
            self.active_obj = r.GetOutputDataObject(0).GetBlock(0)
            
            self.ui.load_label.setText(self.file)
            #call draw_model
            self.ui.component_cb.setEnabled(True)
            self.ui.mesh_display.setEnabled(True)
            self.ui.clip_active_button.setEnabled(True)
            self.draw_model()
            self.display_info('Loaded model from data file.')
        self.ui.vtkWidget.update() #for display of info_actor

    def keypress(self, obj, event):
        '''
        VTK interactor-specific listener for keypresses
        '''
        key = obj.GetKeySym()
        
        if key =="1":
            xyview(self.ren)
        elif key =="2":
            yzview(self.ren)
        elif key =="3":
            xzview(self.ren)
        elif key == "Up":
            self.ren.GetActiveCamera().Roll(30)
        elif key == "Down":
            self.ren.GetActiveCamera().Roll(-30)
        elif key == "w": #debug
            self.write_h5()
        elif key == "l": #debug
            self.load_h5()
        elif key == "m":
            self.mw = modeling_widget(self)
        elif key == "n":
            self.actuate_node_pick()

        elif key=="i":
            im = vtk.vtkWindowToImageFilter()
            writer = vtk.vtkPNGWriter()
            colors = vtk.vtkNamedColors()
            self.ren.SetBackground(colors.GetColor3d("white"))
            im.SetInput(self.ui.vtkWidget._RenderWindow)
            im.Update()
            writer.SetInputConnection(im.GetOutputPort())
            writer.SetFileName("OpenRS_capture.png")
            writer.Write()
            self.ren.SetBackground(colors.GetColor3d("aliceblue"))
            self.display_info('Image saved.')
        
        elif key=="r":
            flip_visible(self.axis_actor)
        
        self.ren.ResetCamera()
        self.ui.vtkWidget.update()

    def on_mouse_move(self, obj, event):
        '''
        causes issues with finalizing when run as a stand-alone widget
        '''
        if hasattr(self,'info_actor'):
            self.ren.RemoveActor(self.info_actor)
        else:
            pass

    def display_info(self,msg):
        '''
        Checks if there's an info_actor and removes it before displaying another one
        '''
        if hasattr(self,'info_actor'):
            self.ren.RemoveActor(self.info_actor)
        self.info_actor = generate_info_actor(msg,self.ren)
        self.ren.AddActor(self.info_actor)

    def actuate_node_pick(self):
        '''
        Starts picking and handles ui button display
        '''
        
        if hasattr(self,'selected_actor'):
            self.ren.RemoveActor(self.selected_actor)
        
        if self.picking:
            #Remove picking observer and re-initialise
            self.iren.RemoveObservers('LeftButtonPressEvent')
            self.iren.AddObserver('LeftButtonPressEvent',self.default_left_button)
            QtWidgets.QApplication.processEvents()
            self.picking = False
            self.ui.translate_drop_button.setChecked(False)

        else:
            self.iren.AddObserver('LeftButtonPressEvent', self.picker_callback)
            self.picking = True
            #meant to keep dropdown engaged through the picking process, but ineffective. Stopping picking suspends, as does 'updating'.
            self.ui.translate_drop_button.setChecked(True)

    def default_left_button(self, obj, event):
        #forward standard events according to the default style`
        self.iren.GetInteractorStyle().OnLeftButtonDown()

    def picker_callback(self, obj, event):
        """
        Actuates a pick of a node
        """
        
        colors = vtk.vtkNamedColors()
        
        picker = vtk.vtkPointPicker()
        picker.SetTolerance(0.005)
        
        pos = self.iren.GetEventPosition()
        
        picker.Pick(pos[0], pos[1], 0, self.ren)
        
        if picker.GetPointId() != -1:

            ids = vtk.vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(picker.GetPointId())

            if hasattr(self,'selected_actor'):
                self.ren.RemoveActor(self.selected_actor)
            self.selected_node = picker.GetPointId()
            centre = self.model_obj.GetPoint(picker.GetPointId())
            self.selected_actor = generate_sphere(centre,1,colors.GetColor3d("orchid"))
            
            self.ui.trans_widget.translate_x.setValue(-centre[0])
            self.ui.trans_widget.translate_y.setValue(-centre[1])
            self.ui.trans_widget.translate_z.setValue(-centre[2])
            
            self.ren.AddActor(self.selected_actor)
            


def read_model_data(obj):
    '''
    Read an unstructured grid from an XML formatted vtu file, or operate on a ug object, returning the ug and component names.
    '''

    #If read is true, then vtuname is a VTU file
    if type(obj) is str and obj.lower().endswith('.vtu'):
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(obj)
        reader.Update()
        output = reader.GetOutput()
    elif type(obj) is str and obj.lower().endswith('.vtp'):
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(obj)
        reader.Update()
        output = reader.GetOutput()
    else: #coming from hdf5reader
        output = obj
    #get the component names
    components = []
    for index in range(output.GetPointData().GetNumberOfArrays()):
        components.append(output.GetPointData().GetArrayName(index))

    return output, components

def gen_ug_actor(ug, component, edges):
    '''
    Return an actor with a look up table and range_ of component selected. Edges are on if true.
    '''
    ug.GetPointData().SetActiveScalars(component)

    #build lookup table according to field
    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.667, 0)
    lut.Build()
    range_ = ug.GetScalarRange()

    # map data set
    mesh_mapper = vtk.vtkDataSetMapper()
    mesh_mapper.SetInputData(ug)
    mesh_mapper.SetScalarRange(range_)
    mesh_mapper.SetLookupTable(lut)

    actor = vtk.vtkActor()
    actor.SetMapper(mesh_mapper)
    if edges:
        actor.GetProperty().EdgeVisibilityOn()
    else:
        actor.GetProperty().EdgeVisibilityOff()
    actor.GetProperty().SetLineWidth(0)

    return actor, mesh_mapper, lut, range_

def gen_pd_actor(pd,component,size=2):
    '''
    Returns vtk objects and actor for a point cloud having size points, returns color array associated with the actor/polydata object as well as a lookuptable for rendering a scalebar.
    '''
    
    pd.GetPointData().SetActiveScalars(component)

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.667, 0.0)
    lut.Build()
    range_ = pd.GetScalarRange()

    # map data set
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(pd)
    mapper.SetScalarRange(range_)
    mapper.SetLookupTable(lut)

    actor = vtk.vtkActor()

    mapper.SetInputData(pd)

    actor=vtk.vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetPointSize(size)
    return actor, mapper, lut, range_


if __name__ == "__main__":
    if len(sys.argv)>1:
        launch(sys.argv[1])
    else:
        launch()