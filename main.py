# -*- coding: utf-8 -*-

# Author: Ajith Pattammattel
# First Version on:06-23-2020

import logging, sys, webbrowser

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDesktopWidget, QApplication

from StackPlot import *
from StackCalcs import *
from MaskView import *

logger = logging.getLogger()


class midasWindow(QtWidgets.QMainWindow):
    def __init__(self, im_stack=None, energy=[], refs=[]):
        super(midasWindow, self).__init__()
        uic.loadUi('uis/mainwindow_admin.ui', self)
        self.im_stack = im_stack
        self.updated_stack = self.im_stack
        self.energy = energy
        self.refs = refs
        self.log_warning=0

        self.actionOpen_Image_Data.triggered.connect(self.browse_file)
        self.actionOpen_Multiple_Files.triggered.connect(self.load_mutliple_file)
        self.actionSave_as.triggered.connect(self.save_stack)
        self.actionExit.triggered.connect(self.close)
        self.actionOpen_in_GitHub.triggered.connect(self.open_github_link)
        self.actionLoad_Energy.triggered.connect(self.select_elist)
        self.menuFile.setToolTipsVisible(True)

        self.actionOpen_Mask_Gen.triggered.connect(self.openMaskMaker)
        self.cb_transpose.stateChanged.connect(self.transpose_stack)
        self.cb_log.stateChanged.connect(self.replot_image)
        self.cb_rebin.stateChanged.connect(self.view_stack)
        self.cb_upscale.stateChanged.connect(self.view_stack)
        self.cb_remove_edges.stateChanged.connect(self.view_stack)
        self.cb_norm.stateChanged.connect(self.replot_image)
        self.cb_smooth.stateChanged.connect(self.replot_image)
        self.hs_smooth_size.valueChanged.connect(self.replot_image)
        self.cb_remove_outliers.stateChanged.connect(self.replot_image)
        self.cb_remove_bg.stateChanged.connect(self.replot_image)
        self.hs_nsigma.valueChanged.connect(self.replot_image)
        self.hs_bg_threshold.valueChanged.connect(self.replot_image)
        self.pb_reset_img.clicked.connect(self.reset_and_load_stack)
        self.pb_crop.clicked.connect(self.crop_to_dim)
        self.pb_crop.clicked.connect(self.view_stack)
        self.pb_ref_xanes.clicked.connect(self.select_ref_file)
        self.pb_elist_xanes.clicked.connect(self.select_elist)

        # save_options
        self.pb_save_disp_img.clicked.connect(self.save_disp_img)
        self.pb_save_disp_spec.clicked.connect(self.save_disp_spec)

        # Analysis
        self.pb_pca_scree.clicked.connect(self.pca_scree_)
        self.pb_calc_components.clicked.connect(self.calc_comp_)
        self.pb_kmeans_elbow.clicked.connect(self.kmeans_elbow)
        self.pb_calc_cluster.clicked.connect(self.clustering_)
        self.pb_xanes_fit.clicked.connect(self.fast_xanes_fitting)
        self.pb_plot_refs.clicked.connect(self.plt_xanes_refs)

        self.show()

    def browse_file(self):
        filename = QFileDialog().getOpenFileName(self, "Select image data", '', 'image file(*.hdf *.h5 *tiff *tif )')
        self.file_name = (str(filename[0]))

        try:
            self.reset_and_load_stack()
        except:
            self.statusbar_main.showMessage("Error: Unable to Load Data")

    def load_mutliple_file(self):
        filter = "TIFF (*.tiff);;TIF (*.tif)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", " ", filter)

        all_images = []
        for im_file in names[0]:
            img = tf.imread(im_file)
            all_images.append(img)
        self.stack_ = np.dstack(all_images)
        self.sb_zrange2.setValue(self.stack_.shape[-1])
        self.set_stack_params()

    def load_stack(self):
        self.sb_zrange2.setMaximum(100000)
        self.sb_zrange1.setValue(0)

        self.statusbar_main.showMessage('Loading.. please wait...')

        if self.file_name.endswith('.h5'):
            self.stack_, mono_e, bl_name, self.avgIo = get_xrf_data(self.file_name)
            self.statusbar_main.showMessage(f'Data from {bl_name}')
            self.sb_zrange2.setValue(mono_e / 10)

        elif self.file_name.endswith('.tiff') or self.file_name.endswith('.tif'):
            self.stack_ = tf.imread(self.file_name).transpose(1, 2, 0)
            self.sb_zrange2.setValue(self.stack_.shape[-1])
            self.avgIo = 1

        else:
            logger.error('Unknown data format')

        self.set_stack_params()

    def set_stack_params(self):

        self.sb_zrange2.setMaximum(100000)
        self.sb_zrange1.setValue(0)

        try:

            logger.info(f' loaded stack with {np.shape(self.stack_)} from the file')
            self.im_stack = self.stack_.T
            self.init_dimZ = self.im_stack.shape[0]
            self.init_dimX = self.im_stack.shape[1]
            self.init_dimY = self.im_stack.shape[2]
            self.sb_xrange2.setMaximum(5000)
            self.sb_yrange2.setMaximum(5000)
            self.sb_xrange2.setValue(self.init_dimX)
            self.sb_yrange2.setValue(self.init_dimY)
            logger.info(f' Transposed to shape: {np.shape(self.im_stack)}')

        except UnboundLocalError:
            logger.error('No file selected')
            pass

        try:
            self.energy = []
            self.view_stack()
            logger.info("Stack displayed correctly")
            self.update_stack_info()

        except:
            logger.error("Trouble with stack display")
            self.statusbar_main.showMessage("Error: Trouble with stack display")

        logger.info(f'completed image shape {np.shape(self.im_stack)}')

        try:
            self.statusbar_main.showMessage(f'Loaded: {self.file_name}')

        except AttributeError:
            self.statusbar_main.showMessage('New Stack is made from selected tiffs')
            pass

    def reset_and_load_stack(self):
        self.rb_math_roi_img.setChecked(False)
        self.cb_log.setChecked(False)
        self.cb_remove_edges.setChecked(False)
        self.cb_norm.setChecked(False)
        self.cb_smooth.setChecked(False)
        self.cb_remove_outliers.setChecked(False)
        self.cb_remove_bg.setChecked(False)
        self.cb_rebin.setChecked(False)
        self.cb_upscale.setChecked(False)
        self.sb_xrange1.setValue(0)
        self.sb_yrange1.setValue(0)
        self.load_stack()

    def update_stack_info(self):
        z, x, y = np.shape(self.updated_stack)
        self.sb_zrange2.setMaximum(z + self.sb_zrange1.value())
        self.sb_xrange2.setValue(x)
        self.sb_xrange2.setMaximum(x)
        self.sb_yrange2.setValue(y)
        self.sb_yrange2.setMaximum(y)
        logger.info('Stack info has been updated')

    def crop_to_dim(self):
        self.x1, self.x2 = self.sb_xrange1.value(), self.sb_xrange2.value()
        self.y1, self.y2 = self.sb_yrange1.value(), self.sb_yrange2.value()
        self.z1, self.z2 = self.sb_zrange1.value(), self.sb_zrange2.value()

        self.updated_stack = remove_nan_inf(self.im_stack[self.z1:self.z2,
                                            self.x1:self.x2, self.y1:self.y2])

    def transpose_stack(self):
        self.updated_stack = self.updated_stack.T
        self.update_spectrum()
        self.update_spec_image_roi()

    def update_stack(self):

        self.crop_to_dim()

        if self.cb_rebin.isChecked():
            self.cb_upscale.setChecked(False)
            self.sb_scaling_factor.setEnabled(True)
            self.updated_stack = resize_stack(self.updated_stack,
                                              scaling_factor=self.sb_scaling_factor.value())
            self.update_stack_info()
        elif self.cb_upscale.isChecked():
            self.cb_rebin.setChecked(False)
            self.sb_scaling_factor.setEnabled(True)
            self.updated_stack = resize_stack(self.updated_stack, upscaling = True,
                                              scaling_factor=self.sb_scaling_factor.value())
            self.update_stack_info()
        else:
            self.sb_scaling_factor.setEnabled(False)


        if self.cb_remove_outliers.isChecked():
            self.hs_nsigma.setEnabled(True)
            nsigma = self.hs_nsigma.value() / 10
            self.updated_stack = remove_hot_pixels(self.updated_stack,
                                                   NSigma=nsigma)
            self.label_nsigma.setText(str(nsigma))
            logger.info(f'Removing Outliers with NSigma {nsigma}')

        elif self.cb_remove_outliers.isChecked() == False:
            self.hs_nsigma.setEnabled(False)

        if self.cb_remove_edges.isChecked():
            self.updated_stack = remove_edges(self.updated_stack)
            logger.info(f'Removed edges, new shape {self.updated_stack.shape}')
            self.update_stack_info()

        if self.cb_remove_bg.isChecked():
            self.hs_bg_threshold.setEnabled(True)
            logger.info('Removing background')
            bg_threshold = self.hs_bg_threshold.value()
            self.label_bg_threshold.setText(str(bg_threshold) + '%')
            self.updated_stack = clean_stack(self.updated_stack,
                                             auto_bg=False,
                                             bg_percentage=bg_threshold)

        elif self.cb_remove_bg.isChecked() == False:
            self.hs_bg_threshold.setEnabled(False)

        if self.cb_log.isChecked():

            if self.avgIo != 1:

                self.updated_stack = remove_nan_inf(np.log10(self.updated_stack * self.avgIo))

                '''
                self.logMsgBox = QMessageBox()
                self.logMsgBox.setIcon(QMessageBox.Warning)
                self.logMsgBox.setText(f'Data is multiplied with average I0 value: {self.avgIo} '
                                       f'\n before taking log to avoid negative peaks')
                self.logMsgBox.setWindowTitle("Log data Warning")
                self.logMsgBox.setStandardButtons(QMessageBox.Ok)

                if self.logMsgBox.exec() == QMessageBox.Ok:
                    self.updated_stack = remove_nan_inf(np.log10(self.updated_stack * self.avgIo))


                elif self.logMsgBox.exec() == QtGui.QMessageBox.YesRole:
                    self.log_warning = 1
                    self.updated_stack = remove_nan_inf(np.log10(self.updated_stack * self.avgIo))
                '''





            logger.info('Log Stack is in use')

        if self.cb_smooth.isChecked():
            self.hs_smooth_size.setEnabled(True)
            window = self.hs_smooth_size.value()
            if window % 2 == 0:
                window = +1
            self.smooth_winow_size.setText('Window size: ' + str(window))
            self.updated_stack = smoothen(self.updated_stack, w_size=window)
            logger.info('Spectrum Smoothening Applied')

        elif self.cb_smooth.isChecked() == False:
            self.hs_smooth_size.setEnabled(False)

        if self.cb_norm.isChecked():
            logger.info('Normalizing spectra')
            self.updated_stack = normalize(self.updated_stack,
                                           norm_point=-1)

        logger.info(f'Updated image is in use')

    def view_stack(self):

        if not self.im_stack.ndim == 3:
            raise ValueError("stack should be an ndarray with ndim == 3")
        else:
            self.update_stack()

        try:
            self.image_view.removeItem(self.image_roi_math)
        except:
            pass

        (self.dim1, self.dim3, self.dim2) = self.updated_stack.shape
        self.image_view.setImage(self.updated_stack)
        self.image_view.ui.menuBtn.hide()
        self.image_view.ui.roiBtn.hide()
        self.image_view.setPredefinedGradient('viridis')
        self.image_view.setCurrentIndex(self.dim1 // 2)
        if len(self.energy) == 0:
            self.energy = np.arange(self.z1, self.z2) * 10
            logger.info("Arbitary X-axis used in the plot for XANES")
        self.sz = np.max([int(self.dim2 * 0.1), int(self.dim3 * 0.1)])  # size of the roi set to be 10% of the image area

        # a second optional ROI for calculations follow
        self.image_roi_math = pg.PolyLineROI([[0, 0], [0, self.sz], [self.sz, self.sz], [self.sz, 0]],
                                             pos=(int(self.dim3 // 3), int(self.dim2 // 3)),
                                             pen='r', closed=True,removable = True)
        self.image_roi_math.addTranslateHandle([self.sz // 2, self.sz // 2], [2, 2])


        self.stack_center = (self.energy[len(self.energy) // 2])
        self.stack_width = (self.energy.max() - self.energy.min()) // 10
        self.spec_roi = pg.LinearRegionItem(values=(self.stack_center - self.stack_width,
                                                    self.stack_center + self.stack_width))

        logger.info('Spectrum ROI Added')

        self.spec_roi_math = pg.LinearRegionItem(values=(self.stack_center - self.stack_width - 10,
                                                         self.stack_center + self.stack_width - 10), pen='r',
                                                 brush=QtGui.QColor(0, 255, 200, 50)
                                                 )
        self.setImageROI()
        self.update_spectrum()
        self.update_image_roi()

        # connections
        self.image_view.mousePressEvent = self.getPointSpectrum
        self.spec_roi.sigRegionChanged.connect(self.update_image_roi)
        self.spec_roi_math.sigRegionChangeFinished.connect(self.spec_roi_calc)
        self.rb_math_roi.clicked.connect(self.update_spectrum)
        self.rb_math_roi_img.clicked.connect(self.math_img_roi_flag)
        self.image_roi_math.sigRegionChangeFinished.connect(self.image_roi_calc)
        self.rb_poly_roi.clicked.connect(self.setImageROI)
        self.rb_elli_roi.clicked.connect(self.setImageROI)
        self.rb_rect_roi.clicked.connect(self.setImageROI)
        self.rb_line_roi.clicked.connect(self.setImageROI)
        self.rb_circle_roi.clicked.connect(self.setImageROI)

    def getPointSpectrum(self, event):

        if event.button() == QtCore.Qt.LeftButton:
            self.xpixel = int(self.image_view.view.mapSceneToView(event.pos()).x())-1
            zlim, xlim, ylim = self.updated_stack.shape

            if self.xpixel > xlim:
                self.xpixel = xlim-1

            self.ypixel  = int(self.image_view.view.mapSceneToView(event.pos()).y())-1
            if self.ypixel > ylim:
                self.ypixel = ylim-1

            self.spectrum_view.addLegend()
            self.point_spectrum = self.updated_stack[:,self.xpixel,self.ypixel]
            self.spectrum_view.plot(self.xdata, self.point_spectrum, clear=True,
                                    name = f'Point Spectrum; x= {self.xpixel}, y= {self.ypixel}')

            self.spectrum_view.addItem(self.spec_roi)

            self.statusbar_main.showMessage(f'{self.xpixel} and {self.ypixel}')

    def setImageROI(self):

        self.lineROI = pg.LineSegmentROI([[int(self.dim3 // 2), int(self.dim2 // 2)],
                                          [self.sz, self.sz]], pen='r')

        self.rectROI = pg.RectROI([int(self.dim3 // 2), int(self.dim2 // 2)],
                                  [self.sz, self.sz], pen='w')

        self.ellipseROI = pg.EllipseROI([int(self.dim3 // 2), int(self.dim2 // 2)],
                                        [self.sz, self.sz], pen='w')

        self.circleROI = pg.CircleROI([int(self.dim3 // 2), int(self.dim2 // 2)],
                                      [self.sz, self.sz], pen='w')  # pos and size

        self.polyLineROI = pg.PolyLineROI([[0, 0], [0, self.sz], [self.sz, self.sz], [self.sz, 0]],
                                          pos=(int(self.dim3 // 2), int(self.dim2 // 2)),
                                          maxBounds=QtCore.QRect(0, 0, self.dim3, self.dim2),
                                          closed=True, removable=True)
        self.polyLineROI.addTranslateHandle([self.sz // 2, self.sz // 2], [2, 2])


        self.rois = {'rb_line_roi':self.lineROI,'rb_rect_roi':self.rectROI,'rb_circle_roi':self.circleROI,
                    'rb_elli_roi':self.ellipseROI,'rb_poly_roi':self.polyLineROI}

        button_name = self.sender()

        if button_name.objectName() in self.rois.keys():
            self.roi_preference = button_name.objectName()

        else:
            self.roi_preference = 'rb_poly_roi'  # default

        try:
            self.image_view.removeItem(self.image_roi)
        except:
            pass

        # ROI settings for image, used polyline roi with non rectangular shape

        self.image_roi = self.rois[self.roi_preference]
        #self.image_roi.addTranslateHandle([self.sz // 2, self.sz // 2], [2, 2])

        self.image_view.addItem(self.image_roi)
        self.image_roi.sigRegionChanged.connect(self.update_spectrum)

    def replot_image(self):
        self.update_stack()
        self.update_spectrum()
        self.update_image_roi()

    def update_spec_roi_values(self):
        self.stack_center = int(self.energy[len(self.energy) // 2])
        self.stack_width = int((self.energy.max() - self.energy.min()) * 0.05)
        self.spec_roi.setBounds([self.xdata[0], self.xdata[-1]])  # if want to set bounds for the spec roi
        self.spec_roi_math.setBounds([self.xdata[0], self.xdata[-1]])

    def update_spectrum(self):

        # set x-axis values; array taken from energy values, if clipped z box values will update the array
        self.xdata = self.energy[self.sb_zrange1.value():self.sb_zrange2.value()]

        # get the cropped stack from ROI region; pyqtgraph function is used
        self.roi_img_stk = self.image_roi.getArrayRegion(self.updated_stack, self.image_view.imageItem, axes=(1, 2))

        posx, posy = self.image_roi.pos()
        self.le_roi.setText(str(int(posx)) + ':' + str(int(posy)))

        # display the ROI features in the line edit boxes
        if self.roi_img_stk.ndim == 3:
            sizex, sizey = self.roi_img_stk.shape[1], self.roi_img_stk.shape[2]
            self.le_roi_size.setText(str(sizex) + ',' + str(sizey))

            self.mean_spectra = get_mean_spectra(self.roi_img_stk)
            self.curr_spec = np.column_stack([self.xdata,self.mean_spectra])

        elif self.roi_img_stk.ndim == 2:
            sizex, sizey = self.roi_img_stk.shape[0], self.roi_img_stk.shape[1]
            self.le_roi_size.setText(str(sizex) + ',' + str(sizey))
            self.mean_spectra = self.roi_img_stk.mean(-1)
            self.curr_spec = np.column_stack([self.xdata,self.mean_spectra])


        self.spectrum_view.addLegend()

        try:
            self.spectrum_view.plot(self.xdata, self.mean_spectra , clear=True, name = 'ROI Spectrum')
        except:
            self.spectrum_view.plot(self.mean_spectra, clear=True, name = 'ROI Spectrum')

        if self.energy[-1] > 1000:
            self.e_unit = 'eV'
        else:
            self.e_unit = 'keV'

        self.spectrum_view.setLabel('bottom', 'Energy', self.e_unit)
        self.spectrum_view.setLabel('left', 'Intensity', 'A.U.')
        self.spectrum_view.addItem(self.spec_roi)
        self.update_spec_roi_values()
        self.math_roi_flag()

    def update_image_roi(self):
        self.spec_lo, self.spec_hi = self.spec_roi.getRegion()
        self.spec_lo_idx = (np.abs(self.energy - self.spec_lo)).argmin()
        self.spec_hi_idx = (np.abs(self.energy - self.spec_hi)).argmin()
        self.le_spec_roi.setText(str(int(self.spec_lo)) + ':' + str(int(self.spec_hi)))
        self.le_spec_roi_size.setText(str(int(self.spec_hi - self.spec_lo)))
        self.update_spec_roi_values()

        try:
            if int(self.spec_lo_idx) == int(self.spec_hi_idx):
                self.disp_img = self.updated_stack[int(self.spec_hi_idx), :, :]
                self.statusbar_main.showMessage(f'Image Display is stack # {self.spec_hi_idx}')

            else:
                self.disp_img = self.updated_stack[int(self.spec_lo_idx):int(self.spec_hi_idx), :, :].mean(0)
                self.statusbar_main.showMessage(f'Image display is stack # range: '
                                                f'{self.spec_lo_idx}:{self.spec_hi_idx}')
            self.image_view.setImage(self.disp_img)
        except:
            logger.warning("Indices are out of range; Image cannot be created")
            pass

    def set_spec_roi(self):
        self.spec_lo_, self.spec_hi_ = int(self.sb_roi_spec_s.value()), int(self.sb_roi_spec_e.value())
        self.spec_lo_idx_ = (np.abs(self.energy - self.spec_lo_)).argmin()
        self.spec_hi_idx_ = (np.abs(self.energy - self.spec_hi_)).argmin()
        self.spec_roi.setRegion((self.xdata[self.spec_lo_idx_], self.xdata[self.spec_hi_idx_]))
        self.update_image_roi()

    def math_roi_flag(self):
        if self.rb_math_roi.isChecked():
            self.rb_math_roi.setStyleSheet("color : green")
            self.spectrum_view.addItem(self.spec_roi_math)
        else:
            self.rb_math_roi.setStyleSheet("color : red")
            self.spectrum_view.removeItem(self.spec_roi_math)

    def spec_roi_calc(self):

        self.spec_lo_m, self.spec_hi_m = self.spec_roi_math.getRegion()
        self.spec_lo_m_idx = (np.abs(self.energy - self.spec_lo_m)).argmin()
        self.spec_hi_m_idx = (np.abs(self.energy - self.spec_hi_m)).argmin()

        if int(self.spec_lo_idx) == int(self.spec_hi_idx):
            self.img1 = self.updated_stack[int(self.spec_hi_idx), :, :]

        else:
            self.img1 = self.updated_stack[int(self.spec_lo_idx):int(self.spec_hi_idx), :, :].mean(0)

        if int(self.spec_lo_m_idx) == int(self.spec_hi_m_idx):
            self.img2 = self.updated_stack[int(self.spec_hi_m_idx), :, :]

        else:
            self.img2 = self.updated_stack[int(self.spec_lo_m_idx):int(self.spec_hi_m_idx), :, :].mean(0)

        if self.cb_roi_operation.currentText() == "Correlation Plot":
            self.correlation_plot()

        else:
            calc = {'Divide': np.divide, 'Subtract': np.subtract, 'Add': np.add}
            self.disp_img = remove_nan_inf(calc[self.cb_roi_operation.currentText()](self.img1, self.img2))
            self.image_view.setImage(self.disp_img)

    def math_img_roi_flag(self):
        if self.rb_math_roi_img.isChecked():
            self.rb_math_roi_img.setStyleSheet("color : green")
            self.image_view.addItem(self.image_roi_math)
        else:
            self.rb_math_roi_img.setStyleSheet("color : red")
            self.image_view.removeItem(self.image_roi_math)

    def image_roi_calc(self):

        if self.rb_math_roi_img.isChecked():
            self.calc = {'Divide': np.divide, 'Subtract': np.subtract, 'Add': np.add}
            ref_region = self.image_roi_math.getArrayRegion(self.updated_stack, self.image_view.imageItem, axes=(1, 2))
            ref_reg_avg = ref_region[int(self.spec_lo_idx):int(self.spec_hi_idx), :, :].mean()
            currentImage = self.updated_stack[int(self.spec_lo_idx):int(self.spec_hi_idx), :, :].mean(0)
            if self.calc[self.cb_img_roi_action.currentText()] == 'Compare':
                pass

            else:
                self.image_view.setImage(self.calc[self.cb_img_roi_action.currentText()]
                                         (currentImage, (ref_reg_avg + currentImage * 0)))
            self.update_spec_image_roi()
        else:
            pass

    def update_spec_image_roi(self):

        self.math_roi_reg = self.image_roi_math.getArrayRegion(self.updated_stack,
                                                               self.image_view.imageItem, axes=(1, 2))
        if self.math_roi_reg.ndim == 3:

            self.math_roi_spectra = get_mean_spectra(self.math_roi_reg)

        elif self.roi_img_stk.ndim == 2:
            self.math_roi_spectra = self.math_roi_reg.mean(-1)

        calc_spec = self.calc[self.cb_img_roi_action.currentText()](self.mean_spectra,
                                                                    self.math_roi_spectra)
        self.spectrum_view.addLegend()
        self.spectrum_view.plot(self.xdata, calc_spec, clear=True, pen='m',
                                name=self.cb_img_roi_action.currentText() + "ed")
        self.spectrum_view.plot(self.xdata, self.math_roi_spectra, pen='y',
                                name="math_region")
        self.spectrum_view.plot(self.xdata, self.mean_spectra, pen='g',
                                name="raw")

        self.spectrum_view.addItem(self.spec_roi)

    def correlation_plot(self):

        self.statusbar_main.showMessage(f'Correlation stack {int(self.spec_lo_idx)}:{int(self.spec_hi_idx)} with '
                                        f'{int(self.spec_lo_m_idx)}:{int(self.spec_hi_m_idx)}')

        self.scatter_window = ScatterPlot(self.img1, self.img2)

        ph = self.geometry().height()
        pw = self.geometry().width()
        px = self.geometry().x()
        py = self.geometry().y()
        dw = self.scatter_window.width()
        dh = self.scatter_window.height()
        # self.scatter_window.setGeometry(px+0.65*pw, py + ph - 2*dh-5, dw, dh)
        self.scatter_window.show()

    def save_stack(self):
        try:
            self.update_stack()
            file_name = QFileDialog().getSaveFileName(self, "Save image data", '', 'image file(*tiff *tif )')
            tf.imsave(str(file_name[0]), self.updated_stack.transpose(0, 2, 1))
            logger.info(f'Updated Image Saved: {str(file_name[0])}')
        except:
            logger.error('No file to save')
            pass

    def save_disp_img(self):
        try:
            file_name = QFileDialog().getSaveFileName(self, "Save image data", '', 'image file(*tiff *tif )')
            tf.imsave(str(file_name[0]) + '.tiff', self.disp_img.T)
            logger.info(f'Updated Image Saved: {str(file_name[0])}')

        except:
            logger.error('No file to save')
            pass

    def save_disp_spec(self):

        exporter = pg.exporters.CSVExporter(self.spectrum_view.plotItem)
        exporter.parameters()['columnMode'] = '(x,y,y,y) for all plots'
        file_name = QFileDialog().getSaveFileName(self, "save spectrum", '', 'spectra (*csv)')
        exporter.export(str(file_name[0])+'.csv')

    def pca_scree_(self):
        logger.info('Process started..')
        self.update_stack()
        pca_scree(self.updated_stack)
        logger.info('Process complete')

    def calc_comp_(self):

        logger.info('Process started..')

        self.update_stack()
        n_components = self.sb_ncomp.value()
        method_ = self.cb_comp_method.currentText()

        ims, comp_spec, decon_spec, decomp_map = decompose_stack(self.updated_stack,
                                                                 decompose_method=method_, n_components_=n_components)

        self._new_window3 = ComponentViewer(ims, self.xdata, comp_spec, decon_spec, decomp_map)
        self._new_window3.show()

        logger.info('Process complete')

    def kmeans_elbow(self):
        logger.info('Process started..')
        self.update_stack()
        try:
            kmeans_variance(self.updated_stack)
            logger.info('Process complete')
        except OverflowError:
            pass
            logger.error('Overflow Error, values are too long')

    def clustering_(self):

        logger.info('Process started..')
        self.update_stack()
        method_ = self.cb_clust_method.currentText()

        decon_images, X_cluster, decon_spectra = cluster_stack(self.updated_stack, method=method_,
                                                               n_clusters_=self.sb_ncluster.value(),
                                                               decomposed=False,
                                                               decompose_method=self.cb_comp_method.currentText(),
                                                               decompose_comp=self.sb_ncomp.value())

        self._new_window4 = ClusterViewer(decon_images, self.xdata, X_cluster, decon_spectra)
        self._new_window4.show()

        logger.info('Process complete')

    def change_color_on_load(self, button_name):
        button_name.setStyleSheet("background-color : green")

    def select_elist(self):
        file_name = QFileDialog().getOpenFileName(self, "Open energy list", '', 'text file (*.txt)')

        try:

            if str(file_name[0]).endswith('log_tiff.txt'):
                self.energy = energy_from_logfile(logfile=str(file_name[0]))
                logger.info("Log file from pyxrf processing")

            else:
                self.energy = np.loadtxt(str(file_name[0]))

            logger.info('Energy file loaded')
            if self.energy.any():
                self.change_color_on_load(self.pb_elist_xanes)

            assert len(self.energy) == self.dim1

            if self.energy.max() < 100:
                self.cb_kev_flag.setChecked(True)
                self.energy *= 1000

            else:
                self.cb_kev_flag.setChecked(False)

            self.view_stack()

        except OSError:
            logger.error('No file selected')
            pass

    def select_ref_file(self):
        self.ref_names = []
        file_name = QFileDialog().getOpenFileName(self, "Open reference file", '', 'text file (*.txt *.nor)')
        try:
            if file_name[0].endswith('.nor'):
                self.refs, self.ref_names = create_df_from_nor_try2(athenafile=str(file_name[0]))
                self.change_color_on_load(self.pb_ref_xanes)

            elif file_name[0].endswith('.txt'):
                self.refs = pd.read_csv(str(file_name[0]), header=None, delim_whitespace=True)
                self.change_color_on_load(self.pb_ref_xanes)

            self.plt_xanes_refs()

        except OSError:
            logger.error('No file selected')
            pass

        except:
            logger.error('Unsupported file format')
            pass

    def plt_xanes_refs(self):
        plt.figure()
        plt.plot(self.refs.values[:, 0], self.refs.values[:, 1:])
        plt.title("Reference Standards")
        plt.xlabel("Energy")
        plt.show()

    def fast_xanes_fitting(self):

        self._new_window5 = XANESViewer(self.updated_stack, self.xdata, self.refs, self.ref_names)
        self._new_window5.show()

    def openMaskMaker(self):
        self.mask_window = MaskSpecViewer(xanes_stack=self.updated_stack, energy=self.energy)
        self.mask_window.show()

    def open_github_link(self):
        webbrowser.open('https://github.com/pattammattel/NSLS-II-MIDAS')


if __name__ == "__main__":

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s : %(levelname)s : %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(stream_handler)

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_Use96Dpi)
    window = midasWindow()
    window.show()
    sys.exit(app.exec_())
