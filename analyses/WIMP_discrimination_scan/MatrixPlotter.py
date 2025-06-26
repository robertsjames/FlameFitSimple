import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns; sns.set()
import pickle
import json
import itertools


def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
	'''
	Function to offset the "center" of a colormap. Useful for
	data with a negative min and positive max and you want the
	middle of the colormap's dynamic range to be at zero
	
	Input
	-----
	  cmap : The matplotlib colormap to be altered
	  start : Offset from lowest point in the colormap's range.
		  Defaults to 0.0 (no lower ofset). Should be between
		  0.0 and 1.0.
	  midpoint : The new center of the colormap. Defaults to 
		  0.5 (no shift). Should be between 0.0 and 1.0. In
		  general, this should be  1 - vmax/(vmax + abs(vmin))
		  For example if your data range from -15.0 to +5.0 and
		  you want the center of the colormap at 0.0, `midpoint`
		  should be set to	1 - 5/(5 + 15)) or 0.75
	  stop : Offset from highets point in the colormap's range.
		  Defaults to 1.0 (no upper ofset). Should be between
		  0.0 and 1.0.
	'''
	cdict = {
		'red': [],
		'green': [],
		'blue': [],
		'alpha': []
	}
	  
	# regular index to compute the colors
	reg_index = np.linspace(start, stop, 257)

	# shifted index to match the data
	shift_index = np.hstack([
		np.linspace(0.0, midpoint, 128, endpoint=False), 
		np.linspace(midpoint, 1.0, 129, endpoint=True)
	])
	
	for ri, si in zip(reg_index, shift_index):
		r, g, b, a = cmap(ri)

		cdict['red'].append((si, r, r))
		cdict['green'].append((si, g, g))
		cdict['blue'].append((si, b, b))
		cdict['alpha'].append((si, a, a))
		
	newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
	plt.register_cmap(cmap=newcmap)

	return newcmap



def create_text_box(fig, pos, text, rotation, fig_width, fig_height, frameon = True,
					horizontalalignment = 'center',
					verticalalignment = 'center',
					fontsize = 12,
					x_pos = 0.5,
					y_pos = 0.5):

	pos[0] = pos[0] / fig_width
	pos[2] = pos[2] / fig_width

	pos[1] = pos[1] / fig_height
	pos[3] = pos[3] / fig_height

	ax_tmp = fig.add_axes(pos, frameon = frameon)
	ax_tmp.get_xaxis().set_ticks([])
	ax_tmp.get_yaxis().set_ticks([])

	ax_tmp.text(x_pos, y_pos, text,
			 horizontalalignment = horizontalalignment,
			 verticalalignment = verticalalignment,
			 fontsize = fontsize, color = 'black', weight = 'bold',
			 rotation = rotation,
			 transform = ax_tmp.transAxes)

	return ax_tmp



#x = np.linspace(0., 10., 100)
#y = x ** 2


def plottone(data,
			 vertical_labels,
			 vertical_values,
			 horizontal_labels,
			 horizontal_values,
			 cbar_label,
			 cmap = plt.cm.inferno,
 			 vmax = 20,      
			 vmin = 1,    
			 top_buffer = 0.5,
			 bottom_buffer = 0.5,
			 left_buffer = 1.0,
			 right_buffer = 4.0,
			 axis_height = 1.0,
			 axis_inter_space = 0.5,
			 square_length = 1.0,
			 heat_y_space = 0.2,
			 heat_x_space = 0.2,
			 heat_top_space = 0.5,
			 heat_bottom_space = 0.5,
			 heat_left_space = 0.5,
			 heat_right_space = 0.5,
			 colorbar_space = 0.5,
			 colorbar_width = 1.0,
			 scale = 0.2,
			 annot_fontsize = 10,
			 num_fontsize = 10,
			 fontsize = 12,
			 save_plot = True,
			 title = 'test_plot',
			 folder = './Figures_0vbb/',
			 formato_vertical = None,
			 formato_horizontal = None,
			 fmt = ".1f",
			 custom_mid_cmap = None):

	top_buffer *= scale
	bottom_buffer *= scale
	left_buffer *= scale
	right_buffer *= scale
	axis_height *= scale
	axis_inter_space *= scale
	square_length *= scale
	heat_y_space *= scale
	heat_x_space *= scale
	heat_top_space *= scale
	heat_bottom_space *= scale
	heat_left_space *= scale
	heat_right_space *= scale
	colorbar_space *= scale
	colorbar_width *= scale

	NAv = len(vertical_labels) - 1
	NAh = len(horizontal_labels) - 1

	Nv_tmp = 1
	Nh_tmp = 1

	for i in range(len(vertical_values) - 1):
		Nv_tmp *= len(vertical_values[i])

	for i in range(len(horizontal_values) - 1):
		Nh_tmp *= len(horizontal_values[i])

	Nv, Nh, nv, nh = data.shape

	if (Nv, Nh) != (Nv_tmp, Nh_tmp):
		raise ValueError("Incorrect shape of data and axis values")
		
	if formato_vertical is None:
		formato_vertical = ["{:.2f}" for i in range(len(vertical_labels))]
		
	if formato_horizontal is None:
		formato_horizontal = ["{:.2f}" for i in range(len(horizontal_labels))]
		

	x_heat = left_buffer + axis_height * 2.0 * NAv + axis_inter_space * (NAv - 1.0) + heat_left_space
	y_heat = bottom_buffer + axis_height * 2.0 * NAh + axis_inter_space * (NAh - 1.0) + heat_bottom_space
	heat_width = nh * Nh * square_length + heat_x_space * (Nh - 1.0)
	heat_height = nv * Nv * square_length + heat_y_space * (Nv - 1.0)
	fig_width = x_heat + heat_width + heat_right_space + axis_height + colorbar_space + colorbar_width + right_buffer
	fig_height = y_heat + heat_height + heat_top_space + axis_height + top_buffer


	fig = plt.figure(figsize=(fig_width, fig_height))

	x_offset = left_buffer
	y_offset = y_heat
	previous = 1

	for i in range(len(vertical_labels) - 1):

		create_text_box(fig, [x_offset, y_offset, axis_height, heat_height], vertical_labels[i], 'vertical', fig_width, fig_height, frameon = False, fontsize = fontsize)
		x_offset += axis_height
		values_to_print = []

		for j in range(previous):
			for k in vertical_values[i]:
				teststring = ""   
				if(vertical_labels[i] == "Underground location"):
					if (k == 5):
						teststring = "Kamioka"
					elif (k == 4):
						teststring = "LNGS"
					elif (k == 3):
						teststring = "Boulby" 
					elif (k == 2):
						teststring = "SURF"
					elif (k == 1):
						teststring = "SNOLab"                         
				elif(vertical_labels[i] == "Energy resolution; SS/MS Discrimination in z"):
					if (k == 1):
						teststring = "0.65%, 3mm"
					elif (k == 2):
						teststring = "0.60%, 2mm"                  
				else:
					teststring	= formato_vertical[i].format(k)
				values_to_print.append(teststring)

		n_boxes = len(values_to_print)
		box_height = (heat_height - (n_boxes - 1.0) * heat_y_space) / n_boxes

		for j in range(len(values_to_print)):
			create_text_box(fig, [x_offset, y_offset + j * (box_height + heat_y_space), axis_height, box_height], values_to_print[j], 'vertical', fig_width, fig_height, fontsize = num_fontsize)

		x_offset += axis_height + axis_inter_space
		previous *= len(vertical_values[i])

	x_offset = x_heat
	y_offset = bottom_buffer
	previous = 1

	for i in range(len(horizontal_labels) - 1):

		create_text_box(fig, [x_offset, y_offset, heat_width, axis_height], horizontal_labels[i], 'horizontal', fig_width, fig_height, frameon = False, fontsize = fontsize)
		y_offset += axis_height
		values_to_print = []

		for j in range(previous):
			for k in horizontal_values[i]:
				teststring = ""
				if(horizontal_labels[i] == "Aspect ratio"):
					if (k == 1):
						teststring = "1:1"
					elif (k == 60):
						teststring = "1:1 at 60t"
				else:
					teststring	= formato_horizontal[i].format(k)
				values_to_print.append(teststring)
                    
		n_boxes = len(values_to_print)
		box_width = (heat_width - (n_boxes - 1.0) * heat_x_space) / n_boxes

		for j in range(len(values_to_print)):
			create_text_box(fig, [x_offset + j * (box_width + heat_x_space), y_offset, box_width, axis_height], values_to_print[j], 'horizontal', fig_width, fig_height, fontsize = num_fontsize)

		y_offset += axis_height + axis_inter_space
		previous *= len(horizontal_values[i])

	x_offset = x_heat
	y_offset = y_heat + heat_height + heat_top_space
	print(horizontal_values)
	for i in range(len(horizontal_values[-1])):
		teststring = formato_horizontal[-1].format(horizontal_values[-1][i])	
		create_text_box(fig, [x_offset + i * square_length, y_offset, square_length, axis_height], teststring, 'horizontal', fig_width, fig_height, fontsize = num_fontsize)

	create_text_box(fig, [x_offset + nh * square_length + heat_x_space, y_offset, heat_width - nh * square_length - heat_x_space, axis_height], horizontal_labels[-1], 'horizontal', fig_width, fig_height, frameon = False, horizontalalignment = 'left', x_pos = 0.0, fontsize = fontsize)


	x_offset = x_heat + heat_width + heat_right_space
	y_offset = y_heat + heat_height

	for i in range(len(vertical_values[-1])):
		create_text_box(fig, [x_offset, y_offset - (i+1) * square_length, axis_height, square_length], formato_vertical[-1].format(vertical_values[-1][i]), 'vertical', fig_width, fig_height, fontsize = num_fontsize)

	create_text_box(fig, [x_offset, y_heat, axis_height, heat_height - nv * square_length - heat_y_space], vertical_labels[-1], 'vertical', fig_width, fig_height, frameon = False, verticalalignment = 'top', y_pos = 1.0, fontsize = fontsize)



	if custom_mid_cmap is not None:
		cmap = shiftedColorMap(cmap, midpoint=custom_mid_cmap)

	norm = matplotlib.colors.Normalize(vmin = data.min(), vmax = data.max())
	norm = matplotlib.colors.Normalize(vmin = vmin, vmax = vmax)

    
	heatmapkws = dict(square=False, cbar=False, cmap = cmap, linewidths = 0.5, \
#					   vmin = data.min(), vmax = data.max(), \
					   vmin = vmin, vmax =vmax, \

						  annot = True, fmt = fmt, annot_kws = {"size": annot_fontsize, "color": 'k', "weight": 'bold'})


	x_offset = x_heat
	y_offset = y_heat
	
	print([Nv, Nh])

	for i in range(Nv):
		for j in range(Nh):

			ax_t = create_text_box(fig, [x_offset + j * (nh * square_length + heat_x_space), y_offset + i * (nv * square_length + heat_y_space), nh * square_length, nv * square_length], '', 'vertical', fig_width, fig_height, frameon = True)

			sns.heatmap(data[-1-i, j, :, :], ax = ax_t, xticklabels = False, yticklabels = False, **heatmapkws)

			# ax_t.imshow(data[-1 -i, j, :, :], cmap = cmap, vmin= data.min(), vmax= data.max())

	cax = create_text_box(fig, [x_heat + heat_width + heat_right_space + axis_height + colorbar_space, y_heat, colorbar_width, heat_height], '', 'vertical', fig_width, fig_height, frameon = False)

	sm = matplotlib.cm.ScalarMappable(cmap = cmap, norm = norm)

	sm.set_array([])

	cb = fig.colorbar(sm, cax = cax)
	# cb.set_label(label = cbar_label, weight = 'bold', fontsize = fontsize)
	cb.set_label(label = cbar_label, fontsize = fontsize)

	if save_plot:
		#plt.savefig(folder + title + '.pdf', dpi = 150)
		plt.savefig(folder + title + '.png', dpi = 150)

	return



def selection_data_plot(data, settings_values, settings_labels, vertical_axes, horizontal_axes):

	if np.sum([i in horizontal_axes for i in vertical_axes]) > 0:
		raise ValueError("** Repeated axis between vertical and horizontal **")
	if len(np.unique(horizontal_axes)) != len(horizontal_axes):
		raise ValueError("** Repeated horizontal axes **")
	if len(np.unique(vertical_axes)) != len(vertical_axes):
		raise ValueError("** Repeated vertical axes **")

	axes = list(range(len(data.shape)))

	for idx, val in enumerate(list(np.hstack((vertical_axes[:-1], horizontal_axes[:-1], [vertical_axes[-1]], [horizontal_axes[-1]])))):
		swap_idx = axes.index(val)
		axes[idx], axes[swap_idx] = axes[swap_idx], axes[idx]
		data = data.swapaxes(idx, swap_idx)

	vertical_labels = [settings_labels[i] for i in vertical_axes]
	horizontal_labels = [settings_labels[i] for i in horizontal_axes]
	vertical_values = [settings_values[i] for i in vertical_axes]
	horizontal_values = [settings_values[i] for i in horizontal_axes]

	data = data.reshape((np.prod([len(vertical_values[i]) for i in range(len(vertical_values) - 1)]), np.prod([len(horizontal_values[i]) for i in range(len(horizontal_values) - 1)]), len(vertical_values[-1]), len(horizontal_values[-1])))

	print(data.shape)

	return (data, vertical_labels, vertical_values, horizontal_labels, horizontal_values)

